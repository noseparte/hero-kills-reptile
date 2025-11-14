import re
import urllib.parse
from collections import defaultdict, Counter
import sys


def analyze_gameservice_logs(log_file_path):
    # 第一层：所有/gameservice/请求的统计
    general_stats = defaultdict(lambda: defaultdict(int))

    # 第二层：RepairOnline的funcName分析 - 添加默认值
    repair_stats = {
        'total': 0,
        'without_funcname': 0,
        'func_counts': Counter(),
        'func_methods': defaultdict(Counter),
        'func_params': defaultdict(lambda: defaultdict(Counter)),
        'func_param_combos': defaultdict(Counter)
    }

    # 日志行解析正则表达式
    log_pattern = re.compile(
        r'"(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH) (/gameservice/[^\s\?]+)'
    )

    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                match = log_pattern.search(line)
                if not match:
                    continue

                method = match.group(1)
                full_path = match.group(2)

                # 只处理/gameservice/开头的路径
                if full_path.startswith('/gameservice/'):
                    # 分离路径和查询参数
                    path_parts = urllib.parse.urlsplit(full_path)
                    command = path_parts.path
                    query_params = urllib.parse.parse_qs(path_parts.query)

                    # 1. 通用统计
                    general_stats[command][method] += 1

                    # 2. 特殊处理RepairOnline
                    if command == '/gameservice/RepairOnline':
                        repair_stats['total'] += 1

                        # 提取funcName参数
                        func_name = query_params.get('funcName', [''])[0]
                        if not func_name:
                            repair_stats['without_funcname'] += 1
                            continue

                        # 统计funcName分布
                        repair_stats['func_counts'][func_name] += 1
                        repair_stats['func_methods'][func_name][method] += 1

                        # 统计funcName下的参数
                        param_names = set(query_params.keys())
                        for param in param_names:
                            if param != 'funcName':  # 排除funcName本身
                                value = query_params[param][0] if query_params[param] else ""
                                repair_stats['func_params'][func_name][param] += 1

                        # 统计参数组合（排除funcName）
                        param_combo = frozenset(k for k in param_names if k != 'funcName')
                        if param_combo:  # 确保组合不为空
                            repair_stats['func_param_combos'][(func_name, param_combo)] += 1

        return general_stats, repair_stats

    except FileNotFoundError:
        print(f"错误：文件未找到 - {log_file_path}")
        return {}, repair_stats  # 返回默认的repair_stats
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return {}, repair_stats  # 返回默认的repair_stats


def print_general_stats(stats):
    if not stats:
        print("未找到有效的/gameservice/请求")
        return

    print("\n" + "=" * 60)
    print("所有/gameservice/请求统计")
    print("=" * 60)
    print(f"{'指令':<40} {'方法':<8} {'数量':<10}")
    print("-" * 60)

    # 按指令名称排序
    for command, methods in sorted(stats.items()):
        # 按方法名称排序
        for method, count in sorted(methods.items()):
            # 格式化输出
            cmd_display = command[:38] + "..." if len(command) > 38 else command.ljust(40)
            print(f"{cmd_display} {method:<8} {count:<10}")


def print_repair_stats(stats):
    # 修复：检查'total'键是否存在
    if 'total' not in stats or stats['total'] == 0:
        print("\n未找到RepairOnline请求")
        return

    print("\n" + "=" * 60)
    print(f"RepairOnline深度分析 (共 {stats['total']} 条请求)")
    if 'without_funcname' in stats and stats['without_funcname'] > 0:
        print(f"⚠️ 注意: 有 {stats['without_funcname']} 条请求缺少funcName参数")
    print("=" * 60)

    # 1. funcName分布
    print("\n[funcName分布]")
    print(f"{'功能名称':<25} {'请求数':<10} {'占比':<8}")
    print("-" * 45)
    total_with_func = stats['total'] - stats['without_funcname']
    for func, count in stats['func_counts'].most_common():
        percent = (count / total_with_func) * 100 if total_with_func > 0 else 0
        print(f"{func:<25} {count:<10} {percent:.1f}%")

    # 2. 各funcName的方法分布
    if 'func_methods' in stats and stats['func_methods']:
        print("\n[各功能的方法使用分布]")
        for func in stats['func_counts']:
            print(f"\n* 功能: {func}")
            print(f"  {'方法':<8} {'数量':<10} {'占比':<8}")
            total_func_req = stats['func_counts'][func]
            for method, count in stats['func_methods'][func].most_common():
                percent = (count / total_func_req) * 100
                print(f"  {method:<8} {count:<10} {percent:.1f}%")

    # 3. 各funcName的参数分析
    if 'func_params' in stats and stats['func_params']:
        print("\n[各功能的参数使用分析]")
        for func in stats['func_counts']:
            print(f"\n* 功能: {func}")
            if func in stats['func_params'] and stats['func_params'][func]:
                print("  参数使用频率:")
                for param, count in stats['func_params'][func].most_common(5):
                    percent = (count / stats['func_counts'][func]) * 100
                    print(f"  - {param}: {count}次 ({percent:.1f}%)")
            else:
                print("  未发现额外参数")

    # 4. 参数组合分析
    if 'func_param_combos' in stats and stats['func_param_combos']:
        print("\n[常见参数组合]")
        print("(显示前10种组合)")
        for (func, combo), count in stats['func_param_combos'].most_common(10):
            params = ", ".join(sorted(combo)) if combo else "(无额外参数)"
            print(f"{func} + [{params}]: {count}次")


if __name__ == "__main__":

    log_file = "C://Users//admin//Desktop//sysrequest.log"
    print(f"正在分析日志文件: {log_file}")

    general_stats, repair_stats = analyze_gameservice_logs(log_file)

    if general_stats:
        print_general_stats(general_stats)
    else:
        print("未找到/gameservice/请求")

    print_repair_stats(repair_stats)

    print("\n分析完成!")

