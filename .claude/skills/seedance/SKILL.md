---
name: seedance
description: 窓際族物語のストーリー（あらすじ）からSeedance用の台本・動画生成プロンプト・セリフ音声（VOICEVOX/Irodori-TTSボイスクローン）・Codex参考画像を作成するワークフロー。ユーザーからストーリーを渡されたとき、台本やSeedanceプロンプトの作成・修正を頼まれたとき、キャラのセリフ音声の生成を頼まれたとき、クリップの参考画像（キーフレーム）生成を頼まれたときに必ず使用する。
---

# Seedance 動画制作ワークフロー

ユーザーからストーリー（あらすじ）を渡されたら、以下の7ステップを一連の流れとして実行する。

1. このラン専用の出力ディレクトリを作成する
2. **使用する全キャラクターシート・スケール参照画像をラン専用ディレクトリへ実ファイルとしてコピーする**
3. 台本＋Seedanceプロンプト（英語）の作成（各クリップに開始状態と終了状態を明記する）
4. VOICEVOX/Irodori-TTSによる全セリフの音声生成
5. Codexによる各クリップのキーフレーム生成（**開始フレーム＋終了フレームの2枚**を作る）
6. Seedanceへの入力対応表と、各Motion prompt内の添付宣言を`script.md`に明記する
7. 生成実行プロトコルを明記し、同梱物の機械検証を通す

### 精度の要（この方式にする理由）

動画生成は**CapCutに統合されたSeedance 2.0**を使う。CapCutは**開始フレームだけでなく「開始＋終了フレーム（Frame A / Frame B）」入力に対応**しており、両端を固定して間を補間させることで、単一フレーム/text-to-videoで起きる**キャラのブレ（identity drift）・ちらつき・構図ズレを減らせる**。さらに**参照画像を多数**渡してキャラの同一性を固定できる。本スキルはこの両方を最大限使う設計にする。中間キーフレーム入力は存在しないため、**細かい動きの制御はクリップを短く割る**ことで代替する。

## 前提となる参照ファイル

- 世界観: `01_WORLD/WORLD_BIBLE.md`
- キャラクター設定: `02_CHARACTERS/*.md`（各キャラのNG変更＝デザイン上変えてはいけない要素に注意）
- ボイスキャスト表: `02_CHARACTERS/VOICE_CAST.md`（キャラ→VOICEVOX話者・スタイルIDの正典）
- 過去の制作物: `03_SCRIPTS/`

## 0. 出力ディレクトリ（毎回、新しい同一ディレクトリにまとめる）

**プロンプト（台本ファイル）と参考画像は、毎回そのラン専用の新しい1つのディレクトリにまとめて出力する。** 従来のように台本を`03_SCRIPTS/`直下、画像を共有の`ref_images/`に分散させない。

- ディレクトリ: `03_SCRIPTS/<NN>_<slug>/`
  - `<NN>` は既存の連番の次の番号（`03_SCRIPTS/`直下・サブディレクトリの最大番号 + 1、ゼロ埋め2桁）。
  - `<slug>` は内容が分かる英語の短い識別子（小文字・アンダースコア区切り。例: `yametaro_43degrees`）。
- そのディレクトリの中に、台本兼プロンプトファイル `script.md` と、全クリップの参考画像 `*.png` を **すべて同じ階層に** 置く。画像用のサブディレクトリは作らない。
- 台本内から画像を参照するときは、同じディレクトリ内の相対パス（例: `clip1_01_ref.png`）で書く。
- **「参考画像」には生成キーフレームだけでなく、CapCutへ添付するキャラクターシート、`height_lineup.png`、小道具・環境参照もすべて含む。** 使用する参照画像を`02_CHARACTERS/`等からラン専用ディレクトリ直下へコピーし、ファイル名を維持する。正典ファイルは変更しない。
- 参照画像はsymlinkではなく**通常ファイルとして物理的に同梱する**。成果物フォルダだけを渡してもCapCut入力が完結する状態にする。
- `script.md`では同梱ファイルをbasenameだけで参照する（例: `Sobaya_sheet.png`）。`../../02_CHARACTERS/Sobaya_sheet.png`のようなラン外への相対パスは禁止する。
- キャラクターシートをラン外から参照できることを、同梱の代用にしてはいけない。1枚でも欠けていればそのランは未完成とする。
- 既存の`03_SCRIPTS/`直下の古い成果物は移動・改変しない。この新ルールは新規ランから適用する。

### 参照画像の同梱手順（必須・台本作成前に実行）

1. 全クリップの登場キャラを列挙する（画面外の声だけのキャラも、Motion promptで`@ImageN`参照するなら対象）。
2. 各キャラ設定mdの「キャラクターシート」に記載された`*_sheet.png`をラン専用ディレクトリ直下へコピーする。
3. `height_lineup.png`等をCapCut入力で使う場合も同じ場所へコピーする。
4. `script.md`冒頭の`Character references`には同梱後のbasenameだけを書く。
5. 以降のキーフレーム生成とCapCut入力には、ラン専用ディレクトリ内のコピーを使う。これにより同梱漏れを制作途中で発見する。

## 1. 台本作成（deliverableはすべて英語）

`WORLD_BIBLE.md`のStory Formula（変なことを始める→巻き込まれる→少し騒ぎになる→最後は笑顔）と各キャラのNG変更を守りつつ、尺に応じてクリップ分割した台本＋Seedanceプロンプトを `03_SCRIPTS/<NN>_<slug>/script.md` に作成する。

`WORLD_BIBLE.md`の禁止事項（ブラック企業描写、いじめ、パワハラ、鬱展開、グロ描写）を厳守する。

### クリップ分割とキーフレーム設計（重要）

