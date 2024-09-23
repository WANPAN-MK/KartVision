from typing import List, Dict

def extract_tags(names: List[str]) -> Dict[str, List[str]]:
    names_to_process = set(names)
    tag_assignments = {}  # name -> tag
    max_tag_length = 5  # 最大タグ長

    while names_to_process and max_tag_length > 0:
        # タグ候補を生成
        tag_groups = {}
        for name in names_to_process:
            tag = name[:max_tag_length] if len(name) >= max_tag_length else name
            if tag not in tag_groups:
                tag_groups[tag] = []
            tag_groups[tag].append(name)

        # グループに2つ以上の名前がある場合、タグを確定
        for tag, group in tag_groups.items():
            if len(group) >= 2:
                for name in group:
                    tag_assignments[name] = tag
                names_to_process -= set(group)
        max_tag_length -= 1

    # 残りの名前に対してタグを割り当て（先頭1文字）
    for name in names_to_process:
        tag = name[0]
        tag_assignments[name] = tag

    # タグとプレイヤー名の辞書を作成
    tag_to_players = {}
    for name, tag in tag_assignments.items():
        player_name = name[len(tag):].strip()
        if tag not in tag_to_players:
            tag_to_players[tag] = []
        tag_to_players[tag].append(player_name)

    return tag_to_players