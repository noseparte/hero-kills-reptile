import argparse
import os
import re
import sys
from collections import defaultdict
import ds_db_util


def read_uids_from_file(uid_file):
    uids = []
    try:
        with open(uid_file, 'r', encoding='utf-8') as f:
            for line in f:
                uid = line.strip()
                if uid and not uid.startswith('#'):  # 忽略空行和注释行
                    uids.append(uid)
    except FileNotFoundError:
        print(f"错误：UID文件 '{uid_file}' 未找到")
        sys.exit(1)
    except Exception as e:
        print(f"读取UID文件时出错: {e}")
        sys.exit(1)

    return uids


def get_log_file_path(base_dir, uid):

    server_id = ds_db_util.get_user_server_id(uid)

    # 构建日志文件路径
    log_file = f"bp_{server_id}.log"
    return os.path.join(base_dir, log_file)


def find_last_uid_records(base_dir, uids):
    # 按日志文件分组UID
    uid_groups = defaultdict(list)
    for uid in uids:
        log_file = get_log_file_path(base_dir, uid)
        uid_groups[log_file].append(uid)

    # 初始化结果字典
    last_records = {uid: None for uid in uids}

    # 处理每个日志文件
    for log_file, file_uids in uid_groups.items():
        if not os.path.exists(log_file):
            print(f"警告：日志文件 {log_file} 不存在，跳过")
            continue

        try:
            with open(log_file, 'r', encoding='utf-8') as file:
                for line in file:
                    # 检查行中是否包含该文件对应的任何UID
                    for uid in file_uids:
                        # 使用正则表达式确保完整匹配UID
                        if f"| {uid} |" in line:
                            last_records[uid] = line.strip()
        except Exception as e:
            print(f"读取文件 {log_file} 时出错: {e}")

    return last_records


def main():
    parser = argparse.ArgumentParser(description='根据UID后三位查找对应日志文件中的最后一条记录')
    parser.add_argument('base_dir', help='日志文件所在的基础目录')
    parser.add_argument('-f', '--uid-file', required=True, help='包含UID列表的文件')
    parser.add_argument('-o', '--output', help='输出结果到文件')

    args = parser.parse_args()

    # 检查基础目录是否存在
    if not os.path.isdir(args.base_dir):
        print(f"错误：目录 '{args.base_dir}' 不存在")
        sys.exit(1)

    # 读取UID列表
    uids = read_uids_from_file(args.uid_file)
    print(f"从文件中读取了 {len(uids)} 个UID")

    # 查找每个UID的最后一条记录
    results = find_last_uid_records(args.base_dir, uids)

    # 输出结果
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                for uid, record in results.items():
                    if record:
                        f.write(record + '\n')
            print(f"结果已保存到 {args.output}")
        except Exception as e:
            print(f"写入输出文件时出错: {e}")
    else:
        for uid, record in results.items():
            if record:
                print(f"UID {uid} 的最后一条记录:")
                print(record)
                print("-" * 80)
            else:
                print(f"未找到UID {uid} 的记录")

    # 统计信息
    found_count = sum(1 for record in results.values() if record)
    print(f"总共找到 {found_count} 个UID的记录，{len(uids) - found_count} 个UID未找到记录")


if __name__ == "__main__":
    main()