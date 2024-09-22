import pyautogui
import datetime
from time import sleep
import os
from typing import List, Tuple
from PIL import Image

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
    # ToDo 時間でソート
    directory = "src/kartvision/static/history"
    images = ['history/' + f for f in os.listdir(directory) if f.endswith('.png')]
    print(images)
    return images


def run():
    # 設定
    wait_time_before_screenshot = 0.3
    flag_image = "src/kartvision/static/images/flag_trigger.png"
    
    screenshot_manager = Screenshot_Manager()
    
    running = True
    while running:
        sleep(0.1)
        print("待機中...")
        try:
            location = pyautogui.locateOnScreen(flag_image, confidence=0.7)
        except pyautogui.ImageNotFoundException:
            continue
            
        if location:
            print("日本国旗が見つかりました。スクリーンショットを撮る前に待機します...")
            sleep(wait_time_before_screenshot)
            screenshot_manager.screenshot()
            screenshot_manager.clip_screenshot((1520, 204, 2125, 1596))
            running = False