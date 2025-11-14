import ds_db_util
import requests


log_file = "uid_score.log"

conn_cache = {}




lines = []
with open(log_file, "r", encoding="utf8") as f:
    lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        arr = line.strip().split('|')
        uid = arr[0]
        scoreDetail = arr[1].strip()

        server_id = ds_db_util.get_user_server_id(uid)
        host = ds_db_util.get_server_ip(server_id)
        url = "http://%s:8080/gameservice/RepairOnline?funcName=testPlayerLevel&func=updateTotalScoreAndDayScore&uid=%s&scoreDetail=%s&zoneId=%s&authenticateKey=gm" % (host, uid, scoreDetail, server_id)
        print(url)
        resp = requests.get(url, timeout=5)
        print(resp.text)


