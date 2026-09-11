#@title 13. 性能・精度レポート（生成後に実行。GPU不要・何度でも再実行可）
#@markdown 各armのmp4を突き合わせて**速度と精度の比較表**を作り、`ab_report.md`・コンタクトシート・
#@markdown 横並び動画を出力する。**最後に出るMarkdownをそのままClaudeへ貼れば採用可否を相談できる。**
#@markdown
#@markdown 自動指標は**スクリーニング**。合否は「横並び動画＋コンタクトシート」の目視と、
#@markdown ローカルの`/image-validation`（Qwen3-VL）で確定させる — 特に**リップシンクは自動指標では判定しない**。
AB_BENCH_CELL_MARKER = True  # セル番号実行の対象から外す目印（消さない）

MAKE_SIDE_BY_SIDE = True   #@param {type:"boolean"}
SHEET_COLUMNS = 6          #@param {type:"integer"}

import csv, glob, json, math, os, re, shutil, subprocess
import numpy as np

AB_OUT = globals().get("AB_OUT") or "/content/outputs"   # セル11の定義を引き継ぐ
AB_META = f"{AB_OUT}/ab_arms.json"
FONT = next((f for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                         "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]
             if os.path.exists(f)), None)

if not os.path.exists(AB_META):
    _drv = (globals().get("OUT_DRIVE_DIR") or "") and os.path.join(OUT_DRIVE_DIR, "ab_arms.json")
    assert _drv and os.path.exists(_drv), (
        f"{AB_META} が無い — 先にセル12を実行する（別セッションの結果を見るなら OUT_DRIVE_DIR を設定してセル1を実行）")
    os.makedirs(AB_OUT, exist_ok=True)
    shutil.copy(_drv, AB_META)
ARMS = json.load(open(AB_META))
CHAPTER = next(iter(ARMS.values()))["chapter"]
MODE = next(iter(ARMS.values()))["mode"]
BUNDLE = globals().get("BUNDLE") or next(iter(glob.glob("/content/bundle/*")), "")


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def num(v, d=1):
    """表に載せる数値を丸める（ffmpegは小数6桁で返すので読みにくい）。"infなら「一致」。"""
    try:
        return "一致" if str(v) == "inf" else f"{float(v):.{d}f}"
    except (TypeError, ValueError):
        return str(v)


def find_mp4(arm):
    for p in (f"{AB_OUT}/{CHAPTER}__{arm}.mp4",
              os.path.join(globals().get("OUT_DRIVE_DIR") or "/nonexistent", f"{CHAPTER}__{arm}.mp4")):
        if os.path.exists(p):
            if not p.startswith(AB_OUT):
                shutil.copy(p, AB_OUT)      # 解析はローカルコピーで行う（Drive越しは遅い）
                p = f"{AB_OUT}/{os.path.basename(p)}"
            return p
    return None


def probe(path):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height,nb_frames,r_frame_rate,duration", "-of", "json", path])
    s = json.loads(r.stdout)["streams"][0]
    num, den = (s["r_frame_rate"].split("/") + ["1"])[:2]
    fps = float(num) / float(den or 1)
    n = int(s.get("nb_frames") or 0)
    if n <= 0:      # コンテナによっては nb_frames を持たない（尺×fpsで代用する）
        n = int(float(s.get("duration") or 0) * fps)
    return dict(w=int(s["width"]), h=int(s["height"]), n=n, fps=fps)


