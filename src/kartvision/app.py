from visionapi import read_result_to_ranking
from screenshot import get_screenshot_by_date, Screenshot_Manager
import image_editor
from user import create_teams_with_tags, assign_points
from server import KartFlask

from flask import render_template, request, jsonify
from pyautogui import locateOnScreen, ImageNotFoundException
from time import sleep
from threading import Lock, Thread


REGION = [1520, 204, 2125, 1596]

# ToDO: global変数をなくす
data_lock = Lock()
data = []
all_users_lock = Lock()
all_users = {}

screenshot_manager = Screenshot_Manager()

app = KartFlask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/result")
def results():
    with data_lock:
        return render_template("result.html", data=data)


@app.route("/history")
def history():
    images_by_date = get_screenshot_by_date()
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


# @app.route("/api/edit_points", methods=["POST"])
# def edit_points():
#     tag_to_update = request.json.get("tag")
#     new_points = request.json.get("points", None)
#     target_tag = request.json.get("target_tag", None)  # タグ統合時のターゲットタグ

#     with all_users_lock:
#         # 編集対象のユーザーを検索
#         users_to_update = [
#             user for user in all_users.values() if user.tag == tag_to_update
#         ]

#         if not users_to_update:
#             return (
#                 jsonify({"status": "error", "message": "タグが見つかりませんでした"}),
#                 404,
#             )

#         if target_tag:
#             # タグの統合処理
#             for user in users_to_update:
#                 user.tag = target_tag  # タグを更新

#         elif new_points is not None:
#             # 点数の更新
#             total_points = sum([user.sum_points() for user in users_to_update])
#             difference = new_points - total_points
#             # 点数を均等に配分
#             per_user_adjustment = difference // len(users_to_update)
#             for user in users_to_update:
#                 if user.points:
#                     user.points[-1] += per_user_adjustment  # 最新のポイントを調整

#         # data を再計算
#         teams = create_teams_with_tags(list(all_users.values()), group_num=2)
#         total_points_by_tag = [
#             {"tag": team.tag, "points": team.sum_points()} for team in teams
#         ]
#         total_points_by_tag.sort(key=lambda x: x["points"], reverse=True)

#         with data_lock:
#             global data
#             data = total_points_by_tag

#         return jsonify({"status": "success"})


# ToDo: タグの編集機能を追加
@app.route("/api/edit_tag", methods=["POST"])
def edit_tag():
    pass


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
            location = locateOnScreen(flag_image, confidence=0.8)
        except ImageNotFoundException:
            continue

        if not location:
            continue

        print("日本国旗が見つかりました。スクリーンショットを撮る前に待機します...")
        sleep(wait_time_before_screenshot)
        screenshot_manager.screenshot()
        screenshot_manager.clip_and_combine_screenshot(REGION)

        image_editor.preprocess_image()
        ranking = read_result_to_ranking()
        assign_points(ranking)

        for user in ranking:
            print(user)

        print("タグと名前を設定します...")
        teams = create_teams_with_tags(
            ranking, group_num=group_num, tag_positions=tag_positions
        )

        for team in teams:
            print(team)

        # ユーザーデータを積累
        with all_users_lock:
            for team in teams:
                for user in team.users:
                    key = user.raw_name
                    if key in all_users:
                        # 既存のユーザーの場合、ポイントを積累
                        all_users[key].points.extend(user.points)
                    else:
                        # 新規ユーザーの場合、ユーザーを追加
                        all_users[key] = user

        total_points_by_tag = [
            {"tag": team.tag, "sum_points": team.sum_points()} for team in teams
        ]
        total_points_by_tag.sort(key=lambda x: x["sum_points"], reverse=True)

        with data_lock:
            data = total_points_by_tag

        print("合計ポイント:")
        for item in data:
            print(f"{item['tag']}: {item['sum_points']}")

        sleep(15)
        # running = False


if __name__ == "__main__":
    # 対戦形式を入力
    is_valid_group_num = False
    while is_valid_group_num == False:
        group_num = input("対戦形式はどれですか？2v2:2, 3v3:3, 4v4:4, 6v6:6 -> ")
        if group_num in ["2", "3", "4", "6"]:
            is_valid_group_num = True
        else:
            print("無効な入力です。もう一度入力してください。")
    # タグの位置を入力
    # ToDO 自動化
    is_valid_tag_positions = False
    while is_valid_tag_positions == False:
        tag_positions = input("この試合は前Tagのみですか？(y/n) -> ")
        if tag_positions in ["y", "n"]:
            is_valid_tag_positions = True
        else:
            print("無効な入力です。もう一度入力してください。")

    # 画像処理スレッドを開始
    flag_detection_thread = Thread(target=run, args=(group_num, tag_positions))
    flag_detection_thread.daemon = True
    flag_detection_thread.start()

    # Flaskアプリを実行
    app.run(port=8888)
