from flask import Flask
from user import User, Team
from typing import List


# Teamのデータを保持するFlaskクラス
class KartFlask(Flask):
    def __init__(self, *args, **kwargs):
        super(KartFlask, self).__init__(*args, **kwargs)
        self.teams = []

    def set_teams(self, teams: List[Team]):
        self.teams = teams

    def get_teams(self) -> List[Team]:
        return self.teams

    def update(self, ranked_users: List[User]):
        pass

    def high_score_list(self):
        spds = [team.sum_points_dict() for team in self.teams]
        spds.sort(key=lambda x: x["sum_points"], reverse=True)
        return spds
