# MySQLに接続するmysql.connectorのラッパークラス
class MySQLConn(object):
    
    def __init__(self, account):
        self.account = account
    
    # with構文を使ってMySQLに接続を行う。
    def __enter__(self):
        import mysql.connector    

        self.connect = mysql.connector.connect(
            db      = self.account["db"],
            host    = self.account["host"],
            user    = self.account["user"],
            passwd  = self.account["passwd"],
            charset = "utf8")
        return self.connect
    
    
    def __exit__(self, exception_type, exception_value, traceback):
        self.connect.close()