各クリップは**開始状態（first frame）と終了状態（last frame）を明確に区別して書く**。台本の各クリップに、次の2つを必ず記述する:

- **First frame**: そのクリップ冒頭の静止画で写っている内容（構図・キャラの位置・表情）。
- **Last frame**: そのクリップ終端の静止画。ここまでにどう動いた結果になるか。
- **Prop states**: そのクリップで状態が変わる小道具（グラス・瓶・食器・箱など）ごとに、First frame時点とLast frame時点の状態（中身の量、開栓/未開栓、手に持つ/置いてある、蓋の有無 等）を1行ずつ明記する。

さらに**つなぎ目を消すため、クリップNの Last frame と クリップN+1の First frame は同一の絵にする**（後述のとおり同じ画像ファイルを共有する）。小道具の状態も同様に引き継ぐ（クリップNのLast frameの状態 ＝ クリップN+1のFirst frameの状態。クリップをまたいで勝手に満杯に戻る/空になる等を起こさない）。

### Prop state ledger（全クリップ通しの状態台帳・必須）

`script.md` の冒頭（クリップ一覧の前）に、状態を持つ小道具すべての**通し状態台帳**を表で書く。行＝小道具、列＝キーフレーム境界。クリップNのLastとクリップN+1のFirstは**1つの列（セル）を共有**させる（2箇所に別々の値を書ける構造にしない。これが食い違いの物理的な防止になる）。

```
| Prop     | C1 start | C1 end = C2 start | C2 end = C3 start | C3 end = C4 start | C4 end |
|----------|----------|-------------------|-------------------|-------------------|--------|
| Beer mug | EMPTY    | EMPTY             | FULL (foam head)  | ONE SIP LOWER     | ONE SIP LOWER |
```

- 各クリップのProp states・キーフレーム生成プロンプト・Motion promptは、すべてこの台帳の該当セルと一致させる（台帳が唯一の正）。
- 台帳の**隣り合うセルで状態が変わるときは、その変化を起こす動作が画面内で見えること**。該当クリップのMotion promptにその動作（前状態→動作→後状態）が書かれていなければ、状態変化を書いてはいけない。

### 物理整合性ルール（小道具の状態遷移・重要）

状態の指定がないと、生成モデルは典型絵に寄る（例:「beer glass」→満杯のグラス、「holding a beer bottle」→ラッパ飲み）。その結果「満杯のグラスにさらに注ぐ」「ラッパ飲みした瓶からグラスに注ぐ」のような非常識な動画になる。これを防ぐため:

- **動作は必ず「前状態→動作→後状態」の形で書く。** 裸の動作だけ（"pours beer into a glass"）を書かない。両端の状態を英語で明示する: "lifts the bottle and pours beer into the EMPTY glass; by the end the glass is full with a foam head and the bottle is visibly emptier"。
- **デフォルトで典型絵になりやすい状態は、望む状態を大文字で強調して指定する**: "an EMPTY glass", "a FULL unopened bottle", "holds the bottle upright by the neck, NOT drinking from it"。
- **起きてほしくない動作は否定形でプロンプトに明記する**: "no one drinks directly from the bottle", "does not pour into an already-full glass"。開始/終了フレームの画像生成プロンプトとSeedanceのMotion promptの両方に入れる。
- **カット・場面転換・爆発/煙/変身などの演出は、小道具の状態を変える理由にならない。** 「煙に隠れている間に空になる」「場所が変わったので中身をリセット」のような**演出を口実にした状態ジャンプを台本に書くこと自体を禁止**する（過去に「ほぼ満杯のジョッキが爆発転換の後に空になる」台本を書いてしまい、ビールが突然消える動画になった）。転換後に別の状態が必要なら、(a) 転換**前に**状態を変える動作を画面内で見せる（例: 飲み干してから爆発する）、(b) 転換後も同じ状態を維持する、のどちらかにする。画面外での状態変化がどうしても必要なら、視聴者が補完できる理由をセリフ・描写で明示する。
- **論理チェック**: 台本を書き終えたらProp state ledgerを左から右へ通しで読み、(1) 状態遷移が物理的・社会常識的に成立しているか（満杯のグラスに注がない、口をつけた容器から他人のグラスに注がない、空の容器から注がない等）、(2) すべての状態変化に画面内の対応する動作があるか、の2点を確認する。

Seedanceの1クリップは4〜15秒。**動きが複雑・カメラワークが多いクリップは短く割る**（中間キーフレーム入力が無いため、割ること自体が中間制御になる）。1本のプロンプトに詰め込みすぎない。

### 機構小物の配置整合性ルール（ドアノブ・蝶番・スイッチ等・重要）

位置の指定がないと、生成モデルはドアノブ・蝶番・取っ手などの**動く建具・機構部品の位置を毎フレーム適当に描く**。その結果「蝶番側にノブが付く」「ドアを閉めている最中はノブがあるのに、閉まった途端に消える」等の破綻が起きる（過去に実際に発生した）。これを防ぐため:

- **開閉・可動する建具/機構小物（ドア・引き戸・窓・引き出し・冷蔵庫・ノートPC等）が映るランでは、`script.md`冒頭（Prop state ledgerの近く）に機構レイアウト台帳（Fixture layout）を書く。** 建具ごとに1行: カメラから見た蝶番側（LEFT/RIGHT）、ノブ/取っ手の位置（**必ず蝶番と反対側の端**・高さ）、開き方向（内開き/外開き・どちらへスイングするか）。この台帳は**全クリップを通して不変**であり、唯一の正とする。

```
## Fixture layout (constant across ALL clips — hinges and handles never move)

| Fixture | Hinge side (from camera) | Handle | Opens |
|---------|--------------------------|--------|-------|
| Entrance door | LEFT edge | silver lever handle on the RIGHT edge (opposite the hinges), mid-height | inward, swinging toward camera-left |
```

