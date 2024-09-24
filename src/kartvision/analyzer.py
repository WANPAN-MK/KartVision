from typing import Any, List, Dict


class User:
    def __init__(self, raw_name: str) -> None:
        self.raw_name = raw_name
        self.tag = None
        self.name = None
        self.points = []

    def get_dict(self) -> Dict[str, Any]:
        return {
            "raw_name": self.raw_name,
            "tag": self.tag,
            "name": self.name,
            "points": self.points,
        }

    def set_tag_and_name(self, tag: str, name: str):
        self.tag = tag
        self.name = name

    def add_points(self, points: int):
        self.points.append(points)

    def set_tag_and_name(self, tag: str, name: str):
        self.tag = tag
        self.name = name

    def sum_points(self):
        return sum(self.points)
    
    


# タグと名前を分ける関数の定義
def set_tag_and_name(users: List[User], group_num: int) -> List[User]:
    remaining_users = users[:]  # 元のユーザーリストをコピーして処理する
    final_users = []

    for tag_len in range(10, 0, -1):  # タグを10文字から1文字の長さで試す
        tag_to_users = {}

        # ユーザーごとにタグと名前を分けて一時的にセット
        for user in remaining_users:
            if len(user.raw_name) < tag_len:
                user.set_tag_and_name(user.raw_name, "")  # raw_name全体をタグとして扱う
            else:
                user.set_tag_and_name(
                    user.raw_name[:tag_len], user.raw_name[tag_len:]
                )  # タグと名前に分ける

            # 同じタグを持つユーザーをグループ化
            if user.tag not in tag_to_users:
                tag_to_users[user.tag] = []
            tag_to_users[user.tag].append(user)

        # グループ数がgroup_num以上のタグを確定
        confirmed_users = []
        for tag, grouped_users in tag_to_users.items():
            if len(grouped_users) >= group_num:
                final_users.extend(grouped_users)  # 確定したユーザーを最終リストに追加
                confirmed_users.extend(grouped_users)  # 確定ユーザーをリストに追加

        # 確定したユーザーをremaining_usersから除外
        remaining_users = [
            user for user in remaining_users if user not in confirmed_users
        ]

        # 全ユーザーが確定したら終了
        if not remaining_users:
            break

    # 確定したユーザーリストを返す
    return final_users

def assign_points(ranking: List[User]):
    points_by_position = [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    
    for idx, user in enumerate(ranking):
        user.add_points(points_by_position[idx])
        