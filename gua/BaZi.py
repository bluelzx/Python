# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 18:54:54 2015

@author: gong
"""

import traceback

class BaZi(object):
    __TianGan__ = u'甲,乙,丙,丁,戊,己,庚,辛,壬,癸'
    __DiZhi__ = u'子,丑,寅,卯,辰,巳,午,未,申,酉,戌,亥'
    __ShiZhu__ = u'甲己;甲,乙庚;丙,丙辛;戊,丁壬;庚,戊癸;壬'
    __YueZhu__ = u'甲己;丙寅,乙庚;戊寅,丙辛;庚寅,丁壬;壬寅,戊癸;甲寅'

    #相隔diff个的支干
    @staticmethod
    def __tiangandizhi__(start,diff):
        try:
            diff = ((diff % 60) + 60) % 60
            
            zhis = BaZi.__TianGan__.split(',')
            gans = BaZi.__DiZhi__.split(',')
            zhi_idx = 0
            gan_idx = 0
            
            zhi = start[0]
            gan = start[1]
            for i,v in enumerate(zhis):
                if v == zhi:
                    zhi_idx = i
                    break
            for i,v in enumerate(gans):
                if v == gan:
                    gan_idx = i
                    break
            
            gan_idx = (gan_idx + diff) % 12
            zhi_idx = (zhi_idx + diff)% 10
            return zhis[zhi_idx]+gans[gan_idx]
        except Exception,e:
            traceback.print_exc()
            print e
    
    #天数差
    @staticmethod
    def get_day_diff(a_year,a_month,a_day,b_year,b_month,b_day):
        try:
            result = 1
            if a_year < b_year:
                result =  -1
                a_year,a_month,a_day,b_year,b_month,b_day = b_year,b_month,b_day,a_year,a_month,a_day
                
            leap_year= lambda x: True if (x % 400 == 0 or (x % 100 != 0 and x % 4 == 0)) else False
            
            days  = [31,28,31,30,31,30,31,31,30,31,30,12]
            #b年经过了多少天
            b_days = 0
            
            b_days += sum(days[:b_month-1])
            b_days += b_day
            if leap_year(b_year):
                if b_month >= 3:
                    b_days += 1
            
            #a年经过了多少天
            a_days = 0
            a_days += sum(days[:a_month-1])
            a_days += a_day
            if leap_year(a_year):
                if a_month >= 3:
                    a_days += 1
            
            year_idx= [i for i in range(b_year,a_year)]
            
            temp = 365*(a_year-b_year)+sum(map(lambda x:1 if leap_year(x) else 0,year_idx))
            result = (temp + a_days - b_days)*result
            return result
        except Exception,e:
            traceback.print_exc()
            print e
            
    #获得日柱
    @staticmethod
    def rizhu(year,month,day):
        try:
            daydiff = BaZi.get_day_diff(2015,12,10,year,month,day)*-1
            return BaZi.__tiangandizhi__(u'庚申',daydiff)
        except Exception,e:
            traceback.print_exc()
            print e
            return None
            
            
    #获得时柱
    @staticmethod
    def shizhu(year,month,day,hour):
        try:
            daydiff = BaZi.get_day_diff(2015,12,10,year,month,day)
            rizhu = BaZi.__tiangandizhi__(u'庚申',daydiff)
            rigan = rizhu[0]
            shichen = BaZi.__DiZhi__.split(',')[((hour + 1) % 24) / 2]
            rigans = map(lambda x:x.split(';'),BaZi.__ShiZhu__.split(','))
            for v in rigans:
                if rigan in v[0]:
                    return v[1]+shichen
            return None
        except Exception,e:
            traceback.print_exc()
            print e
            return None  
    
    #计算春分
    @staticmethod
    def __chunfen_time__(year):
        try:
            diff = 365*24*3600+5*3600+48*60+46
            month = 1
            day = 1
            daydiff = BaZi.get_day_diff(2013,2,4,year,month,day)
            if daydiff > 0:
                remain = daydiff*24*3600 % diff -13*60 - 25
                hour = remain/3600
                day = 1+hour/24
                hour = hour % 24
                hour = remain/3600
                day = 1+hour/24
                hour = hour % 24
                
                second = remain % 3600
                minute = second / 60
                second = second - 60*minute
                if day > 31:
                    month += 1
                    day -= 31
                return [year,month,day,hour,minute,second]
            else:
                daydiff *= -1
                remain = daydiff*24*3600 % diff
                remain = diff - remain
                remain += 13*60 + 25
                hour = remain/3600
                day = 1+hour/24
                hour = hour % 24
                
                second = remain % 3600
                minute = second / 60
                second = second - 60*minute
                if day > 31:
                    month += 1
                    day-= 31
                return [year,month,day,hour,minute,second]
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    #计算年柱
    @staticmethod
    def nianzhu(year,month,day,hour):
        try:
            chunfen = BaZi.__chunfen_time__(year)
            before = False
            if chunfen[1] > month:
                before = True
            elif chunfen[1] == month and chunfen[2] > day:
                before = True
            elif chunfen[1] == month and chunfen[1] == day and chunfen[2] > hour:
                before = True
            yeardiff = 2015 - year
            
            if before:
                yeardiff += 1
            return BaZi.__tiangandizhi__(u'乙未',yeardiff*-1)
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    #计算月柱
    @staticmethod
    def yuezhu(year,month,day,hour):
        try:
            nian = BaZi.nianzhu(year,month,day,hour)
            yanyue = None
            yuezhus = map(lambda x:x.split(';'),BaZi.__YueZhu__.split(','))
            for yue in yuezhus:
                if nian[0] in yue[0]:
                    yanyue = yue[1]
                    break
            chunfen = BaZi.__chunfen_time__(year)
            before = False
            if chunfen[1] > month:
                before = True
            elif chunfen[1] == month and chunfen[2] > day:
                before = True
            elif chunfen[1] == month and chunfen[1] == day and chunfen[2] > hour:
                before = True
            
            monthdiff = None
            if before:
                chunfen = BaZi.__chunfen_time__(year-1)
                monthdiff = 12 + month - chunfen[1]
            else:
                monthdiff = month - chunfen[1]
            return BaZi.__tiangandizhi__(yanyue,monthdiff)
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    #获得八字
    @staticmethod
    def bazi(year,month,day,hour):
        try:
            sz = BaZi.shizhu(year,month,day,hour)
            rz = BaZi.rizhu(year,month,day)
            nz = BaZi.nianzhu(year,month,day,hour)
            yz = BaZi.yuezhu(year,month,day,hour)
            return nz,yz,rz,sz
        except Exception,e:
            traceback.print_exc()
            print e
            return None
            
            
if __name__ == '__main__':
    #丁酉（八月）庚午（十三日）丙子（子时）
    '''
    print BaZi.__chunfen_time__(2014)
    print BaZi.shizhu(1711,9,25,23)
    print BaZi.rizhu(1711,9,25)
    print BaZi.nianzhu(1711,9,25,23)
    print BaZi.yuezhu(1711,9,25,23)
    1992,9,29,3
    1991.6.19 中午12点20
    1989.1.18中午12
    '''
    print BaZi.bazi(1992,1,27,0)[0]
    print BaZi.bazi(1992,1,27,0)[1]
    print BaZi.bazi(1992,1,27,0)[2]
    print BaZi.bazi(1992,1,27,0)[3]