from PIL import Image, ImageEnhance, ImageFilter

def preprocess_image():
    im = Image.open('src/kartvision/static/cashe/clip_screenshot.png') # ToDo Openしないやり方で
    im = im.convert('L') # 白黒変換
    enhancer = ImageEnhance.Brightness(im)
    im = enhancer.enhance(0.8)
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Sharpness(im)
    im = enhancer.enhance(2)
    threshold = 128
    im = im.point(lambda p: p > threshold and 255)
    im.save("src/kartvision/static/cashe/preprocess.png")