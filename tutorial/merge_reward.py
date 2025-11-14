import json
import re
from collections import defaultdict

# 日志文件路径
log_file = "C:/Users/admin/Desktop/rweard.log"

# 定义正则表达式匹配 JSON 数据
json_pattern = re.compile(r"\{.*\}")


# 用于存储奖励的 Map
reward_map = defaultdict(int)

# 解析日志文件
with open(log_file, "r", encoding="utf-8") as file:
    for line in file:
        # 匹配 JSON 数据
        json_match = json_pattern.search(line)
        if json_match:
            try:
                # 提取 JSON 数据
                json_data = json.loads(json_match.group())

                # 提取奖励信息
                rewards = json_data.get("reward", [])
                for reward in rewards:
                    value = reward.get("value")
                    reward_type = value.get("itemId")
                    reward_value = value.get("rewardAdd")

                    # 使用 itemId 作为键，累加奖励
                    reward_map[reward_type] += reward_value
            except json.JSONDecodeError:
                # 如果 JSON 解析失败，跳过该行
                continue

# 打印整合结果
print("整合的奖励：")
for reward_key, total_count in reward_map.items():
    print(f"{reward_key}: {total_count}")