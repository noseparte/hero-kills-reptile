# Python 示例代码
import redis


def delete_keys_with_prefix(redis_conn, prefix):
    cursor = '0'
    keys = []
    while cursor != 0:
        cursor, found_keys = redis_conn.scan(cursor, match=prefix + '*')
        keys.extend(found_keys)
    if keys:
        redis_conn.delete(*keys)



if __name__ == '__main__':
    redis_conn = redis.Redis(host='10.7.88.189', port=6379)
    delete_keys_with_prefix(redis_conn, "monopoly_reward")