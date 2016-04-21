# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 21:54:34 2015

@author: gong

这是用来计算 会元运世的程序
"""
from Gua import Gua
import traceback
from GUACI_64 import GUACI_64
from pandas import DataFrame

class HUI_YUAN_YUN_SHI(object):
    XIANTIAN_60_PEIGUATU = [u'复',u'颐',u'屯',u'益',u'震',u'噬嗑',u'随',u'无妄',
                         u'明夷',u'贲',u'既济',u'家人',u'丰',u'革',u'同人',u'临',
                         u'损',u'节',u'中孚',u'归妹',u'睽',u'兑',u'履',u'泰',u'大畜',
                         u'需',u'小畜',u'大壮',u'大有',u'夬',u'姤',u'大过',u'鼎',u'恒',
                         u'巽',u'井',u'蛊',u'升',u'讼',u'困',u'未济',u'解',u'涣',u'蒙',
                         u'师',u'遁',u'咸',u'旅',u'小过',u'渐',u'蹇',u'艮',u'谦',u'否',
                         u'萃',u'晋',u'豫',u'观',u'比',u'剥']
                        
    HUI = [
    {u'子':[u'复',u'颐',u'屯',u'益',u'震']},
    {u'丑':[u'噬嗑',u'随',u'无妄',u'明夷',u'贲']},
    {u'寅':[u'既济',u'家人',u'丰',u'革',u'同人']},
    {u'卯':[u'临',u'损',u'节',u'中孚',u'归妹']},
    {u'辰':[u'睽',u'兑',u'履',u'泰',u'大畜']},
    {u'巳':[u'需',u'小畜',u'大壮',u'大有',u'夬']},
    {u'午':[u'姤',u'大过',u'鼎',u'恒',u'巽']},
    {u'未':[u'井',u'蛊',u'升',u'讼',u'困']},
    {u'申':[u'未济',u'解',u'涣',u'蒙',u'师']},
    {u'酉':[u'遁',u'咸',u'旅',u'小过',u'渐']},
    {u'戌':[u'蹇',u'艮',u'谦',u'否',u'萃']},
    {u'亥':[u'晋',u'豫',u'观',u'比',u'剥']}]
    
    @staticmethod
    def year_index(year):
        try:
            index = None
            if year > 0:
                index = 67017+year
            else:
                index = 67018+year
            return index
        except Exception,e:
            traceback.print_exc()
            print e
    
    #会
    @staticmethod
    def Hui(year):
        try:
            index = HUI_YUAN_YUN_SHI.year_index(year)
            hui = index/10800
            remain = index % 10800
            if remain == 0:
                remain = 10800
            else:
                hui += 1
            return hui,remain
        except Exception,e:
            traceback.print_exc()
            print e
    
    #运
    @staticmethod
    def Yun(year):
        try:
            hui,hui_remain = HUI_YUAN_YUN_SHI.Hui(year)
            yun = hui_remain/360
            remain = hui_remain % 360
            if remain == 0:
                remain = 360
            else:
                yun += 1
            return yun,remain
        except Exception,e:
            traceback.print_exc()
            print e
    
    #世
    @staticmethod
    def Shi(year):
        try:
            yun,yun_remain = HUI_YUAN_YUN_SHI.Yun(year)
            shi = yun_remain/30
            remain = yun_remain % 30
            if remain == 0:
                remain = 30
            else:
                shi += 1
            return shi,remain
        except Exception,e:
            traceback.print_exc()
            print e
     
    #本年对应的卦     
    @staticmethod
    def gua(year):
        try:
            hui,hui_remain = HUI_YUAN_YUN_SHI.Hui(year)
            yun,yun_remain = HUI_YUAN_YUN_SHI.Yun(year)
            
            guas = HUI_YUAN_YUN_SHI.HUI[hui-1]
      
            values = guas[guas.keys()[0]]
            
            yun_tmp = yun % 6
            if yun_tmp == 0:
                yun_tmp = 6
                return Gua.get_64gua_fullname(values[yun/6-1]),yun_tmp
            else:
                return Gua.get_64gua_fullname(values[yun/6]),yun_tmp

        except Exception,e:
            traceback.print_exc()
            print e
    
    #运卦
    @staticmethod
    def yungua(year):
        try:
            gua,gua_remain = HUI_YUAN_YUN_SHI.gua(year)
            return Gua.biangua(gua,gua_remain)

        except Exception,e:
            traceback.print_exc()
            print e
    #世卦
    @staticmethod
    def shigua(year):
        try:
            gua = HUI_YUAN_YUN_SHI.yungua(year)
            shi = HUI_YUAN_YUN_SHI.Shi(year)[0]
            return Gua.biangua(gua,(shi+1)/2)

        except Exception,e:
            traceback.print_exc()
            print e
    #年卦
    @staticmethod
    def niangua(year):
        try:
            gua = HUI_YUAN_YUN_SHI.shigua(year)
            value = 0
            for i,v in enumerate(HUI_YUAN_YUN_SHI.XIANTIAN_60_PEIGUATU):
                if v in gua:
                    value = i+1
                    break
            
            shi,shi_remain = HUI_YUAN_YUN_SHI.Shi(year)
            value = value -1 + shi_remain
            if shi % 2 == 0:
                value += 30
            tmp = value % 60
            if tmp == 0:
                tmp = 60
            
            return Gua.get_64gua_fullname(HUI_YUAN_YUN_SHI.XIANTIAN_60_PEIGUATU[tmp-1])

        except Exception,e:
            traceback.print_exc()
            print e
    
    #年
    @staticmethod
    def Nian(year):
        try:
           return HUI_YUAN_YUN_SHI.Shi(year)[1]
        except Exception,e:
            traceback.print_exc()
            print e
    
    #返回所有结果     
    @staticmethod
    def total_result(year):
        try:
            result = [year]
            result.append(HUI_YUAN_YUN_SHI.Hui(year)[0])
            result.append(HUI_YUAN_YUN_SHI.Yun(year)[0])
            result.append(HUI_YUAN_YUN_SHI.Shi(year)[0])
            result.append(HUI_YUAN_YUN_SHI.Nian(year))
            result.append(HUI_YUAN_YUN_SHI.yungua(year))
            result.append(HUI_YUAN_YUN_SHI.shigua(year))
            result.append(HUI_YUAN_YUN_SHI.niangua(year))
            '''
            print u'会:'+str(HUI_YUAN_YUN_SHI.Hui(year)[0])
            print u'运:'+str(HUI_YUAN_YUN_SHI.Yun(year)[0])
            print u'世:'+str(HUI_YUAN_YUN_SHI.Shi(year)[0])
            print u'年:'+str(HUI_YUAN_YUN_SHI.Nian(year))
            
            print u'运卦:'+HUI_YUAN_YUN_SHI.yungua(year)
            print u'世卦:'+HUI_YUAN_YUN_SHI.shigua(year)
            print u'年卦:'+HUI_YUAN_YUN_SHI.niangua(year)
            '''
            return result
        except Exception,e:
            traceback.print_exc()
            print e
            
if __name__ == '__main__':
    tmp = []
    for i in range(-770,0):
        tmp.append(HUI_YUAN_YUN_SHI.total_result(i))
    
    for i in range(1,3000):
        tmp.append(HUI_YUAN_YUN_SHI.total_result(i))
    
    result = []
    columns = (u'年数',u'会',u'运',u'世',u'年',u'运卦',u'运卦邵雍解',u'世卦',u'世卦邵雍解',u'年卦',u'年卦邵雍解')
    for year_data in tmp:
        try:
            temp = []
            temp.append(year_data[0])
            temp.append(year_data[1])
            temp.append(year_data[2])
            temp.append(year_data[3])
            temp.append(year_data[4])
            temp.append(year_data[5])
            temp.append(list(GUACI_64.get_guaci(year_data[5])[u'邵雍解'])[0])
            temp.append(year_data[6])
            temp.append(list(GUACI_64.get_guaci(year_data[6])[u'邵雍解'])[0])
            temp.append(year_data[7])
            temp.append(list(GUACI_64.get_guaci(year_data[7])[u'邵雍解'])[0])
            result.append(temp)
        except Exception,e:
            print e
            traceback.print_exc()
            break
        
    dataframe = DataFrame(result,columns = columns)
    dataframe.to_excel(GUACI_64.__PATH__+u'会运世年.xlsx')