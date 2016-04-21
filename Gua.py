# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 18:41:00 2015

@author: gong
"""

class Gua(object):
    gua_dict = {u'乾':1,u'兑':2,u'离':3,u'震':4,u'巽':5,u'坎':6,u'艮':7,u'坤':8}
    gua_value = [u'乾',u'兑',u'离',u'震',u'巽',u'坎',u'艮',u'坤']
    gua_code_dict = {'111':1,'011':2,'101':3,'001':4,'110':5,'010':6,'100':7,'000':8}
    gua_code = ['111','011','101','001','110','010','100','000']
    gua_64 = {
    u'乾乾':u'天',u'天风':u'姤',u'天山':u'遁',u'天地':u'否',u'风地':u'观',u'山地':u'剥',u'火地':u'晋',u'火天':u'大有',
    u'兑兑':u'泽',u'泽水':u'困',u'泽地':u'萃',u'泽山':u'咸',u'水山':u'蹇',u'地山':u'谦',u'雷山':u'小过',u'雷泽':u'归妹',
    u'离离':u'火',u'火山':u'旅',u'火风':u'鼎',u'火水':u'未济',u'山水':u'蒙',u'风水':u'涣',u'天水':u'讼',u'天火':u'同人',
    u'震震':u'雷',u'雷地':u'豫',u'雷水':u'解',u'雷风':u'恒',u'地风':u'升',u'水风':u'井',u'泽风':u'大过',u'泽雷':u'随',
    u'巽巽':u'风',u'风天':u'小畜',u'风火':u'家人',u'风雷':u'益',u'天雷':u'无妄',u'火雷':u'噬嗑',u'山雷':u'颐',u'山风':u'蛊',
    u'坎坎':u'水',u'水泽':u'节',u'水雷':u'屯',u'水火':u'既济',u'泽火':u'革',u'雷火':u'丰',u'地火':u'明夷',u'地水':u'师',
    u'艮艮':u'山',u'山火':u'贲',u'山天':u'大畜',u'山泽':u'损',u'火泽':u'睽',u'天泽':u'履',u'风泽':u'中孚',u'风山':u'渐',
    u'坤坤':u'地',u'地雷':u'复',u'地泽':u'临',u'地天':u'泰',u'雷天':u'大壮',u'泽天':u'夬',u'水天':u'需',u'水地':u'比'
    }
    def __init__(self,up,down):
        self.up = up
        self.down = down
        tmp = {u'天':u'乾',u'泽':u'兑',u'火':u'离',u'雷':u'震',u'风':u'巽',u'水':u'坎',u'山':u'艮',u'地':u'坤'}
        if up not in Gua.gua_value and down not in Gua.gua_value:
            self.up = tmp[up]
            self.down = tmp[down]
    
    #获得卦名
    def get_name(self,up,down):
        
        #上下卦相同
        if up == down:
            return up+u'为'+Gua.gua_64[up+down]
        return Gua.gua_64[up+up]+Gua.gua_64[down+down]+Gua.gua_64[Gua.gua_64[up+up]+Gua.gua_64[down+down]]
    
    #获得变爻
    def bian_yao(self,yao_index):
        tmp = None
        index = yao_index
        if yao_index > 3:
            tmp = Gua.gua_code[Gua.gua_dict[self.up]-1]
            index = yao_index - 3
        else:
            tmp = Gua.gua_code[Gua.gua_dict[self.down]-1]
        temp = []
        #str to array
        for s in tmp:
            temp.append(s)
            
        index -= 1
        
        if temp[2-index] == '0':
            temp[2-index] = '1'
        else:
            temp[2-index] = '0'
        tmp = ''.join(temp)
        #print Gua.gua_code_dict[tmp]
        tmp = Gua.gua_value[Gua.gua_code_dict[tmp]-1]
        #print tmp
        if yao_index > 3:
            return self.get_name(tmp,self.down)
        else:
            return self.get_name(self.up,tmp)
    
    
    #获得上下卦
    def get_up_down(self,gua):
        if gua in Gua.gua_value:
            return gua,gua
        keys = Gua.gua_64.keys()
        up = None
        down = None
        for key in keys:
            if Gua.gua_64[key] == gua:
                up = key[0]
                down = key[1]
                break
        for key in keys:
            if Gua.gua_64[key] == up:
                up = key[0]
                break
        for key in keys:
            if Gua.gua_64[key] == down:
                down = key[0]
                break
        return up,down
        
if __name__ == '__main__':
    gua = Gua(u'坤',u'乾')
    for i in range(1,7):
        print i,gua.bian_yao(i)
    print gua.get_up_down(u'大过')[0],gua.get_up_down(u'大过')[1]
    
    
    