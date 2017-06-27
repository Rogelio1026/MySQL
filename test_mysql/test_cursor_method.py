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

sql = "select * from user"

cursor.execute(sql)

print cursor.rowcount

rs = cursor.fetchone()

print rs

rs = cursor.fetchmany(2)

print rs

rs = cursor.fetchall()

print rs

conn.close()
cursor.close()