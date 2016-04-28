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


def grads(X,epslon=0.0001):
    n = len(X)
    Y = map(lambda i:0 if i == 0 else (X[i]-X[i-1])*100/X[i-1],[i for i in range(n)])
    Z = map(lambda i:0 if i == 0 else Y[i]-Y[i-1],[i for i in range(n)])
    plt.plot(Y)
    plt.plot(Z)
    plt.plot(X)
    max_min = []
    for i in xrange(1,n):
        if abs(X[i]-X[i-1])/X[i-1] <= epslon:
            max_min.append(i)
    return float(max_min[-1]-max_min[0])/len(max_min),len(max_min)
    #

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
    print grads(quad_smooth(X,50))
if __name__ == '__main__':
    history_date('000001')
    


    
