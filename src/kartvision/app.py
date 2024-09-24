from flask import render_template, Flask
import visionapi
import threading
import pyautogui
from time import sleep
import screenshot
import image_editor
import analyzer


data = [
    {'team': "A", 'points': 65},
    {'team': "B", 'points': 56},
    {'team': "C", 'points': 31},
    {'team': "D", 'points': 12},
]

app = Flask(__name__)

@app.route("/")
def results():
    return render_template("result.html", data=data)

@app.route("/history")
def history():
    images = screenshot.get_screenshot()
    return render_template("history.html", images=images)

def run():
    # 設定
    wait_time_before_screenshot = 0.3
    flag_image = "src/kartvision/static/images/flag_trigger.png"
    
    screenshot_manager = screenshot.Screenshot_Manager()
    
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
            image_editor.preprocess_image()
            ranking = visionapi.read_result_to_ranking()
            analyzer.assign_points(ranking)
            for user in ranking:
                print(user.get_dict())
            print("タグと名前を設定します...")
            tag_users = analyzer.set_tag_and_name(ranking, 3)
            for tag_user in tag_users:
                print(tag_user.get_dict())
            
            running = False

if __name__ == "__main__":
    # 画像処理スレッドを開始
    flag_detection_thread = threading.Thread(target=run)
    flag_detection_thread.daemon = True
    flag_detection_thread.start()

    # Flaskアプリを実行
    app.run()