def vquality(a, b, size):
    """b を a（基準）と比べる。解像度が違っても比較できるよう b を a のサイズへ合わせる
    （psnr/ssimフィルタは同サイズ必須で、違うと黙って「-」になってしまうため）。"""
    def run(f):
        w, h = size
        r = sh(["ffmpeg", "-hide_banner", "-i", a, "-i", b, "-lavfi",
                f"[1:v]scale={w}:{h}:flags=bicubic[b];[0:v][b]{f}", "-f", "null", "-"])
        return r.stderr

    out = {}
    m = re.search(r"average:([\d.]+|inf).*?min:([\d.]+|inf)", run("psnr"))
    out["psnr_avg"], out["psnr_min"] = (m.group(1), m.group(2)) if m else ("-", "-")
    if out["psnr_avg"] == "-":
        print(f"⚠ PSNRを取れなかった: {os.path.basename(b)}", flush=True)
    m = re.search(r"All:([\d.]+)", run("ssim"))
    out["ssim"] = m.group(1) if m else "-"
    return out


def audio(path, sr=16000):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr),
                        "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.float32), sr


def envelope(x, sr, hop=320):
    n = len(x) // hop * hop
    if n == 0:
        return np.zeros(0)
    e = np.sqrt((x[:n].reshape(-1, hop).astype(np.float64) ** 2).mean(axis=1))
    return e


def best_corr(ref, sig):
    """refをsigの中で最も一致する位置に合わせたときの相関とオフセット（ホップ数）。"""
    if len(ref) < 4 or len(sig) < len(ref):
        return float("nan"), 0
    r = ref - ref.mean()
    rn = np.linalg.norm(r)
    if rn == 0:
        return float("nan"), 0
    best, off = -2.0, 0
    for s in range(0, len(sig) - len(ref) + 1):
        w = sig[s:s + len(ref)]
        w = w - w.mean()
        wn = np.linalg.norm(w)
        if wn == 0:
            continue
        c = float(np.dot(r, w) / (rn * wn))
        if c > best:
            best, off = c, s
    return best, off


def motion(path, w=96, h=54):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={w}:{h},format=gray",
                        "-f", "rawvideo", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, dtype=np.uint8)
    n = len(a) // (w * h)
    if n < 2:
        return np.zeros(0)
    a = a[:n * w * h].reshape(n, h * w).astype(np.float32)
    return np.abs(np.diff(a, axis=0)).mean(axis=1)


def input_files(cls_pat, key_pat):
    """このチャプターのworkflow原本から入力ファイル名を取り出す（順序＝<Picture N>/<Audio N>の順）。"""
    for cand in (f"{BUNDLE}/{CHAPTER}_workflow.orig.json", f"{BUNDLE}/{CHAPTER}_workflow.json"):
        if os.path.exists(cand):
            g = json.load(open(cand))
            break
    else:
        return []
    hits = []
    for k in sorted(g, key=lambda x: int(x) if x.isdigit() else 0):
        node = g[k]
        if re.fullmatch(cls_pat, node.get("class_type", "")):
            for ik, iv in node["inputs"].items():
                if re.search(key_pat, ik) and isinstance(iv, str):
                    hits.append(iv)
    return hits


# === 1. 性能（セル12の実測 + bench_log.csv の s/it） ==========================
STEP_SEC = {}
for csvp in (f"{AB_OUT}/bench_log.csv",
             os.path.join(globals().get("OUT_DRIVE_DIR") or "/nonexistent", "bench_log.csv")):
    if os.path.exists(csvp):
        for row in csv.DictReader(open(csvp)):
            if row["chapter"] == CHAPTER:
                STEP_SEC[row["label"]] = row["sampling_s_per_step"]

CU = {"A100": (8.0, 12.0)}.get("A100" if "A100" in next(iter(ARMS.values()))["gpu"] else "L4", (2.0, 3.0))
YEN_PER_CU = 1179 / 100

