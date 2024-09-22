import pyautogui
import datetime
from time import sleep
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


def take_screenshot_when_flag_detected():
    # 設定
    wait_time_before_screenshot = 0.3
    flag_image = "src/kartvision/static/images/flag_trigger.png"
    
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
            screenshot()
            running = False
            
        #
        #         regions = [
        #             (1520, 204, 2125, 309), (1520, 321, 2125, 426), 
        #             (1520, 438, 2125, 543), (1520, 555, 2125, 660), 
        #             (1520, 672, 2125, 777), (1520, 789, 2125, 894), 
        #             (1520, 906, 2125, 1011), (1520, 1023, 2125, 1128),
        #             (1520, 1140, 2125, 1245), (1520, 1257, 2125, 1362),
        #             (1520, 1374, 2125, 1479), (1520, 1491, 2125, 1596)
        #         ]

        #         text = crop_and_combine_image(screenshot_filename, regions)
        #         print(text)
        #         team_scores = aggregate_scores(text)
        #         print_team_scores(team_scores)
        #         adjust_score(team_scores)
        #         generate_html()
        #         print("待機中...")
        #         time.sleep(wait_time_after_screenshot)

        # except pyautogui.ImageNotFoundException:
        #     print("読み込み中... ")
        # except Exception as e:
        #     print(f"エラーが発生しました: {e}")

        # time.sleep(0.1)
