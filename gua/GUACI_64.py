# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 11:43:39 2015

@author: gong

http://baike.fututa.com/zhouyi64gua/
"""

import urllib2
import traceback
import pandas as pd
from pandas import DataFrame
from pyquery import PyQuery as pq

class GUACI_64(object):
    __PATH__ = u'/Users/gong/Documents/workspace/Python/gua/卦辞/'
    __GUA_TITLE__ = u'卦名,乾卦原文,断易天机解,邵雍解,傅佩荣解,传统解,张铭仁解,1爻辞,1爻邵雍解,1爻傅佩荣解,1变卦,2爻辞,2爻邵雍解,2爻傅佩荣解,2变卦,3爻辞,3爻邵雍解,3爻傅佩荣解,3变卦,4爻辞,4爻邵雍解,4爻傅佩荣解,4变卦,5爻辞,5爻邵雍解,5爻傅佩荣解,5变卦,6爻辞,6爻邵雍解,6爻傅佩荣解,6变卦'
    __DATAFRAME__ = None
    __LOADED__ = False
    
    @staticmethod
    def __get_data_from_web__(url):
        try:
            request = urllib2.Request(url)
            resp = urllib2.urlopen(request)
            data = resp.read().decode('utf8','ignore')
            return data
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    #解析卦列表
    @staticmethod
    def __parse_list__():
        try:
            data = GUACI_64.__get_data_from_web__('http://baike.fututa.com/zhouyi64gua/')
            doc = pq(data)
            node = doc('body > div.container > div > div > div:nth-child(4) > div.gualist')
            lis = node.find('li')
            result = []
            for li in lis:
                href = doc(li).find('a').eq(0).attr('href')
                gua = doc(li).text()
                gua = gua[gua.find(u'、')+len(u'、'):]
                result.append([href,gua])
            return result
        except Exception,e:
            traceback.print_exc()
            print e
            return None
            
    #解析卦的详情
    @staticmethod
    def __parse_detail__(url,name):
        try:
            data = GUACI_64.__get_data_from_web__(url)
            doc = pq(data)

            divs = doc('body > div.container > div.main > div').find('div')
            wenzhang_node = []
            for div in divs:
                if doc(div).attr('class') == 'gua_wen':
                    wenzhang_node.append(doc(div))
            
            gua_data = [name]
            for gua_wen in wenzhang_node:
                gua_data.append(gua_wen.text())
            return gua_data
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    #下载所有的卦数据
    @staticmethod
    def __download_all_guaci__():
        try:
            guas = GUACI_64.__parse_list__()
            gua_data = []
            for gua in guas:
                data = GUACI_64.__parse_detail__(gua[0],gua[1])
                gua_data.append(data)
            columns = tuple(GUACI_64.__GUA_TITLE__.split(','))
            dataframe = DataFrame(gua_data,columns = columns)
            dataframe.to_excel(GUACI_64.__PATH__+u'卦辞解析.xlsx')
        except Exception,e:
            traceback.print_exc()
            print e
    
    #获得某个卦的信息
    @staticmethod
    def get_guaci(gua):
        try:
            path = GUACI_64.__PATH__+u'卦辞解析.xlsx'
            if not GUACI_64.__LOADED__:
                GUACI_64.__DATAFRAME__ = pd.read_excel(path)
                GUACI_64.__LOADED__ = True
                
            return GUACI_64.__DATAFRAME__[GUACI_64.__DATAFRAME__[u'卦名'] == gua]
        except Exception,e:
            traceback.print_exc()
            print e
            return None


if __name__ == '__main__':
    print GUACI_64.get_guaci(u'乾为天')[u'邵雍解'][0]