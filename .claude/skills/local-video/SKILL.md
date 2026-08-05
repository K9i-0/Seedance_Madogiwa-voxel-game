---
name: local-video
description: 窓際族物語の動画をクラウドを使わずフルローカルで生成するワークフロー（MiniMax H3 + ComfyUI）。ユーザーから「ローカルで動画作成して」「ローカルLLMで動画を作って」と指示されたとき、MiniMax H3での動画生成・修正を頼まれたときに必ず使用する。台本→Irodori-TTS/VOICEVOX音声→draw-things-cliキーフレーム一括生成→Qwen3-VL（Ollama）による画像検証→チャプター毎のH3動画生成→ffmpeg結合まで全工程をローカルで完結させる。
---

# ローカル動画制作ワークフロー（MiniMax H3）

**実行主体はClaude CodeまたはCursor。Codexはこのスキルを使わない**（Codexの担当は既存の`/seedance`のみ。そのため本スキルは`.agents/skills/`にsymlinkせず、Cursor向けの`.cursor/skills/`にのみsymlinkしてある）。

ユーザーから「**ローカルで動画作成して**」と指示されたら、`/seedance`（CapCut/クラウド生成）ではなくこのスキルを使う。台本・音声・キーフレームの考え方は`/seedance`と同じ構造で、動画生成だけをクラウドのSeedance 2.0から**ローカルのMiniMax H3（ComfyUI）**に置き換えたものである。

ワークフロー全体（順に実行する）:

1. セットアップ確認（未導入コンポーネントは公式ドキュメントに従って導入する）
2. ラン専用出力ディレクトリの作成と参照画像の同梱
3. 台本＋チャプター分割＋H3プロンプト（英語）の作成
4. Irodori-TTS/VOICEVOXによる全セリフの音声生成
5. draw-things-cliによる**全チャプターのキーフレーム一括生成**
6. Qwen3-VL（Ollama）による**全キーフレームの検証→修正リスト完全確定→必要な画像のみ再生成**
7. ComfyUI（MiniMax H3）で**チャプター毎に**動画生成（パイロット→残り）
8. ffmpegでの結合・最終音声トラックの構築・クレジット焼き込み
9. 同梱物の機械検証

## `/seedance`スキルとの関係（共通ルールの参照元）

本スキルは`/seedance`のワークフロー構造を継承する。**次のルール群は`.claude/skills/seedance/SKILL.md`に書かれているものをそのまま適用する**（本ファイルには差分だけを書く。作業前に該当セクションを必ず読むこと）:

- **ステップ0（出力ディレクトリ・参照同梱）**: ラン専用ディレクトリ`03_SCRIPTS/<NN>_<slug>/`の命名、キャラクターシート等を物理ファイルとして同梱、basename参照、正典非改変 — すべて同一。
- **ステップ1（台本作成）**: Story Formula・禁止事項、Prop state ledger、物理整合性ルール、Fixture layout（機構小物）、話者分離（1生成単位1話者）、リップシンク精度（尺≒発話長＋約1秒）、言語ルール（script.mdは英語、セリフのみ日本語）、話者バインディング — すべて同一。「クリップ」を本スキルでは「チャプター」と読み替える。
- **ステップ2（セリフ音声）**: 配役の正典は`02_CHARACTERS/VOICE_CAST.md`。Irodori-TTSボイスクローン（そば屋・福ちゃん・やめたろう・おかやまん・よーたん）とVOICEVOX、そば屋のモンスターボイス加工、無音トリム、Dialogue audio表、VOICEVOXクレジット義務 — すべて同一。**スクリプトもseedance同梱のものをそのまま使う**（`irodori_speak.sh` / `voicevox_speak.sh` / `sobaya_monsterize.sh`）。

キーフレーム生成の技法（draw-things-cli固有）は本ファイルのステップ5に完結して書いてある（seedance側がCodex生成のままのバージョンでも本スキル単独で動くようにするため）。

