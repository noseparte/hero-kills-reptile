"""
-- 月卡剩可领取余天数
SELECT m.uid, FLOOR(((m.buyTime + m.totalCount * ( 24 * 60 * 60 * 1000 ) - 1724724000000) / ( 24 * 60 * 60 * 1000 ))) AS remaining_days
FROM
	`monthly_card` m
	JOIN userprofile p ON p.uid = m.uid
WHERE
	m.`available` = '1'
	AND p.banTime < 9223372036854775807
	HAVING remaining_days > 0;
"""


def generate_rewards(file_path, reward_table):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        # 分割每行数据为 uid 和未领取天数
        uid, days = line.strip().split(';')
        days = int(days)

        # 计算奖励并拼接结果
        rewards = []
        for item_id, quantity in reward_table.items():
            total_quantity = quantity * days
            rewards.append(f"goods,{item_id},{total_quantity}")

        # 拼接最终结果字符串
        result = f"{uid}#reward=" + "|".join(rewards)
        print(result)


# 定义 reward 表中的数据
reward_table = {
    "200364": 5,
    "250000": 10,
    "200201": 60,
    "230100": 2,
    "230104": 1000
}

if __name__ == '__main__':
    # 调用函数并传入文件路径
    generate_rewards('C:\\server\\dr_svn\\trunk\\resource\\month.txt', reward_table)
