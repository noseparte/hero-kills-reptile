import json

file_path = "C:/Users/admin/Downloads/battle1.log"
user_count = {}

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            datas = line.split(' | ')
            time = datas[0]
            uid = datas[7].strip()
            content = datas[10].strip()
            init_data = json.loads(content)

            # 获取 itemId 和 count
            itemId = init_data['param']
            count = init_data['count']

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
        print(uid,itemId,total_count,sep=',')
