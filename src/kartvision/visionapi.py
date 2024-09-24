import io
from google.cloud import vision
from typing import List
from analyzer import User


def read_result_to_ranking() -> List[User]:
    client = vision.ImageAnnotatorClient()
    with io.open("src/kartvision/static/cashe/preprocess.png", "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations[0].description.split("\n")
    users = [User(text) for text in texts]
    return users
