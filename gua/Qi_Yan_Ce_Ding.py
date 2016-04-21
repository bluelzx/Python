# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 12:29:36 2015

@author: gong
"""
import traceback
from Gua import Gua
class Qi_Yan_Ce_Ding(Gua):
    __JiaZi_BaGua__ = {
    10:u'戊,癸;辰,戌;坤',
    9:u'甲,己;子,午;乾',
    8:u'乙,庚,丑,未;巽',
    7:u'丙,辛,寅,申;离',
    6:u'丁,壬,卯,酉;坎',
    5:u'戊,癸,辰,戌;艮',
    4:u'申酉;巳亥;兑',
    3:u'寅,卯;震',
    2:u'巳,午;离',
    1:u'亥,子;坎'
    }
    
    __WuXing_BaGua__= {
    u'乾':u'金',
    u'兑':u'金',
    u'坤':u'土',
    u'艮':u'土',
    u'震':u'木',
    u'巽':u'木',
    u'坎':u'水',
    u'离':u'火'
    }
    #获得策数
    @staticmethod
    def get_ceshu(gua,index):
        try:
            code = Gua.guatu64(gua)
            
            answer = 0
            #原策数，阳 36 阴 24
            yuanceshu = 24*6+sum(code)*12
            
            up = Gua.get_8gua_index(code[0:3])
            down = Gua.get_8gua_index(code[3:])
            answer = yuanceshu + up + down + index
            if index > 3:
                
                answer += (index*10+up)*yuanceshu
            else:
                answer += (down*10+index)*yuanceshu
            answer = str(answer)
            answer = answer[len(answer)-4:]
            #元会世运
            result = {}
            result[u'元'] = answer[0]
            result[u'会'] = answer[1]
            result[u'世'] = answer[2]
            result[u'运'] = answer[3]
            print answer
            return result
        except Exception,e:
            traceback.print_exc()
            print e

if __name__ == '__main__':
    print Qi_Yan_Ce_Ding.get_ceshu(u'风水涣',3)