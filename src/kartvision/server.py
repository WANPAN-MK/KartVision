from difflib import SequenceMatcher
from flask import Flask
from user import User, Team
from typing import List, Tuple


def similarity_ratio(s1: str, s2: str) -> float:
    return SequenceMatcher(None, s1, s2).ratio()


def find_similar_user(users: List[User], new_raw_name: str, threshold=0.6) -> User:
    best_user = None
    best_score = 0.0
    for user in users:
        score = similarity_ratio(user.raw_name, new_raw_name)
        if score > best_score:
            best_score = score
            best_user = user
    if best_score >= threshold:
        return best_user
    return None


def find_team_by_first_letter(teams: List[Team], first_letter: str) -> Team:
    for team in teams:
        if team.tag == first_letter:
            return team
    return None


class KartFlask(Flask):
    def __init__(self, *args, **kwargs):
        super(KartFlask, self).__init__(*args, **kwargs)
        self.teams: List[Team] = []

    def set_teams(self, teams: List[Team]):
        self.teams = teams

    def update(self, ranking: List[Tuple[str, int]]):
        all_users = [user for team in self.teams for user in team.users]
        for raw_name, point in ranking:
            matched_user = None
            for user in all_users:
                if user.raw_name == raw_name:
                    matched_user = user
                    break
            if matched_user is None:
                matched_user = find_similar_user(all_users, raw_name, threshold=0.6)
            if matched_user is None:
                new_user = User(raw_name)
                new_user.add_point(point)
                all_users.append(new_user)
                first_letter = raw_name[0]
                existing_team = find_team_by_first_letter(self.teams, first_letter)
                if existing_team:
                    existing_team.users.append(new_user)
                else:
                    new_team = Team([new_user], first_letter)
                    self.teams.append(new_team)
            else:
                matched_user.add_point(point)

    def high_score_list(self):
        spds = [team.sum_points_dict() for team in self.teams]
        spds.sort(key=lambda x: x["sum_points"], reverse=True)
        return spds
