# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 16:38:48 2015

@author: gong

@description:这是用来计算“会元运势数”的程序
"""
from Gua import Gua
XianTian_60_PeiGuaShu = [u'复',u'颐',u'屯',u'益',u'震',u'噬嗑',u'随',u'无妄',
                         u'明夷',u'贲',u'既济',u'家人',u'丰',u'革',u'同人',u'临',
                         u'损',u'节',u'中孚',u'归妹',u'睽',u'兑',u'履',u'泰',u'大畜',
                         u'需',u'小畜',u'大壮',u'大有',u'夬',u'姤',u'大过',u'鼎',u'恒',
                         u'巽',u'井',u'蛊',u'升',u'讼',u'困',u'未济',u'解',u'涣',u'蒙',
                         u'师',u'遁',u'咸',u'旅',u'小过',u'渐',u'蹇',u'艮',u'谦',u'否',
                         u'萃',u'晋',u'豫',u'观',u'比',u'剥']
                        
Hui = [
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

#算出会,year != 0
#返回值是：会，运，世，年，运卦，世卦，年卦
def get_Hui(year):
    if year > 0:
        index = 67017+year
    else:
        index = 67018+year
    hui = index/10800
    
    #这是计算hui
    if index % 10800 != 0:
        hui += 1
   
    hui_value = Hui[(hui-1) % 12].keys()[0]
    
    tmp = index % 10800
    if tmp == 0:
        tmp = 10800
    
    #这是算运
    yun = tmp / 360
    if tmp % 360 != 0:
        yun += 1
    #result[u'运'] = yun
    
    tmp = tmp % 360
    if tmp == 0:
        tmp = 360
    
    #这是算世
    shi = tmp/30
    if tmp % 30 != 0:
        shi += 1
    #result[u'世'] = shi
    shi_yu = tmp % 30
    if shi_yu == 0:
        shi_yu = 30
    
    gua = yun/6
    if yun % 6 != 0:
        gua += 1
    gua_value = Hui[(hui-1) % 12][hui_value][gua-1]
    tmp = yun % 6
    if tmp == 0:
        tmp = 6
    tmp_gua = Gua(u'坤',u'乾')
    up,down = tmp_gua.get_up_down(gua_value)
    tmp_gua = Gua(up,down)
    #gua_value = tmp_gua.get_name(up,down)
    yungua = tmp_gua.bian_yao(tmp)
    
    tmp_gua = Gua(yungua[0],yungua[1])
    #print 1+(result[u'世']-1)/2
    shigua = tmp_gua.bian_yao(1+(shi-1)/2)
    
    
    for i,value in enumerate(XianTian_60_PeiGuaShu):
        if value == shigua[2:]:
            tmp = i + 1
            break
    
    nian = None
    
    if shi % 2 == 0:
        nian = shi_yu + tmp -1 +30
    else:
        nian = shi_yu + tmp -1
    nian = nian % 60
    if nian ==0:
        nian = 60
    
    
    niangua = XianTian_60_PeiGuaShu[nian -1]
    up ,down = tmp_gua.get_up_down(niangua)
    niangua = tmp_gua.get_name(up,down)
    nian = shi_yu
    return (hui,yun,shi,nian,yungua,shigua,niangua)
    
if __name__ == '__main__':
    print get_Hui(2012)
    print get_Hui(2012)[4]
    print get_Hui(2012)[5]
    print get_Hui(2012)[6]

