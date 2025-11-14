from collections import defaultdict


# 解析数据并计算消耗
player_consumption = defaultdict(dict)


# Data structures to store results
player_choices = defaultdict(lambda: defaultdict(int))  # uid -> {item_id: total_count}
item_stats = defaultdict(int)  # item_id -> total_selected_count

with open('C://Users//admin//Desktop//pay.log', 'r', encoding='utf-8') as f:
    data = f.readlines()
    for line in data:
        # Split into uid and items part
        parts = line.strip().split(',')
        if len(parts) < 2:
            continue

        uid = parts[0]
        items_str = parts[1]

        # Split individual item selections
        item_entries = items_str.split('|')

        for entry in item_entries:
            if ';' not in entry:
                continue

            item_id, count = entry.split(';')
            try:
                count = int(count)
                item_id = int(item_id)
            except ValueError:
                continue

            # Record player's choice
            player_choices[uid][item_id] += count

            # Record global item stats
            item_stats[item_id] += count


with open('C://Users//admin//Desktop//玩家剩余的道具.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()
    for line in data:
        line = line.strip()
        if not line:
            continue

        playerId, item_id, remaining = line.split('\t')
        item_id = int(item_id)
        remaining = int(remaining)

        for uid, items in player_choices.items():
            if playerId == uid:
                for itemId, count in items.items():
                    if itemId == item_id:
                        consumed = count - remaining
                        if consumed < 0:
                            consumed = 0  # 处理剩余数量大于初始数量的情况
                        player_consumption[uid][item_id] = {
                            'initial': count,
                            'remaining': remaining,
                            'consumed': consumed
                        }

    # 输出结果
    print("玩家道具消耗统计:")
    for uid, items in player_consumption.items():
        print(f"\n玩家 {uid}:")
        print(f"{'道具ID':<10}{'初始数量':<10}{'剩余数量':<10}{'消耗数量':<10}")
        for item_id, counts in items.items():
            print(f"{item_id:<10}{counts['initial']:<10}{counts['remaining']:<10}{counts['consumed']:<10}")

    # 计算总消耗
    total_consumed = sum(
        item['consumed']
        for items in player_consumption.values()
        for item in items.values()
    )