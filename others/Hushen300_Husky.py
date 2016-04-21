# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 21:23:24 2015

@author: gong
"""

import urllib2
import traceback
from pyquery import PyQuery as pq

class Hushen300_Husky(object):
    def __init__(self):
        self.url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vII_NewestComponent/indexid/000300.phtml'
    
    def get_stocks(self):
        try:
            request = urllib2.Request(self.url)
            resp = urllib2.urlopen(request)
            data = resp.read().decode('gb2312','ignore')
            doc = pq(data)
            trs = doc('#NewStockTable').find('tr')
            result = []
            for i,tr in enumerate(trs):
                if i <= 1:
                    continue
                result.append(doc(tr).find('td').eq(0).text())
            return result
        except Exception,e:
            traceback.print_exc()
            print 'HuShen 300 Husky Get Stocks Error: %s !' % e
            return None

if __name__ == '__main__':
    dog = Hushen300_Husky()
    print dog.get_stocks()
    print len(dog.get_stocks())