# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:01:36 2016

@author: gong

@description:这是从东方财富网上抓取公司数据的程序

http://finance.eastmoney.com/news/cssgs.html
"""
import re
import urllib2
import traceback
from bs4 import BeautifulSoup
from CompanyTextDataDownloader import CompanyTextDataDownloader
class DFCF_CompanyTextDataDownloader(CompanyTextDataDownloader):
    def __init__(self,name = 'DFCF_CompanyTextDataDownloader'):
        self._name = name
    
    def is_myurl(self,url):
        '''判断是不是东方财富的网址链接'''
        try:
            pattern = 'http://[a-zA-Z0-9]+.eastmoney.com/\S*'
            if re.match(pattern, url):
                return True
            return False
        except Exception,e:
            print e
            traceback.print_exc()
            return False
    
    def next_list_url(self,url):
        '''获得下一个列表页的链接'''
        try:
            if url == 'http://finance.eastmoney.com/news/cssgs.html':
                return 'http://finance.eastmoney.com/news/cssgs_2.html'
            tmp_url = url[url.find('http://finance.eastmoney.com/news/cssgs_')+len('http://finance.eastmoney.com/news/cssgs_'):url.find('.html')]
            return 'http://finance.eastmoney.com/news/cssgs_%s.html' % (int(tmp_url)+1)
        except Exception,e:
            print '%s next list url error: %s !' % (self._name,e)
            return None
            
    def parse_list(self,html_data):
        '''这是解析列表页的函数，返回文章的链接列表'''
        try:
            soup = BeautifulSoup(html_data,'html.parser')
            urls = map(lambda x:x.find('a')['href'],soup.select('div.mainCont > div.listBox > div.list  > ul > li'))
            return urls
        except Exception,e:
            print '%s parse list error: %s !' % (self._name,e)
            traceback.print_exc()
    
    def parse_detail(self,html_data):
        '''这是解析列表详情的函数，返回标题，时间，文本等'''
        try:
            soup = BeautifulSoup(html_data,'html.parser)
            metas = soup.find_all('meta')
            title = soup.h1.string
            keywords = metas[1]['content'].split(',')
            description = metas[2]['content']
            time = soup.select('.Info > span')[0].get_text()
            text_data = soup.find(id = 'ContentBody').get_text()
            result = {}
            result['title'] = title
            result['keywords'] = keywords
            result['description'] = description
            result['time'] = time
            result['text_data'] = text_data
            return result
        except Exception,e:
            print '%s parse detail error: %s !' % (self._name,e)
            traceback.print_exc()
            return None
            
def __get_data_from_web__(url):
    try:
        request = urllib2.Request(url)
        resp = urllib2.urlopen(request)
        data = resp.read().decode('gb2312','ignore')
        return data
    except Exception,e:
        traceback.print_exc()
        print e
        return None
        
if __name__ == '__main__':
    dfcf = DFCF_CompanyTextDataDownloader()
    html = __get_data_from_web__('http://finance.eastmoney.com/news/cssgs.html')
    print dfcf.parse_list(html)    
    print dfcf.next_list_url('http://finance.eastmoney.com/news/cssgs_9.html')
