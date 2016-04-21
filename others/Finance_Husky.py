# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 18:15:38 2015

@author: gong

@description: 这是用来从新浪上获取某一只股票历史交易信息的程序
网址:
http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/601006/displaytype/4.phtml


"""
import time
import urllib2
import traceback
import pandas as pd
from pyquery import PyQuery as pq
from pandas import DataFrame
from multiprocessing.dummy import Pool as ThreadPool

class Finance_Husky(object):
    def __init__(self,stockid):
        self.stockid = stockid
    
    #解析链接的链表页面
    def parse_urls(self,html):
        try:
            doc = pq(html)
            urls = doc('#BalanceSheetNewTable0').find('a')
            result = []
            for i,url in enumerate(urls):
                link = 'http://money.finance.sina.com.cn/'+doc(url).attr('href')
                name = doc(url).text()
                description = name[:name.find('(')]
                name = link[link.find('typecode=')+len('typecode='):]
                classification = None
                if i <= 9:
                    classification = u'每股指标'
                elif i <= 29:
                    classification = u'盈利能力'
                elif i <= 33:
                    classification = u'成长能力'
                elif i <= 43:
                    classification = u'营运能力'
                elif i <= 61:
                    classification = u'偿债及资本结构'
                elif i <= 66:
                    classification = u'现金流量'
                else :
                    classification = u'其他'
                result.append([link,name,description,classification])
            return result
        except Exception,e:
            traceback.print_exc()
            print 'Finance Husky Parse Urls Error: %s!' % e
            return None
    
    #解析没想具体财务指标的页面
    def parse_finance_data(self,item):
        try:
            url = item[0]
            request = urllib2.Request(url)
            resp = urllib2.urlopen(request)
            data = resp.read().decode('gb2312','ignore')
            doc = pq(data)
            table = doc('#Table1 > tbody')
            trs = table.find('tr')
            details = []
            for tr in trs:
                tds = doc(tr).find('td')
                detail = [self.stockid]
                for i,td in enumerate(tds):
                    if i == 1:
                        tmp = doc(td).text()
                        try:
                            detail.append(float(tmp))
                        except:
                            detail.append(0)
                    if i == 0:
                        detail.append(doc(td).text())
                #TO DO
                details.append(detail)
            name = '|'.join(item[1:])
            columns = ('stockid','date',name)
            dataframe = DataFrame(details,columns = columns)
            return dataframe
        except Exception,e:
            traceback.print_exc()
            print 'Finance Husky Parse Finance Data Error: %s !' % e
            return None
            
    #获得每一项具体的财务数据的指标
    def get_finance_data(self,item):
        try:
            return self.parse_finance_data(item)
        except Exception,e:
            traceback.print_exc()
            print 'Finance Husky Get Finance Data Error: %s !' % e
    
    #获得股票的财务数据指标链接
    def get_finance(self):
        try:
            url = 'http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/%s/displaytype/4.phtml' % self.stockid            
            request = urllib2.Request(url)
            resp = urllib2.urlopen(request)
            data = resp.read().decode('gb2312','ignore')
            urls = self.parse_urls(data)
            #dfs = map(self.get_finance_data,urls)
            dfs = []
            for url in urls:
                print url[0]
                dfs.append(self.get_finance_data(url))
                #time.sleep(0.1)
            tmpdf = dfs[0]
            for df in dfs[1:]:
                tmpdf = pd.merge(tmpdf,df,on=('date','stockid'))
            return tmpdf
        except Exception,e:
            traceback.print_exc()
            print 'Finance Husky Get Urls Error: %s!' % e

if __name__ == '__main__':
    dog = Finance_Husky('601006')
    print dog.get_finance()