- **ノブ/取っ手は必ず蝶番の反対側の端に置く**（実物の建具の構造）。プロンプトでは片方だけ書かず、"hinged on its LEFT edge, with a silver lever handle on the RIGHT edge (the edge opposite the hinges) at mid-height" のように**蝶番側とノブ側を常にセットで**明示する。
- **建具が映る全キーフレーム生成プロンプトと全Motion promptに、台帳のレイアウトを毎回そのまま繰り返す。** 開いた状態の絵にも閉まった状態の絵にも書く。特に閉まる/閉まった状態では否定形まで入れる: "the lever handle stays visible on the RIGHT edge even when the door is fully closed — the handle does NOT disappear, does NOT move to the hinge side, and is NOT duplicated"。ドアが動くクリップのMotion promptには "the hinges and handle stay fixed to the same edges of the door throughout the swing" を入れる。
- **キーフレームの目視確認に金具を含める**: 生成した各フレームで (1) ノブ・取っ手が台帳どおりの側・高さにあるか、(2) 隣り合うフレーム間で蝶番・ノブの位置が動いたり消えたりしていないか、を確認し、ズレていたら再生成する。キーフレーム同士で金具位置が食い違うと、Seedanceは補間中にノブを消す・瞬間移動させる形で「辻褄合わせ」をしてしまう。

### 話者分離ルール（1クリップ1話者・重要）

Seedance 2.0は**複数人が映るクリップでのリップシンクの話者割り当てが弱い**（公式にも未解決の課題とされ、実際に「福ちゃんの音声でやめ太郎の口が動く」取り違えが起きた）。これを防ぐため:

- **1クリップにつき話者は1人を原則とする。** 会話の掛け合いは、話者が交代するタイミングでクリップを分割する（分割はつなぎ目共有フレームで滑らかに繋がるので尺・演出上の不利益はない）。
- 掛け合いのテンポ上どうしても1クリップに複数話者を入れる場合は、(1) 音声ファイルを発話順に分けて添付し、(2) Motion promptに話者の順番・誰がどの音声かを@メンションと見た目で明示し、(3) "the two lines do NOT overlap" を入れる。それでも取り違えが出たら迷わずクリップを割る。
- 台本上は、各セリフに**話者のキャラ名＋見た目の同定句**を添える（後述「話者バインディング」参照）。

### リップシンク精度ルール（クリップ尺≒発話長・重要）

Seedanceは「話す」と指示されたキャラの口を**クリップ全体にわたって動かしがち**で、クリップ尺が実発話より大幅に長いと口パクが音声からずれる（過去に4〜5秒のクリップへ実発話1.2〜1.7秒のwavを添付し、口の動きが約1.5秒遅れて始まり、音声終了後も1.5秒以上口が動き続ける動画になった）。これを防ぐため:

- **セリフのあるクリップの尺は「添付する音声wavの合計長＋約1秒」を目安にする**（実発話がクリップ尺の6割を下回る設計にしない）。無言のリアクション・ため・間はセリフ入りクリップに詰め込まず、**セリフなしの別クリップに分割**する（つなぎ目共有フレームで滑らかに繋がるので演出上の不利益はない）。
- **Motion promptに発話タイミングの拘束を必ず入れる**（話者バインディングの指示に加えて）: 話者について "begins the line almost immediately" と "the speaker's mouth moves ONLY while @Audio1 is playing — once the line ends the mouth stays CLOSED for the rest of the clip" を明記する。
- **添付するwavは前後の無音をトリムしたものにする**（ステップ2の同梱スクリプトが自動でトリムする。ユーザー提供など別途用意したwavも添付前に無音をトリムする）。wav内の長い無音はSeedanceの口パク開始位置を狂わせる。

### 言語ルール（重要）

**`script.md` は全文を英語で書く。** Seedanceに渡すプロンプト（コードブロック）だけでなく、見出し・尺やアスペクト比の説明・「画面内容」「カメラ」「音」「生成メモ」などの人間向け解説も含めて、すべて英語で記述する。

例外として英語以外を使ってよいのは次のみ:

- **キャラクターのセリフ（発話内容）**: 実際に日本語で発話される台詞は日本語のまま `"..."` で引用して埋め込む（例: `shouting "島流し一択やろ！"`）。ナレーションや画面内の指定文字（温度計の「43℃」など）も同様に、実際に表示・発話される言語のまま引用する。
- **発音・読みを指定したい場合など、非英語でしか正確に表現できない理由があるとき**: その語のみ元言語で書き、必要なら英語で補足する。

理由: 日本語の説明文はSeedanceでの再現精度が落ちること、および成果物を言語横断で扱いやすくするため。

### セリフ音声の扱い（Seedanceの発声禁止・音声添付必須・重要）

**キャラクターのセリフ・ナレーションの音声は、すべてステップ2で生成した音声ファイル（キャラごとにVOICEVOXまたはIrodori-TTS。配役は`VOICE_CAST.md`が正）が正**であり、Seedanceに声を生成させない（生成音声と重なると二重音声になるため）。セリフのあるクリップで音声生成を省略してSeedance任せにすることは禁止。ユーザーから別途音声ファイルが渡された場合は、そのクリップに限りユーザー提供の音声を優先する。

生成した音声は**Seedance（CapCut）生成時に添付ファイルとして渡し、動画にはその音声をそのまま使わせる**（キャラの口の動きは添付音声にリップシンクさせる）。

- 台本の各クリップでは、セリフは**口の動き（リップシンク）の指定としてのみ**書く。引用の後に `(lip-sync to the attached audio file — voice comes from the attached pre-generated audio, NOT generated)` を付ける。
- セリフのあるクリップのMotion promptに**指示を必ず入れる**: "use the attached audio file as the dialogue audio AS-IS and lip-sync the characters to it; do NOT generate any voice — no synthesized speech, no narration"。環境音・効果音まで不要な場合は "no audio other than the attached file" とする。

