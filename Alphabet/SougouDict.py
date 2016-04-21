# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 17:13:33 2016

@author: gong

@description:这是用来从搜狗官网上下载字典的爬虫程序
"""
import time
import json
import urllib2
import traceback
import StringIO, gzip
from pyquery import PyQuery as pq

#获得数据
def get_html_data(url):
    try:
        resp = urllib2.urlopen(url)
        data = resp.read()
        #data = gzdecode(data)
        return data
    except Exception,e:
        print 'get_html_data --> error:',url
        traceback.print_exc()
        print e

def parse_product(data):
    try:
        doc = pq(data)
        divs = doc('#dict_detail_list')
        all_a = divs.find('a')
        result = []
        for a in all_a:
            href = doc(a).attr('href')
            if href and href.startswith('http://download.pinyin.sogou.com/dict/download_cell.php?id='):
                result.append(href)
        return result
    except Exception,e:
        print e
        traceback.print_exc()

def parse_person(data):
    try:
        doc = pq(data)
        result = ''
        for dd in doc('#pg-user-profile > div:nth-child(2) > div > div > div.avatar-invest.border-rt.w260.fn-left > dl').find('dd'):
            result += '|'+doc(dd).text()
        for dd in doc('#pg-user-profile > div:nth-child(2) > div > div > div.avatar-borrow.fn-left > dl').find('dd'):
            result += '|'+doc(dd).text()
        return result
    except Exception,e:
        print e
        traceback.print_exc()
        
        
        
if __name__ == '__main__':
    f = open('/Users/gong/Documents/aaa.scel','w')
    f.write(get_html_data('http://download.pinyin.sogou.com/dict/download_cell.php?id=603&name=建筑词库'))
    f.close()
   #print parse_product(get_html_data('http://pinyin.sogou.com/dict/cate/index/96/default/3'))