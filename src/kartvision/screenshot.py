import os
import pyautogui
from PIL import Image
from typing import List, Tuple
import datetime

class Screenshot_Manager():
    def __init__(self) -> None:
        static_dir = "src/kartvision/static"
        if not os.path.isdir(static_dir):
            os.mkdir(static_dir)
        history_dir = os.path.join(static_dir, "history")
        if not os.path.isdir(history_dir):
            os.mkdir(history_dir)
        cashe_dir = os.path.join(static_dir, "cashe")
        if not os.path.isdir(cashe_dir):
            os.mkdir(cashe_dir)
        
    def screenshot(self):
        now = datetime.datetime.now()
        self.screenshot_filename = f"src/kartvision/static/history/screenshot_{now.strftime('%Y%m%d_%H%M%S')}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(self.screenshot_filename)
        print(f"スクリーンショットを保存しました: {self.screenshot_filename}")
    
    def clip_screenshot(self, region: Tuple[int]):
        # ToDo エラー処理（self.screenshot_filename）
        with Image.open(self.screenshot_filename) as img:
            cropped_image = img.crop(region)
            cropped_image.save("src/kartvision/static/cashe/clip_screenshot.png")

def get_screenshot() -> List[str]:
    directory = "src/kartvision/static/history"
    images = ['history/' + f for f in os.listdir(directory) if f.endswith('.png')]
    images.sort(reverse=True, key=lambda x: os.path.getmtime(os.path.join(directory, x.split('history/')[1])))
    return images