### 話者バインディング（音声→キャラの紐付け・重要）

モデルはキャラ名を知らないため、名前だけ書くと**別のキャラの口が動く取り違え**が起きる。セリフのあるクリップでは以下を必ず行う:

- **@メンションで役割を固定する**: Seedance 2.0（Omni Reference）は添付ファイルを`@Image1`/`@Audio1`のようにプロンプト内で参照し役割を指定できる。Motion promptで音声と参照画像を明示的に結びつける: "ONLY Fukuchan (@Image3, the stylish man in the ...) speaks, lip-syncing to @Audio1"。
- **話者は名前＋見た目の同定句で指定する**: キャラ名単独ではなく "Fukuchan — the slim stylish black-haired man in a black long coat" のように、参照画像から一意に分かる外見描写を毎回添える。同定句は各キャラ設定md（`02_CHARACTERS/0N_*.md`）の「プロンプト用同定句（英語）：」を正典として使い、クリップごとに言い換えない（表記ゆれ自体が取り違えの原因になる）。
- **話さないキャラは否定形で口を閉じさせる**: 画面内の非話者全員について "Yametaro (@Image4) does NOT speak — his mouth stays CLOSED, he only listens/reacts" を明記する。話者の指定だけでは足りず、非話者の禁止まで書くのが取り違え防止の肝。
- `script.md` のCapCut inputs表に `Audio` 行を追加し、添付する音声ファイル名と「Seedance生成の入力として添付し、そのまま使わせる」ことを明記する（記載例は後述）。
- **添付音声は「生成時の参照」で終わらせない。** 生成時に添付してもSeedanceが参照音声として扱い、最終動画に元音声が乗らない事故が起きた。**最終的な音声の正は、CapCutタイムライン上に明示的に並べ直したローカルwav**とする（生成クリップに埋め込まれた音声はミュートして差し替える）。手順はステップ5「生成実行プロトコル」で必ず`script.md`に記載する。

## 2. セリフ音声の生成（全セリフ必須）

台本が完成したら、**台本中のすべてのセリフ・ナレーションの音声をローカルで生成し、ラン専用ディレクトリに保存する**。このwavはSeedance（CapCut）生成時に添付ファイルとして渡し、動画にそのまま使わせる（Seedanceの生成音声は使わない）。

### 配役（正典）

- キャラごとの使用エンジンと指定（Irodori-TTSの参照音声 / VOICEVOXの話者・スタイルID）は **`02_CHARACTERS/VOICE_CAST.md` が唯一の正**。この表にない声を勝手に割り当てない。
- **本人の声サンプルがあるキャラ（そば屋・福ちゃん・やめたろう・おかやまん・よーたん）はIrodori-TTSのボイスクローン**で生成する。参照音声は`02_CHARACTERS/<キャラ>_voice.wav`（各キャラ設定ファイルの「声ファイル：」に記載）。事前学習は不要で、**合成のたびに参照音声を渡す**ゼロショット方式。
- それ以外のキャラはVOICEVOXで生成する。感情差分スタイルはシーンに合わせてVOICE_CAST.mdの範囲で選んでよい。
- **ゆめみんは言葉を話さない**設定のため、台本にセリフ（言葉）を書かない。鳴き声（「きゅー！」「ぼんっ！」等）が必要な場合はVOICE_CAST.mdの指定voice（ずんだもん）で鳴き声テキストを生成する。

### 生成手順

1クリップ内のセリフ1つ（1人の連続した発話）につき1ファイル生成する。エンジンに応じて同梱スクリプトを使い分ける:

```
# Irodori-TTSのキャラ（そば屋・福ちゃん・やめたろう・おかやまん・よーたん）
.claude/skills/seedance/irodori_speak.sh "セリフテキスト" 03_SCRIPTS/<NN>_<slug>/clipN_lineM_<char>.wav 02_CHARACTERS/<キャラ>_voice.wav

# そば屋のみ: クローン生成後にモンスターボイス加工を必ずかける（in-place。VOICE_CAST.md参照）
.claude/skills/seedance/sobaya_monsterize.sh 03_SCRIPTS/<NN>_<slug>/clipN_lineM_sobaya.wav

# VOICEVOXのキャラ
.claude/skills/seedance/voicevox_speak.sh "セリフテキスト" 03_SCRIPTS/<NN>_<slug>/clipN_lineM_<char>.wav <スタイルID> [話速]
```

- VOICEVOXはエンジン未起動なら自動起動する（設置場所は`~/voicevox_engine/`）。Irodori-TTSは`~/irodori_tts`に設置済みであること（無いマシンではスクリプトのエラーメッセージに従う。1文あたり数十秒〜数分かかる）。
- 両スクリプトは合成後に**前後の無音を自動トリム**する（先頭約0.1秒・末尾約0.2秒だけ残す。長い無音はSeedanceの口パク開始位置を狂わせるため）。Dialogue audio表に記録する再生時間はトリム後の値を使う。
- **ファイル名**: `clipN_lineM_<char>.wav`（N=クリップ番号、M=クリップ内の発話順、char=キャラ名小文字。例: `clip1_line2_sobaya.wav`）。台本ファイル・画像と同じ階層に置く。
- 生成テキストは**実際に発話される日本語のセリフそのまま**を渡す（英訳やローマ字にしない）。イントネーションがおかしい場合は読み仮名に直したテキストで再生成してよい（台本上の表記は変えない）。
- Irodori-TTSは生成ごとに揺らぎがある。**再生成して選び直したいときはシード値（第4引数）を変えて数候補作る**。良い結果のシードは`script.md`のDialogue audio表に記録しておくと再現できる。
- スクリプトが出力する**再生時間（秒）を`script.md`のDialogue audio表に記録する**。クリップ尺はセリフの合計時間より長くしつつ、**「音声wavの合計長＋約1秒」を目安に詰める**（ステップ1「リップシンク精度ルール」参照）。尺に収まらない場合はクリップを延ばすか、VOICEVOXは話速を上げる。
- 生成後、各wavを再生確認できない環境でも、少なくとも全ファイルの存在と再生時間の妥当性（0.5秒未満や異常に長いものがないか）を確認する。

