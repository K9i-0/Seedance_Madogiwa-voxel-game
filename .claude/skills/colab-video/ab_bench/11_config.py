#@title 11. A/Bベンチ設定（ここだけ編集 — 既定は DRY RUN＝配線検証と見積りだけ）
#@markdown 同一チャプター・**同一シード**を複数の条件（arm）で生成し、**速度と精度の両方**を比較する。
#@markdown - **既定は `BENCH_DRY_RUN=True`** ＝ 生成せずに「各armのworkflowが実際のComfyUIで組めるか」を検証し、所要時間と費用の見積りを出す。**まずこのまま1回流して配線を確認する**（数分・GPU課金は立ち上げ分のみ）
#@markdown - 検証が通ったら `BENCH_DRY_RUN=False` にしてセル12を実行 → 全armを生成 → セル13でレポート
#@markdown - armは1本ずつ `ch*__<arm>.mp4` として保存され、生成済みはスキップ＝**中断・再開・セッション跨ぎに強い**
AB_BENCH_CELL_MARKER = True  # このセルを「#@title <番号>.」のセル番号実行の対象から外す目印（消さない）

BENCH_ARMS = ["base", "pdd8", "turbo8"]  #@param {type:"raw"}
BENCH_CHAPTER = ""            #@param {type:"string"}
BENCH_DRY_RUN = True          #@param {type:"boolean"}
BENCH_FRAMES = 0              #@param {type:"integer"}
BENCH_SHUTDOWN = False        #@param {type:"boolean"}
BENCH_SPARSE_TAU = 1.0        #@param {type:"number"}
BENCH_LORA_STRENGTH = 1.0     #@param {type:"number"}

#@markdown ---
#@markdown **`BENCH_ARMS` に指定できるarm**（`base`は比較の基準なので常に先頭へ自動で足される）
#@markdown
#@markdown | arm | 中身 | 追加DL |
#@markdown |---|---|---|
#@markdown | `base` | **現行の本番設定**（そのGPUの既定重み・`res_multistep`/`simple`・20step） | — |
#@markdown | `pdd8` | 公式PDD Acc **8step**（alibaba-pai・専用ノード・euler・訓練済みsigma・CFG1） | node + 1.4GB |
#@markdown | `pdd4` | 同上を **4step** で（公式が認めた範囲。品質の下限確認用） | 同上 |
#@markdown | `turbo8` | lightx2v Turbo **8step v1.0 768p** LoRA（素のLoRA・euler・shift 12/3） | 約1.4GB |
#@markdown | `sparse` | core **Block Sparse Attention**（20step据え置き・attentionだけ疎に） | — |
#@markdown | `enc_nvfp4` | テキストエンコーダを **nvfp4_awq**（14.6GB）に（既定32GBの置換） | 14.6GB |
#@markdown | `unet_int8` | UNETを **int8_convrot** に（L4の既定`fp8_scaled`との比較。A100は既定が同じなので無意味） | 21GB |
#@markdown | `best` | `pdd8` + `enc_nvfp4` + `sparse` の合成（採用候補の最終確認用） | 上記合計 |
#@markdown
#@markdown ⚠ ディスクは L4 実測65GB。`enc_nvfp4`/`unet_int8`/`best` を混ぜると重みの入れ替えが起きて
#@markdown 立ち上げが延びる（既存の`reclaim_disk`が自動で古い方を捨てる）。**まずは重みを変えない
#@markdown `base`/`pdd8`/`turbo8`/`sparse` だけで回すのが安い。**

import json, os, re, subprocess, sys, urllib.request

