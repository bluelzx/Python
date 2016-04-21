# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 18:00:14 2015

@author: gong
"""
import time
import json
import urllib2
import traceback
import StringIO, gzip
from pyquery import PyQuery as pq

#解压gzip  
def gzdecode(data) :  
    compressedstream = StringIO.StringIO(data)  
    gziper = gzip.GzipFile(fileobj = compressedstream)    
    data2 = gziper.read().decode('utf8','ignore')   # 读取解压缩后数据   
    return data2

def get_html_data(url):
    try:
        request = urllib2.Request(url)
        request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        request.add_header('Accept-Encoding','gzip, deflate, sdch')
        request.add_header('Accept-Language','zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4,zh-TW;q=0.2')
        request.add_header('Cache-Control','max-age=0')
        request.add_header('Connection','keep-alive')
        request.add_header('Cookie','JSESSIONID=901013584E4E4AD9E4D4E0553D076C797B4F536B1818AF300141890707D6C316; rrd_key=c3VudWFuYW5AMTYzLmNvbToxNDUwMTgwNjM1NjI2OmIyZDdlYjE4MzQ4YzRhZjk2MjcxYjU4YjI5Njc1YzYwOjIwMi4xMjAuMTkuMTc3; jforumUserInfo=pUw66AH5oaK2c%2B7N87c5WQ2a3l3Wo1oZ%0A; IS_MOBLIE_IDPASS=true-true; activeTimestamp=1548447; Hm_lvt_16f9bb97b83369e62ee1386631124bb1=1450178834; Hm_lpvt_16f9bb97b83369e62ee1386631124bb1=1450178883')
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36')
        resp = urllib2.urlopen(request)
        data = resp.read()
        data = gzdecode(data)
        return data
    except Exception,e:
        print 'get_html_data --> error:',url
        traceback.print_exc()
        print e
        

def parse_product(data):
    try:
        doc = pq(data)
        
        dlls = doc('#loan-basic-panel > div > div.pl25.pr25.fn-clear > div.fn-left.pt10.loaninfo')
        
        dls = dlls.find('dl')
        result = ''
        for dl in dls:
            result += '|'+doc(dl).text()
        
        lis = dlls.find('li')
        for li in lis:
            result += '|'+doc(li).text()
        
        
        divs = doc('#loan-basic-panel > div > div.pl25.pr25.fn-clear > div.fn-right.loan-status').find('div')
        try:        
            result += '|'+doc('#fullTime').attr('data-time')
        except:
            result += '|'
        result += '|'
        for i,div in enumerate(divs):
            result += doc(div).text()
            try:
                result += doc(div).find('em').eq(0).attr('class')
            except:
                pass
        #result += '|'+ doc('#loan-tab-content > div > div.ui-tab-content.ui-tab-content-info.ui-tab-content-current > div.ui-tab-content-basic.border-bottom.pt25.mlr60 > table > tbody > div > em').attr('title')
        #result += '|'+doc('#loan-tab-content > div > div.ui-tab-content.ui-tab-content-info.ui-tab-content-current > div.ui-tab-content-basic.border-bottom.pt25.mlr60 > table > tbody > div > em > i').attr('class')
       
        
        
        trs = doc('#loan-tab-content > div > div.ui-tab-content.ui-tab-content-info.ui-tab-content-current > div.ui-tab-content-basic.border-bottom.pt25.mlr60 > table').find('tr')
         
        text = data[data.find(u'<span>信用评级</span><')+len(u'<span>信用评级</span><'):]
        text = text[:text.find('</em></div>')]
        result += '|'+text
        for i,tr in enumerate(trs):
            result += '|'+doc(tr).text()
            
        tmp = data[data.find('script id="credit-info-data" type="text/x-json">')+len('script id="credit-info-data" type="text/x-json">'):]
        tmp = tmp[:tmp.find('</script>')]
        #print tmp
        mydata = json.loads(tmp)
        tmpdata = mydata['data']['creditInfo']
        keys = tmpdata.keys()
        for k in keys:
            result += '|'+str(k)+':'+str(tmpdata[k])
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
    '''
    url= 'http://www.we.com/lend/detailPage.action?loanId=200089'
    data = get_html_data(url)
    result = parse_product(data)
    print result
    '''
    f = open('/Users/gong/Documents/aaa.txt','a')
    for i in range(1,10):
        url = 'http://www.we.com/lend/detailPage.action?loanId='+str(i)
        try:
            print url        
            data = get_html_data(url)
            result = parse_product(data)
            #tmp_url = 'http://www.renrendai.com/lend/getborrowerandlenderinfo.action?id=lenderRecords&loanId='+str(i)
            #r3 = get_html_data(tmp_url)
            '''
            tmp = json.loads(r3)
            length = len(tmp['data']['lenderRecords'])
            r2 = parse_person(get_html_data_2(muyrl))
            f.write(result.encode('utf8','ignore'))
            f.write(r2.encode('utf8','ignore'))
            f.write('|')
            f.write(str(length))
            #f.write(r3.encode('gb2312','ignore'))
            f.write('|'+str(i))
            f.write('\n')
            '''
            f.write(result.encode('gb2312','ignore'))
            f.write('\n')
            f.flush()
            time.sleep(0.1)
        except Exception,e:
            print url,'Error!'
            print e
            traceback.print_exc()
    f.close()
    
    

    
