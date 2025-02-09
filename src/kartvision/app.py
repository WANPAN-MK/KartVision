import json
import os

from visionapi import result2ranking, NotFoundResult
from screenshot import get_screenshot_by_date, Screenshot_Manager
import image_editor
from user import create_teams_with_tags
from server import KartFlask

from flask import render_template, request, jsonify
from pyautogui import locateOnScreen, ImageNotFoundException
from time import sleep
from threading import Thread


def load_region():
    """
    config.json があれば読み込み、なければデフォルトのREGIONを返す
    """
    default_region = [1520, 204, 2125, 1596]
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if "REGION" in data:
                return data["REGION"]
    return default_region


# 1) REGIONを先に決める
REGION = load_region()
print("使用するREGION:", REGION)

# 2) スクリーンショットマネージャ & Flaskアプリを生成
screenshot_manager = Screenshot_Manager()
app = KartFlask(__name__)


# ---------- Flask ルート定義 ----------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/result")
def results():
    data = app.high_score_list()
    print("Resultデータ:", data)
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


@app.route("/api/edit_tag", methods=["POST"])
def edit_tag():
    """
    タグの編集API
    リクエストのJSONには 'tag'（現在のタグ）と 'new_tag'（更新後のタグ）が必要
    """
    data = request.get_json()
    current_tag = data.get("tag")
    new_tag = data.get("new_tag")

    if not current_tag or not new_tag:
        return jsonify({"status": "error", "message": "タグ情報が不足しています"}), 400

    found = False
    for team in app.teams:
        if team.tag == current_tag:
            team.tag = new_tag
            found = True
            print(f"タグ更新: {current_tag} -> {new_tag}")
            break

    if not found:
        return (
            jsonify(
                {"status": "error", "message": "指定されたタグが見つかりませんでした"}
            ),
            404,
        )

    return jsonify({"status": "success"})


@app.route("/api/edit_points", methods=["POST"])
def edit_points():
    """
    - tag: 編集対象のチームタグ
    - new_points: 新しく設定したい合計点 (整数) → チーム全体の最新ラウンド点を再分配
    - target_tag: ドラッグ&ドロップなどで統合先のタグ
    """
    data = request.get_json()
    tag = data.get("tag")
    new_points = data.get("points", None)
    target_tag = data.get("target_tag", None)

    # ① ドラッグ＆ドロップによるチーム統合の場合
    if target_tag:
        source_team = None
        dest_team = None
        for team in app.teams:
            if team.tag == tag:
                source_team = team
            elif team.tag == target_tag:
                dest_team = team
        if not source_team or not dest_team:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "指定されたタグが見つかりませんでした",
                    }
                ),
                404,
            )

        # 統合処理：source_teamのユーザーをdest_teamに移す
        dest_team.users.extend(source_team.users)
        # 元チームを削除
        app.teams = [t for t in app.teams if t.tag != tag]
        print(f"統合完了: {tag} → {target_tag}")
        return jsonify({"status": "success"})

    # ② 直接編集の場合
    elif new_points is not None:
        updated = False
        for team in app.teams:
            if team.tag == tag:
                current_total = team.sum_points()
                diff = new_points - current_total
                num_members = len(team.users)
                if num_members > 0:
                    # 差分を人数分に分配 (余りも考慮)
                    adjustment = diff // num_members
                    remainder = diff % num_members
                    for i, user in enumerate(team.users):
                        user.points[-1] += adjustment
                        if i < remainder:
                            user.points[-1] += 1
                    updated = True
                    print(f"点数更新: {tag} の合計点 {current_total} → {new_points}")
                break
        if not updated:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "指定されたタグが見つかりませんでした",
                    }
                ),
                404,
            )
        return jsonify({"status": "success"})

    # ③ いずれでもない不正リクエスト
    else:
        return jsonify({"status": "error", "message": "更新内容が不正です"}), 400


def run(group_num):
    """
    スレッド上で常時フラグ画像を探し、
    見つかったらスクリーンショット→OCR→チーム更新
    """
    flag_image = "src/kartvision/static/images/flag_trigger.png"
    group_num_int = int(group_num)

    # 常に 前タグ+後ろタグ 両方を解析
    positions = ["prefix", "suffix"]
    is_init = True

    while True:
        sleep(0.1)
        print("待機中...")

        # 日本国旗の検出
        try:
            locateOnScreen(flag_image, confidence=0.8)
        except ImageNotFoundException:
            continue

        print("日本国旗が見つかりました。スクリーンショットを撮る前に待機します...")
        sleep(0.3)

        # スクショ → 切り抜き → 前処理
        screenshot_manager.screenshot()
        screenshot_manager.clip_and_combine_screenshot(REGION)
        image_editor.preprocess_image()

        # OCR
        try:
            ranking = result2ranking()
            print("OCR結果:", ranking)
        except NotFoundResult as e:
            print(e)
            continue

        # 初回 or 2回目以降
        if is_init:
            print("タグと名前を設定します...")
            teams = create_teams_with_tags(
                ranking, group_num=group_num_int, tag_positions=positions
            )
            app.set_teams(teams)
            is_init = False
        else:
            print("ユーザーの情報を更新します...")
            app.update(ranking)

        # デバッグ出力
        for team in app.teams:
            print(team)

        print("合計ポイント:")
        print(app.high_score_list())
        sleep(30)  # 次のチェックまでのインターバル


if __name__ == "__main__":
    # コンソールから 対戦形式(2/3/4/6) を入力
    is_valid_group_num = False
    while not is_valid_group_num:
        group_num = input("対戦形式はどれですか？2v2:2, 3v3:3, 4v4:4, 6v6:6 -> ")
        if group_num in ["2", "3", "4", "6"]:
            is_valid_group_num = True
        else:
            print("無効な入力です。もう一度入力してください。")

    # 別スレッドでフラグ検出ループを回す
    flag_detection_thread = Thread(target=run, args=(group_num,))
    flag_detection_thread.daemon = True
    flag_detection_thread.start()

    # Flaskサーバーを起動
    app.run(port=8888)
