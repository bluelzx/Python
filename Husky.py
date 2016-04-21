# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:07:36 2015

@author: gong
"""
import time
import traceback
import pandas as pd
#from DBManager import DBManager
from Finance_Husky import Finance_Husky
from Hushen300_Husky import Hushen300_Husky
#from Transaction_Husky import Transaction_Husky

class Husky(object):
    def __init__(self):
        hs300 = Hushen300_Husky()
        #获得所有的沪深300
        self.stocks = hs300.get_stocks()
        #self.transaction_huskies = map(lambda stockid:Transaction_Husky(stockid),self.stocks)
        
        if len(self.stocks) == 300:
            #self.transaction_huskies = map(lambda stockid:Transaction_Husky(stockid),self.stocks)
            self.finance_huskies = map(lambda stockid:Finance_Husky(stockid),self.stocks)
        
        
    #下载历史数据
    def download_history_data(self,path,start_year = 2010):
        try:
            for transaction_husky in self.transaction_huskies:
                print 'Now processing stock: %s ...' % transaction_husky.stockid
                tmp = [(2010,1),(2010,2),(2010,3),(2010,4),
                       (2011,1),(2011,2),(2011,3),(2011,4),
                       (2012,1),(2012,2),(2012,3),(2012,4),
                       (2013,1),(2013,2),(2014,3),(2013,4),
                       (2014,1),(2014,2),(2014,3),(2014,4),
                       (2015,1),(2015,2),(2015,3)]
                #dataframs = map(lambda x:transaction_husky.get_quarter_data(x[0],x[1]),tmp)
                datafram = pd.concat(map(lambda x:transaction_husky.get_quarter_data(x[0],x[1]),tmp),ignore_index = True)
                name = path+'/'+transaction_husky.stockid+'.xlsx'            
                datafram.sort_values(by='date').to_excel(name, sheet_name='Sheet1')
                time.sleep(5)
        except Exception,e:
            traceback.print_exc() 
            print 'Husky Dowload History Data Error: %s !' % e
    
    def download_finance_data(self,path):
        try:
            for i,finance_husky in enumerate(self.finance_huskies):
                if i <= 232:
                    continue
                print 'Now processing stock: %s...' % finance_husky.stockid
                name = path+'/'+ finance_husky.stockid+'.xlsx'
                finance_husky.get_finance().to_excel(name,sheet_name='Sheet1')
                time.sleep(5)
        except Exception,e:
            traceback.print_exc()
            print 'Husky Download Finance Data Error: %s !' % e


if __name__ == '__main__':
    dog = Husky()
    dog.download_finance_data('/Volumes/ELEMENTS/Stock/Finance_Data')