### script.mdへの記載（Dialogue audio表・必須）

`script.md`の冒頭（Prop state ledgerの近く）に、全セリフの通し表を書く（英語。セリフ本文のみ日本語のまま）:

```
## Dialogue audio (all voices pre-generated locally — Seedance must NOT generate any voice)

| File | Clip | Character | Voice (engine) | Line (ja) | Duration |
|------|------|-----------|----------------|-----------|----------|
| clip1_line1_sobaya.wav | 1 | Sobaya | Irodori-TTS (ref: Sobaya_voice.wav, seed 42) + monsterize | 快適です！ | 1.8s |
| clip1_line2_yotan.wav  | 1 | Yotan  | VOICEVOX (style 100) | ロックだぜ。 | 1.5s |
```

### VOICEVOXクレジット表記（動画内表示・必須）

VOICEVOXの利用規約により、**VOICEVOXの声を1つでも使った動画には、動画内（画面内）に使用キャラクターのクレジット表記を必ず入れる**（概要欄だけで済ませない）。

- `script.md`末尾に `## Credits` セクションを必ず書き、使用したVOICEVOX話者の一覧を記載する（例: `VOICEVOX:白上虎太郎 / VOICEVOX:ずんだもん`。話者名の対応は`VOICE_CAST.md`参照。Irodori-TTSのキャラはクレジット不要）。
- 同セクションに、**CapCut編集時に動画内へクレジットを表示する指示**を明記する: 動画末尾のエンドカード、または最終クリップへのテキストオーバーレイとして、上記のクレジット文字列をそのまま表示する（例: `On-screen credit (add in CapCut as end-card/overlay text): VOICEVOX:白上虎太郎 / VOICEVOX:ずんだもん`）。
- クレジットはSeedanceに画像・プロンプト経由で描画させない（文字が崩れるため）。**必ずCapCutのテキスト機能で載せる**。

## 3. Codexによるキーフレーム生成（開始＋終了の2枚）

Seedance用プロンプトを作成したら、`codex` CLIの画像生成ツールで各クリップの**開始フレームと終了フレームの2枚**を生成し、**ステップ0で作成したラン専用ディレクトリに保存する**。これがSeedanceの First-Last-Frame 入力にそのまま渡る本番アセットになる。

### 枚数とファイル名

- **1クリップにつき開始フレーム1枚＋終了フレーム1枚の計2枚**を生成する（従来の「loose3枚」は廃止）。
- ファイル名は役割が分かる形にする: `clipN_start.png` / `clipN_end.png`（Nはクリップ番号）。
- 保存先は必ずラン専用ディレクトリ `03_SCRIPTS/<NN>_<slug>/` 内。台本ファイルと同じ階層に置く。

### 生成順序（整合性を壊さないため必須）

キーフレーム同士が食い違うとSeedanceの補間がモーフィング崩壊を起こすため、**必ず前の絵を種にして次の絵を作る**（ゼロから独立生成しない）。

1. **クリップ1の開始フレーム**を、登場キャラ全員の参照画像を`-i`で渡して生成する。
2. **クリップ1の終了フレーム**は、たった今作った**クリップ1の開始フレームを`-i`に加えて**「同じ絵のまま、状態だけ終了状態に変える」形で img2img 生成する（キャラ参照画像も引き続き渡す）。
3. **クリップ2の開始フレーム = クリップ1の終了フレーム**。原則ここは**新規生成せず同じ画像ファイルをコピー/参照して共有する**（つなぎ目消し）。カメラや場所が切り替わって共有できない場合のみ、クリップ1終了フレームを種に新規生成する。
4. 以降のクリップも 開始→終了 の順で、前フレームを種にチェーンしていく。

### キャラクター参照画像（同一性の固定）

- **そのクリップに登場するキャラクター全員の参照画像を`-i`で渡す**。各キャラの**第一参照はキャラクターシート**`02_CHARACTERS/<キャラ名>_sheet.png`（多面図モデルシート: 三面図＋NG要素クローズアップ＋表情/アクション差分＋身長比較＋カラーパレット。各キャラ設定mdの「キャラクターシート：」に記載）。三面図は横顔・後ろ姿・振り向きのカットで、クローズアップはNG要素（仮面・触手・ウクレレ等）の維持に、表情差分は演技時の顔崩れ防止に効く。単体参照画像（「画像ファイル：」記載）は、シートで再現が甘い場合に追加で渡す。
- 正典のシートをラン専用ディレクトリへコピーした後は、`codex exec -i`にも同梱コピー（`03_SCRIPTS/<NN>_<slug>/<Name>_sheet.png`）を渡す。正典パスを直接使って同梱確認を迂回しない。
- プロンプト文中で「Image N: <キャラ名> reference — keep face/design and NG-change elements consistent」のように役割を明記し、NG変更対象（そば屋の仮面/たこさんの触手/とーくんのウクレレ等）を維持させる。

### コマンド例（クリップ1・そば屋/とーくん/よーたん/福ちゃん/無職やめたろう登場）