AB_OUT = "/content/outputs"
AB_META = f"{AB_OUT}/ab_arms.json"          # arm毎の条件と実測（セル13が読む）
AB_NVFP4 = "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors"
AB_PDD_NODE = "https://github.com/Jalen-Brunson/ComfyUI-MiniMax-H3-PDD-Acc"
AB_PDD_REPO = "aptech0081/MiniMax-H3-Acc-LoRAs-ComfyUI"   # ComfyUIキーに変換済みの再配布
AB_TURBO_REPO = "lightx2v/Minimax-h3-Turbo"
AB_CU_PER_HOUR = {"L4": (2.0, 3.0), "A100": (8.0, 12.0)}  # SKILL.md 0章の目安
AB_YEN_PER_CU = 1179 / 100                                 # 100CU ¥1,179

# --- arm定義 ----------------------------------------------------------------
# encoder/unet_quant: セル1の自動選択を上書きする（Noneならそのまま）
# lora: "turbo" = lightx2v Turbo LoRA を LoraLoaderModelOnly で適用
# pdd:  整数 = 公式PDD Acc（専用ノードでnfe段数を指定。sigmasもこのノードから取る）
# sparse: True = core Block Sparse Attention を model パッチとして挿す
# shift: (video, audio) = SigmaShiftノードがあれば挿入して固定する
AB_ARMS = {
    "base":      dict(desc="現行の本番設定（比較の基準）"),
    "pdd8":      dict(desc="公式PDD Acc 8step", pdd=8, sampler="euler", shift=(12.0, 3.0)),
    "pdd4":      dict(desc="公式PDD Acc 4step", pdd=4, sampler="euler", shift=(12.0, 3.0)),
    "turbo8":    dict(desc="lightx2v Turbo 8step v1.0", lora="turbo", steps=8,
                      sampler="euler", scheduler="beta", shift=(12.0, 3.0)),
    "sparse":    dict(desc="core Block Sparse Attention（20step据え置き）", sparse=True),
    "enc_nvfp4": dict(desc="エンコーダ nvfp4_awq", encoder=AB_NVFP4),
    "unet_int8": dict(desc="UNET int8_convrot", unet_quant="int8_convrot"),
    "best":      dict(desc="pdd8 + nvfp4 + sparse の合成", pdd=8, sampler="euler",
                      shift=(12.0, 3.0), encoder=AB_NVFP4, sparse=True),
}

# --- ComfyUIのノード定義（/object_info）を正として組み立てる ------------------
# ノードのクラス名・入力名はComfyUIの更新で変わりうるので、**推測で書かず実機の定義から引く**。
# 見つからない・埋められない場合は、実際の定義を出力してそのarmだけスキップする（他は流す）。

AB_SCALAR_TYPES = {"INT", "FLOAT", "STRING", "BOOLEAN"}


class Pick:
    """COMBO入力（選択肢がリストで返る入力）から正規表現で値を選ぶ指定。"""
    def __init__(self, *patterns, prefer_last=True):
        self.patterns, self.prefer_last = patterns, prefer_last

    def resolve(self, options):
        hits = [o for o in options
                if all(re.search(p, str(o), re.I) for p in self.patterns)]
        if not hits:
            return None
        return sorted(hits)[-1] if self.prefer_last else sorted(hits)[0]


def ab_object_info(server):
    with urllib.request.urlopen(f"http://{server}/object_info", timeout=60) as r:
        return json.load(r)


def ab_find_class(info, *patterns):
    """クラス名の正規表現（前のものほど優先）で1つ選ぶ。戻り値 (クラス名 or None, 候補一覧)。"""
    for pat in patterns:
        hits = sorted(k for k in info if re.search(pat, k))
        if hits:
            return hits[0], hits
    return None, []


def ab_schema(info, cls):
    spec = info[cls].get("input", {})
    req = dict(spec.get("required") or {})
    opt = dict(spec.get("optional") or {})
    return req, opt


def ab_output_index(info, cls, want):
    """出力名（"SIGMAS"等）が何番目かを返す。無ければNone。"""
    for i, name in enumerate(info[cls].get("output_name") or info[cls].get("output") or []):
        if str(name).upper() == want.upper():
            return i
    return None


