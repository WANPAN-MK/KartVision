import pyautogui
import datetime
import os
from typing import List

# 初期設定
def init():
    static_dir = "src/kartvision/static"
    if not os.path.isdir(static_dir):
        os.mkdir(static_dir)

    images_dir = os.path.join(static_dir, "history")
    if not os.path.isdir(images_dir):
        os.mkdir(images_dir)

# スクリーンショットを撮り保存
def screenshot(): 
    now = datetime.datetime.now()
    screenshot_filename = f"src/kartvision/static/history/screenshot_{now.strftime('%Y%m%d_%H%M%S')}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_filename)
    print(f"スクリーンショットを保存しました: {screenshot_filename}")

def get_screenshot() -> List[str]:
    # ToDo 時間でソート
    directory = "src/kartvision/static/history"
    images = ['history/' + f for f in os.listdir(directory) if f.endswith('.png')]
    print(images)
    return images
