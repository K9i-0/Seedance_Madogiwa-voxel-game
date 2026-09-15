#!/usr/bin/env python3
"""H3のA/Bベンチ用ノートブックを組み立てる（colab-videoスキル同梱ツール）。

正典 `h3_colab.ipynb` のセル1〜9をそのまま取り込み、末尾に `ab_bench/` のベンチ3セル
（11=設定 / 12=実行 / 13=レポート）を足した `h3_ab_bench_colab.ipynb` を作る。

正典を丸ごと取り込むのは、重み配置・ディスク管理・生成・Drive退避といった既存の機構を
ベンチでもそのまま使うため（セル12はセル1〜7を内部から呼ぶ）。正典を更新したらこのスクリプトを
再実行してベンチ側にも反映させる。

usage:
  python3 build_ab_bench_notebook.py                      # スキル直下に h3_ab_bench_colab.ipynb を作る
  python3 build_ab_bench_notebook.py 03_SCRIPTS/<NN>_<slug> [--chapter ch8]
      → <ランディレクトリ>/h3/h3_ab_bench_colab.ipynb（セル1のDriveパスと対象チャプターを設定済み）
"""
import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CELLS = [("11_config.py", 11), ("12_run.py", 12), ("13_report.py", 13)]
INTRO = """# MiniMax H3 — A/Bベンチ用ノートブック（窓際族物語 / colab-video スキル）

**同一チャプター・同一シードを複数条件（arm）で生成し、速度と精度を突き合わせる**ための派生ノートブック。
セル1〜9は製品生成用 `h3_colab.ipynb` と同一（セル12がそれらを内部から呼ぶ）。

## 使い方

1. **セル1** のDriveパス（`BUNDLE_ZIP_FROM_DRIVE` / `OUT_DRIVE_DIR`）を確認する。生成対象は
   セル11の `BENCH_CHAPTER` で決めるので、セル1の `CHAPTERS` は触らなくてよい
2. **セル11** で `BENCH_ARMS` を選ぶ（既定 `["base", "pdd8", "turbo8"]`）
3. **セル12** を実行する。既定は `BENCH_DRY_RUN=True` ＝ **生成せずに配線検証と時間・費用の見積りだけ**
4. 検証が通ったら セル11の `BENCH_DRY_RUN=False` にして **セル12** を再実行 → 全armを生成
5. **セル13** でレポート（比較表・コンタクトシート・横並び動画）を出す。
   ⚠ `BENCH_SHUTDOWN=True` にしているとセル12の最後で切断されるので、**レポートは切断前に**

## 注意

- armは `ch*__<arm>.mp4` として個別に保存され、生成済みはスキップ＝**中断・再開・セッション跨ぎに強い**
- 重みを差し替えるarm（`enc_nvfp4` / `unet_int8` / `best`）は追加DLと入れ替えが発生する。
  まずは重みを変えない `base` / `pdd8` / `turbo8` / `sparse` だけで回すのが安い
- **リップシンクと音声の忠実性は自動指標では判定しない。** セル13が出す横並び動画・
  コンタクトシート・チェックリストで目視し、ローカルの `/image-validation` で確定させる
"""


def load_cell(name):
    src = open(os.path.join(HERE, "ab_bench", name), encoding="utf-8").read()
    return {"cell_type": "code", "metadata": {"cellView": "form"}, "execution_count": None,
            "outputs": [], "source": src.splitlines(keepends=True)}


def chapter_mode(run_dir, ch):
    g = json.load(open(os.path.join(run_dir, f"{ch}_workflow.json")))
    return "r2v" if any(v.get("class_type") == "MiniMaxH3ReferenceToVideo" for v in g.values()) else "i2v"


def chapter_info(run_dir, ch):
    """そのチャプターの mode / frames / 不足している入力ファイル を返す。

    素材の不足はローカルで弾く。Colabへ上げてDriveをマウントしてから
    「参照ファイルが無い」で落ちるのは、GPU課金を払ってから気付くということなので。
    """
    g = json.load(open(os.path.join(run_dir, f"{ch}_workflow.json")))
    frames = next((int(v["inputs"]["length"]) for v in g.values()
                   if str(v.get("class_type", "")).startswith("MiniMaxH3") and "length" in v.get("inputs", {})),
                  None)
    missing = sorted({v for n in g.values() for k, v in n.get("inputs", {}).items()
                      if k in ("image", "audio") and isinstance(v, str)
                      and not os.path.exists(os.path.join(run_dir, v))})
    return chapter_mode(run_dir, ch), frames, missing