# === 2. 精度 ================================================================
BASE = ARMS.get("base") or next(iter(ARMS.values()))
base_mp4 = find_mp4(BASE["arm"])
REF_AUDIO = [f for f in input_files(r"LoadAudio", r"audio")]
REF_IMAGE = [f for f in input_files(r"LoadImage", r"image")]
rows = {}
for arm, meta in ARMS.items():
    mp4 = find_mp4(arm)
    row = dict(meta)
    row["mp4"] = mp4
    if not mp4:
        row["note"] = "mp4が見つからない（生成失敗 or 未実行）"
        rows[arm] = row
        continue
    info = probe(mp4)
    row.update(info)
    # 2-1. 基準（base）との映像差
    if base_mp4 and mp4 != base_mp4:
        row.update(vquality(base_mp4, mp4, (probe(base_mp4)["w"], probe(base_mp4)["h"])))
    # 2-2. 音声: クリップと、添付wavが素材として使われているか（包絡の一致）
    x, sr = audio(mp4)
    if len(x):
        peak = float(np.abs(x).max())
        row["peak_dbfs"] = 20 * math.log10(peak) if peak > 0 else -99.0
        row["clipped"] = int((np.abs(x) >= 0.999).sum())
        env = envelope(x, sr)
        row["wav_match"] = []
        for w in REF_AUDIO:
            wp = os.path.join(BUNDLE, w)
            if not os.path.exists(wp):
                continue
            y, _ = audio(wp, sr)
            c, off = best_corr(envelope(y, sr), env)
            row["wav_match"].append((w, c, off * 320 / sr))
        # 2-3. 口の動きと音声の同期（参考値・顔検出なしの全画面プロキシ）
        mo = motion(mp4)
        if len(mo) > 4 and len(env) > 4:
            e = np.interp(np.linspace(0, len(env) - 1, len(mo)), np.arange(len(env)), env)
            if e.std() > 0 and mo.std() > 0:
                row["motion_audio_r"] = float(np.corrcoef(mo, e)[0, 1])
    # 2-4. キーフレーム追従（start/endのPNGが在るチャプターのみ）
    kf = {}
    for label, idx, pat in (("start", 0, r"_start\.png$"), ("end", info["n"] - 1, r"_end\.png$")):
        ref = next((os.path.join(BUNDLE, f) for f in REF_IMAGE if re.search(pat, f)), None)
        if not ref or not os.path.exists(ref) or idx < 0:
            continue
        png = f"{AB_OUT}/_kf_{arm}_{label}.png"
        sh(["ffmpeg", "-y", "-v", "error", "-i", mp4, "-vf", f"select=eq(n\\,{idx})",
            "-frames:v", "1", "-update", "1", png])
        if not os.path.exists(png):
            continue
        r = sh(["ffmpeg", "-hide_banner", "-i", png, "-i", ref, "-lavfi",
                f"[1:v]scale={info['w']}:{info['h']}[r];[0:v][r]psnr", "-f", "null", "-"])
        m = re.search(r"average:([\d.]+|inf)", r.stderr)
        if m:
            kf[label] = m.group(1)
    row["keyframe_psnr"] = kf
    rows[arm] = row

# === 3. 目で見る材料（コンタクトシート・横並び動画） =========================
ok_arms = [a for a in ARMS if rows.get(a, {}).get("mp4")]
sheets = []
for arm in ok_arms:
    mp4, n = rows[arm]["mp4"], max(rows[arm].get("n") or 0, 1)
    k = max(1, n // max(1, SHEET_COLUMNS))
    png = f"{AB_OUT}/_sheet_{arm}.png"
    vf = (f"select='not(mod(n\\,{k}))',scale=320:-2,tile={SHEET_COLUMNS}x1")
    if FONT:
        vf += (f",drawtext=fontfile={FONT}:text='{arm}':x=8:y=8:fontsize=22:"
               "fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=6")
    r = sh(["ffmpeg", "-y", "-v", "error", "-i", mp4, "-vf", vf, "-frames:v", "1", png])
    if os.path.exists(png):
        sheets.append(png)
SHEET = f"{AB_OUT}/{CHAPTER}_ab_contact_sheet.png"
if len(sheets) >= 2:
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for s in sheets:
        cmd += ["-i", s]
    cmd += ["-filter_complex", f"vstack=inputs={len(sheets)}", SHEET]
    sh(cmd)
elif sheets:
    shutil.copy(sheets[0], SHEET)

SBS = f"{AB_OUT}/{CHAPTER}_ab_side_by_side.mp4"
if MAKE_SIDE_BY_SIDE and len(ok_arms) >= 2:
    cmd, parts = ["ffmpeg", "-y", "-v", "error"], []
    for i, arm in enumerate(ok_arms):
        cmd += ["-i", rows[arm]["mp4"]]
        f = f"[{i}:v]scale=384:-2"
        if FONT:
            f += (f",drawtext=fontfile={FONT}:text='{arm}':x=6:y=6:fontsize=18:"
                  "fontcolor=white:box=1:boxcolor=black@0.6:boxborderw=5")
        parts.append(f + f"[v{i}]")
    fc = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(len(ok_arms))) + \
         f"hstack=inputs={len(ok_arms)}[v]"
    r = sh(cmd + ["-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264",
                  "-crf", "20", "-pix_fmt", "yuv420p", SBS])
    if r.returncode != 0:
        print("⚠ 横並び動画の作成に失敗（個別mp4で比較する）:", r.stderr[-400:])

