#@title 12. A/Bベンチ実行（セットアップ→armごとに同一シードで生成。DRY RUN時は配線検証と見積りだけ）
#@markdown セル11の設定で全armを順に回す。セットアップ（セル1→4→3→2→5→6）はこのセルが内部で実行するので、
#@markdown **事前に必要なのはセル1のDriveパスだけ**。生成済みarmはスキップするので、切断されても再実行で続きから。
AB_BENCH_CELL_MARKER = True  # セル番号実行の対象から外す目印（消さない）

import glob, json, os, re, shutil, subprocess, threading, time

G = globals()
AB_T0 = time.time()


def ab_load_steps():
    """ノートブック自身のセルソースを「#@title <1桁数字>.」で拾う（★一括実行セルと同じ方法）。"""
    from google.colab import _message
    res = _message.blocking_request("get_ipynb", timeout_sec=120)
    nb = res["ipynb"] if isinstance(res, dict) and "ipynb" in res else res
    steps = {}
    for c in nb["cells"]:
        if c.get("cell_type") != "code":
            continue
        src = c["source"] if isinstance(c["source"], str) else "".join(c["source"])
        if "BENCH_CELL_MARKER" in src:      # 計測セル（本セル・セル10・セル13）は対象外
            continue
        for line in src.split("\n")[:3]:
            m = re.match(r"\s*(?:#@title|#)\s*(\d)[.．]", line)
            if m:
                steps.setdefault(int(m.group(1)), src)
                break
    return steps


try:
    AB_STEPS = ab_load_steps()
except Exception as _e:
    raise SystemExit(f"この環境ではノートブックのセルを取り出せない（{type(_e).__name__}: {_e}）"
                     " — セル1〜6を手で実行してから、このセルを再実行する")

_ip = get_ipython()


def ab_run(n):
    res = _ip.run_cell(AB_STEPS[n])
    if not res.success:
        err = getattr(res, "error_in_exec", None) or getattr(res, "error_before_exec", None)
        raise RuntimeError(f"セル{n} で失敗: {err!r}" if err is not None else f"セル{n} で失敗（直前のトレースバック参照）")


def ab_premount():
    if not any(G.get(k) for k in ("WEIGHTS_DRIVE_DIR", "BUNDLE_ZIP_FROM_DRIVE", "OUT_DRIVE_DIR")):
        return
    if os.path.isdir("/content/drive/MyDrive"):
        return
    from google.colab import drive as _gd
    print("★ 先にGoogle Driveをマウントする（初回は承認ダイアログ）", flush=True)
    _gd.mount("/content/drive")


def ab_preupload():
    if G.get("BUNDLE_ZIP_FROM_DRIVE"):
        return
    cur = G.get("BUNDLE_ZIP_LOCAL") or ""
    if cur and os.path.exists(cur):
        return
    from google.colab import files
    print("★ 先にバンドルzipをアップロードする — 操作が必要なのはここだけ", flush=True)
    up = files.upload()
    zips = [n for n in up if n.lower().endswith(".zip")]
    assert zips, "zipが選ばれていない — セル1で BUNDLE_ZIP_FROM_DRIVE を設定してもよい"
    G["BUNDLE_ZIP_LOCAL"] = os.path.join(os.getcwd(), zips[0])


class AbVram:
    """生成中のVRAM使用量のピークを nvidia-smi のポーリングで拾う（ComfyUIは別プロセスなので
    torch.cuda.max_memory_allocated では見えない）。"""

    def __init__(self, interval=5.0):
        self.interval, self.peak, self._stop = interval, 0, threading.Event()

    def _loop(self):
        while not self._stop.wait(self.interval):
            try:
                out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used",
                                      "--format=csv,noheader,nounits"],
                                     capture_output=True, text=True, timeout=10).stdout
                self.peak = max(self.peak, max(int(v) for v in out.split() if v.isdigit()))
            except Exception:
                pass

    def __enter__(self):
        self._t = threading.Thread(target=self._loop, daemon=True)
        self._t.start()
        return self

    def __exit__(self, *a):
        self._stop.set()
        self._t.join(timeout=self.interval + 2)
        return False


