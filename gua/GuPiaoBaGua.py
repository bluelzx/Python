# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 13:50:41 2015

@author: gong
"""
import traceback
import tushare as ts
from Gua import Gua
from GUACI_64 import GUACI_64


import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import metrics
from sklearn.cross_validation import train_test_split


class GuPiaoBaGua(Gua):
    @staticmethod
    def get_state(data):
        d = data['bianyao_guaci'][9]
        if d == u'吉':
            return 1
        if d == u'平':
            return 0
        if d == u'凶':
            return -1
            
    @staticmethod
    def loaddata(stockid):
        try:
            sotck_data = ts.get_hist_data(str(stockid))
            
            p_yao = lambda x,name: 1 if x['close'] > x[name] else 0
            v_yao = lambda x,name: 1 if x['volume'] > x[name] else 0
            sotck_data['yao_1'] = sotck_data.apply(lambda row: p_yao(row,'ma5'), axis=1)
            sotck_data['yao_2'] = sotck_data.apply(lambda row: p_yao(row,'ma10'), axis=1)
            sotck_data['yao_3'] = sotck_data.apply(lambda row: p_yao(row,'ma20'), axis=1)
            sotck_data['yao_4'] = sotck_data.apply(lambda row: v_yao(row,'v_ma5'), axis=1)
            sotck_data['yao_5'] = sotck_data.apply(lambda row: v_yao(row,'v_ma10'), axis=1)
            sotck_data['yao_6'] = sotck_data.apply(lambda row: v_yao(row,'v_ma20'), axis=1)
            
            '''
            sotck_data['gua_code'] = sotck_data.apply(lambda row:[row['yao_6'],row['yao_5'],row['yao_4'],row['yao_3'],row['yao_2'],row['yao_1']], axis=1)
            sotck_data['gua'] = sotck_data.apply(lambda row: Gua.get_64gua_by_code(row['gua_code']), axis=1)
            
            bianyao = lambda x:6 if int(x['close']*100) % 6 == 0 else int(x['close']*100) % 6
            sotck_data['bianyao'] =   sotck_data.apply(lambda row:bianyao(row), axis=1) 
            
            ben_guaci = lambda x: list(GUACI_64.get_guaci(x['gua'])[u'邵雍解'])[0]
            bianyao_guaci = lambda x: list(GUACI_64.get_guaci(x['gua'])[unicode(x['bianyao'])+u'爻邵雍解'])[0]
            sotck_data['ben_guaci'] = sotck_data.apply(lambda row: ben_guaci(row), axis=1)
            sotck_data['bianyao_guaci'] = sotck_data.apply(lambda row: bianyao_guaci(row), axis=1)
            sotck_data['state'] = sotck_data.apply(lambda row: GuPiaoBaGua.get_state(row), axis=1)
            #return sotck_data[['close','state','gua','ben_guaci','bianyao','bianyao_guaci']]
            '''
            #print sotck_data.head
            
            sotck_data.sort_index(axis=0,ascending=False)
            #sotck_data.sort(columns = ,ascending=True)
            sotck_data['diff'] = sotck_data['close'].diff()
            sotck_data['updown'] = sotck_data.apply(lambda x:1 if x['diff'] >0 else 0,axis=1)
            #sotck_data['diff'] = sotck_data['diff'].shift(-1)
            sotck_data[['updown','yao_1','yao_2','yao_3','yao_4','yao_5','yao_6']]
        except Exception,e:
            traceback.print_exc()
            print e


if __name__ == '__main__':
    #print GuPiaoBaGua.get_state(u'北宋易学家邵雍解 平： 得此爻')
    GuPiaoBaGua.loaddata('002385')#.to_excel('/Users/gong/Documents/002385.xlsx')