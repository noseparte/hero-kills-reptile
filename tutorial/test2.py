import json

# 定义两个文件的路径
file_path_1 = "C:/Users/admin/Downloads/user_data_change.txt"
file_path_2 = "C:/Users/admin/Downloads/scorec.txt"

# 用于存储第一个文件中的 uid 和 itemId 的 count
user_count_1 = {}
user_count_2 = {}

# 读取第一个文件
with open(file_path_1, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            datas = line.split(',')
            uid = datas[0].strip()
            itemId = datas[1].strip()
            count = int(datas[2].strip())

            # 初始化用户的 item 字典
            if uid not in user_count_1:
                user_count_1[uid] = {}

            # 存储 uid 和 itemId 的 count
            user_count_1[uid][itemId] = count

        except Exception as e:
            print(f"Error processing line in file 1: {e}")

# 读取第二个文件并与第一个文件的 count 进行比较
with open(file_path_2, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            datas = line.split(',')
            uid = datas[0].strip()
            itemId = datas[1].strip()
            count = int(datas[2].strip())

            # 初始化用户的 item 字典
            if uid not in user_count_2:
                user_count_2[uid] = {}

            # 存储 uid 和 itemId 的 count
            user_count_2[uid][itemId] = count

        except Exception as e:
            print(f"Error processing line in file 2: {e}")

# 用于存储结果
result = {}

# 遍历 user_count_1
for uid, items in user_count_1.items():
    result[uid] = {}
    for itemId, count1 in items.items():
        # 如果在 user_count_2 中找到相同的 uid 和 itemId
        if uid in user_count_2 and itemId in user_count_2[uid]:
            count2 = user_count_2[uid][itemId]
            result[uid][itemId] = count1 - count2
        else:
            # 如果 itemId 不在 user_count_2 中，直接输出 user_count_1 的值
            result[uid][itemId] = count1

# 遍历 user_count_2，查找 user_count_1 中没有的项目
for uid, items in user_count_2.items():
    if uid not in result:
        result[uid] = {}
    for itemId, count2 in items.items():
        if itemId not in result[uid]:
            # 如果 itemId 不在 user_count_1 中，直接输出 user_count_2 的负数值
            result[uid][itemId] = -count2

# 输出结果
for uid, items in result.items():
    for itemId, final_count in items.items():
        if final_count > 0:
            print(f"{uid},{itemId},{final_count}")

