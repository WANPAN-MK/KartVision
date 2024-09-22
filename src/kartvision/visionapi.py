import io
from google.cloud import vision

def read_image_to_text() -> str:
    client = vision.ImageAnnotatorClient()
    with io.open('src/kartvision/static/cashe/preprocess.png', 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts[0].description