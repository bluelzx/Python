#coding=utf-8
__author__ = 'Chen'

#如果程序异常，手动更换cookie和token
#日期顺序混乱

####################################################
#修改：李龚
#兼容2.*和3.*两个版本，同时处理字符串的编码问题
#需要进一步修改，先放着
#####################################################
try:
    from urllib.request import Request
    from urllib.parse import urlencode
except:
    from urllib2 import Request
    from urllib import urlencode

import re
from datetime import *
from YCParser import YCParser
import json
import traceback

class GetYCParser(YCParser):

    def getpagepostdata(self,pageNos):
        postdata=urlencode({
            'page':'%d'% pageNos,
        }).encode('utf-8')
        return postdata

    def getinfopostdata(self,encrpripid):
        postdata=urlencode({
            'encrpripid':encrpripid
        }).encode('utf-8')
        return postdata

    def setdate(self,date_json):
        if not date_json:return ""
        day=date_json['date']
        month=date_json['month']+1
        year=date_json['year']+1900
        return date(year,month,day)

    def getentlist(self,startdate,enddate):
        pageNos=0
        #X-CSRF-TOKEN
        self.token='51347c65-cfff-4e35-9dfb-7e5d7b236d13'
        self.cookie='SESSIONID=FC0E8549ECD1F0E0E73DDE3F74B90A2E; ROBOTCOOKIEID=c7603451d4f7dc258ed4a1c09870af740897dd92; SECSESSIONID=8aa0b8ad43d5cfc2f0a53b468a54fda7; CNZZDATA1000300906=1793994023-1461558412-http%253A%252F%252F211.141.74.198%253A8081%252F%7C1461569261'
        while True:
            try:
                pageNos+=1
                if pageNos>7090:break
                req=Request(
                    url='http://211.141.74.198:8081/aiccips/pub/jyyc',
                    data=self.getpagepostdata(pageNos),
                    headers={
                    'Accept':'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding':'gzip, deflate',
                    'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4,zh-TW;q=0.2',
                    'Cache-Control':'max-age=0',
                    'Connection':'keep-alive',
                    'Content-Length':6,
                    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                    'Cookie':'JSESSIONID=FC0E8549ECD1F0E0E73DDE3F74B90A2E; ROBOTCOOKIEID=c7603451d4f7dc258ed4a1c09870af740897dd92; SECSESSIONID=8aa0b8ad43d5cfc2f0a53b468a54fda7; CNZZDATA1000300906=1793994023-1461558412-http%253A%252F%252F211.141.74.198%253A8081%252F%7C1461569261',
                    'Host':'211.141.74.198:8081',
                    'Origin':'http://211.141.74.198:8081',
                    'Referer':'http://211.141.74.198:8081/aiccips/pub/abnormalrecordindex',
                    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
                    'X-CSRF-TOKEN':'51347c65-cfff-4e35-9dfb-7e5d7b236d13',
                    'X-Requested-With':'XMLHttpRequest'
                    }
                )
                result=self.gethtml(req)
                jsonlist=json.loads(str(result))
            except Exception:
                self.printpageerror(pageNos)
                traceback.print_exc()
                continue
            else:
                print('Page %d Reading' % pageNos)
                br=0
                for i,jsonre in enumerate(jsonlist):
                    try:
                        cdate=self.setdate(jsonre['abntime'])
                        if cdate<startdate:
                            br=1
                            break
                        else:
                            if cdate<=enddate:
                                Name=jsonre['entname'].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                entdict=dict(Name=Name,pri=jsonre['pripid'],reg=jsonre['regno'],type=jsonre['enttype'])
                                self.PrintInfo(entdict,self.f)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        traceback.print_exc()
                        continue
            if br==1:break

    def PrintInfo(self,ent,f):
        req=Request(
            url='http://211.141.74.198:8081/aiccips/pub/jyyc/'+ent.get('type'),
            data=self.getinfopostdata(ent.get('pri')),
            headers={
                'Accept':'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4,zh-TW;q=0.2',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                #'Content-Length':'107',
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie':self.cookie,
                'Host':'211.141.74.198:8081',
                'Origin':'http://211.141.74.198:8081',
                'Referer':'http://211.141.74.198:8081/aiccips/pub/gsgsdetail/1130/33559830d02af9fb9f6fb404de44d410e31bb39654fb06dab94747f8621642ad1d5eec624be9b88698011ee9cbf73959',
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
                'X-CSRF-TOKEN':self.token,
                'X-Requested-With':'XMLHttpRequest'
            }
        )
        inforesult=str(self.gethtml(req))
        infolist=json.loads(inforesult)
        l=len(infolist)
        for i in range(l):
            f.write(self.to_utf8(ent.get('Name')+'|'))
            f.write(self.to_utf8(ent.get('reg')+'|'))
            f.write(str(i+1)+'|')
            f.write(self.to_utf8(infolist[i]['specause']+'|'))
            f.write(str(self.setdate(infolist[i]['abntime']))+'|')
            f.write(infolist[i]['remexcpres']+'|')
            f.write(str(self.setdate(infolist[i]['remdate']))+'|')
            f.write(self.infolist[i]['decorg']+'|')
            f.write('\n')

if __name__=='__main__':
    location='吉林'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,11,1),enddate=date.today())
