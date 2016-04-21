# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 15:42:07 2015

"""
import tushare as ts
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn import metrics
from sklearn.cross_validation import train_test_split
#加载数据
def load_data(stockid = '600036'):
    sotck_data = ts.get_hist_data(str(stockid))
            
    p_yao = lambda x,name: 1 if x['close'] > x[name] else 0
    v_yao = lambda x,name: 1 if x['volume'] > x[name] else 0
    sotck_data['yao_1'] = sotck_data.apply(lambda row: p_yao(row,'ma5'), axis=1)
    sotck_data['yao_2'] = sotck_data.apply(lambda row: p_yao(row,'ma10'), axis=1)
    sotck_data['yao_3'] = sotck_data.apply(lambda row: p_yao(row,'ma20'), axis=1)
    sotck_data['yao_4'] = sotck_data.apply(lambda row: v_yao(row,'v_ma5'), axis=1)
    sotck_data['yao_5'] = sotck_data.apply(lambda row: v_yao(row,'v_ma10'), axis=1)
    sotck_data['yao_6'] = sotck_data.apply(lambda row: v_yao(row,'v_ma20'), axis=1)
            
            
        
    sotck_data['diff'] = sotck_data['close'].diff()
    sotck_data['updown'] = sotck_data.apply(lambda x:1 if x['diff'] >0 else 0,axis=1)
    sotck_data =  sotck_data.dropna()
    return sotck_data[['diff','close','yao_1','yao_2','yao_3','yao_4','yao_5','yao_6']]

#评价
def evalurate(true,pred):
    mae = metrics.mean_absolute_error(true, pred)
    mse = metrics.mean_squared_error(true, pred)
    rmse = np.sqrt(metrics.mean_squared_error(true, pred))
    r_2 = 1 - ((pred - true)**2).sum() / ((true - true.mean())**2).sum() 
    return 'MAE: %s, MSE: %s, RMSE: %s, R2: %s.' % (mae,mse,rmse,r_2)


def train_test(df,model,name):
    y = df['diff']
    x = df[['close','yao_1','yao_2','yao_3','yao_4','yao_5','yao_6']]
    
    #分割数据
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1,test_size = 0.2)
    model.fit(x_train,y_train)
    pred = model.predict(x_test)
    print 'The result of Model %s:' % name
    print evalurate(y_test,pred)

if __name__ == '__main__':
    df = load_data()
    
    print 'Now processing OLS...' 
    ols = linear_model.LinearRegression()
    train_test(df,ols,'OLS')
    
    print '\nNow processing Ridge...' 
    ridge = linear_model.Ridge (alpha = 0.5)
    train_test(df,ridge,'Ridge')
    
    
    print '\nNow processing SVR...' 
    from sklearn import svm
    svr = svm.SVR()
    train_test(df,svr,'SVR')
    
    