開始フレーム:
```
codex exec -s workspace-write --enable image_generation \
  -i 03_SCRIPTS/<NN>_<slug>/Sobaya_sheet.png -i 03_SCRIPTS/<NN>_<slug>/Tokun_sheet.png -i 03_SCRIPTS/<NN>_<slug>/Yotan_sheet.png -i 03_SCRIPTS/<NN>_<slug>/Fukuchan_sheet.png -i 03_SCRIPTS/<NN>_<slug>/Yametaro_sheet.png \
  "Use your image generation tool to create the FIRST-FRAME still of a video shot. Input images Image 1..5 are character sheets (front/side/back turnarounds of each character; Sobaya: keep face/mask/build; Tokun: keep aloha/hat/ukulele; Yotan: keep blond/guitar/rock outfit; Fukuchan: keep stylish outfit; Yametaro: keep design) — identity/design references only, keep every face/design and NG-change element consistent. Prompt: <English scene description of the clip's START state, excluding dialogue and camera-work notation>. Comedic slice-of-life anime-illustration style, single still frame, no text overlay. Save as 03_SCRIPTS/<NN>_<slug>/clip1_start.png."
```

終了フレーム（開始フレームを種にする）:
```
codex exec -s workspace-write --enable image_generation \
  -i 03_SCRIPTS/<NN>_<slug>/clip1_start.png \
  -i 03_SCRIPTS/<NN>_<slug>/Sobaya_sheet.png -i 03_SCRIPTS/<NN>_<slug>/Tokun_sheet.png -i 03_SCRIPTS/<NN>_<slug>/Yotan_sheet.png -i 03_SCRIPTS/<NN>_<slug>/Fukuchan_sheet.png -i 03_SCRIPTS/<NN>_<slug>/Yametaro_sheet.png \
  "Use your image generation tool to create the LAST-FRAME still of the same shot. Image 1 is this clip's start frame — keep the same characters, art style, framing, lighting and location, change ONLY what the motion changes. Images 2..6 are character sheets (front/side/back turnarounds) — identity/design references only, keep every face/design and NG-change element consistent. Prompt: <English scene description of the clip's END state>. Single still frame, no text overlay. Save as 03_SCRIPTS/<NN>_<slug>/clip1_end.png."
```

### ポイント

- **Codexで生成するのは静止画のキーフレームPNGのみ。** 参考動画（モーション参照用のwebm/mp4など、動画ファイル全般）はCodexでは作らない。
- `--enable image_generation` と、プロンプト内での明示的な "Use your image generation tool" を必ず両方指定する（省くとPythonの簡易描画にフォールバックすることがある）。
- 終了フレーム生成では**開始フレームを必ず`-i`の先頭に入れ**、「framing/lighting/locationは維持、動きが変える部分だけ変更」と指示する。これが崩壊防止の肝。
- クリップ間で同じ絵を共有できるときは**再生成せずファイルを使い回す**（生成ゆらぎを持ち込まない）。
- **セリフのあるクリップのキーフレームには話者を視覚的に示す**: 話者は口を開けて話している最中の状態（ジェスチャー含む）で描き、非話者は口を閉じた状態で描く（例: "Fukuchan is mid-speech with his mouth open; Yametaro's mouth is closed, listening"）。キーフレーム自体が「誰が話しているか」の最も強いシグナルになり、リップシンクの取り違えを防ぐ。生成後の目視確認でも話者の口の開閉をチェックする。
- 画像生成プロンプトには台本のProp states（グラスの中身の量、瓶の持ち方等）とFixture layout（蝶番側・ノブ側・開き方向）をそのまま含める。**生成後は各画像をReadで開き、小道具の状態がProp state ledgerの該当セルと一致しているか、建具の蝶番・ノブがFixture layoutどおりの側にあるか目視確認する**（例: 開始フレームのグラスが空であるべきなのに満杯で描かれていないか、瓶に口をつけていないか、閉まったドアのノブが蝶番側に付いたり消えたりしていないか）。ズレていたら再生成する。キーフレームが間違っているとSeedanceは間違った状態間を忠実に補間してしまう。
- 全キーフレーム生成後、**台帳の1行ごとに全フレームを時系列で見比べる最終チェック**を行う: 隣り合うフレーム間で小道具の状態が変わっている箇所すべてに、そのクリップのMotion prompt内の対応する動作があるか確認する。動作なしに状態が飛んでいる境界が1つでもあれば、該当フレームを再生成するか台本を直してから次の工程に進む。
- 保存先は必ず `03_SCRIPTS/<NN>_<slug>/` 配下。
- ユーザーからストーリーを渡された際は、台本・Seedanceプロンプト作成に続けて、このルール（クリップごとに開始＋終了の2枚、前フレームを種にチェーン、キャラ参照を必ず添付、つなぎ目は共有）に沿ってキーフレームも生成する。

## 4. CapCut（Seedance 2.0）への入力対応表

動画生成は**CapCutに統合されたSeedance 2.0**で行う。CapCutは**開始フレーム（Frame A）と終了フレーム（Frame B）のデュアル参照**に対応し、参照画像も多数渡せる。`script.md`の各クリップに、**CapCutの各スロットへ何を渡すか**の対応表を必ず書く（ユーザーがそのまま設定できるようにするため）。

各クリップの記載例（英語で書く）:

