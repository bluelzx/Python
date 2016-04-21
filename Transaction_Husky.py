# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 20:49:10 2015

@author: gong

@description: 这是用来从新浪上获取某一只股票历史交易信息的程序
网址:
http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/601006.phtml?year=2015&jidu=3

http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000300/type/S.phtml
jidu: 表示季度
year: 表示年
"""
import urllib2
import traceback
from pyquery import PyQuery as pq
from pandas import DataFrame

class Transaction_Husky(object):
    def __init__(self,stockid):
        #股票编号
        self.stockid = stockid
    
    #解析网页
    def parse_data(self,html):
        try:
            columns = ('stockid','detail','date','open','high','close','low','volume','turn')
            doc = pq(html)
            tbody = doc('#FundHoldSharesTable')
            trs = tbody.find('tr')
            stock_data = []
            for i,tr in enumerate(trs):
                if i == 1:
                    continue
                tmp_data = [self.stockid]
                tds = doc(tr).find('td')
                for j,td in enumerate(tds):
                    if j == 0:
                        date = doc(td).text()
                        href = doc(td).find('a').attr('href')
                        url = 'http://market.finance.sina.com.cn/downxls.php?'+href[href.find('?')+1:]
                        
                        tmp_data.append(url)
                        tmp_data.append(date)
                        
                    else:
                        tmp_data.append(float(doc(td).text()))
                if len(tmp_data) > 1:
                    stock_data.append(tmp_data)
            dataframe = DataFrame(stock_data,columns = columns).sort(columns = 'date')
            return dataframe
        except Exception,e:
            traceback.print_exc()
            print 'Transaction Husky Parse Data Error: %s !' % e
            return None
            
    #获得季度的股票交易数据
    def get_quarter_data(self,year,quarter):
        try:
            url = 'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%s&jidu=%s' %(self.stockid,year,quarter)
            request = urllib2.Request(url)
        
            resp = urllib2.urlopen(request)
            data = resp.read()
            return self.parse_data(data.decode('gb2312','ignore'))
        except Exception,e:
            traceback.print_exc()
            print 'Transaction Husky Get Quarter Data Error: year:%s, quarter:%s !' % (year,quarter)
            print e
            return None
        
if __name__ == '__main__':
    dog = Transaction_Husky('600036')
    print dog.get_quarter_data(2015,3)
