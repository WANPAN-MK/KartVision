import sys
from flask import render_template, Flask
from google.cloud import vision
import imagelib
import threading

# 初期化
imagelib.init()

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
    images = imagelib.get_screenshot()
    return render_template("history.html", images=images)

def start_flag_detection():
    imagelib.take_screenshot_when_flag_detected()

if __name__ == "__main__":
    # 画像処理スレッドを開始
    flag_detection_thread = threading.Thread(target=start_flag_detection)
    flag_detection_thread.daemon = True  # メインプログラム終了時にスレッドも終了
    flag_detection_thread.start()

    # Flaskアプリを実行
    app.run()
