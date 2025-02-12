import io
from google.cloud import vision
from typing import List, Tuple


def result2ranking():
    points_by_position = [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    client = vision.ImageAnnotatorClient()
    with io.open("src/kartvision/static/cashe/preprocess.png", "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    if not response.text_annotations:
        print("OCR結果が空です。画像が読めませんでした。")
        return []

    raw_text = response.text_annotations[0].description
    lines = raw_text.split("\n")

    print("[DEBUG] OCR全文:")
    print(raw_text)
    print("[DEBUG] 行数:", len(lines))
    for i, line in enumerate(lines):
        print(f"  {i}: '{line}'")

    if len(lines) < 12:
        print("警告: 行数が 12 行未満、集計には不足している可能性があります。")
        return []
    elif len(lines) > 12:
        print("警告: 行数が 12 行より多い、余分な文字があるかもしれません。")

    needed_lines = lines[:12]
    return list(zip(needed_lines, points_by_position))


class NotFoundResult(Exception):
    def __str__(self) -> str:
        return "Flagの誤検知が発生しました"
