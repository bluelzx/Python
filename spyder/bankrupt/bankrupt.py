# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 13:32:38 2016

@author: gong

@description:下载“佛山法院网”中的“破产公告”，“中国破产资产网”中的“行业新闻”，“中国法院网”中的“法院公告”整理破产企业信息

"""
import StringIO,gzip
import time
import json
import datetime
from WebSpyder import WebSpyder
from bs4 import BeautifulSoup

webspyder = WebSpyder()
DAY = 10

#解压gzip  
def gzdecode(data) :  
    compressedstream = StringIO.StringIO(data)  
    gziper = gzip.GzipFile(fileobj=compressedstream)    
    data2 = gziper.read()   # 读取解压缩后数据   
    return data2
    
def get_foshan(spyder = webspyder):
    #先获得时间数组格式的日期
    three_day_ago = (datetime.datetime.now() - datetime.timedelta(days = DAY))
    daystr = three_day_ago.strftime("%Y-%m-%d")
    
    url = 'http://www.fszjfy.gov.cn/pub/court_7/sifagongkai/fayuangonggao/pcgg/'
    
    foshan_spyder = spyder
    data = gzdecode(foshan_spyder.get_htmldata(url))
    soup = BeautifulSoup(data,'lxml')

    trs = filter(lambda tr:tr.attrs.has_key('style') and tr.attrs['style']=='font-size:12px',soup.findAll('tr'))
    result = []
    for tr in trs:
        url = 'http://www.fszjfy.gov.cn/pub/court_7/sifagongkai/fayuangonggao/pcgg'+tr.find('a').attrs['href'][1:]
        date = tr.findAll('td')[1].get_text()
        if date >= daystr:
            result.append((url,date))
    return result

def get_pochanzichan(spyder = webspyder):
    url = 'http://www.pczc.cn/news/view/7_%s.html'
    #先获得时间数组格式的日期
    three_day_ago = (datetime.datetime.now() - datetime.timedelta(days = DAY))
    daystr = three_day_ago.strftime("%Y-%m-%d")
    
    pochanzichan = spyder
    result = []
    for i in range(1,5*DAY):
        print url % i
        data = pochanzichan.get_htmldata(url % i)
        soup = BeautifulSoup(data,'lxml')
        lis = soup.find('div',attrs={'class':'sub_con'}).findAll('li')
        lis = filter(lambda x:not x.attrs.has_key('class'),lis)
        tmp = lambda li:('http://www.pczc.cn/'+li.find('a').attrs['href'],li.find('a').get_text(),li.find('cite').get_text()[1:-1])
        result += filter(lambda x:x[2] >= daystr,map(tmp,lis))
    return result
    
def get_fayuangonggao(spyder = webspyder):
    start = int(time.time()*1000)
    tmp = 'callback=jQuery_'+str(start-30000)
    url = 'http://rmfygg.court.gov.cn/psca/lgnot/solr/searchBulletinInterface.do?start=****&limit=16&wd=rmfybulletin&list%5B0%5D=bltntype%3A64&_'+str(start)+'&'+tmp
    #先获得时间数组格式的日期
    three_day_ago = (datetime.datetime.now() - datetime.timedelta(days = DAY))
    daystr = three_day_ago.strftime("%Y-%m-%d")
    fayuangonggao = spyder
    result = []
    for i in range(1,2*DAY):
        data = gzdecode(fayuangonggao.get_htmldata(url.replace('****',str(i))))
        data = data[data.find('(')+1:-1]
        mydicts = json.loads(data)['objs']
        result += filter(lambda x:x['publishdate'] >= daystr,mydicts)
    return result
    
if __name__ == '__main__':
    filename = datetime.datetime.now().strftime(u"bankrupt_%Y-%m-%d.txt")
    f = open(filename,'w')
    fayuan = get_fayuangonggao()
    pochan = get_pochanzichan()
    foshan = get_foshan()
    f.write(u'佛山\n\n'.encode('gbk'))
    
    for s in foshan:
        f.write(s[0].encode('gbk')+','+s[1].encode('gbk')+'\n')
    f.write(u'*'*100+'\n\n')
    f.flush()
    f.write(u'破产资产网\n\n'.encode('gbk'))
    for s in pochan:
        f.write(s[0].encode('gbk')+','+s[1].encode('gbk')+','+s[2].encode('gbk')+'\n')
    f.write(u'*'*100+'\n\n')
    f.flush()
    f.write(u'法院网\n\n'.encode('gbk'))
    
    
    for s in fayuan:
        #print s
        for k,v in s.iteritems():
            if k == 'id':continue
            f.write(k.encode('gbk','ignore')+':'+v.encode('gbk','ignore')+';')
        f.write('\n')
    f.write(u'*'*100+'\n\n')
    f.close()
    
