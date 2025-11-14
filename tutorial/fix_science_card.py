import ds_db_util
import requests


log_file = "sciencecard.log"

conn_cache = {}




lines = []
with open(log_file, "r", encoding="utf8") as f:
    lines = f.readlines()


for line in lines:
    line = line.strip()
    if not line:  # Skip empty lines
        continue
        
    arr = line.split(',')
    if len(arr) < 2:  # Check if line has both uid and time
        print(f"Skipping malformed line: {line}")
        continue

    arr = line.strip().split(',')
    uid = arr[0]
    time = arr[1]
   
    server_id = ds_db_util.get_user_server_id(uid)
    host = ds_db_util.get_server_ip(server_id)
    url = "http://%s:8080/gameservice/RepairOnline?funcName=testPlayerLevel&func=fixScienceCardBuff&stateId=700001&uid=%s&time=%s&zoneId=%s&authenticateKey=gm" % (host, uid, time, server_id)
    print(url)
    resp = requests.get(url, timeout=5)
    print(resp.text)


