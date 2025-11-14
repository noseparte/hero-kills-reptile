from collections import defaultdict

"""
###周卡剩可领取余天数
SELECT
	c.uid,
	c.id,
	FLOOR((
		c.endTime - GREATEST( c.lastReceiveTime, 1724724000000 )) / ( 24 * 60 * 60 * 1000 )) AS remaining_days
FROM
	user_week_card_new c
	JOIN userprofile p ON CAST( p.uid AS CHAR ) = c.uid
WHERE
	UNIX_TIMESTAMP(
	NOW()) * 1000 < c.endTime
	AND p.banTime < 9223372036854775807 HAVING remaining_days > 0;
"""


def generate_rewards(file_path, rewards):
    user_rewards = defaultdict(list)  # 使用 defaultdict 来存储每个用户的奖励

    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        # 分割每行数据为 uid, 月卡类型ID, 未领取天数
        uid, card_type, days = line.strip().split(';')
        days = int(days)

        # 获取该月卡类型的奖励表
        reward_table = rewards.get(card_type)
        if not reward_table:
            print(f"No reward found for card type {card_type}")
            continue

        # 计算奖励并将其添加到用户的奖励列表中
        for item_id, quantity in reward_table.items():
            total_quantity = quantity * days
            user_rewards[uid].append(f"goods,{item_id},{total_quantity}")

    # 输出最终拼接的结果
    for uid, rewards_list in user_rewards.items():
        result = f"{uid}#reward=" + "|".join(rewards_list)
        print(result)


# 定义不同月卡类型对应的 reward 表数据
rewards = {
    "10001": {
        "210873": 40
    },
    "20001": {
        "210922": 8
    },
    "30001": {
        "210913": 80
    },
    "40001": {
        "210893": 80
    },
    "50001": {
        "210903": 80
    },
    "60001": {
        "200364": 3
    }
}
#1461048738000003#reward=goods,210873,240|goods,210922,48|goods,210913,480|goods,210893,480|goods,210903,480|goods,200364,18

# 调用函数并传入文件路径
if __name__ == '__main__':
    # 调用函数并传入文件路径
    generate_rewards('C:\\server\\dr_svn\\trunk\\resource\\week_card.txt', rewards)
