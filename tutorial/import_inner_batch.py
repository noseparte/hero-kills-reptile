import requests


def import_account(uid, new_uid, new_server):
    # 设置请求的 URL
    url = "http://10.7.88.182:81/apsadmin/admincp.php"

    # 定义请求参数
    params = {
        "mod": "mysql",
        "act": "import",
        "subact": "import",
        "uid": uid,
        "newuid": new_uid,
        "newserver": new_server
    }

    try:
        # 发送 GET 请求
        response = requests.get(url, params=params)

        # 检查请求是否成功
        if response.status_code == 200:
            print("导号成功")
            print("响应内容：", response.text)
        else:
            print("导号失败，状态码：", response.status_code)
            print("错误信息：", response.text)
    except requests.exceptions.RequestException as e:
        print("请求出错：", e)


# 示例使用
uid = "1000281830000007"
new_uid = "1000281830000007"
new_server = "997"


def import_from_file(filename, newserver):
    with open(filename, 'r') as file:
        for line in file:
            uid = line.strip()
            if uid:  # 检查非空行
                import_account(uid, uid, newserver)

# 使用示例
filename = "D://users.txt"
newserver = 3  # 设置目标服务器

import_from_file(filename, newserver)