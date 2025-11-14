import subprocess
import gzip
import glob
import re

# 配置参数
keywords = ["rose heart send rank reward", "rose charm send rank reward"]
uids = [
    "1678807094000171", "1843973390000165", "1389636808000171", "1155239738000170",
    "1025543840000171", "1455000097000171", "1609070823000165", "1157722819000167",
    "1399477820000170", "1742865935000167", "1338563206000165", "1492554723000165",
    "1638927661000170", "1636212650000167", "1524414053000167", "1032528249000167",
    "1434541008000170", "1678009334000171", "1887069509000167", "1500576494000171",
    "1996943773000171", "1782319701000167", "1410003796000171", "1150330968000171",
    "1357885070000166", "1627247686000171", "1040252316000171", "2028590520000171",
    "1286355134000171", "1435278118000170", "1016423496000165"
]
log_pattern = "ziplogs/smartfox.log.2025-08-25-00*"


def search_logs():
    # 获取匹配的日志文件列表
    log_files = glob.glob(log_pattern)

    results = {}

    for keyword in keywords:
        results[keyword] = {}
        for uid in uids:
            results[keyword][uid] = []

    # 搜索每个日志文件
    for log_file in log_files:
        print(f"Processing {log_file}...")

        try:
            # 使用zgrep进行搜索
            for keyword in keywords:
                # 构建zgrep命令
                cmd = ["zgrep", keyword, log_file]

                # 执行命令
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()

                if stderr:
                    print(f"Error processing {log_file}: {stderr.decode()}")
                    continue

                # 处理输出
                lines = stdout.decode().split('\n')
                for line in lines:
                    if not line:
                        continue

                    # 检查行中是否包含任何UID
                    for uid in uids:
                        if uid in line:
                            results[keyword][uid].append((log_file, line))

        except Exception as e:
            print(f"Error processing {log_file}: {e}")

    # 输出结果
    for keyword in keywords:
        print(f"\nResults for keyword: '{keyword}'")
        print("=" * 60)

        found_any = False
        for uid in uids:
            if results[keyword][uid]:
                found_any = True
                print(f"\nUID: {uid}")
                for file_path, line in results[keyword][uid]:
                    print(f"  File: {file_path}")
                    print(f"  Line: {line}")

        if not found_any:
            print("No matches found for this keyword.")

    return results


if __name__ == "__main__":
    search_logs()