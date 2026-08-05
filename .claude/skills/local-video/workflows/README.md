# ComfyUI APIワークフローJSONの置き場所

初回セットアップ時に、ComfyUIで公式テンプレート **MiniMax H3 I2V** / **MiniMax H3 R2V** を開き、
**Export (API)** した結果をここへ保存する（SKILL.mdの「APIワークフローJSONの準備」参照）:

- `h3_i2v_api.json` — セリフのないチャプター用（first/last frame条件付け）
- `h3_r2v_api.json` — セリフのあるチャプター用（参照画像＋音声）

各ランではこのJSONをラン専用ディレクトリへ `chN_workflow.json` としてコピーし、
H3 inputs表どおりに入力を書き換えてから `h3_run.py` に渡す。
