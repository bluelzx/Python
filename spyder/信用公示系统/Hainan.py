#coding=utf-8
__author__ = 'Chen'

#有时可能无法读取经营异常数据
#（待清理）
########################################
#修改：李龚
#兼容2.*和3.*两个版本，同时处理字符串的编码问题
########################################
try:
    from urllib.request import Request
    from urllib.parse import urlencode
except:
    from urllib2 import Request
    from urllib import urlencode
    
import re
from datetime import *
from YCParser import YCParser
import time
import json

class GetYCParser(YCParser):

    def getpostdata(self,pageNos):
        postdata=urlencode({
            'pageNo':'%d'% pageNos,
            'textfield':''
        }).encode('utf-8')
        return postdata

    def getinfopostdata(self,ent):
        postdata=urlencode({
            'entNo':ent.get('entNo'),
            'entType':ent.get('entType')+'++',
            'regOrg':ent.get('regOrg')
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=-1
        while True:
            try:
                pageNos+=1
                if pageNos>6520:break
                time.sleep(1)
                req=Request(
                    url='http://aic.hainan.gov.cn:1888/aiccips/main/abnInfoList.html',
                    data=self.getpostdata(pageNos),
                    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
                             'Accept':'application/json, text/javascript, */*; q=0.01',
                             'Cookie':self.gen_cookie(),
                             'Content-Length':'19'}
                )
                result=self.gethtml(req)
                resultlist=json.loads(self.to_utf8(result.string))['rows']
            except Exception:
                self.printpageerror(pageNos+1)
                continue
            else:
                print('Page %d Reading' % (pageNos+1))
                br=0
                for result in resultlist:
                    try:
                        cdate=result['abnTimeStr']
                        cdate=date(int(cdate[0:4]),int(cdate[5:7]),int(cdate[8:10]))
                        if cdate<startdate:
                            br=1
                            break
                        else:
                            if cdate<=enddate:
                                Name=result['entName'].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                entdict=dict(Name=Name,reg=result['regNO'],entNo=result['entNo'],entType=result['entType'],regOrg=result['decOrg'])
                                self.PrintInfo(entdict,self.f)
                    except Exception:
                        self.printitemerror(pageNos,result)
                        continue
                if br==1:break

    def PrintInfo(self,ent,f):
        time.sleep(2)
        req=Request(
            url='http://aic.hainan.gov.cn:1888/aiccips/GSpublicity/GSpublicityList.html?service=cipUnuDirInfo',
            data=self.getinfopostdata(ent),
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
                     'Content-Length':'71',
                     'Cookie':self.gen_cookie(),
                     'Content-Type': 'application/x-www-form-urlencoded'})
        inforesult=self.gethtml(req)
        infolist=inforesult.findAll('td')
        l=int(len(infolist)/6)
        for j in range(l):
            f.write(self.to_utf8(ent.get('Name'))+'|')
            f.write(self.to_utf8(ent.get('reg').strip())+'|')
            for k in range(6):
                i=j*6+k
                infostr=infolist[i].contents
                if infostr:
                    infostr=infostr[0]
                    f.write(self.to_utf8(infostr.replace('\n','').strip()))
                f.write('|')
            f.write('\n')

if __name__=='__main__':
    location='海南'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,8,10),enddate=date.today()-timedelta(days=0))