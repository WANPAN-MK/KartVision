# app.py
from flask import render_template, Flask, request
import visionapi
import threading
import pyautogui
from time import sleep
import screenshot
import image_editor
import analyzer
from threading import Lock
import time
from flask import jsonify

data_lock = Lock()
data = []
all_users_lock = Lock()
all_users = {}

screenshot_manager = screenshot.Screenshot_Manager()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/result")
def results():
    with data_lock:
        return render_template("result.html", data=data)

@app.route("/history")
def history():
    images_by_date = screenshot.get_screenshot_by_date()
    dates = sorted(images_by_date.keys(), reverse=True)
    return render_template("history.html", images_by_date=images_by_date, dates=dates)

@app.route("/edit")
def edit():
    with data_lock:
        return render_template("edit.html", data=data)

@app.route("/api/data")
def get_data():
    with data_lock:
        return jsonify(data)

@app.route("/api/edit_points", methods=["POST"])
def edit_points():
    tag_to_update = request.json.get("tag")
    new_points = request.json.get("points", None)
    target_tag = request.json.get("target_tag", None)  # タグ統合時のターゲットタグ

    with all_users_lock:
        # 編集対象のユーザーを検索
        users_to_update = [user for user in all_users.values() if user.tag == tag_to_update]

        if users_to_update:
            if target_tag:
                # タグの統合処理
                for user in users_to_update:
                    user.tag = target_tag  # タグを更新

            elif new_points is not None:
                # 点数の更新
                total_points = sum([user.sum_points() for user in users_to_update])
                difference = new_points - total_points
                # 点数を均等に配分
                per_user_adjustment = difference // len(users_to_update)
                for user in users_to_update:
                    if user.points:
                        user.points[-1] += per_user_adjustment  # 最新のポイントを調整

            # data を再計算
            total_points_by_tag = analyzer.calculate_total_points_by_tag(list(all_users.values()))
            total_points_by_tag.sort(key=lambda x: x['points'], reverse=True)

            with data_lock:
                global data
                data = total_points_by_tag

            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "タグが見つかりませんでした"}), 404

def run(group_num, tag_positions):
    global data, all_users
    # 設定
    wait_time_before_screenshot = 0.3
    flag_image = "src/kartvision/static/images/flag_trigger.png"
    
    running = True
    while running:
        sleep(0.1)
        print("待機中...")
        try:
            location = pyautogui.locateOnScreen(flag_image, confidence=0.8)
        except pyautogui.ImageNotFoundException:
            continue

        if not location:
            continue
        
        print("日本国旗が見つかりました。スクリーンショットを撮る前に待機します...")
        sleep(wait_time_before_screenshot)
        screenshot_manager.screenshot()

        region = [1520, 204, 2125, 1596]
        regions = screenshot.get_regions(region)
        
        screenshot_manager.clip_and_combine_screenshot(
            regions, "src/kartvision/static/cashe/combined_image.png"
        )

        image_editor.preprocess_image()
        ranking = visionapi.read_result_to_ranking()
        analyzer.assign_points(ranking)

        for user in ranking:
            print(user.get_dict())

        print("タグと名前を設定します...")
        tag_users = analyzer.set_tag_and_name(ranking, group_num=group_num, tag_positions=tag_positions)

        for tag_user in tag_users:
            print(tag_user.get_dict())

        # ユーザーデータを累積
        with all_users_lock:
            for user in tag_users:
                key = user.raw_name
                if key in all_users:
                    # 既存のユーザーの場合、ポイントを累積
                    all_users[key].points.extend(user.points)
                else:
                    # 新規ユーザーの場合、ユーザーを追加
                    all_users[key] = user

        total_points_by_tag = analyzer.calculate_total_points_by_tag(list(all_users.values()))
        total_points_by_tag.sort(key=lambda x: x['points'], reverse=True)
        
        with data_lock:
            data = total_points_by_tag

        print("合計ポイント:")
        for item in data:
            print(f"{item['tag']}: {item['points']}")

        time.sleep(15)
        # running = False

if __name__ == "__main__":
   # 対戦形式を入力
    is_valid_group_num = False
    while is_valid_group_num == False:
        group_num = input("対戦形式はどれですか？2v2:2, 3v3:3, 4v4:4, 6v6:6 -> ")
        if group_num in ['2', '3', '4', '6']:
            is_valid_group_num = True
        else:
            print("無効な入力です。もう一度入力してください。")
    # タグの位置を入力
    # ToDO 自動化
    is_valid_tag_positions = False
    while is_valid_tag_positions == False:
        tag_positions = input("この試合は前Tagのみですか？(y/n) -> ")
        if tag_positions in ['y', 'n']:
            is_valid_tag_positions = True
        else:
            print("無効な入力です。もう一度入力してください。")     

    # 画像処理スレッドを開始
    flag_detection_thread = threading.Thread(target=run, args=(group_num, tag_positions))
    flag_detection_thread.daemon = True
    flag_detection_thread.start()

    # Flaskアプリを実行
    app.run(port=8888)