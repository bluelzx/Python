# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:07:36 2015

@author: gong
"""
import traceback
from DBManager import DBManager
from Hushen300_Husky import Hushen300_Husky
from Transaction_Husky import Transaction_Husky

class Husky(object):
    def __init__(self):
        hs300 = Hushen300_Husky()
        #获得所有的沪深300
        self.stocks = hs300.get_stocks()
        if len(self.stocks) == 300:
            self.transaction_huskies = map(lambda stockid:Transaction_Husky(stockid),self.stocks)
            self.finance_huskies = map(lambda stockid:Finance_Husky(stockid),self.stocks)
    
    #下载历史数据
    def download_history_data(self,start_year = 2010):
        try:
            
        except Exception,e:
            traceback.print_exc() 
            print 'Husky Dowload History Data Error: %s !' % e
        