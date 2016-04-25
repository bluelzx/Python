#coding=utf-8
__author__ = 'Chen'


########################################
#修改：李龚
#兼容2.*和3.*两个版本，同时处理字符串的编码问题
#以及添加cookies的问题
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
import json
import time

class GetYCParser(YCParser):

    def getinfopostdata(self,nbxh):
        postdata=urlencode({
            'c':'0',
            't':'33',
            'nbxh':nbxh
        }).encode('utf-8')
        return postdata

    def getpostdata(self,pageNos):
        postdata=urlencode({
            'pageNo':'%d'% pageNos,
            'pageSize':'50'
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        time.sleep(3)
        pageNos=0
        
        while True:
            pageNos+=1
            req=Request(
                url='http://gsxt.gzgs.gov.cn/addition/search!searchJyyc.shtml',
                data=self.getpostdata(pageNos),
                headers={'User-Agent':'Magic Browser',
                         'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
                         'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                         'Accept-Encoding':'gzip, deflate',
                         'X-Requested-With':'XMLHttpRequest',
                         'Referer':'http://gsxt.gzgs.gov.cn/addition/jyyc.jsp',
                         'Cookie':self.gen_cookie(),
                         'Content-Length':'20'
                        }
            )
            result=self.gethtml(req,timeout=100)
            if result=='Get Failed':
                self.printpageerror(pageNos)
                continue
            
            print('Page %d Reading' % pageNos)
            result=json.loads(self.to_utf8(result.string))
            result=result['data']
            br=0
            for res in result:
                try:
                    cdate = unicode(res['lrrq'])
                except:
                   cdate = str(res['lrrq'])

                reg=u'年(.*?)月'
                pattern=re.compile(reg)
                month=int(pattern.findall(cdate)[0])
                reg=u'月(.*?)日'
                pattern=re.compile(reg)
                day=int(pattern.findall(cdate)[0])
                cdate=date(int(cdate[0:4]),month,day)
                if cdate<startdate:
                    br=1
                    break
                else:
                    if cdate<=enddate:
                        Name=res['qymc'].replace('\n','').strip()
                        if self.checkname(Name)==False:continue
                        entdict=dict(Name=Name,nbxh=res['nbxh'],regID=res['zch'],date=cdate)
                        self.PrintInfo(entdict,self.f)
            if br==1:break

    def PrintInfo(self,ent,f):
        #time.sleep(3)
        req=Request(
            url='http://gsxt.gzgs.gov.cn/nzgs/search!searchData.shtml',
            data=self.getinfopostdata(ent['nbxh']),
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
                     'Host':'gsxt.gzgs.gov.cn',
                     'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
                     'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                     'Accept-Encoding':'gzip, deflate',
                     'X-Requested-With':'XMLHttpRequest',
                     'Referer':'http://gsxt.gzgs.gov.cn/nzgs/index.jsp',
                     'Cookie':self.gen_cookie(),
                     'Content-Length':'78',
                     'Connection':'keep-alive',
                     'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache'}
        )
        inforesult=self.gethtml(req)
        if inforesult=='Get Failed':
            print('Item Failed')
        else:
            infolist=json.loads(self.to_utf8(inforesult.string))['data']
            for info in infolist:
                f.write(self.to_utf8(ent.get('Name'))+'|')
                f.write(self.to_utf8(ent.get('regID'))+'|')
                f.write(self.to_utf8(info['rownum'])+'|')
                if info['lryy']:f.write(self.to_utf8(info['lryy']))
                f.write('|')
                f.write(self.to_utf8(info['lrrq']+'|'))
                if info['ycyy']:f.write(self.to_utf8(info['ycyy']))
                f.write('|')
                if info['ycrq']:f.write(self.to_utf8(info['ycrq']))
                f.write('|')
                f.write(self.to_utf8((info['zcjdjg'])+'|'))
                f.write('\n')

if __name__=='__main__':
    location='贵州'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,10,10),enddate=date.today()-timedelta(days=0))