import sys
from flask import render_template, Flask
from google.cloud import vision
import imagelib
import threading

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

def run():
    imagelib.run()

if __name__ == "__main__":
    # 画像処理スレッドを開始
    flag_detection_thread = threading.Thread(target=run)
    flag_detection_thread.daemon = True
    flag_detection_thread.start()

    # Flaskアプリを実行
    app.run()
