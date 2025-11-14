#!/bin/bash

# 配置参数
KEYWORDS=("rose heart send rank reward" "rose charm send rank reward")
UIDS=(
    "1678807094000171|1843973390000165|1389636808000171|1155239738000170|1025543840000171|1455000097000171|1609070823000165|1157722819000167|1399477820000170|1742865935000167|1338563206000165|1492554723000165|1638927661000170|1636212650000167|1524414053000167|1032528249000167|1434541008000170|1678009334000171|1887069509000167|1500576494000171|1996943773000171|1782319701000167|1410003796000171|1150330968000171|1357885070000166|1627247686000171|1040252316000171|2028590520000171|1286355134000171|1435278118000170|1016423496000165"
)
LOG_PATTERN="ziplogs/smartfox.log.2025-08-25-00*"

# 创建临时目录
TMP_DIR=$(mktemp -d)
echo "Using temporary directory: $TMP_DIR"

# 函数：清理临时文件
cleanup() {
    rm -rf "$TMP_DIR"
    echo "Cleaned up temporary directory."
}
trap cleanup EXIT

# 处理每个关键字
for keyword in "${KEYWORDS[@]}"; do
    echo "Searching for keyword: '$keyword'"
    echo "============================================================"

    # 为当前关键字创建结果文件
    RESULT_FILE="$TMP_DIR/results_${keyword// /_}.txt"
    > "$RESULT_FILE"

    # 处理每个日志文件
    for log_file in $LOG_PATTERN; do

        # 使用zgrep搜索关键字
        if zgrep -F "$keyword" "$log_file" > /dev/null 2>&1; then

            # 提取包含关键字的行，并检查是否包含任何UID
            zgrep -F "$keyword" "$log_file" | while read -r line; do
                for uid in "${UIDS[@]}"; do
                    if echo "$line" | grep -q "$uid"; then
                        echo "Line: $line" >> "$RESULT_FILE"
                    fi
                done
            done
        fi
    done

    # 显示当前关键字的结果
    if [ -s "$RESULT_FILE" ]; then
        cat "$RESULT_FILE"
    else
        echo "No results found for '$keyword'."
    fi

    echo ""
done