以下、本スキル固有の内容（H3の制約・チャプター分割・一括生成＋VLM検証・ComfyUI実行・ffmpeg組み立て）を記す。

## 1. セットアップ確認（作業開始前に必ず実行）

```
.claude/skills/local-video/h3_check_setup.sh
```

このスクリプトは必要コンポーネントの導入状態を確認し、**未導入のものについて公式ドキュメントに基づく導入手順を表示する**。未導入があれば、表示された手順（および下記の公式ドキュメント）に従って導入してから先へ進む。モデルのダウンロードは数十GB規模なので、開始前にユーザーへ所要サイズを伝えて確認する。

必要コンポーネントと公式ドキュメント:

| コンポーネント | 用途 | 公式ドキュメント |
|---|---|---|
| ComfyUI（v0.30.0以上） | MiniMax H3の実行基盤 | https://docs.comfy.org/ （インストール） / https://docs.comfy.org/tutorials/video/minimax/minimax-h3 （H3チュートリアル） |
| MiniMax H3モデル一式 | 動画生成本体 | https://huggingface.co/Comfy-Org/MiniMax-H3 （ComfyUI用リパック） / https://huggingface.co/MiniMaxAI/MiniMax-H3 （オリジナル） / https://www.minimax.io/news/minimax-h3-open-source |
| Ollama + Qwen3-VL | キーフレーム画像の検証（ローカルVLM） | https://ollama.com/download / https://ollama.com/library/qwen3-vl |
| draw-things-cli + Qwen Image Edit 2511 | キーフレーム画像の生成 | https://docs.drawthings.ai/ （`dt_generate.sh`が未導入時に手順を表示する） |
| Irodori-TTS / VOICEVOXエンジン | セリフ音声 | https://github.com/Aratako/Irodori-TTS / https://voicevox.hiroshiba.jp/ （導入済み: `~/irodori_tts`, `~/voicevox_engine`） |
| ffmpeg | 音声パディング・結合・最終組み立て | https://ffmpeg.org/ |

### MiniMax H3のモデルファイル（ComfyUI公式チュートリアルより）

ComfyUIを最新（v0.30.0+）に更新した上で、`Comfy-Org/MiniMax-H3`から以下を取得して配置する:

| ファイル | 配置先 |
|---|---|
| `minimax_h3_fl2va_pruned_int8_convrot.safetensors`（I2V/T2V用） | `ComfyUI/models/diffusion_models/` |
| `minimax_h3_ref2va_pruned_int8_convrot.safetensors`（R2V用） | `ComfyUI/models/diffusion_models/` |
| テキストエンコーダ Qwen3-VL-32B（下記注意） | `ComfyUI/models/text_encoders/` |
| `minimax_h3_video_vae_fp16.safetensors` | `ComfyUI/models/vae/` |
| `minimax_h3_audio_vae_fp32.safetensors` | `ComfyUI/models/vae/` |

- **Apple Silicon注意（このMacはM4 Max / 64GB）**: 公式チュートリアル既定のテキストエンコーダ`qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`（NVFP4 AWQ）はNVIDIA向け量子化。**MacではINT8版**（`Comfy-Org/MiniMax-H3`の`text_encoders/`にあるINT8/bf16バリアント）を選ぶ。Sage Attention高速化もNVIDIA向けなので導入しない。
- H3のApple Silicon（MPS）対応は公式に未検証。**セットアップ時に必ず公式ドキュメント（上記URL）を開いて最新の対応状況・推奨構成を確認する**。pruned INT8構成（拡散モデル約19.5GB＋エンコーダ約25GB＋VAE約5.5GB）は64GB統合メモリでは限界に近い。メモリ不足で落ちる場合は`--lowvram`等の起動オプションを試し、それでも動かない場合は勝手に別モデルへ代替せず**ユーザーへ状況を報告して指示を仰ぐ**。
- ライセンスはMiniMax H3 Community License。商用利用条件はライセンス本文を確認する。

