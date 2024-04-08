# -*- config: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from libs.db_connect import DBConnection

dbconn = DBConnection()

class DBClass:
    def __init__(self):
        pass
    
    def select_one(self, sql, args=None):
        dbconn.execute(sql, args)
        result = dbconn.fetchone()
        return result

    # 클래스 내부에서 사용 시 args의 self는 필요 없음
    # def select_one_in(sql, args=None):
    #     dbconn.execute(sql, args)
    #     result = dbconn.fetchone()
    #     return result
    
    def select_all(self, sql, args=None):
        dbconn.execute(sql, args)
        result = dbconn.fetchall()
        return result
    
    def save_all(self, sql, args=None):        
        try:
            dbconn.executemany(sql, args)
            dbconn.commit() # commit()
            
            return 1
        except:
            dbconn.rollback() # rollback() & close()
            return 0
    
    def save_all_close(self, sql, args=None):
        try:
            dbconn.executemany(sql, args)
            dbconn.close() # commit() & close()
            return 1
        except:
            dbconn.rollback()
            return 0
    
    def db_execute(self, sql):
        dbconn.execute(sql)
        dbconn.commit()
    
    def db_commit(self):
        dbconn.commit()

    def db_close(self):
        dbconn.close()

