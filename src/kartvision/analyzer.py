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

    def sum_points(self):
        return sum(self.points)


def set_tag_and_name(users: List[User], group_num: int) -> List[User]:
    remaining_users = users[:]  # 元のユーザーリストをコピーして処理する
    final_users = []

    for tag_len in range(10, 0, -1):  # タグを10文字から1文字の長さで試す
        tag_to_users = {}
        tag_positions = ['prefix', 'suffix']  # タグの位置：先頭か末尾

        for position in tag_positions:
            # ユーザーごとにタグと名前を分けて一時的にセット
            for user in remaining_users:
                raw_name_length = len(user.raw_name)
                if raw_name_length < tag_len:
                    continue  # ユーザー名がタグ候補より短い場合はスキップ

                if position == 'prefix':
                    tag_candidate = user.raw_name[:tag_len]
                    name_candidate = user.raw_name[tag_len:]
                elif position == 'suffix':
                    tag_candidate = user.raw_name[-tag_len:]
                    name_candidate = user.raw_name[:-tag_len]

                if not name_candidate:
                    continue  # 名前が空の場合はスキップ

                # タグ候補でユーザーをグループ化
                key = (position, tag_candidate)
                if key not in tag_to_users:
                    tag_to_users[key] = []
                tag_to_users[key].append((user, tag_candidate, name_candidate))

        # グループ数がgroup_num以上のタグを確定
        confirmed_users = []
        for (position, tag), grouped_users in tag_to_users.items():
            if len(grouped_users) >= group_num:
                for user, tag_candidate, name_candidate in grouped_users:
                    user.set_tag_and_name(tag_candidate, name_candidate)
                    final_users.append(user)
                    confirmed_users.append(user)

        # 確定したユーザーをremaining_usersから除外
        remaining_users = [
            user for user in remaining_users if user not in confirmed_users
        ]

        # 全ユーザーが確定したら終了
        if not remaining_users:
            break

    # 残ったユーザーはタグなしで名前だけ設定
    for user in remaining_users:
        user.set_tag_and_name('', user.raw_name)
        final_users.append(user)

    return final_users


def assign_points(ranking: List[User]):
    points_by_position = [15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    for idx, user in enumerate(ranking):
        if idx < len(points_by_position):
            user.add_points(points_by_position[idx])
        else:
            user.add_points(0)  # 順位がポイントリストを超える場合は0ポイント