def ab_build_inputs(info, cls, values, links=None, must=()):
    """values={入力名の正規表現: 値 or Pick} から、そのノードの実際の入力dictを組む。

    must に挙げた正規表現は「実機に対応する入力が必ず在る」ことを要求する（無ければ例外）。
    ノードの入力名が改版で変わったのに、既定値のまま黙って走ってしまうのを防ぐためのガード。
    必須入力が埋まらない場合も、実機のスキーマを添えて例外にする。
    """
    req, opt = ab_schema(info, cls)
    allspec = {**req, **opt}
    out = dict(links or {})
    hit_pats = set()
    for pat, val in (values or {}).items():
        names = [n for n in allspec if n not in out
                 and (re.fullmatch(pat, n, re.I) or re.search(pat, n, re.I))]
        if not names:
            continue
        hit_pats.add(pat)
        name = sorted(names, key=len)[0]
        spec = allspec[name]
        options = spec[0] if isinstance(spec, (list, tuple)) and isinstance(spec[0], list) else None
        if isinstance(val, Pick):
            assert options is not None, f"{cls}.{name} はCOMBOではないので Pick を解決できない（定義: {spec}）"
            got = val.resolve(options)
            assert got is not None, (
                f"{cls}.{name}: {val.patterns} に一致する選択肢が無い。実機の選択肢: {options}")
            out[name] = got
        elif options is not None:
            # COMBOなら選択肢の側の型に合わせる（nfe=8 が "8" で定義されている等）
            got = next((o for o in options if str(o) == str(val)), None)
            assert got is not None, f"{cls}.{name}: {val!r} は選択肢に無い。実機の選択肢: {options}"
            out[name] = got
        else:
            out[name] = val
    unmatched = [p for p in must if p not in hit_pats]
    assert not unmatched, (f"{cls}: 期待した入力 {unmatched} がこのノードに無い（名前が変わった可能性）\n"
                           f"  実機の入力: {sorted(allspec)}")
    # **必須入力は既定値があっても省略できない。** ノード定義の既定値を埋めるのはフロントエンドで、
    # API形式のprompt（このworkflow JSON）では埋まらず `required_input_missing` で弾かれる
    # （2026-09実測: MiniMaxH3PDDAccApply の on_off_grid を省いて拒否された）。ここで実体化する。
    missing = []
    for name, spec in req.items():
        if name in out:
            continue
        if not isinstance(spec, (list, tuple)) or not spec:
            missing.append((name, spec, "定義を解釈できない"))
            continue
        typ = spec[0]
        opts = spec[1] if len(spec) > 1 and isinstance(spec[1], dict) else {}
        if isinstance(typ, list):                       # COMBO
            val = opts.get("default", typ[0] if typ else None)
            if val is None:
                missing.append((name, spec, "選択肢が空"))
            else:
                out[name] = val
        elif isinstance(typ, str) and typ in AB_SCALAR_TYPES:
            if "default" in opts:
                out[name] = opts["default"]
            else:
                missing.append((name, spec, "既定値が無いので値を決められない"))
        elif isinstance(typ, str) and typ.isupper():    # MODEL/SIGMAS等＝リンクで渡す型
            missing.append((name, spec, "リンクが必要だが繋いでいない"))
        else:
            missing.append((name, spec, "未知の型"))
    assert not missing, (f"{cls}: 必須入力を埋められない {missing}\n"
                         f"  実機の定義: required={req} optional={opt}")
    return out


# --- workflow(JSON API形式)へのパッチ ---------------------------------------

def ab_ids(g, cls):
    return [k for k, v in g.items() if v.get("class_type") == cls]


def ab_one(g, cls):
    ids = ab_ids(g, cls)
    assert len(ids) == 1, f"{cls} のノードが {len(ids)} 個ある（1個を期待）— workflowを確認"
    return ids[0]


