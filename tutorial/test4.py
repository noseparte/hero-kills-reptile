from collections import defaultdict

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

    # Analysis Results
    print("=== Player Choices ===")
    for uid, items in player_choices.items():
        print(f"SELECT * from user_item where ownerId = {uid}")
        print(" and itemId in (")
        for item_id, count in items.items():
            print(f"{item_id},")
        print(")")

    print("\n=== Item Popularity ===")
    for item_id, total in sorted(item_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"Item {item_id}: selected {total} times in total")

    # Additional statistics
    total_players = len(player_choices)
    total_items_selected = sum(item_stats.values())
    unique_items = len(item_stats)

    print(f"\n=== Summary ===")
    print(f"Total players: {total_players}")
    print(f"Total items selected: {total_items_selected}")
    print(f"Unique items: {unique_items}")