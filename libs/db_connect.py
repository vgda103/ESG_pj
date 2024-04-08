# DB Connection

import configparser
import pymysql

# config open
config = configparser.ConfigParser()
config.read('../config/config.ini')

class DBConnection:
    def __init__(self):
        self._conn = pymysql.connect(
            # 운영 DB
            # host = config['DB_ESG']['HOST'],
            # port = 3306,
            # user = config['DB_ESG']['USER'],
            # password = config['DB_ESG']['PASSWD'],
            # db = config['DB_ESG']['DB_NAME'],

            # Local DB
            host = config['DB_TEST']['HOST'],
            port = 3306,
            user = config['DB_TEST']['USER'],
            password = config['DB_TEST']['PASSWD'],
            db = config['DB_TEST']['DB_NAME'],

            #autocommit = True,           
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor # DB조회시 컬럼명을 동시에 보여줌
        )
        self._cursor = self._conn.cursor()
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn
    
    @property
    def cursor(self):
        return self._cursor
    
    def rollback(self, rollback=True):
        if rollback:
            self.rollback()
        self.connection.close()
    
    def commit(self):
        self.connection.commit()
    
    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()
    
    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def executemany(self, sql, params=None):
        self.cursor.executemany(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()
    
    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
    
    def rows(self):
        return self.cursor.rowcount

    