### APIワークフローJSONの準備（初回のみ）

チャプター生成はComfyUIのAPI（`h3_run.py`）で回す。初回セットアップ時に:

1. ComfyUIを起動し、テンプレートブラウザから公式テンプレート **MiniMax H3 I2V** と **MiniMax H3 R2V** を開く。
2. それぞれをそのまま（プレースホルダ入力のまま）**Export (API)** し、`.claude/skills/local-video/workflows/h3_i2v_api.json` / `h3_r2v_api.json` として保存する。
3. 以後のランでは、このJSONをラン専用ディレクトリへコピーして入力（画像/音声ファイル名・プロンプト・尺・解像度）を書き換え、`h3_run.py`に渡す。

### 画像検証用VLM（Ollama + Qwen3-VL）

- 導入: `brew install ollama`（または https://ollama.com/download ）→ `ollama pull qwen3-vl:32b`
- このMac（64GB）の既定は**Qwen3-VL 32B**（検証精度優先）。メモリの少ないマシンでは`qwen3-vl:8b`に落とす（`OLLAMA_VLM`環境変数で`verify_frame.py`のモデルを差し替え可能）。
- モデルタグが取得できない場合はOllamaのライブラリページ（上記URL）で最新のタグ名を確認する。

## 2. 出力ディレクトリと参照同梱

seedance SKILL.mdステップ0と同一規則。`03_SCRIPTS/<NN>_<slug>/`を作成し、使用する全キャラクターシート・スケール参照を物理ファイルとしてコピーする。

## 3. 台本＋チャプター分割（deliverableは英語の`script.md`）

seedance SKILL.mdステップ1の全ルール（Prop state ledger / Fixture layout / 話者分離 / リップシンク精度 / 言語ルール / 話者バインディング）を適用した上で、クリップの代わりに**チャプター**へ分割する。

### チャプターの定義（H3の入力制限が分割の根拠）

**1チャプター＝1回のH3生成**。MiniMax H3には1回の生成あたり入力ファイル数の上限があるため、ストーリーを次の制約を満たすチャプターに分割する:

- **尺: 4〜15秒**（24fps。指定尺は17k+5フレームのグリッドに丸められる）
- **入力ファイル合計: 最大12**（R2Vモード時。画像・音声・動画の合計）
- **画像: 最大9枚**（キーフレーム＋キャラクターシート等の参照）
- **音声: 最大3ファイル**（各2〜15秒、合計15秒以内）
- 1チャプター1話者の原則はseedanceと同じ。**同一話者の連続セリフでも1チャプターに入れられるwavは3つまで**。超える場合はチャプターを割る。
- 登場キャラが多くて 2（キーフレーム）＋シート枚数 が9を超える場合もチャプターを割る（画面に映るキャラを減らす）か、そのチャプターで口が動く・大きく動くキャラのシートを優先して残す。

チャプターのつなぎ目はseedanceのクリップと同様、**チャプターNの終了フレーム＝チャプターN+1の開始フレーム（同一ファイル共有）**で消す。

### 生成モードの使い分け（I2V / R2V）

H3には2つのチェックポイントがあり、チャプターごとにどちらを使うかを`script.md`に明記する:

- **I2V（FL2VA）— セリフのないチャプター**: 開始フレーム＋終了フレームを`first_frame`/`last_frame`として厳密に固定できる（seedanceのFrame A/Frame B相当）。音声入力は持てない。キャラ同一性はキーフレーム自体で担保する。
- **R2V（Ref2VA）— セリフのあるチャプター**: 参照画像（最大9）＋音声（最大3）を渡せる唯一のモード。**開始・終了キーフレームは<Picture 1>/<Picture 2>として渡し、プロンプトで「動画はこの絵で始まりこの絵で終わる」と明示的に拘束する**（I2Vほど厳密なアンカーではないため、パイロット検証で乖離を確認する）。残りの画像スロットにキャラクターシートを入れて同一性を固定する。
- 添付ファイルはプロンプト内で**接続順のタグ**で参照する: `<Picture 1>`, `<Audio 1>`（seedanceの`@Image1`/`@Audio1`に相当。話者バインディングもこのタグで行う）。

