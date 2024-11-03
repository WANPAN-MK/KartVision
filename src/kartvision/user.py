from typing import List, Tuple


class User:
    def __init__(self, raw_name: str) -> None:
        self.raw_name = raw_name

    def __str__(self) -> str:
        if hasattr(self, "name") and self.name:
            return f"{self.raw_name}: name={self.name}, points={self.points}"
        return f"{self.raw_name}: points={self.points}"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.raw_name == other.raw_name

    def set_name(self, name: str):
        self.name = name

    def add_point(self, point: int):
        if not hasattr(self, "points"):
            self.points = [point]
        else:
            self.points.append(point)

    def sum_points(self):
        return sum(self.points)


class Team:
    def __init__(self, users: List[User], tag: str):
        self.users = users
        self.tag = tag

    def __str__(self) -> str:
        return f"Team {self.tag}:\n" + "\n".join([str(user) for user in self.users])

    def add_points(self, points: int):
        for user in self.users:
            user.add_points(points)

    def sum_points_dict(self):
        return {
            "tag": self.tag,
            "sum_points": sum([user.sum_points() for user in self.users]),
        }


# ToDo: 後ろタグの動作が悪い
def create_teams_with_tags(
    ranking: List[Tuple[str, int]], group_num: int, tag_positions=["prefix", "suffix"]
) -> List[Team]:
    remaining_users = []
    for r in ranking:
        user = User(r[0])
        user.add_point(r[1])
        remaining_users.append(user)

    final_teams = []
    confirmed_users = []

    for tag_len in range(10, 0, -1):
        tag_to_users = {}

        for position in tag_positions:
            for user in remaining_users:
                raw_name_length = len(user.raw_name)
                if raw_name_length < tag_len:
                    continue

                if position == "prefix":
                    tag_candidate = user.raw_name[:tag_len]
                    name_candidate = user.raw_name[tag_len:]
                elif position == "suffix":
                    tag_candidate = user.raw_name[-tag_len:]
                    name_candidate = user.raw_name[:-tag_len]
                else:
                    continue

                key = (position, tag_candidate)
                if key not in tag_to_users:
                    tag_to_users[key] = []
                tag_to_users[key].append((user, name_candidate))

        for (position, tag), grouped_users in tag_to_users.items():
            if len(grouped_users) >= group_num:
                team_users = []
                for user, name_candidate in grouped_users:
                    user.set_name(name_candidate)
                    team_users.append(user)
                    confirmed_users.append(user)
                final_teams.append(Team(team_users, tag))

        remaining_users = [
            user for user in remaining_users if user not in confirmed_users
        ]

        if not remaining_users:
            break

    tag_to_team = {team.tag: team for team in final_teams}

    for user in remaining_users:
        if user.raw_name:
            tag = user.raw_name[0]
            name = user.raw_name[1:] if len(user.raw_name) > 1 else ""
            user.set_name(name)
            if tag in tag_to_team:
                tag_to_team[tag].users.append(user)
            else:
                new_team = Team([user], tag)
                final_teams.append(new_team)
                tag_to_team[tag] = new_team
        else:
            user.set_name(user.raw_name)
            if "" in tag_to_team:
                tag_to_team[""].users.append(user)
            else:
                new_team = Team([user], "")
                final_teams.append(new_team)
                tag_to_team[""] = new_team

    return final_teams
