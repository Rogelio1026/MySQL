import pymysql
import sys

class TransferMoney(object):
    def __init__(self, conn):
        self.conn = conn

    def transfer(self, tr_acct, re_acct, money):
        try:
            self.check_acct_valid(tr_acct)
            self.check_acct_valid(re_acct)
            self.check_enough_money(money,tr_acct)
            self.reduce_money(money,tr_acct)
            self.add_money(money,re_acct)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def check_acct_valid(self, tr_acct):
        cursor = self.conn.cursor()
        try:
            sql = "select * from account where acct_id = %s" % tr_acct
            cursor.execute(sql)
            print "check_acct_valid " + sql
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("account %s do not exist" % tr_acct)
        finally:
            cursor.close()

    def check_enough_money(self, money, tr_acct):
        cursor = self.conn.cursor()
        try:
            sql = "select money from account where acct_id = %s and money > %s" % (tr_acct, money)
            cursor.execute(sql)
            print "check_enough_money " + sql
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("account %s do not have %s dollars" % tr_acct,money)
        finally:
            cursor.close()

    def reduce_money(self, money, tr_acct):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money = money - %s where acct_id = %s" % (money, tr_acct)
            cursor.execute(sql)
            print "reduce_money " + sql
            if cursor.rowcount != 1:
                raise Exception("transfer error" % tr_acct,money)
        finally:
            cursor.close()

    def add_money(self, money, re_acct):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money = money + %s where acct_id = %s" % (money, re_acct)
            cursor.execute(sql)
            print "add_money " + sql
            if cursor.rowcount != 1:
                raise Exception("transfer error" % re_acct,money)
        finally:
            cursor.close()
if __name__ == '__main__':

    # transfer_acct = sys.argv[1]
    # receive_acct = sys.argv[2]
    # money = sys.argv[3]

    conn = pymysql.connect(
        host = '127.0.0.1',
        port = 3306,
        user = 'root',
        passwd = 'zyh123',
        db = 'bank',
        charset = 'utf8'
    )

    tr_money = TransferMoney(conn)

    try:
        # tr_money.transfer(transfer_acct,receive_acct,money)
        tr_money.transfer(1,2,100)
    except Exception as e:
        print "Error" + str(e)
    finally:
        conn.close()
