# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 09:14:44 2016

@author: gong

@description:这是用来将风险等级分类的程序
"""
import pandas as pd
from tgrocery import Grocery
import jieba

class Classify(object):
    __MODEL_LOADED__ = False
    __FILE_PATH__ = u'企业风险等级（201602）.xls'
    __MODEL_PATH__ = 'Classify'
    __MODEL__ = None
    
    #加载模型
    @staticmethod
    def __load_model__():
        if not Classify.__MODEL_LOADED__:
            Classify.__MODEL_LOADED__ = True
            Classify.__train__model__()
        else:
            if Classify.__MODEL__:
                Classify.__MODEL__ = Grocery('Classify')
                Classify.__MODEL__.load()
                
    #训练模型
    @staticmethod
    def __train__model__():
        dataframe = pd.read_excel(Classify.__FILE_PATH__)
        data = dataframe[[u'类型',	u'释义']]
        train_data = [(x[0],x[1]) for x in data.values]
        
        grocery = Grocery('Classify')
        
        grocery.train(train_data)
        grocery.save()
        Classify.__MODEL__ = grocery
    
    @staticmethod
    def __predict__(word):
        words = jieba.cut(word)
        for w in words:
            if w in [u'年报',u'年度报告']:
                return u'未公示年报'
            if w in [u'行政']:
                return u'行政处罚'
            if w in [u'弄虚作假']:
                return u'虚假公示信息'
            if w in [u'拖欠',u'工资']:
                return u'欠薪'
            if w in [u'费用',u'费',u'缴纳']:
                return u'欠费'
            if w in [u'营业执照',u'工商登记']:
                return u'无照经营'
            if w in [u'欺诈',u'注册资本']:
                return u'虚假企业'
            if w in [u'强制']:
                return u'吊销'
            if w in [u'注销']:
                return u'注销'
            if w in [u'合同']:
                return u'合同欺诈'
            if w in [u'税款',u'税收',u'发票']:
                return u'合同欺诈'
            if w in [u'假冒伪劣',u'消费者']:
                return u'质量失信'
            if w in [u'信用']:
                return u'信用丧失'
            if w in [u'准备']:
                return u'拟吊销'
            #return u'经营异常'
                
    
    @staticmethod
    def predict(word):
        Classify.__load_model__()
        result = Classify.__MODEL__.predict(word)
        result_2 = Classify.__predict__(word)
        if result_2:
            return result_2
        return result
        
        
    @staticmethod
    def get_risk_score(words):
        word = Classify.predict(words)
        if word in [u'行政处罚',u'经营异常',u'未公示年报']:
            return 1
        if word in [u'虚假公示信息',u'欠薪',u'欠费']:
            return 2
        if word in [u'查无下落',u'不良司法',u'拟吊销',u'信用丧失']:
            return 3
        if word in [u'质量失信',u'税收违法',u'合同欺诈',u'注销']:
            return 4
        if word in [u'吊销',u'虚假企业']:
            return 5



if __name__ == '__main__':
    print Classify.get_risk_score(u'在全国企业信用信息公示系统-经营异常中公示，但未披露经营异常的详细原因')
