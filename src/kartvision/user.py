from typing import List, Tuple
import re


class User:
    def __init__(self, raw_name: str):
        self.raw_name = raw_name
        self.points = []

    def add_point(self, point: int):
        self.points.append(point)

    def sum_points(self):
        return sum(self.points)

    def set_name(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return f"{self.raw_name}: points={self.points}"


class Team:
    def __init__(self, users: List[User], tag: str):
        self.users = users
        self.tag = tag

    def sum_points_dict(self):
        return {
            "tag": self.tag,
            "sum_points": sum(user.sum_points() for user in self.users),
        }

    def __str__(self):
        return f"Team {self.tag}: " + ", ".join(str(u) for u in self.users)


def create_teams_with_tags(
    ranking: List[Tuple[str, int]],
    group_num: int = 3,
    tag_positions: List[str] = ["prefix", "suffix"],
) -> List[Team]:
    all_users = []
    for raw_name, point in ranking:
        user = User(raw_name)
        user.add_point(point)
        all_users.append(user)

    final_teams: List[Team] = []
    remaining_users = all_users[:]

    for tag_len in range(10, 0, -1):
        for position in tag_positions:
            grouping_map = {}
            for user in remaining_users:
                rn = user.raw_name
                if len(rn) < tag_len:
                    continue
                if position == "prefix":
                    candidate = rn[:tag_len].strip()
                    rest = rn[tag_len:].strip()
                elif position == "suffix":
                    suffix_candidate = rn[-tag_len:]
                    rest = rn[:-tag_len].rstrip()
                    if suffix_candidate.endswith("/s"):
                        candidate = "/s"
                        rest = rn[:-2].rstrip()
                    else:
                        candidate = re.sub(r"^[_\s]+", "", suffix_candidate)
                    candidate = candidate.strip()
                else:
                    continue
                if not candidate:
                    continue
                if candidate not in grouping_map:
                    grouping_map[candidate] = []
                grouping_map[candidate].append((user, rest))
            to_remove = []
            for tag_candidate, user_info_list in grouping_map.items():
                if len(user_info_list) >= group_num:
                    team_users = []
                    for u, name_remaining in user_info_list:
                        u.set_name(name_remaining)
                        team_users.append(u)
                        to_remove.append(u)
                    new_team = Team(team_users, tag_candidate)
                    final_teams.append(new_team)
            remaining_users = [u for u in remaining_users if u not in to_remove]
            if not remaining_users:
                break
        if not remaining_users:
            break

    while remaining_users:
        user = remaining_users.pop()
        fallback_tag = user.raw_name.split()[0]
        new_team = Team([user], fallback_tag)
        final_teams.append(new_team)

    return final_teams