# === セットアップ ==========================================================
print("★ A/Bベンチ: セットアップ（セル1→4→3→2→5→6）から始める", flush=True)
ab_run(1)
assert G.get("VRAM", 0) > 0, "GPUランタイムでない（ランタイム → ランタイムのタイプを変更 → L4/A100）"
G["AUTO_SHUTDOWN"] = False          # armごとに切断されないよう固定（切断は最後に BENCH_SHUTDOWN で）
# 正典セル7の自動蒸留は必ず切る。ベンチはarmごとに自分でworkflowを組むので、
# ここが有効だと base arm にまで蒸留が乗って比較が成立しなくなる。
G["TURBO_8STEP"] = False
AB_BASE_ENCODER, AB_BASE_I2V, AB_BASE_R2V = G["ENCODER"], G["UNET_I2V"], G["UNET_R2V"]
ab_premount()
ab_preupload()
for _n in (4, 3, 2, 5):             # 4→3 の順（セル3のモード自動判定がバンドルを読む）
    ab_run(_n)

# 対象チャプターを決めて、素のworkflowを退避（armごとにここから作り直す）
BUNDLE = G["BUNDLE"]
if not BENCH_CHAPTER:
    _wfs = sorted(glob.glob(f"{BUNDLE}/ch*_workflow.json"),
                  key=lambda p: int(re.sub(r"\D", "", os.path.basename(p)) or 0))
    assert _wfs, f"{BUNDLE} に ch*_workflow.json が無い — バンドルを確認"
    BENCH_CHAPTER = os.path.basename(_wfs[0])[: -len("_workflow.json")]
AB_WF = f"{BUNDLE}/{BENCH_CHAPTER}_workflow.json"
AB_WF_ORIG = f"{BUNDLE}/{BENCH_CHAPTER}_workflow.orig.json"
assert os.path.exists(AB_WF), f"{AB_WF} が無い"
if not os.path.exists(AB_WF_ORIG):
    shutil.copy(AB_WF, AB_WF_ORIG)
_g0 = json.load(open(AB_WF_ORIG))
AB_MODE = "r2v" if any(v.get("class_type") == "MiniMaxH3ReferenceToVideo" for v in _g0.values()) else "i2v"
AB_CTX = {"modes": [AB_MODE], "turbo_lora": {}}
print(f"★ 対象チャプター: {BENCH_CHAPTER}（{AB_MODE.upper()}）  workflowの原本 → "
      f"{os.path.basename(AB_WF_ORIG)}", flush=True)

AB_PLAN = ["base"] + [a for a in BENCH_ARMS if a != "base"]

# armが要る重み・カスタムノードを先にまとめて用意（COMBOの選択肢に出させるため生成前に置く）
print(f"\n★ 追加素材の用意（arm: {AB_PLAN}）", flush=True)
_restart = False
for _a in AB_PLAN:
    _restart |= bool(ab_prepare(AB_ARMS[_a], AB_CTX))
ab_run(6)                            # ComfyUI起動（カスタムノード導入後なのでここで反映される）
AB_INFO = ab_object_info(G["SERVERS"][0])
print(f"★ ComfyUIのノード定義を取得: {len(AB_INFO)}クラス", flush=True)

# === 全armのworkflowを組んで検証（DRY RUNはここまで） ======================
AB_WFS, AB_APPLIED, AB_SKIP = {}, {}, {}
for _a in AB_PLAN:
    g = json.load(open(AB_WF_ORIG))
    # 重み名はarmの指定（無ければセル1の既定）に合わせる
    spec = AB_ARMS[_a]
    enc = spec.get("encoder") or AB_BASE_ENCODER
    if spec.get("unet_quant"):
        i2v = re.sub(r"pruned_\w+\.safetensors$", f"pruned_{spec['unet_quant']}.safetensors", AB_BASE_I2V)
        r2v = re.sub(r"pruned_\w+\.safetensors$", f"pruned_{spec['unet_quant']}.safetensors", AB_BASE_R2V)
    else:
        i2v, r2v = AB_BASE_I2V, AB_BASE_R2V
    for node in g.values():
        for k, v in node.get("inputs", {}).items():
            if not isinstance(v, str):
                continue
            if v.startswith("minimax_h3_fl2va"):
                node["inputs"][k] = i2v
            elif v.startswith("minimax_h3_ref2va"):
                node["inputs"][k] = r2v
            elif v.startswith("qwen3vl_32b"):
                node["inputs"][k] = enc
        if node.get("class_type") == "SaveVideo":
            node["inputs"].setdefault("codec", "auto")
            node["inputs"].setdefault("format", "auto")
    try:
        AB_APPLIED[_a] = ab_patch_workflow(g, AB_INFO, spec, AB_CTX)
        AB_WFS[_a] = (g, enc, i2v if AB_MODE == "i2v" else r2v)
    except Exception as e:
        AB_SKIP[_a] = f"{type(e).__name__}: {e}"

