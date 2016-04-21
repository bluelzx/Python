# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 15:12:25 2015

@author: gong
"""
import datetime
import pandas as pd

def loaddata(filename = '/Users/gong/Documents/bids.csv'):
    dataframe = pd.read_csv(filename)
    data = dataframe[['CreationDate','Amount','ParticipationAmount']]
    #data['money'] = data['AmountBorrowed']*data['BorrowerRate']   
    
    #mylambda = lambda x:x[:4]+'-'+str(datetime.datetime(int(x[:4]),int(x[5:7]),int(x[8:10])).strftime("%W"))
    mylambda = lambda x:x['CreationDate'][:10]
    
    data['day'] = data.apply(lambda row: mylambda(row), axis=1)
    tmpdata = data[['day','Amount','ParticipationAmount']]
 
    grouped = tmpdata.groupby('day')
    
    AmountBorrowed = grouped['Amount'].sum()
    money_all = grouped['ParticipationAmount'].sum()
    
    answer = [AmountBorrowed,money_all]
    
    '''
    for r in zip(result.index,result.values):
        answer.append(r)
    '''
    
    pd.DataFrame(answer).T.to_excel('/Users/gong/Documents/ddd.xlsx')
if __name__ == '__main__':
    loaddata()