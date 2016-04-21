# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 19:33:57 2015

@author: gong

@description:这是用来抓取股吧股票的程序
"""
import os
import time
import urllib2
import traceback
import pandas as pd
from pyquery import PyQuery as pq

class Eastmoney_Guba(object):
    #下载网络数据
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
    
    #获得总页数
    @staticmethod
    def __get_total_pages__(stockid):
        try:
            url = 'http://guba.eastmoney.com/list,%s_%s.html' % (stockid,1)
            data = Eastmoney_Guba.__get_data_from_web__(url)
            doc = pq(data)
            pages = doc('#articlelistnew > div.pager').html()
            pages = pages[pages.find('pager="list,')+len('pager="list,'):]
            pages = pages[:pages.find('"')]
            values = pages.split('|')
            page_num = int(values[1])/int(values[2])+1
            return page_num
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    #解析列表数据
    @staticmethod
    def __parse_list_data__(stockid,index=1):
        try:
            url = 'http://guba.eastmoney.com/list,%s_%s.html' % (stockid,index)
            data = Eastmoney_Guba.__get_data_from_web__(url)
            #获取网络数据有问题，则不断获取
            while data == None:
                time.sleep(0.5)
                data = Eastmoney_Guba.__get_data_from_web__(url)
            doc = pq(data)
            divs = doc('#articlelistnew').find('div')
            list_data = []
            columns = (u'股票代码',u'阅读',u'评论',u'标题',u'文章链接',u'作者',u'发表日期',u'最后更新')
            for div in divs:
                #去掉第一行
                if doc(div).attr('class').find('articleh') >= 0:
                    tmp = [stockid]
                    spans = doc(div).find('span')
                    temp = {}
                    for span in spans:
                        if doc(span).attr('class') == 'l1':
                            temp[u'阅读'] = int(doc(span).text())
                        if doc(span).attr('class') == 'l2':
                            temp[u'评论'] = int(doc(span).text())
                        if doc(span).attr('class') == 'l3':
                            temp[u'标题'] = doc(span).text()
                            temp[u'文章链接'] = 'http://guba.eastmoney.com/'+doc(span).find('a').attr('href')
                        
                        if doc(span).attr('class') == 'l4':
                            temp[u'作者'] = doc(span).text()
                        
                        if doc(span).attr('class') == 'l6':
                            temp[u'发表日期'] = doc(span).text()
                        if doc(span).attr('class') == 'l5':
                            temp[u'最后更新'] = doc(span).text()
                    '''
                    tmp.append(int(spans.eq(0).text()))
                    tmp.append(int(spans.eq(1).text()))
                    tmp.append(spans.eq(2).text())
                    eassy_url = 'http://guba.eastmoney.com/'+spans.eq(2).find('a').attr('href')
                    tmp.append(eassy_url)
                    tmp.append(spans.eq(3).text())
                    #tmp.append(spans.eq(3).find('a').attr('href'))
                    
                    
                    tmp.append(spans.eq(4).text())
                    tmp.append(spans.eq(5).text())
                    #print spans.eq(2).text()
                    #list_data.append(Eastmoney_Guba. __get_detail_time__('http://guba.eastmoney.com/'+spans.eq(2).find('a').attr('href')))
                    '''
                    tmp.append(temp[u'阅读'])
                    tmp.append(temp[u'评论'])
                    tmp.append(temp[u'标题'])
                    tmp.append(temp[u'文章链接'])
                    tmp.append(temp[u'作者'])
                    tmp.append(temp[u'发表日期'])
                    tmp.append(temp[u'最后更新'])

                    if temp[u'文章链接'].find(str(stockid)) >= 0:                
                        list_data.append(tmp)
            #避免空值
            if len(list_data) == 0:
                return None
            return pd.DataFrame(list_data,columns = columns)
        except Exception,e:
            traceback.print_exc()
            print e
            return None
    
    @staticmethod
    def __process__(stockid,path,step = 20):
        try:
            pre_filename = path+'/'+str(stockid)
            page_num = Eastmoney_Guba.__get_total_pages__(stockid)
            index = page_num/step+1
            filenames = []
            for i in range(index):
                result = []
                for j in range(1,step+1):
                    print 'Now processing stock %s page %s...' %(stockid,j + i*step)
                    tmp = Eastmoney_Guba.__parse_list_data__(stockid,j + i*step)
                    if isinstance(tmp,pd.DataFrame):
                        result.append(tmp)
                if len(result) > 0:
                    filenames.append(pre_filename+'_'+str(i)+'.xlsx')
                    pd.concat(result).to_excel(pre_filename+'_'+str(i)+'.xlsx')
                time.sleep(1)
            read_xls = lambda filename:pd.read_excel(filename)

            #生成最终文件s
            pd.concat(map(read_xls,filenames)).drop_duplicates([u'文章链接']).sort([u'文章链接'], ascending=[0]).to_excel(pre_filename+'.xlsx')
            
            #删除文件            
            map(os.remove,filenames)
        except Exception,e:
            traceback.print_exc()
            print e
if __name__ == '__main__':
    Eastmoney_Guba.__process__('300494','/Users/gong/Documents')