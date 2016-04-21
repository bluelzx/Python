# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 16:20:04 2016

@author: gong

@description: 这是从股票数据中计算出状态的程序
"""
import os
import traceback
import pandas as pd
import tushare as ts

class StockState(object):
    
    @staticmethod
    def loaddata(stockid):
        try:
            sotck_data = ts.get_hist_data(str(stockid))
            price_index = lambda x,name: 1 if x['close'] > x[name] else 0
            volume_index = lambda x,name: 1 if x['volume'] > x[name] else 0
            
            
            sotck_data['p_1'] = sotck_data.apply(lambda row: price_index(row,'ma5'), axis=1)
            sotck_data['p_2'] = sotck_data.apply(lambda row: price_index(row,'ma10'), axis=1)
            sotck_data['p_3'] = sotck_data.apply(lambda row: price_index(row,'ma20'), axis=1)
            
            sotck_data['v_1'] = sotck_data.apply(lambda row: volume_index(row,'v_ma5'), axis=1)
            sotck_data['v_2'] = sotck_data.apply(lambda row: volume_index(row,'v_ma10'), axis=1)
            sotck_data['v_3'] = sotck_data.apply(lambda row: volume_index(row,'v_ma20'), axis=1)
            
            sotck_data.sort_index(axis=0,ascending=False)
            sotck_data['diff'] = -sotck_data['close'].diff()
            sotck_data['updown'] = sotck_data.apply(lambda x:1 if x['diff'] >= 0 else -1,axis=1)
            sotck_data['value'] = sotck_data['p_1']+2*sotck_data['p_2']+4*sotck_data['p_3']+8*sotck_data['v_1']+16*sotck_data['v_2']+32*sotck_data['v_3']
        
            return sotck_data[['updown','value']]
        except Exception,e:
            traceback.print_exc()
            print e 
    
    
    @staticmethod
    def get_concept(path='stock_concept.csv'):
        try:
            dataframe = None
            if os.path.exists(path):
                dataframe = pd.read_csv(path)
            else:
                dataframe = ts.get_concept_classified()
                dataframe.to_csv(path,encoding="utf8")
            return dataframe
        except Exception,e:
            print e
            traceback.print_exc()
    #@staticmethod
    
    @staticmethod
    def gen_same_concept():
        try:
            dataframe = StockState.get_concept()
            group_data = dataframe.groupby('c_name')
        except Exception,e:
            print e
            traceback.print_exc()
            

if __name__ == '__main__':
    d = StockState.loaddata('600036')
    #print d,d.shift(-1)
    c = zip(d.values,d.shift(-1).values)
    merged = pd.DataFrame(c, index=d.index)
    print merged
    
    