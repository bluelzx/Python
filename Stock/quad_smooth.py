# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 13:05:58 2016

@author: gong

@description:一维信号的二次光滑程序

公式：X_hat = (I+delta*D'D)^-1X
"""
import os
import time
import numpy as np
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt

#这是二次光滑的程序
def quad_smooth(x,delta):
    x = np.array(x)
    n = len(x)
    D = []
    for i in xrange(n-1):
        tmp = [0 for j in xrange(n)]
        tmp[i] = -1
        tmp[i+1] = 1
        D.append(tmp)
    D = np.array(D)

    I = []
    for i in xrange(n):
        tmp = [0 for j in xrange(n)]
        tmp[i] = 1
        I.append(tmp)
    
    tmp = np.linalg.inv(np.add(I,delta*np.dot(D.T,D)))
    return np.dot(tmp,x.T)


def draw_pic():
    pass

def get_data(stock_id,date):
    if os.path.exists(stock_id+'_'+date+'.xlsx'):
        df = pd.read_excel(stock_id+'_'+date+'.xlsx')
    else:
        df = ts.get_tick_data(stock_id,date=date)
        df['type'] = df['type'].apply(lambda x:x.decode('utf8','ignore'))
        df.to_excel(stock_id+'_'+date+'.xlsx')
    tmp = df[['time','price']]
    
    tmp = df.sort_index(by=['time'],ascending=True)
    X = tmp['price'].values
    #plt.figure()
    plt.plot(X)
    
    plt.plot(quad_smooth(X,50))
    
#历史行情
def history_date(stock_id):
    if os.path.exists(stock_id+'.xlsx'):
        df = pd.read_excel(stock_id+'.xlsx')
    else:
        df = ts.get_hist_data(stock_id)
        df.to_excel(stock_id+'.xlsx')
    df = df.sort_index(by=['date'],ascending=True)
    X = df['close'].values
    #Y = df['date'].apply(lambda x:time.strptime(x,'%Y-%m-%d')).values
    #plt.plot(X)
    plt.plot(quad_smooth(X,10))
if __name__ == '__main__':
    history_date('000001')
    


    
