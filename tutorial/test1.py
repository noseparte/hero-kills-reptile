import json

file_path = "C:/Users/admin/Downloads/sql.txt"
user_count = {}

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            datas = line.split(',')
            uid = datas[0].strip()
            itemId = datas[1].strip()
            count = float(datas[2].strip())
            # 初始化用户的item字典
            if uid not in user_count:
                user_count[uid] = {}

            # 汇总相同uid和itemId的count
            if itemId in user_count[uid]:
                user_count[uid][itemId] += count
            else:
                user_count[uid][itemId] = count

        except Exception as e:
            print(f"Error processing line: {e}")

# 输出汇总结果
for uid, items in user_count.items():
    for itemId, total_count in items.items():
        # print(f"UID: {uid}, ItemId: {itemId}, Total Count: {total_count}")
        print(uid,itemId,int(total_count),sep=',')