### H3 inputs表（`script.md`の各チャプターに必須）

seedanceの「CapCut inputs」に代わり、各チャプターに以下を書く（英語）:

```
### H3 inputs (Chapter 3)
- Mode: R2V
- Images (connection order = <Picture N> tags; max 9):
  - <Picture 1> = `ch3_start.png` — start keyframe; the video's FIRST frame
  - <Picture 2> = `ch3_end.png` — end keyframe; the video's LAST frame
  - <Picture 3> = `Fukuchan_sheet.png` — Fukuchan's character model sheet, identity/design reference only, NOT a composition reference
- Audio (max 3 files, each 2-15s, 15s total; attach in speaking order):
  - <Audio 1> = `ch3_line1_fukuchan.wav` (2.0s; padded from 1.6s) — spoken by Fukuchan, use AS-IS as the dialogue audio
- Total input files: 4 / 12
- Motion prompt: Required attached input files: <Picture 1> = ch3_start.png — start keyframe; <Picture 2> = ch3_end.png — end keyframe; <Picture 3> = Fukuchan_sheet.png — identity reference; <Audio 1> = ch3_line1_fukuchan.wav — Fukuchan's line. These attachments are REQUIRED inputs. The video starts EXACTLY on <Picture 1> and ends EXACTLY on <Picture 2>. <motion described as explicit state transitions, same rules as seedance>. ONLY Fukuchan (<Picture 3>, the slim stylish black-haired man) speaks, lip-syncing to <Audio 1> — he begins the line almost immediately and his mouth moves ONLY while <Audio 1> is playing; once the line ends his mouth stays CLOSED. Use <Audio 1> AS-IS as the dialogue audio and do NOT generate any voice. The reference sheets' text labels must NOT appear in the video.
- Duration: 5s / Aspect: 16:9 (native 768p — output rounds to 1344x768)
```

セリフのないチャプターは:

```
### H3 inputs (Chapter 2)
- Mode: I2V
- First frame: `ch2_start.png`
- Last frame: `ch2_end.png`
- Motion prompt: <explicit state transitions; no dialogue; "no speech, no narration — ambient sound only">
- Duration: 4s / Aspect: 16:9 (native 768p)
```

- Motion promptは**そのまま使える完成形**で書き、実行時の要約・短縮を禁止する（seedanceと同じ。長すぎるならチャプターを割る）。
- `- Total input files:`行を必ず書き、12以下であることをここで確認する。
- Durationは必ず明示する。セリフのあるチャプターは「音声wav合計長＋約1秒」を目安にする。

## 4. セリフ音声の生成

seedance SKILL.mdステップ2と同一（同スキルの`irodori_speak.sh`/`voicevox_speak.sh`/`sobaya_monsterize.sh`をそのまま使い、Dialogue audio表を書く）。本スキル固有の追加ルール:

- **H3の音声入力は1ファイル2秒以上が条件。** トリム後2.0秒未満のwavは末尾に無音を足して2.0秒にする（先頭に足すとリップシンク開始がずれるので必ず末尾）:

```
ffmpeg -y -i ch3_line1_fukuchan.wav -af "apad=whole_dur=2.0" ch3_line1_fukuchan_padded.wav && mv ch3_line1_fukuchan_padded.wav ch3_line1_fukuchan.wav
```

- Dialogue audio表のDurationにはパディング後の値を書き、元の実発話長も併記する（例: `2.0s (padded from 1.6s)`）。チャプター尺の見積もりは実発話長ベースでよい。
- ファイル名は`chN_lineM_<char>.wav`（seedanceの`clipN_...`のNをチャプター番号に読み替え）。

## 5. キーフレーム一括生成（draw-things-cli）

