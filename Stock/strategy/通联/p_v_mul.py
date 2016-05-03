# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 10:21:23 2016

@author: gong
"""

start = '2014-01-01'                       # 回测起始时间
end = '2015-01-01'                         # 回测结束时间
benchmark = 'HS300'                        # 策略参考标准
#universe = ['000001.XSHE', '600000.XSHG']  # 证券池，支持股票和基金
capital_base = 100000                      # 起始资金
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟
universe = set_universe('HS300')
def initialize(account):                   # 初始化虚拟账户状态
    pass

def handle_data(account):                  # 每个交易日的买入卖出指令
    price = account.get_attribute_history('closePrice', 20)
    turnover = account.get_attribute_history('turnoverVol', 20)
    for stk in account.universe:
        p_ma5 = price[stk][-5:].mean()     # 计算股票过去5天收盘平均值
        p_ma20 = price[stk][:].mean()      # 计算股票过去20天收盘平均值
        
        v_ma5 = turnover[stk][-5:].mean()     # 计算股票过去5天成交量平均值
        v_ma20 = turnover[stk][:].mean()      # 计算股票过去20天成交量平均值
        
        p_1 = price[stk][-1:].mean()
        v_1 = turnover[stk][-1:].mean()
        if v_ma5*p_ma5 > p_ma20*v_ma20:
            order(stk, 10000)
        else:
            order_to(stk,0)
        
    return