def ab_new_id(g):
    return str(max(int(k) for k in g if k.isdigit()) + 1)


def ab_insert_model_patch(g, info, cls, values, head, must=()):
    """MODEL経路に1ノード割り込ませる。headの出力を使っていた全ノードを新ノードへ付け替える。"""
    nid = ab_new_id(g)
    g[nid] = {"class_type": cls,
              "inputs": ab_build_inputs(info, cls, values, links={"model": [head, 0]}, must=must)}
    for k, node in g.items():
        if k == nid:
            continue
        for ik, iv in list(node.get("inputs", {}).items()):
            if ik == "model" and isinstance(iv, list) and len(iv) == 2 and iv[0] == head:
                node["inputs"][ik] = [nid, 0]
    return nid


def ab_validate_graph(g, info, strict_ids=()):
    """グラフの全ノードについて、実機定義の必須入力が揃っているかを確認する。

    ComfyUIの検証と同じことを投入前にやる（37分かけて1本焼いた後に次のarmが
    `required_input_missing` で落ちる、という事故を防ぐ）。ベンチが挿したノード
    （strict_ids）は例外にし、元からあるノードは警告に留める — 動いている本番
    workflowを検証器の解釈違いで止めないため。
    """
    problems = []
    for nid, node in g.items():
        cls = node.get("class_type")
        if cls not in info:
            problems.append((nid, cls, "このComfyUIに存在しないノード"))
            continue
        req, _opt = ab_schema(info, cls)
        for name, spec in req.items():
            if name in node.get("inputs", {}):
                continue
            problems.append((nid, cls, f"必須入力 {name} が無い（定義: {spec}）"))
    hard = [p for p in problems if p[0] in strict_ids]
    assert not hard, "ベンチが組んだノードに不備がある:\n" + "\n".join(
        f"  node {n} ({c}): {m}" for n, c, m in hard)
    for n, c, m in problems:
        print(f"  ⚠ 元のworkflowのnode {n} ({c}): {m}", flush=True)
    return problems