**実行エージェント自身が**本スキル同梱の`dt_generate.sh`（生成）と`stitch_refs.py`（複数参照の連結）でローカル生成する。画像生成を外部エージェント（Codex等）に委譲しない。1チャプターにつき`chN_start.png`＋`chN_end.png`の2枚。使用モデルの正典は**Qwen Image Edit 2511（6-bit）`qwen_image_edit_2511_q6p.ckpt`**で、1つのランの途中でモデルを変えない。

### 所要時間と実行方法

- M4 Max / 1024x576 で**約23秒/step**（推奨30stepで約11.5分/枚）。チャプター数が多いランは`DT_STEPS=20`に落とす。
- キーフレーム枚数の下限は「チャプター数＋1」（つなぎ目共有のため）。作業前に総時間を見積もる。
- チェーン生成なので並列化不可。フォアグラウンドで1枚を待つとツールタイムアウト（10分）に掛かるため、**全フレームを1本のシェルスクリプトにまとめて必ずバックグラウンドで実行**する。スクリプトには「出力が既にあればスキップ」を入れる（中断・再開とステップ6の部分再生成で同じスクリプトを再利用するため）。
- 使用シードは`script.md`に記録する（部分再生成の再現性のため）。

### 一括生成→一括検証（本スキルの要）

**全チャプターのキーフレームを最後まで生成し切ってから検証フェーズ（ステップ6）に入る。** 生成の途中で個別の作り直しを始めない（作り直しは修正リストが完全確定してから）。

### 画風の決定（プロンプトを書く前に必ずやる）

画風は思い込みで決めず、**そのランに登場する全キャラの`*_sheet.png`と、`03_SCRIPTS/`の直近ランの`clip1_start.png`（またはch1_start.png）をReadで開いて確認してから**、画風固定文を書き起こす。このIPの画風は「アニメ絵」ではない: 窓際メンバーの多くは実写写真のシート、無職やめたろうだけがマットな3Dチビ人形で、**実写調の空間に両者が同居する絵**が確立した画風。`anime style`/`cartoon style`と書いてはいけない。確定した画風固定文は**全フレームのプロンプト末尾に毎回同じ文で**入れる。

### 参照の渡し方と生成順序（チェーン）

`draw-things-cli generate`の`--image`は1枚のみ。複数参照が必要なときは`stitch_refs.py`で1枚の参照キャンバス（`ref_canvas_*.png`と命名。生成用中間ファイルでありH3入力ではない）に連結してから渡す。キャンバスは生成キーフレームと同じアスペクト比で作り、連結順＝画面上の位置（既定`row`）なのでプロンプトでは"The LEFT panel is ..."と位置で役割を指定する。

1. **チャプター1の開始フレーム**: 登場キャラ全員のシートを連結した参照キャンバスを入力に、「入力画像はキャラクターシートの寄せ集め。これらのキャラで新しいシーンを描く」形で生成する。
2. **チャプター1の終了フレーム**: いま作った開始フレーム単体を入力に、「同じ絵のまま、動きが変える部分だけ終了状態に変える」編集プロンプトで生成する。
3. **チャプター2の開始フレーム＝チャプター1の終了フレーム**（原則、再生成せず同一ファイルを共有。カメラ・場所が変わるときのみ前フレームを種に新規生成）。
4. 以降も 開始→終了 の順で前フレームを種にチェーンする。ゼロから独立生成しない。

```
python3 .claude/skills/local-video/stitch_refs.py 03_SCRIPTS/<NN>_<slug>/ref_canvas_ch1_start.png \
  03_SCRIPTS/<NN>_<slug>/Sobaya_sheet.png 03_SCRIPTS/<NN>_<slug>/Fukuchan_sheet.png

.claude/skills/local-video/dt_generate.sh 03_SCRIPTS/<NN>_<slug>/ch1_start.png \
  03_SCRIPTS/<NN>_<slug>/ref_canvas_ch1_start.png 42 1024x576 <<'EOF'
The input image is a contact sheet of character model sheets — identity/design references only, NOT a composition reference. Using exactly these characters, create the FIRST-FRAME still of a video shot: <START state incl. Prop states and Fixture layout>. <the run's style block>. Single still frame, one coherent scene, no text overlay, no sheet-style panels or labels.
EOF
```

