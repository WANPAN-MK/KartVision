# KartVision

マリオカート 8 デラックスの画像認識型即時集計機

# 環境構築

- [Rye](https://rye.astral.sh/)をインストール
- [KartVision](https://github.com/WANPAN01/KartVision)をクローン
- Google Vision API を有効にし、作られた JSON ファイルの環境変数を登録する (参考サイト:[Cloud Vision API](https://cloud.google.com/vision/docs/before-you-begin?hl=ja))
- `rye sync`を実行
- `rye run kart`を実行し、サーバーを立てる

# 実行後

- 対戦形式を入力する
  （2v2 の場合は、「2」、3v3 は、「3」、4v4 は、「4」と入力）
- その模擬で宣言された Tag が前 Tag のみか後ろ Tag が存在するかを入力する(前 Tag のみの場合は、「y」、後ろ Tag がある場合は、「n」と入力)
