import io
from google.cloud import vision
from typing import Tuple, List


# [("SPゴキブリ", 15), ("Aigas": 12), ....)]で左から順に一位
def result2ranking() -> List[Tuple[str, int]]:
    points_by_position = [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    client = vision.ImageAnnotatorClient()
    with io.open("src/kartvision/static/cashe/preprocess.png", "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations[0].description.split("\n")
    users = [text for text in texts]
    # 走行中のflagを検知したときの処理
    if len(users) != 12:
        raise NotFoundResult
    return list(zip(users, points_by_position))


class NotFoundResult(Exception):
    def __str__(self) -> str:
        return "Flagの誤検知が発生しました"
