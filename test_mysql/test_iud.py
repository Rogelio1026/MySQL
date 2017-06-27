import pymysql

conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'zyh123',
    db = 'sys',
    charset = 'utf8'
)

cursor = conn.cursor()

sql_insert = "insert into user(user_id, user_name) values(10, 'name10')"
sql_update = "update user set user_name = 'name91' where user_id = 9"
sql_delete = "delete from user where user_d < 3" # user_d should be user_id

try:
    cursor.execute(sql_insert)
    print cursor.rowcount

    cursor.execute(sql_update)
    print cursor.rowcount

    cursor.execute(sql_delete)
    print cursor.rowcount

    conn.commit()
     
except Exception as e:
    print e
    conn.rollback()

conn.close()
cursor.close()