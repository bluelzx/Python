# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 15:07:51 2015

@author: gong
"""
from pandas import DataFrame
class zhaiquan(object):
    def __init__(self,start_month,time_length,weiyue_rate,money,fuwufei = 0.005):
        self.start_month = start_month
        self.time_length = time_length
        self.weiyue_rate = weiyue_rate
        self.money = money
        self.fuwufei = fuwufei
    
    
    def get_money_by_month(self,month):
        if month <= self.start_month:
            return 0
        if month > self.start_month+self.time_length:
            return 0
        benjin = float(self.money)/float(self.time_length)
        lixi = self.money*self.fuwufei*self.time_length
        result = 0
        if month - self.start_month == 1:
            result = benjin+lixi
        else:
            result = benjin
        result *= self.weiyue_rate
        return result
 

def buy_zhaiquan(month,money,weiyue_rate,fuwufei = 0.005):
    if month <= 6:
        return zhaiquan(month,6,weiyue_rate,money,fuwufei)
    elif month <=9 and month >= 7:
        return zhaiquan(month,3,weiyue_rate,money,fuwufei)
    elif month >= 10 and month <= 12:
        return zhaiquan(month,12,weiyue_rate,money,fuwufei)
    return None

def each_month_huankuan(month):
    moneys = [0.00,0.00,954.80,0.00,0.00,954.80,0.00,0.00,954.80,0.00,0.00,954.80,6184.93,6184.93,6184.93,6184.93,6184.93,6184.93,6184.93,6184.93,6184.93,6184.93,6184.93,6184.93] 
    return moneys[month - 1]
    
def Main(weiyue_rate,fuwufei = 0.005):
    zhaiquans = []
    zhaiquans.append(zhaiquan(0,3,weiyue_rate,16832.00,fuwufei))
    zhaiquans.append(zhaiquan(0,6,weiyue_rate,7544.00,fuwufei))
    zhaiquans.append(zhaiquan(0,12,weiyue_rate,32624.00,fuwufei))
    zhaiquans.append(zhaiquan(0,24,weiyue_rate,23000.00,fuwufei))
    remains = 0
    for i in range(1,25):
        tmp_money = 0
        for zq in zhaiquans:
            tmp_money += zq.get_money_by_month(i)
        tmp_money = tmp_money - each_month_huankuan(i)
        print i,tmp_money
        new_zq = buy_zhaiquan(i,tmp_money,weiyue_rate,fuwufei)
        if new_zq != None:
            zhaiquans.append(new_zq)
        else:
            remains += tmp_money
    print remains
    if remains < 0:
        remains = 0
    return (remains-9600.00)/9600.00

if __name__ == '__main__':
    print Main(0.98)
    '''
    result = []
    for i in range(0,500):
       tmp =  Main(1.0-float(i)/float(10000))
       result.append([float(i)/float(100),tmp])
    dataframe = DataFrame(result,columns = (u'违约率',u'次级债收益率'))
    dataframe.to_excel('/Users/gong/Documents/mutou.xlsx')
    '''