def pick_chapter(run_dir, chapters, requested):
    """ベンチ対象を決める。素材が揃っているチャプターの中から、R2V（セリフあり）を優先する。"""
    info = {ch: chapter_info(run_dir, ch) for ch in chapters}
    print("★ チャプターの素材チェック")
    for ch, (mode, frames, missing) in info.items():
        est = f"{frames}f≒{frames / 24:.1f}s" if frames else "?"
        note = "揃っている" if not missing else f"不足: {', '.join(missing)}"
        print(f"  {ch:<6}{mode.upper():<5}{est:>12}  {note}")
    if requested:
        assert requested in info, f"{requested} が {run_dir} に無い（あるのは {list(info)}）"
        mode, _f, missing = info[requested]
        assert not missing, (
            f"\n指定された {requested} は入力ファイルが足りない: {missing}\n"
            f"  → ラン側で用意してから再実行する（キーフレームなら {run_dir}/gen_keyframes.sh）。\n"
            f"  ⚠ gen_keyframes.sh のキーフレームは直列チェーン（各フレームが次の種になる）なので、"
            f"途中の1枚だけを作り直すことはできない")
        return requested
    ok = [ch for ch, (_m, _f, miss) in info.items() if not miss]
    assert ok, (
        f"\n{run_dir} には入力ファイルが揃ったチャプターが1本も無い — ベンチを組めない。\n"
        f"  → ラン側で素材を用意するか、素材の揃った別のランを指定する。\n"
        f"  ⚠ キーフレームは直列チェーンなので、gen_keyframes.sh を通しで流し直すことになる")
    r2v = [ch for ch in ok if info[ch][0] == "r2v"]
    if r2v:
        return r2v[0]
    print("\n⚠ 素材の揃ったR2V（セリフあり）チャプターが無いので I2V でベンチする。\n"
          "  I2Vには音声入力が無いため、**wav駆動リップシンクの劣化は測れない**"
          "（速度・映像品質・キーフレーム追従は測れる）。\n"
          "  リップシンクまで見るなら、セリフありチャプターの素材が揃ったランを指定すること")
    return ok[0]


def patch_cell1(src, zip_drive_path, out_drive_dir, chapter):
    subs = [
        (r"(?m)^CHAPTERS = .*$",
         f'CHAPTERS = {json.dumps([chapter])}  # 自動設定 — ベンチ対象の1本だけ'
         f'（セル4の素材チェックとセル3の重み選択がこの範囲に絞られる）'),
        (r"(?m)^BUNDLE_ZIP_FROM_DRIVE = .*$",
         f'BUNDLE_ZIP_FROM_DRIVE = "{zip_drive_path}"  # 自動設定（build_ab_bench_notebook.py）'),
        (r"(?m)^OUT_DRIVE_DIR = .*$",
         f'OUT_DRIVE_DIR = "{out_drive_dir}"  # 自動設定 — ベンチの成果物とレポートもここへ退避される'),
    ]
    for pat, rep in subs:
        assert re.search(pat, src), f"セル1に置換対象が見つからない: {pat}"
        src = re.sub(pat, rep, src, count=1)
    return src


BENCH_FRAMES_CAP = 160   # これより長いチャプターはベンチ時だけ短く切る（下の理由）
BENCH_FRAMES_TO = 124    # 17k+5グリッド上の約5.2秒


