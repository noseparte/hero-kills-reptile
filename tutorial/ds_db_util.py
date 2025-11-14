import pymysql
is_local = False

def get_admin_db_conn():
    host = "10.7.88.23"
    port = 3306
    user = "root"
    pw = "admin123"
    db = "admin_deploy"
    if not is_local:
        host = "pc-0xi0a5a83188nd364.rwlb.rds.aliyuncs.com"
        port = 3306
        user = "aps_admin"
        pw = "ES@9!@&Lub8W"
    return get_db_conn(host, port, user, pw, db)

def get_global_db_conn():
    host = "10.7.88.23"
    port = 3306
    user = "root"
    pw = "admin123"
    db = "dsdb_global"
    if not is_local:
        host = "pc-0xi0t17u48u6xj414.rwlb.rds.aliyuncs.com"
        port = 3306
        user = "aps_admin"
        pw = "V2ewCaP2&yjN"
    return get_db_conn(host, port, user, pw, db)

def get_alliance_db_conn():
    host = "10.7.88.23"
    port = 3306
    user = "root"
    pw = "admin123"
    db = "alliancedb"
    if not is_local:
        host = "pc-0xir3qzz38697dn9v.mysql.polardb.rds.aliyuncs.com"
        port = 3306
        user = "aps_admin"
        pw = "V3J$s$@Wt@P7"
    return get_db_conn(host, port, user, pw, db)



def get_domain_db_conn():
    host = "10.7.88.23"
    port = 3306
    user = "root"
    pw = "admin123"
    db = "domain_db"
    if not is_local:
        host = "pc-0xi0t17u48u6xj414.rwlb.rds.aliyuncs.com"
        port = 3306
        user = "aps_admin"
        pw = "V2ewCaP2&yjN"
    return get_db_conn(host, port, user, pw, db)


def get_bi_db_conn():
    host = "10.7.88.27"
    port = 4000
    user = "root"
    pw = "admin123"
    db = "dw_raw"
    if not is_local:
        host = "10.0.82.0"
        port = 4000
        user = "root"
        pw = "ReadyGo220329"
    return get_db_conn(host, port, user, pw, db)


def get_mail_db_conn():
    host = "10.7.88.23"
    port = 3306
    user = "root"
    pw = "admin123"
    db = "dsdb_ingamemail"
    if not is_local:
        host = "pc-0xi4zvh34p2pk4x81.rwlb.rds.aliyuncs.com"
        port = 3306
        user = "aps_admin"
        pw = "A3bKkgVwv$@X"
    return get_db_conn(host, port, user, pw, db)



def get_game_db_conn(server_id):
    db = "dsdb" + str(server_id)
    sql = "select ip_inner from tbl_db where db_id = %s" % server_id
    conn = get_admin_db_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is None:
        return None
    cursor.close()
    conn.close()
    host = row[0]
    port = 3306
    user = "root"
    pw = "admin123"
    if not is_local:
        user = "aps_admin"
        pw = "uap3STw6&9Z@"
    return get_db_conn(host, port, user, pw, db)




def get_game_log_db_conn(server_id):
    db = "ApsLogDB"
    host = "10.7.88.23"
    port = 3306
    user = "root"
    pw = "admin123"
    if not is_local:
        sql = "select ip_inner from tbl_db where db_id = %s" % server_id
        conn = get_admin_db_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is None:
            return None
        cursor.close()
        conn.close()
        host = row[0]
        user = "aps_admin"
        pw = "uap3STw6&9Z@"
        db = "dslogdb" + str(server_id)
    return get_db_conn(host, port, user, pw, db)


def get_all_server():
    conn = get_admin_db_conn()
    cursor = conn.cursor()
    cursor.execute("select svr_id from tbl_webserver")
    rows = cursor.fetchall()
    servers = []
    for row in rows:
        servers.append(row[0])
    cursor.close()
    conn.close()
    return servers


def get_server_ip(sid):
    conn = get_admin_db_conn()
    cursor = conn.cursor()
    cursor.execute("select ip_inner from tbl_webserver where svr_id = %s" %(sid))
    rows = cursor.fetchone()
    host = rows[0]
    cursor.close()
    conn.close()
    return host


def get_server_redis_ip(sid):
    conn = get_admin_db_conn()
    cursor = conn.cursor()
    cursor.execute("select redis_ip from tbl_webserver where svr_id = %s" %(sid))
    rows = cursor.fetchone()
    host = rows[0]
    cursor.close()
    conn.close()
    return host



def get_user_server_id(uid):
    conn = get_global_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT server from account_new where gameUid = '%s'" %(uid))
    row = cursor.fetchone()
    if row is None:
        return None
    sid = int(row[0])
    cursor.close()
    conn.close()
    return sid

def get_db_conn(host, port, user, pw, db):
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=pw,
        database=db,
        charset="utf8")
    return conn


def query_all_server(sql):
    servers = get_all_server()
    for sid in servers:
        conn = get_game_db_conn(sid)
        if conn is None:
            continue
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.close()
        print("server = %s, query success, sql = %s" % (sid, sql))



def execute_all_server(sql):
    servers = get_all_server()
    for sid in servers:
        try:
            conn = get_game_db_conn(sid)
            if conn is None:
                continue
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.close()
            conn.commit()
            conn.close()
        except Exception as e:
            print("server = %s, execute fail, sql = %s" % (sid, sql), e)
        print("server = %s, execute success, sql = %s" % (sid, sql))


def query(server, sql):
    conn = get_game_db_conn(server)
    if conn is None:
        return None
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows



def execute(server, sql, is_commit):
    conn = get_game_db_conn(server)
    cursor = conn.cursor()
    print(sql)
    cursor.execute(sql)
    cursor.close()
    if is_commit:
        conn.commit()
    conn.close()




def execute_sql_list(server, sqls, is_commit):
    conn = get_game_db_conn(server)
    cursor = conn.cursor()
    for sql in sqls:
        print(sql)
        cursor.execute(sql)
    cursor.close()
    if is_commit:
        conn.commit()
    conn.close()

def execute_many(server, sql, rows, is_commit):
    conn = get_game_db_conn(server)
    cursor = conn.cursor()
    print(sql, rows)
    cursor.executemany(sql, rows)
    cursor.close()
    if is_commit:
        conn.commit()
    conn.close()