```
### CapCut inputs (Clip 1)
- Start frame (Frame A): clip1_start.png
- End frame (Frame B):   clip1_end.png
- Reference images (identity lock — one line per file so CapCut slot numbers map to characters):
  - @Image1 = Sobaya_sheet.png → Sobaya (the hulking 180cm/100kg masked man)
  - @Image2 = Tokun_sheet.png → Tokun (the chubby 165cm man in straw hat and aloha shirt)
  - @Image3 = Yotan_sheet.png → Yotan (the slim 170cm blond rocker)
  - @Image4 = Fukuchan_sheet.png → Fukuchan (the slim stylish 170cm man in a black long coat)
  - @Image5 = Yametaro_sheet.png → Yametaro (the chibi cartoon man with round glasses)
- Motion prompt: <the clip's Seedance prompt — describe the motion BETWEEN the two frames as explicit state transitions (e.g. "pours beer into the EMPTY glass until it is full; no one drinks from the bottle"); dialogue kept in original language>
- Duration: 5s / Aspect: 16:9
```

- **開始/終了フレームは必ず両方セット**する。片方だけだと単一フレームからの外挿になりブレやすい。
- **Motion promptは「そのまま貼れる完成形」で書き、実行時の要約・短縮を禁止する。** `script.md`のMotion promptがCapCutに入力される最終文字列そのものであり、生成実行者（人間・エージェント問わず）が独自に圧縮・言い換えしてはならない（過去に要約で開始/終了状態・プロップ・NG変更の制約が欠落し、整合性が崩れた）。プロンプトが長すぎて入らない・守られない場合は、要約するのではなく**台本に戻ってクリップを分割**し、1本あたりの情報量を減らす。
- **Durationは必ず明示設定する。** CapCut側のデフォルト尺（約8秒）のまま生成しない。対応表のDuration値を毎クリップ設定し、生成後に実尺が一致しているか確認する（全クリップが同じ約8秒になっていたらデフォルト尺のまま生成された兆候）。セリフのあるクリップのDurationは**「添付音声の合計長＋約1秒」**を目安にする（ステップ1「リップシンク精度ルール」参照）。
- 参照画像は**必要な枚数だけ渡してよい**（CapCut/Seedance 2.0は多数の参照画像を受け付ける）。登場キャラ全員分＋必要なら小道具・環境の参照を足して同一性を固める。プロンプト側で「これらは identity/design reference であって構図ではない」と役割を明記する。
- **Reference images表に書いた全ファイルはラン専用ディレクトリ直下に実在しなければならない。** 表だけ書いて実ファイルを同梱しない状態は禁止する。
- **キャラの参照はキャラクターシート`02_CHARACTERS/<キャラ名>_sheet.png`を第一に使う**（多面図モデルシート。複数アングル＋NG要素クローズアップ＋表情差分を1枚で渡せるため、横顔・後ろ姿・演技でのidentity driftに強い）。プロンプトには "Image N: <name>'s character model sheet — turnaround, detail close-ups and expressions of the SAME character, identity/design reference only, NOT a composition reference" のように役割を明記する。参照は画風の揃ったものだけを混ぜる（実写写真とアニメ調シートを同時に渡すと折衷して顔が変わるため、原則シート側に統一する）。
- **シート上の文字ラベルの扱い**: シートには「SOBAYA」「MASK」等の短い英語ラベルが入っており、これは部位とキャラ名の紐付けを強めるため意図的なもの（実運用で精度向上が確認されている）。ただし**補間対象になるキーフレーム（clipN_start/end.png）には文字を入れない**方針は変わらない。Motion promptに "the reference sheets' text labels must NOT appear in the video" を入れておくと安全。
- **シートとキャラの紐付けを対応表とプロンプトの両方で明示する**: 対応表のReference imagesは「@ImageN = ファイル名 → キャラ名（短い同定句）」の形で1行ずつ書く。Motion prompt内でキャラに言及するときは、毎回「キャラ名＋同定句＋@ImageN」で書く（例: "Sobaya (@Image1, the hulking masked man) lifts the mug"）。同定句は各キャラ設定md（`02_CHARACTERS/0N_*.md`）の「プロンプト用同定句（英語）：」が正典。年齢・身長・体格などの設定はシート画像に文字で書き込まず、この同定句としてプロンプト側で渡す（画像内の文字は動画に漏れて崩れるリスクがあり、モデルも文章仕様を確実には読まないため）。
- **各Motion promptの冒頭に、添付必須ファイルをファイル名付きで再宣言する。** 対応表の外に書いただけでは不十分。次の形式で、該当クリップの全`@ImageN`を列挙する:

```
Required attached reference files: @Image1 = Sobaya_sheet.png — Sobaya's character model sheet, identity/design reference only, NOT a composition reference; @Image2 = Yotan_sheet.png — Yotan's character model sheet, identity/design reference only, NOT a composition reference. These reference attachments are REQUIRED inputs and must remain attached for this generation.
```

- Motion prompt中で`@ImageN`を使う場合、その同じプロンプト内の`Required attached reference files:`行に、`@ImageN = 実ファイル名`と役割が必ず存在しなければならない。名前＋外見同定句だけでは添付宣言の代用にならない。
- **複数キャラが同時に映るクリップ**では、相対的な体格差を固定するため、身長比較画像`02_CHARACTERS/height_lineup.png`（全キャラ横並び・文字なし）をスケール参照として追加で渡してよい。プロンプトに "@ImageN is the height/scale reference for relative body sizes — NOT a composition reference" と役割を明記する。
- クリップをまたぐつなぎ目は、**前クリップの Frame B と次クリップの Frame A を同一画像**にすることで消す（ステップ3のチェーンで担保）。
- **（上級）動きの誘導を強めたいクリップ**では、`04_GAME_ASSETS/voxel`の該当キャラGLBをThree.jsで動かして書き出した短い動画（webm/mp4、合計15秒以内）を**モーション参照として追加で渡す**（Seedance 2.0は動画参照に対応）。構図とキャラはキーフレームで固定したまま、動きだけ正確になぞらせられる。**この参考動画をCodexに作らせることは禁止**（Codexの担当は静止画キーフレームのみ）。ユーザーから明示的に依頼されたときに限り、Codex以外の手段（Three.jsレンダリング等）で作成する。
- **セリフのあるクリップすべて**で、対応表に `Audio` 行を追加し（ステップ2で生成した音声ファイルをクリップ内の発話順に列挙）、**Seedance生成の入力として添付してそのまま使わせる**。Motion promptに音声添付の指示と発声禁止の否定指示を含める:

```
- Audio (attach to Seedance as input): clip1_line1_fukuchan.wav (@Audio1 — spoken by Fukuchan) — use AS-IS as the dialogue audio track
- Motion prompt: <... ONLY Fukuchan (@Image3, the stylish man in the green jacket) speaks, lip-syncing to @Audio1 — he begins the line almost immediately, and his mouth moves ONLY while @Audio1 is playing; once the line ends his mouth stays CLOSED for the rest of the clip; Yametaro (@Image4) does NOT speak — his mouth stays CLOSED, he only listens; use the attached audio AS-IS and do NOT generate any voice — no synthesized speech, no narration>
```

- 話者バインディング（@メンション＋見た目の同定句＋非話者の口閉じ指示）はステップ1「話者バインディング」のルールに従い、**セリフのある全クリップのMotion promptに必ず入れる**。1クリップ1話者の原則（話者交代でクリップを割る）もここで守られていること。

- **VOICEVOXの声を使ったランでは、対応表の末尾（全クリップの後）に動画内クレジットの指示を必ず書く**（ステップ2の「VOICEVOXクレジット表記」参照）。CapCutでの最終組み立て時に、エンドカードまたはテキストオーバーレイで `VOICEVOX:話者名` を動画内に表示させる:

```
### Credits (REQUIRED — add in CapCut before export)
- On-screen credit text (end-card or overlay on the final clip): VOICEVOX:白上虎太郎 / VOICEVOX:ずんだもん
- Add this with CapCut's text tool — do NOT render it via Seedance/keyframe images.
```

## 5. 生成実行プロトコル（script.mdに必ず含める・実行者への指示）

過去のランで「音声が生成時の参照扱いで終わり最終動画に元音声が乗らない」「12本を一括生成して尺・音声の検証を挟めない」「プロンプトの要約で制約が欠落する」「クリップ尺が発話より大幅に長く、口パクが音声から1秒以上ずれる」失敗が起きた。再発防止のため、**`script.md`の末尾（Creditsの前）に以下のプロトコルをそのまま（英語で）記載する**。CapCutで生成・編集する実行者（ユーザー・エージェント問わず）はこれに従う。

```
## Generation & assembly protocol (REQUIRED — read before generating anything in CapCut)

### Step 1 — Pilot clip first (batch generation is FORBIDDEN until the pilot passes)
Generate ONLY Clip 1, then verify ALL of the following before touching any other clip:
- [ ] The dialogue audio in the output is the attached wav AS-IS (no synthesized voice, no doubled voices)
- [ ] The CORRECT character lip-syncs to each line (the speaker named in the prompt moves their mouth; every non-speaker's mouth stays closed)
- [ ] Mouth motion starts and ends WITH the audio: the speaker's mouth starts moving when the line starts and stays CLOSED after the line ends (no lip-flap during silence)
- [ ] Motion, poses and prop states match the Motion prompt and the Prop state ledger
- [ ] Hinges, handles and other fixture hardware stay on the edges given in the Fixture layout table in EVERY frame (handles never disappear, jump to the hinge side, or duplicate — especially when a door finishes closing)
- [ ] The clip duration equals the Duration specified in the CapCut inputs table (NOT the ~8s default)
If any check fails, fix the inputs/prompt and regenerate Clip 1 until all pass.
Only then generate the remaining clips, and re-run at least the audio + duration checks on every clip.

### Step 2 — Prompts are verbatim
Paste each clip's Motion prompt into CapCut EXACTLY as written in this file.
Do NOT summarize, shorten, or paraphrase it. If it seems too long, do not compress it —
go back to the script and split the clip instead.

### Step 3 — Final audio track (assembly)
The audio embedded in the generated clips is NOT the final audio, even when the wav was
attached at generation time. When assembling the final video on the CapCut timeline:
1. Mute (or delete) the audio embedded in every generated clip.
2. Lay the original wav files from the Dialogue audio table onto the timeline as the
   final dialogue track. Align each wav to the VIDEO's mouth movement, NOT to the clip
   boundary: nudge the wav until the speech onset lands on the frame where the speaker's
   mouth starts moving.
3. Play back the full timeline before export and confirm every line sounds exactly like
   the local VOICEVOX / Irodori-TTS takes (the source wavs are the single source of truth).
```

- このプロトコルは**全クリップ生成前に読まれる位置**に置くこと（対応表の直後・Creditsの前）。
- クリップ数が多いランほどStep 1の効果が大きい。パイロット検証を省略して一括生成することを本スキルでは禁止する。

## 6. 同梱物の最終検証（必須・完了報告の直前）

次を実行し、成功するまで成果物を完了扱いにしない:

```
python3 .claude/skills/seedance/validate_run_bundle.py 03_SCRIPTS/<NN>_<slug>
```

検証は次を強制する:

- CapCut入力表にある全PNG/WAVがラン専用ディレクトリ直下に存在する
- キャラクターシートとスケール参照がsymlinkではなく通常ファイルとして同梱されている
- `script.md`が`../../02_CHARACTERS/`等の外部パスを参照していない
- 各Motion promptに`Required attached reference files:`があり、対応表の全`@ImageN = filename`がファイル名ごと再宣言されている
- 各クリップのFrame A、Frame B、Audioが存在する

検証失敗時は不足ファイルをコピーするかプロンプトを修正し、再実行する。**失敗したままユーザーへ完了報告してはいけない。**
