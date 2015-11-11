# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:42:09 2015

@author: gong

@description: 这是用来连接数据库的连接池
"""
import MySQLdb
import Singleton
from config import configs
from DBUtils.PooledDB import PooledDB

class DBManager(Singleton):
  
    def __init__(self):  
        connKwargs = {'host':configs['localhost'], 'user':configs['root'], 'passwd':configs['root'], 'db':configs['Robot'], 'charset':"utf8"}  
        self._pool = PooledDB(MySQLdb, mincached=0, maxcached=10, maxshared=10, maxusage=10000, **connKwargs)  
  
    def get_connection(self):  
        return self._pool.connection()


if __name__ == '__main__':
    db = DBManager()
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('select * from transaction')
    cursor.close()
    conn.close()