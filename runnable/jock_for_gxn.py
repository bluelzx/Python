# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 20:02:50 2016

@author: gong

@description: 这是写的段子的爬虫给gxn的
"""
import datetime
import random
import urllib2
import traceback
from pyquery import PyQuery as pq
from Send_Data import Send_Data
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

def parse_html(data):
    try:
        doc = pq(data)
        
        select_a = 'body > div.cd-wrapper.cd-main > div.fleft.cd-container > div.post-line-list > div:nth-child(%s) > div.item-detail > h2 > a'
        select_up = 'body > div.cd-wrapper.cd-main > div.fleft.cd-container > div.post-line-list > div:nth-child(%s) > div.item-toolbar > ul > li:nth-child(1)'
        select_down = 'body > div.cd-wrapper.cd-main > div.fleft.cd-container > div.post-line-list > div:nth-child(%s) > div.item-toolbar > ul > li:nth-child(2)'
        
        divs = doc('body > div.cd-wrapper.cd-main > div.fleft.cd-container > div.post-line-list > div')
        max_href = None   
        max_rate = 1
        n = len(divs)
        '''
        for i in range(1,len(divs)):
            try:
                href = doc(select_a % i).attr('href')
                up = int(doc(select_up % i).text())
                down = int(doc(select_down % i).text())*(-1)
                if href and float(up)/float(down) > max_rate:
                    max_rate = float(up)/float(down)
                    max_href = href
            except:
                pass
        '''
        while max_href== None:
            random.seed(datetime.datetime.now())
            index = random.randint(1,n)
            max_href = doc(select_a % index).attr('href')

        return max_href
    except Exception,e:
        print e

if __name__ == '__main__':
    sd = Send_Data('smtp.qq.com','bGlnb25nMTk=','MTk5Mi4wMS4wNGxpZ29uZw==','ligong19@qq.com')
    
    msg = ''
    
    #获得当前时间
    now = datetime.datetime.now()
    #转换为指定的格式:
    otherStyleTime = now.strftime("%Y年%m月%d日 的笑话")
    
    for i in range(1,10):
        msg += parse_html(get_html_data('http://www.waduanzi.com/lengtu/page/%s?source=barhometext' % i))+'\r\n<br/>'
    sd.send_message(otherStyleTime,msg,'1510090564@qq.com')