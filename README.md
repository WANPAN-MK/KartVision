# KartVision

マリオカート 8 デラックスの画像認識型即時集計機

# 環境構築

- [Rye](https://rye.astral.sh/)をインストール
- [KartVision](https://github.com/WANPAN01/KartVision)をクローン
- Google Vision API を有効にし、作られた JSON ファイルの環境変数を登録する (参考サイト:[Cloud Vision API](https://cloud.google.com/vision/docs/before-you-begin?hl=ja))
- `rye sync`を実行
- `rye run kart`を実行し、サーバーを立てる
