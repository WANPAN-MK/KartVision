import io
from google.cloud import vision
from typing import Tuple, List


# [("SPゴキブリ", 15), ("Aigas": 12), ....)]で左から順に一位
def result2ranking():
    points_by_position = [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    client = vision.ImageAnnotatorClient()
    with io.open("src/kartvision/static/cashe/preprocess.png", "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if not response.text_annotations:
        print("OCR結果が空です。画像が読めませんでした。")
        # ここでエラーにせず単純に return []
        return []

    raw_text = response.text_annotations[0].description
    lines = raw_text.split("\n")

    print("[DEBUG] OCR全文:")
    print(raw_text)
    print("[DEBUG] 行数:", len(lines))
    for i, line in enumerate(lines):
        print(f"  {i}: '{line}'")

    # 行数が 12 じゃない場合でもとりあえずデータを返してみる
    # => 後段でどう扱うかは要検討
    if len(lines) < 12:
        print("警告: 行数が 12 行未満、集計には不足している可能性があります。")
        # 例として少ない行数はスキップ:
        return []
    elif len(lines) > 12:
        print("警告: 行数が 12 行より多い、余分な文字があるかもしれません。")

    # ひとまず最初の 12 行を使う
    needed_lines = lines[:12]

    # ここでは (1位の名前, 15), (2位の名前, 12), ... という単純対応
    return list(zip(needed_lines, points_by_position))


class NotFoundResult(Exception):
    def __str__(self) -> str:
        return "Flagの誤検知が発生しました"
