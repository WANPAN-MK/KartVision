# region_setup.py
import pyautogui
import time
import json
import os


def show_realtime_mouse():
    """
    マウス座標をリアルタイム表示し続け、
    Ctrl + C 押下で、その瞬間の座標を返す。
    """
    print("マウス座標をリアルタイム表示します。")
    print("マウスを動かして位置を決め、Ctrl + C で確定してください。")
    try:
        while True:
            x, y = pyautogui.position()
            print(f"\r現在のマウス座標: ({x}, {y})   ", end="")
            time.sleep(0.1)
    except KeyboardInterrupt:
        x, y = pyautogui.position()
        print(f"\n確定座標: ({x}, {y})")
        return x, y


def main():
    print("=== KartVision: 領域設定ツール (Retina対策 2倍) ===")
    print(
        "まず、スクショしたい範囲の 左上 にカーソルを合わせて Ctrl + C で確定してください。"
    )

    x1, y1 = show_realtime_mouse()

    print("\n次に、範囲の 右下 にカーソルを合わせて Ctrl + C で確定してください。")
    x2, y2 = show_realtime_mouse()

    # 左右上下を補正
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)

    # Retinaで座標が半分になる場合、2倍
    left *= 2
    top *= 2
    right *= 2
    bottom *= 2

    region = [left, top, right, bottom]

    config_data = {"REGION": region}
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config_data, f, ensure_ascii=False, indent=2)

    print(f"\nREGION = {region} を config.json に保存しました。")
    print("今後この領域がスクリーンショットに使用されます。")


if __name__ == "__main__":
    main()
