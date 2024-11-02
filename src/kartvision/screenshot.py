import os
import pyautogui
from PIL import Image
from typing import List, Dict
import datetime


class Screenshot_Manager:
    def __init__(self) -> None:
        static_dir = "src/kartvision/static"
        if not os.path.isdir(static_dir):
            os.mkdir(static_dir)
        history_dir = os.path.join(static_dir, "history")
        if not os.path.isdir(history_dir):
            os.mkdir(history_dir)
        cashe_dir = os.path.join(static_dir, "cashe")
        if not os.path.isdir(cashe_dir):
            os.mkdir(cashe_dir)

    def screenshot(self):
        now = datetime.datetime.now()
        self.screenshot_filename = f"src/kartvision/static/history/screenshot_{now.strftime('%Y%m%d_%H%M%S')}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(self.screenshot_filename)
        print(f"スクリーンショットを保存しました: {self.screenshot_filename}")

    def clip_and_combine_screenshot(
        self, regions: List[List[int]], output_filename: str
    ):
        # 複数の座標でクロッピングし、それらを縦に結合
        with Image.open(self.screenshot_filename) as img:
            cropped_images = [img.crop(region) for region in regions]
            total_height = sum(cropped.height for cropped in cropped_images)
            max_width = max(cropped.width for cropped in cropped_images)
            combined_image = Image.new("RGB", (max_width, total_height))
            # 各画像を結合
            y_offset = 0
            for cropped in cropped_images:
                combined_image.paste(cropped, (0, y_offset))
                y_offset += cropped.height
            combined_image.save(output_filename)
            print(f"結合された画像を保存しました: {output_filename}")


def get_screenshot() -> List[str]:
    directory = "src/kartvision/static/history"
    images = ["history/" + f for f in os.listdir(directory) if f.endswith(".png")]
    images.sort(
        reverse=True,
        key=lambda x: os.path.getmtime(os.path.join(directory, x.split("history/")[1])),
    )
    return images


def get_screenshot_by_date() -> Dict[str, List[str]]:
    directory = "src/kartvision/static/history"
    images = ["history/" + f for f in os.listdir(directory) if f.endswith(".png")]
    images.sort(
        reverse=True,
        key=lambda x: os.path.getmtime(os.path.join(directory, x.split("history/")[1])),
    )
    images_by_date = {}
    for image in images:
        # ファイル名から日付を抽出（例：screenshot_YYYYMMDD_HHMMSS.png）
        filename = image.split("/")[-1]
        date_time_str = filename.replace("screenshot_", "").replace(".png", "")
        date_part = date_time_str.split("_")[0]  # 'YYYYMMDD'
        if date_part not in images_by_date:
            images_by_date[date_part] = []
        images_by_date[date_part].append(image)
    return images_by_date


def get_regions(region: List[int]) -> List[List[int]]:
    result_ratio = [10, 1]

    region_len = region[3] - region[1]
    num = result_ratio[0] * 12 + result_ratio[1] * 11
    unit_len = region_len / num
    regions = []
    for i in range(num + 1):
        if i % (result_ratio[0] + result_ratio[1]) == result_ratio[0]:
            regions.append(
                [
                    region[0],
                    region[1] + (i - result_ratio[0]) * unit_len,
                    region[2],
                    region[1] + i * unit_len,
                ]
            )
    return regions
