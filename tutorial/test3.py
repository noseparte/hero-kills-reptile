import redis

from tutorial.message import GlobalRefreshTimeValue_pb2

# 连接到Redis
r = redis.Redis(host='10.7.88.182', port=6379, db=0)

# 获取HEX编码的字符串
hex_str = r.get('march_plunder_res_gold:223333457')
if hex_str:
    # 反解析HEX字符串
    print(type(hex_str))
    message = GlobalRefreshTimeValue_pb2.MyMessage()
    message.ParseFromString(hex_str)
    print(message)
    # original_str = bytes.fromhex(hex_str.decode('utf-8')).decode('utf-8')
    # print(original_str)