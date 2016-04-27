# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 09:08:19 2016

@author: gong

@description:这是用来在11315上查询的程序爬虫
"""
import bs4
import json
import urllib
from WebSpyder import WebSpyder
from BrowserSpyder import BrowserSpyder
from detail import ParseDetail  
import StringIO, gzip
import traceback
  

class ZhengXin11315(object):
    def __init__(self,spyder = None):
        self.spyder = spyder
        if not self.spyder:
            self.spyder = WebSpyder()
        self.dictionary = {
                    u"北京": ("110000", u"北京市"), u"天津": ("120000", u"天津市"), u"河北": ("130000", u"河北省"), u"山西": ("140000", u"山西省"),u"内蒙古": ("150000", u"内蒙古"),
                    u"辽宁": ("210000", u"辽宁省"), u"吉林": ("220000", u"吉林省"), u"黑龙江": ("230000", u"黑龙江省"),
                    u"上海": ("310000", u"上海市"), u"江苏": ("320000", u"江苏省"), u"浙江": ("330000", u"浙江省"), u"安徽": ("340000", u"安徽省"), u"福建": ("350000", u"福建省"), u"江西": ("360000", u"江西省"), u"山东": ("370000", u"山东省"),
                    u"河南": ("410000", u"河南省"), u"湖北": ("420000", u"湖北省"), u"湖南": ("430000", u"湖南省"), u"广东": ("440000", u"广东省"), u"广西": ("450000", u"广西"), u"海南": ("460000", u"海南省"),
                    u"重庆": ("500000", u"重庆市"), u"四川": ("510000", u"四川省"), u"贵州": ("520000", u"贵州省"), u"云南": ("530000", u"云南省"), u"西藏": ("540000", u"西藏"),
                    u"陕西": ("610000", u"陕西省"), u"甘肃": ("620000", u"甘肃省"), u"青海": ("630000", u"青海省"), u"宁夏": ("640000", u"宁夏"), u"新疆": ("650000", u"新疆"),
                    "":"",
                    }
        
    #最长公共子串
    def max_substring(self, strA, strB):
        #计算呈现条目与搜索企业的相似度
        lenA, lenB = len(strA), len(strB)
        c = [[0 for i in range(lenB)] for j in range(lenA)]
        
        #初始化
        for i in range(lenB):
            if strA[0] == strB[i]:c[0][i] = 1
            else:c[0][i] = 0 if i == 0 else c[0][i-1]
        
        for i in range(lenA):
            if strA[i] == strB[0]:c[i][0] = 1
            else:c[i][0] = 0 if i== 0 else c[i-1][0]
        
        for i in range(1,lenB):
            for j in range(1,lenA):
                if strA[j] == strB[i]:c[i][j] = 1+c[i-1][j-1]
            else:c[i][j] = max(c[i][j-1],c[i-1][j])
        
        return c[lenB-1][lenA-1]
    
    #解压gzip  
    def gzdecode(self,data) :  
        compressedstream = StringIO.StringIO(data)  
        gziper = gzip.GzipFile(fileobj=compressedstream)    
        data2 = gziper.read()   # 读取解压缩后数据   
        return data2
        
    #编辑距离
    def string_distance(self, strA, strB):
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
    
    def get_content(self, name, province=''):
        url = "http://www.11315.com/newSearch?regionMc=%s&regionDm=%s&searchType=1&searchTypeHead=1&name=%s"
        
        keyword_n = urllib.quote(name.encode('utf-8'))
        keyword_p = ''
        keyword_id = ''
        if province:
            region = self.dictionary[province]
            keyword_p = urllib.quote(region[1].encode('utf-8'))
            keyword_id = region[0]
        
        url = url % (keyword_p ,keyword_id ,keyword_n)
        if isinstance(self.spyder,WebSpyder):
            return self.gzdecode(self.spyder.get_htmldata(url))
        else:
            return self.spyder.get_htmldata(url)
        
    def match(self, content, name):
        #找出最可能匹配的条目
        distance = []
        records = [i for i in content.find_all("div") if i["class"][0] == u"innerBox"]
        for i in records:
            distance.append(self.string_distance(name, i.find_all("a")[1].text))
        target = 0
        mindis = len(name)
        for i in range(len(records)):
            if distance[i] < mindis:
                mindis = distance[i]
                target = i
        
        #信用网址，之后抓取此页
        crediturl = records[target].find_all("td")[1].text.strip()
        delegate = records[target].find_all("td")[2].text.strip()       #法人在之后的页面通常为一图片，这里提前把文本抓好
                
        return crediturl, delegate
        
    #写入到文件
    def to_file(self,dict_data,filename):
        for k,v in dict_data.iteritems():
            print k,v
        f = open(filename,'a')
        f.write(json.dumps(dict_data).encode('utf8')+'\n')
        f.close()
        
    #Query类的包裹函数
    def search(self,name,outfile, province=''):
        try:
            #if province=='': province = "选择地区"
            #return query.get_content()
            html = self.get_content(name, province)

            if html.find(u'系统检测到您的请求存在异常') >= 0:
                print u'IP被网站封了，oh yeah！\n'
                return None
            content = bs4.BeautifulSoup(html, "html.parser").find("div", id="main")
            
            records_num = int(content.find("p").a.text)
            if records_num==0: return -1 #未查询成功
            
            crediturl, delegate = self.match(content, name) #delegate尚未用到
            
            if isinstance(self.spyder,WebSpyder):
                creditdata = self.gzdecode(self.spyder.get_htmldata(crediturl))
            else:
                creditdata = self.spyder.get_htmldata(crediturl)
            
            if creditdata.find(u'系统检测到您的请求存在异常') >= 0:
                print u'IP被网站封了，oh yeah！\n'
                return None
            #print creditdata
            result_1 = ParseDetail.parse_datail(creditdata)
            if isinstance(self.spyder,WebSpyder):
                deepdata = self.gzdecode(self.spyder.get_htmldata(crediturl+result_1[u'更多信息']))
            else:
                deepdata = self.spyder.get_htmldata(crediturl+result_1[u'更多信息'])
            
            result_2 = ParseDetail.deep_detail(deepdata)
            result_1[u'企业法人'] = delegate
            result_1[u'主营产品'] = result_2[u'主营产品']
            result_1[u'公司介绍'] = result_2[u'公司介绍']
            result_1.iteritems
            self.to_file(result_1,outfile)
        except:
            traceback.print_exc()
        
if __name__ == '__main__':
    zhengxin = ZhengXin11315(BrowserSpyder())
    zhengxin.search(u"平安", '/Users/gong/Documents/aaa.txt')
        