# === 4. レポート ============================================================
L = []
A = L.append
A(f"# H3 A/Bベンチ結果 — {CHAPTER}（{MODE.upper()}）")
A("")
A(f"- GPU: {BASE['gpu']} / フレーム数: {BASE['frames']}（{BASE['frames'] / 24:.1f}秒）")
A(f"- 基準arm: `{BASE['arm']}`（{BASE['desc']}）")
A("")
A("## 性能")
A("")
A("| arm | 条件 | steps | sampler | 分 | s/step | vs base | VRAMピーク | 円/本(目安) |")
A("|---|---|---:|---|---:|---:|---:|---:|---:|")
for arm in ARMS:
    r = rows[arm]
    w = r.get("wall_sec") or 0
    ratio = f"x{(BASE['wall_sec'] / w):.2f}" if w and BASE.get("wall_sec") else "-"
    yen = f"¥{w / 3600 * CU[0] * YEN_PER_CU:.0f}〜{w / 3600 * CU[1] * YEN_PER_CU:.0f}" if w else "-"
    A(f"| `{arm}` | {r['desc']} | {r.get('steps', '-')} | {r.get('sampler', '-')} | "
      f"{w / 60:.1f} | {STEP_SEC.get(arm, '-')} | {ratio} | {r.get('vram_peak_mb', '-')}MB | {yen} |")
A("")
A("## 精度（自動指標）")
A("")
A("| arm | baseとの映像差 PSNR平均/最小 | SSIM | 音声ピーク | クリップ数 | 添付wavとの包絡一致 | キーフレーム追従 PSNR |")
A("|---|---|---|---:|---:|---|---|")
for arm in ARMS:
    r = rows[arm]
    if not r.get("mp4"):
        A(f"| `{arm}` | — | — | — | — | — | {r.get('note', '生成なし')} |")
        continue
    psnr = "（基準）" if arm == BASE["arm"] else f"{num(r.get('psnr_avg', '-'))} / {num(r.get('psnr_min', '-'))}"
    wm = " ".join(f"{os.path.basename(w)}={c:.2f}@{o:.2f}s" for w, c, o in r.get("wav_match", [])) or "—"
    kf = " ".join(f"{k}={num(v)}" for k, v in (r.get("keyframe_psnr") or {}).items()) or "—"
    A(f"| `{arm}` | {psnr} | {'（基準）' if arm == BASE['arm'] else num(r.get('ssim', '-'), 3)} | "
      f"{r.get('peak_dbfs', float('nan')):.1f}dBFS | {r.get('clipped', '-')} | {wm} | {kf} |")
A("")
A("**読み方**")
A("")
A("- **baseとの映像差**: 蒸留armは絵が変わるのが当然なので、これは「劣化」ではなく**変化の大きさ**。"
  "PSNR 30dB超なら概ね同じ絵、20dB台なら見て分かる差。**最小PSNRが極端に低いフレーム**がある場合は"
  "その瞬間だけ破綻している可能性があるので必ず目視する")
