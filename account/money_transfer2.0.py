import pymysql
import sys

class TransferMoney(object):
    def __init__(self, conn):
        self.conn = conn

    def transfer(self, tr_acct, re_acct, money):
        try:
            self.check_acct_valid(tr_acct)
            self.check_acct_valid(re_acct)
            self.check_enough_money(tr_acct,money)
            self.reduce_money(tr_acct,money)
            self.add_money(re_acct,money)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def check_acct_valid(self, acct):
        cursor = self.conn.cursor()
        try:
            sql = "select * from account where acct_id = %s" % acct
            cursor.execute(sql)
            print "check_acct_valid " + sql
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("The account %s is not valid" % acct)
        finally:
            cursor.close()

    def check_enough_money(self, acct, money):
        cursor = self.conn.cursor()
        try:
            sql = "select money from account where acct_id = %s and money >= %d" % (acct, money)
            cursor.execute(sql)
            print "check_enough_money " +sql
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("The account %s does not have enough money: $%d" % (acct, money))
        finally:
            cursor.close()

    def add_money(self, acct, money):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money = money + %d where acct_id = %s" % (money, acct)
            cursor.execute(sql)
            print "transfer_money " + sql
            if cursor.rowcount != 1:
                raise Exception("Tansfer Error")
        finally:
            cursor.close()

    def reduce_money(self, acct, money):
        money = -money
        self.add_money(acct, money)


if __name__ == '__main__':
    transfer_acct = sys.argv[1]
    receive_acct = sys.argv[2]
    money = int(sys.argv[3])
    # pay attention to the data type

    conn = pymysql.connect(
        host = '127.0.0.1',
        port = 3306,
        user = 'root',
        passwd = 'zyh123',
        db = 'bank',
        charset = 'utf8'
    )

    transfer_money = TransferMoney(conn)
    try:
        transfer_money.transfer(transfer_acct, receive_acct, money)
    except Exception as e:
        print "Error: " + str(e)
    finally:
        conn.close()