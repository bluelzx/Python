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
from multiprocessing.dummy import Pool as ThreadPool
from extract_company_name import segmentation
#全局的字典
global P2P_DICT
P2P_DICT = None

#全局爬虫
global SPYDER
SPYDER = WebSpyder()

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


def find_lcs_len(s1, s2): 
    m = [ [ 0 for x in s2 ] for y in s1] 
    for p1 in range(len(s1)): 
        for p2 in range(len(s2)): 
            if s1[p1] == s2[p2]: 
                if p1 == 0 or p2 == 0: 
                    m[p1][p2] = 1
                else: 
                    m[p1][p2] = m[p1-1][p2-1]+1
            elif m[p1-1][p2] < m[p1][p2-1]: 
                m[p1][p2] = m[p1][p2-1] 
            else:               # m[p1][p2-1] < m[p1-1][p2] 
                m[p1][p2] = m[p1-1][p2] 
    return m[-1][-1] 
 
#编辑距离
def string_distance(strA, strB):
    #计算呈现条目与搜索企业的相似度
    lenA, lenB = len(strA), len(strB)
    c = [[0 for i in range(lenB+1)] for j in range(lenA+1)]
        
    for i in range(lenA): c[i][lenB] = lenA - i
    for i in range(lenB): c[lenA][i] = lenB - j
    c[lenA][lenB] = 0
        
    for i in range(lenA-1, -1, -1):
        for j in range(lenB-1, -1, -1):
            if strB[j] == strA[i]: c[i][j] = c[i+1][j+1]
            else: c[i][j] = min(c[i][j+1], c[i+1][j], c[i+1][j+1]) + 1
        
    return c[0][0]
       
#获得公司的名字
def get_company_info_from_text(short_name,text):
    #获得文本中的
    companys = segmentation(text)
    companys = map(lambda x:(find_lcs_len(short_name,x),x),companys)
    companys = map(lambda x:x[1],sorted(companys, key=lambda company : company[0],reverse=True))
    return companys

#下载信息的函数
def __download_info__(item):
    print 'Now processing: %s %s ......' % (item[0],item[1])
    try:
        short_name = item[1].decode('utf8')
    except:
        short_name = item[1].decode('gbk')
    if os.path.exists(short_name+'.txt'):
        return False
    global SPYDER
    spyder = SPYDER
    data = spyder.get_data(item[0])
    soup = BeautifulSoup(data,'lxml')
    info_data = soup.find('div',attrs={'class':'ue_s_c','id':'select_adv'}).get_text().strip()
    f = open(short_name+'.txt','w')
    f.write(info_data.encode('utf8','ignore'))
    f.close()
    return True
    
    
#从文本里面获得公司的名字
def get_company_texts(spyder,infile = 'p2p.csv'):
    dataframe = pd.read_csv(infile)
    pool = ThreadPool(4) 
    pool.map(__download_info__, dataframe.values)
    pool.close() 
    pool.join()
    
#用搜索引擎来获得公司的名字
def get_company_full_name_by_search_engine(short_name,search_engine = 'bing'):
    url = None
    if search_engine.lower() == 'bing':
        url = 'http://cn.bing.com/search?q='+urlencode(short_name)+'+'+urlencode(u'有限公司')
    global SPYDER
    spyder = SPYDER
    data = spyder.get_htmldata(url)
    parse_bing_data(data)


#用融金宝的数据来获得公司名字
def get_company_full_name_by_search_dict(short_name,dict_file = 'p2p.csv'):
    if os.path.exists(u'p2p/'+short_name+u'.txt'):
        info_data = open(u'p2p/'+short_name+u'.txt','r').read().decode('utf8','ignore')
        return get_company_info_from_text(short_name,info_data)
    global SPYDER
    spyder = SPYDER
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
        info_data = soup.find('div',attrs={'class':'ue_s_c','id':'select_adv'}).get_text().strip()
        f = open(u'p2p/'+short_name+u'.txt','w')
        f.write(info_data.encode('utf8','ignore'))
        f.close()
        return get_company_info_from_text(u'p2p/'+short_name,info_data)
    
    return None

if __name__ == '__main__':
    dataframe = pd.read_csv('p2p.csv')
    f = open('company_name.csv','w')
    for item in dataframe.values:
        try:
            try:
                short_name = item[1].decode('utf8')
            except:
                try:
                    short_name = item[1].decode('gbk')
                except:
                    short_name = item[1].decode('gb2312')
            companys = get_company_full_name_by_search_dict(short_name)
            line = short_name
            for c in companys:
                line += u','+c
            line += u'\n'
            f.write(line.encode('gbk','ignore'))
        except:
            print item[1],'error!'
            traceback.print_exc()
            break
    f.close()
        