A("- **クリップ数 / 音声ピーク**: 0dBFS以上（＝フルスケール超過）とクリップ数の増加は音が割れている印。"
  "低step蒸留で実際に報告のある劣化（6stepで−0.0dBまでクリップした実測例）。**base比で悪化したら不採用**")
A("- **添付wavとの包絡一致**: 入力wavの音量エンベロープが出力音声のどこにどれだけ一致するか（1.0が完全一致）。"
  "**このパイプラインの肝はwavをAS-ISで使わせること**なので、baseで高い値がarmで大きく落ちたら"
  "「別の声を生成し始めた」疑い。値そのものより**base比**を見る")
A("- **キーフレーム追従**: 出力の先頭/末尾フレームと`ch*_start.png`/`ch*_end.png`のPSNR。"
  "I2V（FL2VA）は厳密アンカーなので高いはず。R2Vは元々ゆるいので低くても異常ではない")
if any("motion_audio_r" in r for r in rows.values()):
    A("- **動き↔音声の相関**（参考値）: " + ", ".join(
        f"`{a}`={rows[a]['motion_audio_r']:.2f}" for a in ARMS if "motion_audio_r" in rows.get(a, {})) +
      " — 顔検出をしない全画面プロキシなので**リップシンクの判定には使えない**。目視/VLMで確定させる")
A("")
A("## 目視チェック（自動指標では判定できない — armごとに埋める）")
A("")
for arm in ok_arms:
    A(f"### `{arm}`")
    A("")
    A("- [ ] セリフが添付wavの声で鳴っている（合成音・二重音声になっていない）")
    A("- [ ] 話しているキャラが正しく、その口だけが音の鳴っている間だけ動く")
    A("- [ ] 非話者の口が閉じたまま")
    A("- [ ] キャラクターの同一性（仮面・触手・ウクレレ等のNG変更要素）が崩れていない")
    A("- [ ] 小道具の状態・時間帯・天気が台本どおり")
    A("- [ ] 手・髪・激しい動きの破綻が base と同等以下")
    A("")
A("## 成果物")
A("")
A(f"- 横並び動画（無音・目視用）: `{os.path.basename(SBS)}`" if os.path.exists(SBS) else "- 横並び動画: 未作成")
A(f"- コンタクトシート: `{os.path.basename(SHEET)}`（行は上から {' / '.join(ok_arms)}"
  + ("）" if FONT else "。フォントが無くラベルを焼けなかったので行順で読む）")
  if os.path.exists(SHEET) else "- コンタクトシート: 未作成")
A(f"- 各armのmp4（音声はこちらで確認）: " + ", ".join(f"`{CHAPTER}__{a}.mp4`" for a in ok_arms))

REPORT = "\n".join(L)
open(f"{AB_OUT}/{CHAPTER}_ab_report.md", "w").write(REPORT)
if globals().get("OUT_DRIVE_DIR"):
    os.makedirs(OUT_DRIVE_DIR, exist_ok=True)
    for p in [f"{AB_OUT}/{CHAPTER}_ab_report.md", SHEET, SBS]:
        if os.path.exists(p):
            shutil.copy(p, OUT_DRIVE_DIR)
print(REPORT)
print(f"\n{'=' * 78}\n★ 上のMarkdownをそのままClaudeへ貼れば採用可否を相談できる"
      f"（{AB_OUT}/{CHAPTER}_ab_report.md にも保存済み"
      + (f"・Driveへも退避済み: {OUT_DRIVE_DIR}" if globals().get("OUT_DRIVE_DIR") else "") + "）")
print("★ 目視は横並び動画とコンタクトシートで行う。音声は各armのmp4を個別に聞く", flush=True)
try:
    from IPython.display import Image, display
    if os.path.exists(SHEET):
        display(Image(filename=SHEET))
except Exception:
    pass
