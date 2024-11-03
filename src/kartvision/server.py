from flask import Flask
from user import User, Team
from typing import List, Tuple


# Teamのデータを保持するFlaskクラス
class KartFlask(Flask):
    def __init__(self, *args, **kwargs):
        super(KartFlask, self).__init__(*args, **kwargs)
        self.teams = []

    def set_teams(self, teams: List[Team]):
        self.teams = teams

    # ToDo: 2度目で同じ名前がくるとは限らず、その処理
    def update(self, ranking: List[Tuple[str, int]]):
        points_len = len(self.teams[0].users[0].points)  # Userのpointsの配列の長さ
        for name, point in ranking:
            u = User(name)
            users = [user for team in self.teams for user in team.users]
            for user in users:
                if (user == u) and (len(user.points) == points_len):
                    user.add_point(point)
                    break

    def high_score_list(self):
        spds = [team.sum_points_dict() for team in self.teams]
        spds.sort(key=lambda x: x["sum_points"], reverse=True)
        return spds
