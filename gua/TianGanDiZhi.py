# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 18:05:07 2015

@author: gong
"""
import traceback
class TianGanDizhi(object):
    __TianGan__ = u'甲木;乙木;丙火;丁火;戊土;己土;庚金;辛金;壬水;癸水'
    __DiZhi__ = u'子水;丑土;寅木;卯木;辰土;巳火;午火;未土;申金;酉金;戌土;亥水'
    
    #获得天干的五行
    @staticmethod
    def get_wuxing_of_tiangan(tiangan):
        try:
            if not isinstance(tiangan,unicode) or len(tiangan) != 1 or tiangan not in TianGanDizhi.__TianGan__:
                return None
            Tiangans = TianGanDizhi.__TianGan__.split(';')
            for tg in Tiangans:
                if tg[0] == tiangan:
                    return tg[1]
            return None  
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    
    #获得地支的五行
    @staticmethod
    def get_wuxing_of_dizhi(dizhi):
        try:
            if not isinstance(dizhi,unicode) or len(dizhi) != 1 or dizhi not in TianGanDizhi.__DiZhi__:
                return None
            Dizhis = TianGanDizhi.__DiZhi__.split(';')
            for dz in Dizhis:
                if dz[0] == dizhi:
                    return dz[1]
            return None  
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    #获得五行的天干
    @staticmethod
    def get_tiangan_of_wuxing(wuxing):
        try:
            if not isinstance(wuxing,unicode) or len(wuxing) != 1 or wuxing not in TianGanDizhi.__TianGan__:
                return None
            Tiangans = TianGanDizhi.__TianGan__.split(';')
            result = []
            for tg in Tiangans:
                if tg[1] == wuxing:
                    result.append(tg[1])
            return result
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    
    #获得五行的地支
    @staticmethod
    def get_dizhi_of_wuxing(wuxing):
        try:
            if not isinstance(wuxing,unicode) or len(wuxing) != 1 or wuxing not in TianGanDizhi.__DiZhi__:
                return None
            Dizhis = TianGanDizhi.__DiZhi__.split(';')
            result = []
            for dz in Dizhis:
                if dz[1] == wuxing:
                    result.append(dz[1])
            return result
        except Exception,e:
            traceback.print_exc()
            print e
            return None
        