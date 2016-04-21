# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 10:51:41 2016

@author: gong

@description: 加载情感字典，然后提供查询接口的类
"""
import pandas as pd
def build_dict(line,word_dict):
    word_dict[line[u'词语']] =[int(line[u'强度']),int(line[u'极性'])]
    
class Sentiment(object):
    #是否加载数据
    __DATA_LOADED__ = False
    word_dict = {}
    
    @staticmethod
    def __LOAD_DATA__():
        if Sentiment.__DATA_LOADED__ == False:
            '''加载数据'''
            dataframe = pd.read_excel(u'情感词汇本体.xlsx')
            word_list = dataframe[[u'词语',u'强度',u'极性']]
            word_list.apply(lambda row: build_dict(row,Sentiment.word_dict), axis=1)
            Sentiment.__DATA_LOADED__ = True

    @staticmethod
    def get_sentiment(word):
        '''返回一个向量，第一列是贬义，第二列是褒义'''
        if Sentiment.__DATA_LOADED__ == False:
            Sentiment.__LOAD_DATA__()
        value = Sentiment.word_dict.get(word,[0,0])
        if value[1] == 0:
            return (0,value[0],0)
        if value[1] == 1:
            return (0,0,value[0])
        if value[1] == 2:
            return (value[0],0,0)
        
        
if __name__ == '__main__':
    print Sentiment.get_sentiment(u'冰炭不相容')
    
    

