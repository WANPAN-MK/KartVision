from visionapi import result2ranking, NotFoundResult
from screenshot import get_screenshot_by_date, Screenshot_Manager
import image_editor
from user import create_teams_with_tags
from server import KartFlask

from flask import render_template, request, jsonify
from pyautogui import locateOnScreen, ImageNotFoundException
from time import sleep
from threading import Thread


REGION = [1520, 204, 2125, 1596]

screenshot_manager = Screenshot_Manager()

app = KartFlask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/result")
def results():
    data = app.high_score_list()
    print(data)
    return render_template("result.html", data=data)


@app.route("/history")
def history():
    images_by_date = get_screenshot_by_date()
    dates = sorted(images_by_date.keys(), reverse=True)
    return render_template("history.html", images_by_date=images_by_date, dates=dates)


@app.route("/edit")
def edit():
    data = app.high_score_list()
    return render_template("edit.html", data=data)


@app.route("/api/data")
def get_data():
    data = app.high_score_list()
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
    # 設定
    flag_image = "src/kartvision/static/images/flag_trigger.png"

    is_init = True
    while True:
        sleep(0.1)
        print("待機中...")
        try:
            locateOnScreen(flag_image, confidence=0.8)
        except ImageNotFoundException:
            continue

        print("日本国旗が見つかりました。スクリーンショットを撮る前に待機します...")
        sleep(0.3)
        screenshot_manager.screenshot()
        screenshot_manager.clip_and_combine_screenshot(REGION)
        image_editor.preprocess_image()

        try:
            ranking = result2ranking()
            print(ranking)
        except NotFoundResult as e:  # 誤検知したとき
            print(e)
            continue

        if is_init:
            print("タグと名前を設定します...")
            teams = create_teams_with_tags(
                ranking, group_num=group_num, tag_positions=tag_positions
            )
            for team in teams:
                print(team)
            # ユーザーデータを積累
            app.set_teams(teams)
            is_init = False
        else:
            print("ユーザーの情報を更新します...")
            app.update(ranking)
        print("合計ポイント:")
        print(f"{app.high_score_list()}")
        sleep(15)


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
