# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:28:15 2015

@author: gong

@description:这是跟基本卦象的类
"""
import copy
import traceback

class Gua(object):
    GUA_8 = [u'乾',u'兑',u'离',u'震',u'巽',u'坎',u'艮',u'坤']
    GUA_WU = [u'天',u'泽',u'火',u'雷',u'风',u'水',u'山',u'地']
    GUA_8_CODE = [[1,1,1],[0,1,1],[1,0,1],[0,0,1],[1,1,0],[0,1,0],[1,0,0],[0,0,0]]
    GUA_64 = {
    u'乾乾':u'天',u'天风':u'姤',u'天山':u'遁',u'天地':u'否',u'风地':u'观',u'山地':u'剥',u'火地':u'晋',u'火天':u'大有',
    u'兑兑':u'泽',u'泽水':u'困',u'泽地':u'萃',u'泽山':u'咸',u'水山':u'蹇',u'地山':u'谦',u'雷山':u'小过',u'雷泽':u'归妹',
    u'离离':u'火',u'火山':u'旅',u'火风':u'鼎',u'火水':u'未济',u'山水':u'蒙',u'风水':u'涣',u'天水':u'讼',u'天火':u'同人',
    u'震震':u'雷',u'雷地':u'豫',u'雷水':u'解',u'雷风':u'恒',u'地风':u'升',u'水风':u'井',u'泽风':u'大过',u'泽雷':u'随',
    u'巽巽':u'风',u'风天':u'小畜',u'风火':u'家人',u'风雷':u'益',u'天雷':u'无妄',u'火雷':u'噬嗑',u'山雷':u'颐',u'山风':u'蛊',
    u'坎坎':u'水',u'水泽':u'节',u'水雷':u'屯',u'水火':u'既济',u'泽火':u'革',u'雷火':u'丰',u'地火':u'明夷',u'地水':u'师',
    u'艮艮':u'山',u'山火':u'贲',u'山天':u'大畜',u'山泽':u'损',u'火泽':u'睽',u'天泽':u'履',u'风泽':u'中孚',u'风山':u'渐',
    u'坤坤':u'地',u'地雷':u'复',u'地泽':u'临',u'地天':u'泰',u'雷天':u'大壮',u'泽天':u'夬',u'水天':u'需',u'水地':u'比'
    }
    
    #根据卦获得值
    @staticmethod
    def get_8gua_index(gua):
        try:
            if isinstance(gua,int):
                tmp = gua % 8
                if tmp == 0:
                    tmp = 8
                return tmp
            
            if isinstance(gua,list) and len(gua) ==3:
                index = 0
                for i,v in enumerate(gua):
                    index += v*(2**i)
                return 8-index
                
            if gua in Gua.GUA_8:
                for i,v in enumerate(Gua.GUA_8):
                    if v == gua:
                        return i+1
            
            if gua in Gua.GUA_WU:
                for i,v in enumerate(Gua.GUA_WU):
                    if v == gua:
                        return i+1

            return None
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    #根据卦图获得卦
    @staticmethod
    def get_8gua_by_code(code):
        try:
            index = 0
            for i,v in enumerate(code):
                index += v*(2**i)
            index = int(index)
            return Gua.get_8gua_by_index(8-index)
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    #根据值获得卦
    @staticmethod
    def get_8gua_by_index(index):
        try:
            tmp = (index % 8 + 8) % 8
            if tmp == 0:
                tmp += 8
            tmp -= 1
            return Gua.GUA_8[tmp]
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    #根据卦获得符号
    @staticmethod
    def guatu(gua):
        try:
            code = None
            if isinstance(gua,int):
                code = copy.deepcopy(Gua.GUA_8_CODE[gua-1])
            elif isinstance(gua,unicode):
                code = copy.deepcopy(Gua.GUA_8_CODE[Gua.get_8gua_index(gua)-1])
            return code
        except Exception,e:
            traceback.print_exc()
            print e
            return None
            
    #八卦变爻
    @staticmethod
    def __8gua_bianyao__(gua,index):
        try:
            code = Gua.guatu(gua)
            index = (index % 3 + 3) % 3
            if index == 0:
                index = 3
            index = 4 - index
            
            code[index-1] = (code[index-1] + 1) % 2

            return Gua.get_8gua_by_code(code)
        except Exception,e:
            traceback.print_exc()
            print e
            return None

    #获得64卦
    @staticmethod
    def get_64gua_by_updown(up,down):
        try:
            up_code = Gua.guatu(up)
            down_code = Gua.guatu(down)
            code = []
            map(lambda x:code.append(x),up_code)
            map(lambda x:code.append(x),down_code)
            return Gua.get_64gua_by_code(code)
        except Exception,e:
            traceback.print_exc()
            print e
            return None
            
    #获得64卦
    @staticmethod
    def get_64gua_by_code(code):
        try:
            up = Gua.get_8gua_by_code(code[0:3])
            down = Gua.get_8gua_by_code(code[3:])
            if up == down:
                return up+u'为'+Gua.GUA_64[up+down]
            key = Gua.GUA_WU[Gua.get_8gua_index(up)-1]
            key += Gua.GUA_WU[Gua.get_8gua_index(down)-1]
            return key + Gua.GUA_64[key]
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    #获得卦的图
    @staticmethod
    def guatu64(gua):
        try:
            if len(gua) <= 2:
                tmp = Gua.get_64gua_fullname(gua)
                if tmp != None:
                    gua = tmp
            code = []
            up = None
            down = None
            if gua[1] == u'为':
                up = Gua.guatu(gua[0])
                down = Gua.guatu(gua[0])
            else:
                up = Gua.guatu(gua[0])
                down = Gua.guatu(gua[1])
                
            map(lambda x:code.append(x),up)
            map(lambda x:code.append(x),down)
            return code
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    #64卦变爻
    @staticmethod
    def __biangua64__(gua_U,gua_D,index):
        try:
            up = Gua.get_8gua_index(gua_U)
            down = Gua.get_8gua_index(gua_D)
            index = index % 6
            if index == 0:
                index = 6
            if index > 3:
                #变上卦
                index -= 3
                return Gua.get_64gua_by_updown(Gua.__8gua_bianyao__(up,index),down)
                
            else:
                #变下卦
                return Gua.get_64gua_by_updown(up,Gua.__8gua_bianyao__(down,index))
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    #变卦
    @staticmethod
    def biangua(gua,index):
        try:
            if isinstance(gua,list) and len(gua) == 6:
                up = gua[0:3]
                down = gua[3:]
                return Gua.__biangua64__(Gua.get_8gua_index(up),Gua.get_8gua_index(down),index)
            elif isinstance(gua,unicode) and len(gua) >= 3:
                if gua[1] == u'为':
                    return Gua.__biangua64__(gua[0],gua[0],index)
                else:
                    return Gua.__biangua64__(gua[0],gua[1],index)
            return None
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    #获得互卦
    @staticmethod
    def hugua(gua):
        try:
            code = Gua.guatu64(gua)
            up = code[2:5]
            down = code[1:4]
            mycode = []
            map(lambda x:mycode.append(x),up)
            map(lambda x:mycode.append(x),down)
            return Gua.get_64gua_by_code(mycode)
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    #获得全卦名称
    @staticmethod
    def get_64gua_fullname(gua):
        try:
            if gua in Gua.GUA_WU or gua in Gua.GUA_8:
                return Gua.get_64gua_by_updown(gua,gua)
            for k,v in Gua.GUA_64.items():
                if v == gua:
                    return k+v
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    #获得错卦
    @staticmethod
    def cuogua(gua):
        try:
            code = Gua.guatu64(gua)
            return Gua.get_64gua_by_code(map(lambda x:(x+1)%2,code))
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    #获得综卦
    @staticmethod
    def zonggua(gua):
        try:
            code = Gua.guatu64(gua)
            code.reverse()
            return Gua.get_64gua_by_code(code)
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    #获得复卦
    @staticmethod
    def fugua(gua):
        return Gua.hugua(gua)
    
    #获得杂卦
    @staticmethod
    def zagua(gua):
        return Gua.cuogua(Gua.zonggua(Gua.hugua(gua)))
    
            
if __name__ == '__main__':
    print Gua.__8gua_bianyao__(u'乾',3)
    print Gua.get_8gua_by_code([1,0,1])
    print Gua.zagua(u'天风姤')