### チェーン中のデザイン劣化とシート再投入

前フレームだけを種に繋ぐと数フレームでデザインが劣化する（実測: 5枚目でやめ太郎の丸メガネが四角い黒縁に変わった）。対策:

- NG要素が崩れたフレームは**前フレーム＋キャラクターシートの連結キャンバス**を種に作り直す（前フレーム単体で作り直しても同じ崩れ方をする）。
- 同一キャラが5枚以上続くチェーンでは、崩れる前でも数フレームおきにシートを再投入する。
- **NG要素は毎フレーム明文で固定する**（正しい形＋否定形のセット。例: "he keeps SMALL ROUND white-rimmed glasses — NOT rectangular, NOT thick dark-rimmed"）。「形が変わる」だけでなく「丸ごと消える」ドリフトも起きるため、存在自体も守る（"he is ALWAYS WEARING his round glasses ... the glasses do NOT disappear"）。
- ラン途中の新キャラ登場は、シート連結より**文章指定**のほうが画風混在（その新キャラだけ写実顔になる等）を起こしにくい。前フレーム単体を種に、各キャラ設定mdの「プロンプト用同定句（英語）」＋"Draw <name> in EXACTLY the same rendering style as the rest of the input image"で指定する。キーフレーム上の似姿は多少甘くてよい（動画側の同一性はH3へ渡すシートで担保する。優先すべきは画風の統一と構図）。
- セリフのあるチャプターのキーフレームは**話者の口を開け、非話者の口を閉じて**描く（リップシンク取り違え防止の最強シグナル）。

## 6. 画像検証（Qwen3-VL一括検証→修正リスト確定→部分再生成）

**全キーフレームが出揃ってから**検証フェーズに入る。逐次「1枚直してはまた生成」はチェーンの再共有を繰り返して整合性を壊すため禁止。手順:

### 6-1. 全フレームをVLMで検証する

各キーフレームについて、`script.md`から**そのフレーム固有のチェックリスト**を組み立て、同梱の`verify_frame.py`（Ollama + Qwen3-VL）に渡す:

```
python3 .claude/skills/local-video/verify_frame.py 03_SCRIPTS/<NN>_<slug>/ch3_start.png <<'EOF'
This image should be the first frame of a video shot. Verify ALL of the following and answer PASS or FAIL per item:
1. Exactly one coherent scene (not a multi-panel sheet, no contact-sheet layout, no text/labels/watermarks).
2. Fukuchan — a slim stylish black-haired man in a black long coat — is standing on the LEFT, mouth OPEN mid-speech.
3. Yametaro — a chibi 3D figure with an oversized head — wears SMALL ROUND white-rimmed glasses (not rectangular, not missing), mouth CLOSED.
4. The beer mug on the table is EMPTY (per the prop ledger cell for C3 start).
5. The entrance door is hinged on its LEFT edge with a silver lever handle on the RIGHT edge at mid-height.
6. Style: photorealistic live-action-style scene (NOT flat 2D anime), with Yametaro alone rendered as a soft matte 3D chibi figure.
EOF
```

チェックリストに必ず含める観点（フレームごとに`script.md`の該当箇所から具体化する）:

1. **1枚絵として成立しているか**（複数パネル・シート化・文字混入・ウォーターマークがない）
2. **登場キャラ全員のNG要素**（各`02_CHARACTERS/0N_*.md`のNG変更。形の崩れと「丸ごと消える」の両方）
3. **Prop state ledgerの該当セルとの一致**（グラスの中身・持ち方等）
4. **Fixture layoutとの一致**（蝶番側・ノブ側・開き方向）
5. **話者の口の開閉**（セリフのあるチャプター: 話者は口が開き、非話者は閉じている）
6. **画風の一致**（そのランの画風固定文と合っているか）

