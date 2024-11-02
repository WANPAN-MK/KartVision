from flask import Flask
from user import Team
from typing import List


class KartFlask(Flask):
    def __init__(self, *args, **kwargs):
        super(KartFlask, self).__init__(*args, **kwargs)
        self.teams = []

    def set_teams(self, teams: List[Team]):
        self.teams = teams

    def get_teams(self) -> List[Team]:
        return self.teams

    def to_list(self):
        return [team.to_dict() for team in self.teams]