print(f"\n{'=' * 78}\n★ 各armのworkflow検証結果\n{'=' * 78}", flush=True)
for _a in AB_PLAN:
    if _a in AB_SKIP:
        print(f"\n✗ {_a}: 組めない — このarmはスキップする\n   {AB_SKIP[_a]}", flush=True)
        continue
    g, enc, unet = AB_WFS[_a]
    steps = g[ab_one(g, "BasicScheduler")]["inputs"]["steps"]
    nfe = AB_ARMS[_a].get("pdd")
    print(f"\n✓ {_a}: {AB_ARMS[_a]['desc']}", flush=True)
    print(f"   weights: {unet} / {enc}", flush=True)
    print(f"   sampler={g[ab_one(g, 'KSamplerSelect')]['inputs']['sampler_name']}  "
          f"steps={nfe if nfe else steps}{'（PDDのnfe）' if nfe else ''}", flush=True)
    for line in AB_APPLIED[_a] or ["（素のまま＝基準）"]:
        print(f"   + {line}", flush=True)

# 所要時間・費用の見積り（L4+sage実測の線形則: 0.645秒/フレーム/step・2026-09 ch3 158f）
_h3 = [v for v in _g0.values() if str(v.get("class_type", "")).startswith("MiniMaxH3")][0]
AB_FRAMES = int(BENCH_FRAMES) if BENCH_FRAMES else int(_h3["inputs"]["length"])
_lo, _hi = AB_CU_PER_HOUR.get("A100" if "A100" in G["NAME"] else "L4", (2.0, 3.0))
_total_min = 0.0
print(f"\n{'arm':<12}{'steps':>7}{'見積り分':>10}", flush=True)
for _a in AB_PLAN:
    if _a in AB_SKIP:
        continue
    g, _e, _u = AB_WFS[_a]
    st = AB_ARMS[_a].get("pdd") or g[ab_one(g, "BasicScheduler")]["inputs"]["steps"]
    est = AB_FRAMES * 0.645 * st / 60 + 3
    _total_min += est
    print(f"{_a:<12}{st:>7}{est:>10.0f}", flush=True)
print(f"\n合計の目安: 約{_total_min:.0f}分（{AB_FRAMES}フレーム＝{AB_FRAMES / 24:.1f}秒のチャプター×"
      f"{len([a for a in AB_PLAN if a not in AB_SKIP])}arm）"
      f" ≒ {_total_min / 60 * _lo:.0f}〜{_total_min / 60 * _hi:.0f} CU"
      f" ≒ ¥{_total_min / 60 * _lo * AB_YEN_PER_CU:.0f}〜{_total_min / 60 * _hi * AB_YEN_PER_CU:.0f}", flush=True)
print("※ 見積りはL4+sage実測（0.645秒/フレーム/step）からの線形外挿", flush=True)

if BENCH_DRY_RUN:
    print(f"\n★ DRY RUN — ここで停止する。配線と見積りに問題が無ければ "
          f"セル11の BENCH_DRY_RUN を False にしてこのセルを再実行する", flush=True)
    if AB_SKIP:
        print("  ⚠ 組めなかったarmがある。上のエラーとノード定義をClaudeへ貼れば配線を直せる", flush=True)