- `verify_frame.py`は`VERDICT: PASS`/`VERDICT: FAIL`＋指摘リストを返す。**FAILだけでなくPASSでも指摘内容を読み、ClaudeもReadで画像を開いて突き合わせる**（VLMの見落とし・誤検出の両方があり得る。最終判断はClaudeが行う）。
- 隣接フレーム間の整合（つなぎ目共有、金具位置の連続性、状態遷移に対応する動作の有無）はVLMの単画像検証では見えないため、**Prop state ledgerの1行ごとに全フレームを時系列で見比べる最終チェック**をClaudeが行う（動作なしに状態が飛んでいる境界があれば修正リストに載せる）。

### 6-2. 修正リストを完全確定させる

全フレームの検証結果を`03_SCRIPTS/<NN>_<slug>/fix_list.md`にまとめる（英語）。1行＝1修正: 対象ファイル / 問題 / 修正方針（プロンプト修正・種の変更・シート再投入） / 影響を受ける下流フレーム（共有・チェーン先）。

**fix_list.mdが完全に確定するまで、1枚も再生成しない。** これがこのスキルの画像工程の要（検証と修正の混走はチェーン崩壊と手戻りの温床）。

### 6-3. 必要な画像だけ再生成し、再検証する

- fix_list.mdの項目を**チャプター番号の若い順（チェーンの上流から）**に処理する。
- NG要素の崩れは「前フレーム＋キャラクターシートの連結キャンバス」を種に作り直す（ステップ5のデザイン引き戻しルール）。
- 再生成したフレームを種・共有元にしていた下流フレームは追従させる（共有フレームはコピーし直し、チェーン先は必要なら再生成）。追従したフレームもfix_list.mdに再検証行を足す。
- 再検証はfix_list.mdに載ったフレームだけでよい（全数再検証は不要）。全行が解消したらステップ7へ。

## 7. H3動画生成（チャプター毎・ComfyUI）

### 実行方法

1. ComfyUIをバックグラウンドで起動する（起動済みならそのまま使う）: `cd ~/ComfyUI && python3 main.py --listen 127.0.0.1 --port 8188`（環境により`--lowvram`等を付与）。
2. チャプターの入力ファイル（キーフレームPNG・シートPNG・wav）を`ComfyUI/input/`へコピーする。
3. セットアップ時に保存したAPIワークフローJSON（`h3_i2v_api.json`/`h3_r2v_api.json`）をラン専用ディレクトリへ`chN_workflow.json`としてコピーし、そのチャプターのH3 inputs表どおりに書き換える（画像/音声ファイル名、Motion prompt原文、尺、解像度、モードに応じたチェックポイント）。
4. 同梱の`h3_run.py`で投入し、完了を待って出力を回収する:

```
python3 .claude/skills/local-video/h3_run.py 03_SCRIPTS/<NN>_<slug>/ch3_workflow.json \
  --out 03_SCRIPTS/<NN>_<slug>/ch3.mp4
```

- 生成は1本あたり長時間かかる（Apple Silicon実測値はセットアップ後に必ず1本目で計測して見積もる）。**必ずバックグラウンドで実行**し、`h3_run.py`のポーリング出力をモニタする。
- Motion promptはH3 inputs表の**原文をそのまま**JSONに入れる（要約・短縮禁止）。

### 生成実行プロトコル（`script.md`末尾に英語で必ず記載）

seedance SKILL.mdステップ5のプロトコルを本スキル用に置き換えて記載する:

