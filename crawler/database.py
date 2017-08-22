import pymysql

class Database :
    conn = None

    def __init__ (self, ip, user, passwd, database) :
        self.conn = pymysql.connect(ip, user, passwd, database)

    def __del__ (self) :
        self.conn.close()
