from dataclasses import dataclass
from typing import List, Dict
import re


@dataclass
class RewardBox:
    threshold: int
    items: List[int]
    quantities: List[int]


@dataclass
class Player:
    player_id: int
    score: int


def load_players_from_file(filename: str) -> List[Player]:
    """Load player data from file in format 'player_id,score'"""
    players = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):  # Skip empty lines and comments
                if ',' in line:
                    player_id, score = map(str.strip, line.split(',', 1))
                    try:
                        players.append(Player(int(player_id), int(score)))
                    except ValueError:
                        print(f"Invalid data format in line: {line}")
    return players


# Define the reward boxes configuration
reward_boxes = [
    RewardBox(75000, [252016, 230101, 200034, 200363, 210921, 230104], [1000, 50, 300, 1, 10, 10000]),
    RewardBox(125000, [252016, 230101, 200034, 200363, 210921, 230104], [1000, 50, 300, 1, 10, 10000]),
    RewardBox(187500, [252016, 230101, 200034, 200363, 210921, 230104], [4000, 200, 750, 1, 10, 10000]),
    RewardBox(250000, [252016, 230101, 200034, 200363, 210921, 230104], [3000, 100, 500, 3, 10, 20000]),
    RewardBox(312500, [252016, 230101, 200034, 200363, 210921, 230104], [3000, 100, 500, 3, 10, 20000]),
    RewardBox(750000, [252016, 230101, 200034, 200363, 210921, 230104], [6000, 300, 1000, 3, 10, 30000]),
    RewardBox(1000000, [252016, 230101, 200034, 200363, 210921, 230104], [6000, 500, 1500, 5, 10, 30000]),
    RewardBox(1500000, [252016, 230101, 200034, 200363, 210921, 230104], [6000, 800, 2000, 5, 10, 30000]),
    RewardBox(2250000, [252016, 230101, 200034, 200363, 210921, 230104], [12000, 1000, 2500, 5, 10, 30000])
]


def calculate_rewards(score: int) -> Dict[int, int]:
    """Calculate accumulated rewards for a given score."""
    rewards = {}
    for box in reward_boxes:
        if score >= box.threshold:
            for item, quantity in zip(box.items, box.quantities):
                rewards[item] = rewards.get(item, 0) + quantity
        else:
            break  # Reward boxes are in order, so we can break early
    return rewards


def format_rewards(player: Player) -> str:
    """Format the rewards in the specified output format."""
    rewards = calculate_rewards(player.score)
    reward_parts = [f"goods,{item_id},{quantity}" for item_id, quantity in rewards.items()]
    return f"#{player.player_id}#reward={'|'.join(reward_parts)}"


def main():
    # Read players from file (change filename as needed)
    input_file = "D:/players.txt"  # File containing playerID,score lines
    output_file = "D:/player_rewards.txt"  # Output file

    try:
        players = load_players_from_file(input_file)

        with open(output_file, 'w') as out:
            for player in players:
                reward_str = format_rewards(player)
                print(reward_str)  # Print to console
                out.write(reward_str + '\n')  # Write to file

        print(f"\nProcessed {len(players)} players. Results saved to {output_file}")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()










# 1005975091000096,86305
# 1009025567000096,147582
# 1013458760000096,81547
# 1032144733000096,161200
# 1123649822000096,78600
# 1168694160000096,199442
# 备注 id rate item num score
# 跨服首都战积分宝箱1 813001 1|1|1|1|1|1 252016|230101|200034|200363|210921|230104 1000|50|300|1|10|10000 75000
# 跨服首都战积分宝箱2 813002 1|1|1|1|1|1 252016|230101|200034|200363|210921|230104 1000|50|300|1|10|10000 125000
# 跨服首都战积分宝箱3 813003 1|1|1|1|1|1 252016|230101|200034|200363|210921|230104 4000|200|750|1|10|10000 187500
# 跨服首都战积分宝箱4 813004 1|1|1|1|1|1 252016|230101|200034|200363|210921|230104 3000|100|500|3|10|20000 250000
# 跨服首都战积分宝箱5 813005 1|1|1|1|1|1 252016|230101|200034|200363|210921|230104 3000|100|500|3|10|20000 312500
# 跨服首都战积分宝箱6 813006 1|1|1|1|1|1 252016|230101|200034|200363|210921|230104 6000|300|1000|3|10|30000 750000
# 跨服首都战积分宝箱7 813007 1|1|1|1|1|1 252016|230101|200034|200363|210921|230104 6000|500|1500|5|10|30000 1000000
# 跨服首都战积分宝箱8 813008 1|1|1|1|1|1 252016|230101|200034|200363|210921|230104 6000|800|2000|5|10|30000 1500000
# 跨服首都战积分宝箱9 813009 1|1|1|1|1|1 252016|230101|200034|200363|210921|230104 12000|1000|2500|5|10|30000 2250000
# 用python实现 根据玩家的分数取对应的等级以及前面等级的奖励之和item和num | 分隔对应道具id和数量 然后汇总 格式如下
# #1461048738000003#reward=goods,210873,240|goods,210922,48|goods,210913,480|goods,210893,480|goods,210903,480|goods,200364,18