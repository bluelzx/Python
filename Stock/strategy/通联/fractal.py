# -*- coding: utf-8 -*-
"""
Created on Tue May  3 22:38:26 2016

@author: gong

@description:这是计算是否存在回形的程序
fractal
"""
import re
import pandas as pd
#先把序列编码
def sequence_code(sequence):
    mas = [5,10,30]
    tmp = map(lambda ma:pd.rolling_mean(sequence, mas[0])-sequence,mas)
    tmp = map(lambda r:r.apply(lambda x:1 if x > 0 else 0),tmp)
    return tmp[0]+tmp[1]*2+tmp[2]*4
    

#发现最接近的字串
def find_most_similar_seq(sequence,length=5):
    sub_seq = sequence[-length:]
    seq_str = ''.join(map(lambda x:str(x),sequence))
    sub_str = ''.join(map(lambda x:str(x),sub_seq))
    n = len(seq_str)
    index = 0
    results = set()
    while index < n:
        tmp = seq_str.find(sub_str,index)
        if tmp < 0:
            break
        index = tmp
        if index+length < n:
            results.add(seq_str[index+length])
            index += 1
        else:
            break
    tmp = map(lambda x:(int(x)% 2,(int(x) >> 1) % 2,(int(x) >> 2)%2),list(results))
    print tmp
        
if __name__ == '__main__':
    df = pd.read_excel('000001.xlsx')
    df = df.sort_index(by=['date'],ascending=True)
    X = df['close']
    sequence_code(X)
    print find_most_similar_seq([1,2,4,7,1,2,4,5,1,2,4],3)
    