def patch_cell11(src, chapter, arms, frames=0):
    if frames:
        src = re.sub(r'(?m)^BENCH_FRAMES = .*$',
                     f'BENCH_FRAMES = {frames}              #@param {{type:"integer"}}'
                     f'  # 自動設定 — 計測用に短縮（0で台本どおりの尺）', src, count=1)
    if chapter:
        src = re.sub(r'(?m)^BENCH_CHAPTER = .*$',
                     f'BENCH_CHAPTER = "{chapter}"            #@param {{type:"string"}}', src, count=1)
    if arms:
        src = re.sub(r'(?m)^BENCH_ARMS = .*$',
                     f'BENCH_ARMS = {json.dumps(arms)}  #@param {{type:"raw"}}', src, count=1)
    return src


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", nargs="?", help="ラン専用ディレクトリ（省略時はスキル直下に汎用版を作る）")
    ap.add_argument("--chapter", default="", help="ベンチ対象チャプター（例 ch8。省略時はバンドル先頭）")
    ap.add_argument("--arms", default="", help="カンマ区切りのarm（例 base,pdd8,turbo8,sparse）")
    ap.add_argument("--notebook", default=os.path.join(HERE, "h3_colab.ipynb"))
    a = ap.parse_args()

    nb = json.load(open(a.notebook, encoding="utf-8"))
    arms = [s.strip() for s in a.arms.split(",") if s.strip()]
    chapter = a.chapter
    bench_frames = 0      # 長いチャプターを選んだときだけ、計測用に短い尺へ切る

    if a.run_dir:
        run_dir = a.run_dir.rstrip("/")
        slug = os.path.basename(os.path.abspath(run_dir))
        assert os.path.exists(os.path.join(run_dir, "script.md")), \
            f"{run_dir}/script.md が無い — ラン専用ディレクトリを指定する"
        wfs = sorted(glob.glob(os.path.join(run_dir, "ch*_workflow.json")),
                     key=lambda p: int(re.sub(r"\D", "", os.path.basename(p)) or 0))
        assert wfs, f"{run_dir} に ch*_workflow.json が無い — 先にworkflowを生成する"
        # セリフのあるR2Vを優先しつつ、**素材が揃っているチャプター**から選ぶ
        chapter = pick_chapter(run_dir,
                               [os.path.basename(w)[: -len("_workflow.json")] for w in wfs],
                               chapter)
        _mode, _frames, _ = chapter_info(run_dir, chapter)
        if _frames and _frames > BENCH_FRAMES_CAP:
            bench_frames = BENCH_FRAMES_TO
            print(f"\n★ {chapter} は {_frames}f（{_frames / 24:.1f}秒）と長いので、"
                  f"計測は {BENCH_FRAMES_TO}f（{BENCH_FRAMES_TO / 24:.1f}秒）に切って回す"
                  f"（セル11の BENCH_FRAMES。全armで同じ尺なので比較は成立する。0にすれば台本どおり）")
            print("  ⚠ ただし sparse arm の効きは系列長に比例して大きくなるので、"
                  "sparse の採用可否まで詰めるときは BENCH_FRAMES=0 で本来の尺を測り直すこと")
        zip_drive = f"/content/drive/MyDrive/h3_inputs/{slug}_h3_bundle.zip"
        out_drive = f"/content/drive/MyDrive/h3_outputs/{slug}"
        out_dir = os.path.join(run_dir, "h3")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "h3_ab_bench_colab.ipynb")
    else:
        slug = zip_drive = out_drive = out_path = None
        out_path = os.path.join(HERE, "h3_ab_bench_colab.ipynb")

    cells, intro_done = [], False
    for c in nb["cells"]:
        src = c["source"] if isinstance(c["source"], str) else "".join(c["source"])
        if c["cell_type"] == "markdown" and not intro_done:
            intro_done = True
            cells.append({"cell_type": "markdown", "metadata": {},
                          "source": (INTRO + ("\n\n---\n\n" if not a.run_dir else
                                              f"\n\n**対象ラン: {slug} / チャプター {chapter}**\n\n---\n\n")
                                     ).splitlines(keepends=True)})
            continue
        if c["cell_type"] == "code" and src.startswith("#@title 1.") and a.run_dir:
            c = dict(c, source=patch_cell1(src, zip_drive, out_drive, chapter))
        cells.append(c)

    for name, _n in CELLS:
        cell = load_cell(name)
        if name == "11_config.py":
            cell["source"] = patch_cell11("".join(cell["source"]), chapter, arms, bench_frames)
        cells.append(cell)

    nb["cells"] = cells
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

    print(f"★ 生成: {out_path}")
    print(f"  取り込んだ正典: {a.notebook}（セル1〜9）＋ ベンチ3セル（11 設定 / 12 実行 / 13 レポート）")
    if a.run_dir:
        print(f"  対象チャプター: {chapter}（{chapter_mode(a.run_dir.rstrip('/'), chapter).upper()}）")
        print(f"  バンドルzip: {zip_drive}（build_h3_run_package.py が作ったものをDriveへ置く）")
        print(f"  成果物・レポート: {out_drive}")
    print("  Colabへアップロードして、セル1 → セル11 → セル12（既定はDRY RUN）の順に実行する")


if __name__ == "__main__":
    main()
