# -*- coding: utf-8 -*-
"""
Created on Thu May 05 14:46:01 2016

@author: gong

@description:这是用程序寻找企业公司名称的程序
"""
import os
from WebSpyder import WebSpyder
from urllib import urlencode
from bs4 import BeautifulSoup
import traceback
import pandas as pd

#全局的字典
global P2P_DICT
P2P_DICT = None

#解析必应的返回数据
def parse_bing_data(data):
    soup = BeautifulSoup(data,'lxml')
    soup.find('ol',attrs={'id':'b_results'}).findAll('')
    
    
#获得p2p的相关信息和链接
def get_all_p2p_names(spyder,outfile = 'p2p.csv',max_list=92):
    url = 'http://www.rjb777.com/a/pingtai/list_%s.html'
    result = []
    for i in xrange(1,max_list+1):
        tmp_url = url % i
        print 'Now processing %s!' % tmp_url
        data = spyder.get_data(tmp_url)
        soup = BeautifulSoup(data,'lxml')
        
        extract = lambda link:(unicode('http://www.rjb777.com'+link['href']),unicode(link.get_text()))
        links = soup.find('ul',attrs={'class':'ue_list'}).findAll('a')
        
        result += map(extract,links)
    if not os.path.exists(outfile):
        f = open(outfile,'w')
        for r in result:
            f.write(r[0].encode('utf8','ignore')+','+r[1].encode('utf8','ignore')+'\n')
        f.close()
        
    return result


#从文本里面获得公司的名字
def get_company_name_from_text():
    pass
    
#用搜索引擎来获得公司的名字
def get_company_full_name_by_search_engine(short_name,spyder,search_engine = 'bing'):
    url = None
    if search_engine.lower() == 'bing':
        url = 'http://cn.bing.com/search?q='+urlencode(short_name)+'+'+urlencode(u'有限公司')
    
    data = spyder.get_htmldata(url)
    parse_bing_data(data)


#用融金宝的数据来获得公司名字
def get_company_full_name_by_search_dict(short_name,spyder,dict_file = 'p2p.csv'):
    #全局字典是否加载成功
    global P2P_DICT
    if P2P_DICT == None:
        if not os.path.exists(dict_file):
            get_all_p2p_names(spyder,dict_file)
        dataframe = pd.read_csv(dict_file)
        P2P_DICT = {}
        for item in dataframe.values:
            P2P_DICT[unicode(item[1].decode('utf8','ignore'))] = unicode(item[0].decode('utf8','ignore'))
    if P2P_DICT.has_key(short_name):
        url = P2P_DICT[short_name]
        data = spyder.get_data(url)
        soup = BeautifulSoup(data,'lxml')
        info = soup.find('div',attrs={'class':'ue_s_c','id':'select_adv'}).get_text().strip()
        print info
    return None

if __name__ == '__main__':
    try:
        get_company_full_name_by_search_dict(u'长金保',WebSpyder())
    except:
        traceback.print_exc()