def ab_patch_workflow(g, info, spec, ctx):
    """armの指定どおりにworkflowを書き換える。戻り値は人が読める適用内容のリスト。"""
    applied, inserted = [], []
    head = ab_one(g, "UNETLoader")
    mode = "r2v" if ab_ids(g, "MiniMaxH3ReferenceToVideo") else "i2v"

    if BENCH_FRAMES:
        h3 = ab_ids(g, "MiniMaxH3ReferenceToVideo") + ab_ids(g, "MiniMaxH3ImageToVideo")
        n = max(22, ((int(BENCH_FRAMES) - 5) // 17) * 17 + 5)   # H3の 17k+5 グリッドに丸める
        g[h3[0]]["inputs"]["length"] = n
        applied.append(f"frames={n}（BENCH_FRAMES指定・17k+5に丸め）")

    if spec.get("shift"):
        cls, cands = ab_find_class(info, r"^MiniMaxH3.*Shift$", r"MiniMax.*SigmaShift", r"SigmaShift")
        if cls:
            v, a = spec["shift"]
            head = ab_insert_model_patch(g, info, cls, {r"video": v, r"audio": a}, head,
                                         must=(r"video", r"audio"))
            inserted.append(head)
            applied.append(f"{cls}(video={v}, audio={a})")
        else:
            applied.append("⚠ SigmaShiftノードが見つからない → モデル既定のshiftのまま"
                           "（PDD/Turboは shift 12/3 前提。出力の音が破綻していたらここを疑う）")

    if spec.get("lora") == "turbo":
        fname = ctx["turbo_lora"][mode]
        cls, _ = ab_find_class(info, r"^LoraLoaderModelOnly$", r"^LoraLoader$")
        assert cls, "LoraLoaderModelOnly が無い — ComfyUIのバージョンを確認"
        head = ab_insert_model_patch(
            g, info, cls,
            {r"lora_name": Pick(re.escape(os.path.basename(fname))),
             r"strength_model": float(BENCH_LORA_STRENGTH)}, head,
            must=(r"lora_name",))
        inserted.append(head)
        applied.append(f"{cls}({os.path.basename(fname)}, strength={BENCH_LORA_STRENGTH})")

    if spec.get("pdd"):
        cls, _ = ab_find_class(info, r"MiniMaxH3PDDAccApply", r"PDDAcc.*Apply", r"PDD.*Acc")
        assert cls, ("PDD Acc のノードが登録されていない — カスタムノードの導入とComfyUI再起動を確認\n"
                     f"  {AB_PDD_NODE}")
        key = "fl2va" if mode == "i2v" else "ref2va"
        nfe = int(spec["pdd"])
        head = ab_insert_model_patch(
            g, info, cls,
            {r"(pdd|lora|acc).*(name|file)|^name$": Pick(key, r"8step"),
             r"^nfe$|steps": nfe,
             r"lora_strength": 1.0, r"head_strength": 1.0}, head,
            must=(r"(pdd|lora|acc).*(name|file)|^name$", r"^nfe$|steps"))
        inserted.append(head)
        si = ab_output_index(info, cls, "SIGMAS")
        assert si is not None, f"{cls} が SIGMAS を出力しない — ノードの仕様変更を確認"
        g[ab_one(g, "SamplerCustomAdvanced")]["inputs"]["sigmas"] = [head, si]
        applied.append(f"{cls}(nfe={nfe}, {key}) → SamplerCustomAdvanced.sigmas を"
                       "このノードの訓練済みsigmaへ差し替え（BasicSchedulerは不使用になる）")

    if spec.get("sparse"):
        cls, cands = ab_find_class(info, r"BlockSparseAttention", r"SparseAttention", r"Sparse.*Attn")
        if cls:
            head = ab_insert_model_patch(
                g, info, cls,
                {r"^(backend|mode|method)$": Pick(r"sol"),
                 r"^tau$|threshold|sparsity": float(BENCH_SPARSE_TAU),
                 r"sink": True}, head,
                must=(r"^(backend|mode|method)$", r"^tau$|threshold|sparsity"))
            inserted.append(head)
            applied.append(f"{cls}(tau={BENCH_SPARSE_TAU}) — 候補: {cands}")
        else:
            raise AssertionError(
                "Block Sparse Attention のノードが無い（ComfyUI core PR #16072 / 2026-09-06マージ）"
                " — ComfyUIが古い可能性。セル2を再実行して最新masterを取り直す")

    if spec.get("sampler"):
        g[ab_one(g, "KSamplerSelect")]["inputs"]["sampler_name"] = spec["sampler"]
        applied.append(f"sampler={spec['sampler']}")
    if spec.get("scheduler"):
        g[ab_one(g, "BasicScheduler")]["inputs"]["scheduler"] = spec["scheduler"]
        applied.append(f"scheduler={spec['scheduler']}")
    if spec.get("steps"):
        g[ab_one(g, "BasicScheduler")]["inputs"]["steps"] = int(spec["steps"])
        applied.append(f"steps={spec['steps']}")
    ab_validate_graph(g, info, strict_ids=set(inserted))
    return applied


# --- 追加の重み・ノードの取得 ------------------------------------------------

def ab_hf_files(repo):
    url = f"https://huggingface.co/api/models/{repo}/tree/main?recursive=1"
    with urllib.request.urlopen(url, timeout=60) as r:
        return [e["path"] for e in json.load(r) if e.get("type") == "file"]


def ab_hf_pick(repo, *patterns):
    """リポジトリのファイル一覧から全パターンに一致するものを選ぶ（版が複数あれば新しい方）。"""
    files = ab_hf_files(repo)
    hits = [f for f in files if all(re.search(p, f, re.I) for p in patterns)]
    assert hits, (f"{repo} に {patterns} へ一致するファイルが無い。\n"
                  f"  リポジトリの中身: {files}")
    best = sorted(hits)[-1]
    if len(hits) > 1:
        print(f"  候補 {hits} → {best} を使う", flush=True)
    return best


def ab_download(repo, path, subdir, min_mb=200):
    """HFの1ファイルを ComfyUI/models/<subdir>/ へ置く（aria2・レジューム可）。"""
    d = f"/content/ComfyUI/models/{subdir}"
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, os.path.basename(path))
    if os.path.exists(dst) and os.path.getsize(dst) >= min_mb * 2**20:
        print(f"  skip（配置済み）{os.path.basename(dst)}", flush=True)
        return dst
    if "reclaim_disk" in globals():
        globals()["reclaim_disk"](int(min_mb * 1.5) * 2**20, keep=(dst,))
    url = f"https://huggingface.co/{repo}/resolve/main/{path}"
    print(f"  DL中: {os.path.basename(path)} ← {repo}", flush=True)
    r = subprocess.run(["aria2c", "-c", "-x16", "-s16", "--file-allocation=none",
                        "--summary-interval=30", "--console-log-level=warn",
                        "-d", d, "-o", os.path.basename(path), url])
    assert r.returncode == 0 and os.path.getsize(dst) >= min_mb * 2**20, \
        f"{path} のDLに失敗 — セルを再実行すれば途中から再開する"
    return dst


def ab_clone_node(url):
    dst = f"/content/ComfyUI/custom_nodes/{os.path.basename(url)}"
    if os.path.isdir(os.path.join(dst, ".git")):
        print(f"  skip（導入済み）{os.path.basename(url)}", flush=True)
        return False
    print(f"  カスタムノード導入: {url}", flush=True)
    subprocess.run(["git", "clone", "--depth", "1", url, dst], check=True)
    req = os.path.join(dst, "requirements.txt")
    if os.path.exists(req):
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", req], check=False)
    return True     # Trueを返したら呼び出し側はComfyUIを再起動する


def ab_prepare(spec, ctx):
    """armが必要とする重み・カスタムノードを用意する。戻り値=ComfyUIの再起動が必要か。"""
    restart = False
    if spec.get("lora") == "turbo":
        for mode, key in (("i2v", "fl2v"), ("r2v", "ref2v")):
            if ctx["modes"] and mode not in ctx["modes"]:
                continue
            path = ab_hf_pick(AB_TURBO_REPO, rf"{key}[^/]*turbo", r"8step", r"comfyui", r"\.safetensors$")
            ctx["turbo_lora"][mode] = ab_download(AB_TURBO_REPO, path, "loras", min_mb=500)
    if spec.get("pdd"):
        restart |= ab_clone_node(AB_PDD_NODE)
        for mode, key in (("i2v", "fl2va"), ("r2v", "ref2va")):
            if ctx["modes"] and mode not in ctx["modes"]:
                continue
            path = ab_hf_pick(AB_PDD_REPO, key, r"8step", r"\.safetensors$")
            ab_download(AB_PDD_REPO, path, "pdd_acc", min_mb=500)
        restart = True      # 置いたファイルをノードに認識させるため必ず再起動する
    return restart


print("★ セル11: A/Bベンチの設定と部品を読み込んだ")
print(f"  arms={BENCH_ARMS}  chapter={BENCH_CHAPTER or '(バンドル先頭)'}  "
      f"DRY_RUN={BENCH_DRY_RUN}  frames={BENCH_FRAMES or '(台本どおり)'}")
_unknown = [a for a in BENCH_ARMS if a not in AB_ARMS]
assert not _unknown, f"未定義のarm: {_unknown} — 指定できるのは {sorted(AB_ARMS)}"
print("  次はセル12を実行する"
      + ("（DRY RUN: 配線検証と見積りだけで、生成はしない）" if BENCH_DRY_RUN else "（本番: 全armを生成する）"))
