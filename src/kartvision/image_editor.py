from PIL import Image, ImageEnhance, ImageFilter

def divide_rectangle_into_regions(x1, y1, x2, y2):
    num_divisions = 12
    total_height = y2 - y1
    region_height = total_height / num_divisions
    regions = []
    for i in range(num_divisions):
        y_start = y1 + region_height * i
        y_end = y_start + region_height
        region = (x1, int(y_start), x2, int(y_end))
        regions.append(region)
    return regions

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