```
## Generation & assembly protocol (REQUIRED — read before generating any chapter)

### Step 1 — Pilot chapter first (batch generation is FORBIDDEN until the pilot passes)
Generate ONLY the first dialogue chapter, then verify ALL of the following:
- [ ] The dialogue in the output is driven by the attached wav (correct voice, no synthesized/doubled voice)
- [ ] The CORRECT character lip-syncs (speaker's mouth moves only while the audio plays; non-speakers stay closed)
- [ ] The video starts/ends on (or acceptably close to) the start/end keyframes — check R2V frame anchoring
- [ ] Motion, poses, prop states and fixture hardware match the Motion prompt / ledgers
- [ ] Character identity and NG-change elements survive H3 generation (compare against the sheets)
- [ ] Duration matches the H3 inputs table (remember the 17k+5-frame grid rounding)
If any check fails, fix the workflow inputs/prompt and regenerate the pilot until all pass.
Only then generate the remaining chapters, and re-run at least the audio + duration checks on each.

### Step 2 — Prompts are verbatim
Copy each chapter's Motion prompt into the workflow JSON EXACTLY as written here. Do NOT
summarize or shorten. If it seems too long, go back to the script and split the chapter.

### Step 3 — Final audio track (assembly)
The audio embedded in generated chapters is NOT the final dialogue audio. During assembly:
1. For every dialogue chapter, strip the embedded audio and lay the original wavs from the
   Dialogue audio table over the video, aligned to the frame where the speaker's mouth starts moving.
2. Chapters without dialogue may keep their generated ambient audio.
3. Play back the assembled video before delivery and confirm every line is the local
   Irodori-TTS / VOICEVOX take (the source wavs are the single source of truth).
```

## 8. 結合と最終音声（ffmpeg）

1. **チャプター単位で音声を確定させる**（セリフ入りチャプターは埋め込み音声を捨て、ローカルwavを口の動きに合わせたオフセットで載せる）:

```
# offset: 話者の口が動き始めるフレームの時刻（ms）。動画を確認して決める
ffmpeg -y -i ch3.mp4 -i ch3_line1_fukuchan.wav \
  -filter_complex "[1:a]adelay=800|800,apad[a]" \
  -map 0:v -map "[a]" -c:v copy -shortest ch3_final.mp4
```

セリフのないチャプターは`cp chN.mp4 chN_final.mp4`（生成環境音を残す）。環境音とセリフを混ぜたい場合のみ`amix`を使い、セリフが二重になっていないことを確認する。

2. **全チャプターを結合する**:

```
printf "file 'ch1_final.mp4'\nfile 'ch2_final.mp4'\n" > concat.txt   # 全チャプター分
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy final_draft.mp4
```

3. **VOICEVOXクレジットの焼き込み（VOICEVOXの声を使ったランでは必須）**: CapCutが無いので、ffmpegの`drawtext`で動画末尾にクレジットを表示する（`script.md`の`## Credits`にこのコマンドを記載する）:

```
ffmpeg -y -i final_draft.mp4 -vf "drawtext=fontfile='/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc':text='VOICEVOX\:白上虎太郎 / VOICEVOX\:ずんだもん':fontsize=28:fontcolor=white:borderw=2:bordercolor=black:x=w-tw-24:y=h-th-24:enable='gte(t,<末尾クリップ開始秒>)'" -c:a copy final.mp4
```

4. 結合後の`final.mp4`を通しで確認する（つなぎ目の絵飛び、音声のズレ・二重、尺）。成果物はラン専用ディレクトリに置く。

## 9. 同梱物の最終検証（必須・完了報告の直前）

```
python3 .claude/skills/local-video/validate_local_run_bundle.py 03_SCRIPTS/<NN>_<slug>
```

検証内容: H3 inputs表の全ファイルがラン直下に物理ファイルとして存在する / R2Vチャプターの入力が「画像9・音声3・合計12」以内 / 各Motion promptが`Required attached input files:`で全`<Picture N>`/`<Audio N>`をファイル名ごと再宣言している / I2VチャプターにFirst/Last frameがある / `script.md`がラン外パスを参照していない。

**検証が失敗したままユーザーへ完了報告してはいけない。**