else:
    # === 本番: armごとに生成 ================================================
    assert AB_WFS, "実行できるarmが1つも無い"
    ab_run(3)                 # armが重みを差し替えている場合に備えて配置を流し直す（配置済みはskip）
    G["wait_weights"]()
    os.makedirs(AB_OUT, exist_ok=True)
    AB_RESULT = json.load(open(AB_META)) if os.path.exists(AB_META) else {}
    _prev_weights = None
    for _a in AB_PLAN:
        if _a in AB_SKIP:
            continue
        g, enc, unet = AB_WFS[_a]
        print(f"\n{'=' * 78}\n▶ arm {_a}（経過 {(time.time() - AB_T0) / 60:.1f}分）"
              f"\n{'=' * 78}", flush=True)
        # 重みが前のarmと違うならグローバルを差し替えてセル3で配置し直す
        cur = (enc, unet)
        if cur != _prev_weights:
            G["ENCODER"] = enc
            if AB_MODE == "i2v":
                G["UNET_I2V"] = unet
            else:
                G["UNET_R2V"] = unet
            if _prev_weights is not None:
                ab_run(3)
                G["wait_weights"]()
            _prev_weights = cur
        json.dump(g, open(AB_WF, "w"), ensure_ascii=False, indent=1)
        G["CHAPTERS"], G["AB_LABEL"], G["AUTO_SHUTDOWN"] = [BENCH_CHAPTER], _a, False
        _rec = dict(arm=_a, desc=AB_ARMS[_a]["desc"], chapter=BENCH_CHAPTER, mode=AB_MODE,
                    frames=AB_FRAMES, gpu=G["NAME"], encoder=enc, unet=unet,
                    steps=AB_ARMS[_a].get("pdd") or g[ab_one(g, "BasicScheduler")]["inputs"]["steps"],
                    sampler=g[ab_one(g, "KSamplerSelect")]["inputs"]["sampler_name"],
                    applied=AB_APPLIED[_a], out=f"{AB_OUT}/{BENCH_CHAPTER}__{_a}.mp4")
        # このarmが既に生成済みならセル7はスキップする＝所要時間を測れない。
        # **前回の実測を0で上書きしない**（中断・再開で回すのが前提なので、
        # 再実行のたびに基準armの計測値が消えると比較表が壊れる・2026-09実測）。
        _drv = os.path.join(G.get("OUT_DRIVE_DIR") or "/nonexistent", f"{BENCH_CHAPTER}__{_a}.mp4")
        if os.path.exists(_rec["out"]) or os.path.exists(_drv):
            _prev = AB_RESULT.get(_a) or {}
            _rec.update(ok=True, err="", skipped=True,
                        wall_sec=_prev.get("wall_sec") or 0,
                        vram_peak_mb=_prev.get("vram_peak_mb") or 0)
            print(f"skip（生成済み）— " + (f"前回の実測 {_rec['wall_sec'] / 60:.1f}分 を保持"
                                          if _rec["wall_sec"] else
                                          "このセッションでは測っていない（所要時間はbench_log.csvから読む）"),
                  flush=True)
            AB_RESULT[_a] = _rec
            json.dump(AB_RESULT, open(AB_META, "w"), ensure_ascii=False, indent=1)
            if G.get("OUT_DRIVE_DIR"):
                shutil.copy(AB_META, G["OUT_DRIVE_DIR"])
            continue
        t0, vm_peak = time.time(), 0
        try:
            with AbVram() as vm:
                ab_run(7)
            vm_peak = vm.peak
            ok, err = True, ""
        except KeyboardInterrupt:
            raise
        except BaseException as e:
            vm_peak = getattr(locals().get("vm"), "peak", 0)
            ok, err = False, f"{type(e).__name__}: {e}"
            for lg in sorted(glob.glob("/content/comfyui_*.log")):
                with open(lg, errors="replace") as fo:
                    print(f"--- {lg}（末尾） ---\n{fo.read()[-2000:]}", flush=True)
            print(f"⚠ arm {_a} 失敗 — 残りのarmは続行する", flush=True)
        _rec.update(ok=ok, err=err, skipped=False,
                    wall_sec=round(time.time() - t0), vram_peak_mb=vm_peak)
        AB_RESULT[_a] = _rec
        json.dump(AB_RESULT, open(AB_META, "w"), ensure_ascii=False, indent=1)
        if G.get("OUT_DRIVE_DIR"):
            shutil.copy(AB_META, G["OUT_DRIVE_DIR"])
    shutil.copy(AB_WF_ORIG, AB_WF)     # バンドルのworkflowを素の状態へ戻す
    print(f"\n★ 全arm終了（合計 {(time.time() - AB_T0) / 60:.1f}分）→ **セル13** でレポートを出す", flush=True)
    for _a, r in AB_RESULT.items():
        print(f"  {_a:<12}{'OK' if r['ok'] else '失敗'}  {r['wall_sec'] / 60:.1f}分  "
              f"VRAMピーク {r['vram_peak_mb']}MB  {r['err']}", flush=True)
    if BENCH_SHUTDOWN:
        _unsaved = [os.path.basename(o) for o in sorted(glob.glob(f"{AB_OUT}/*.mp4"))
                    if not (G.get("OUT_DRIVE_DIR")
                            and os.path.exists(os.path.join(G["OUT_DRIVE_DIR"], os.path.basename(o))))]
        if _unsaved or not G.get("OUT_DRIVE_DIR"):
            print(f"⚠ 自動切断を中止: Drive未退避がある {_unsaved} — セル13/セル8で回収してから手動で削除する",
                  flush=True)
        else:
            print("★ 60秒後にランタイムを切断・削除する（■で取り消し）。"
                  "⚠ セル13のレポートは切断前に実行しておくこと", flush=True)
            time.sleep(60)
            from google.colab import drive as _gd, runtime
            try:
                _gd.flush_and_unmount()
            except Exception:
                pass
            runtime.unassign()
