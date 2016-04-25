#coding=utf-8
__author__ = 'Chen'

#日期顺序有问题
####################################################
#修改：李龚
#兼容2.*和3.*两个版本，同时处理字符串的编码问题
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
import time
import traceback
#import http.cookiejar

class GetYCParser(YCParser):

    def getinfopostdata(self,ent):
        postdata= urlencode({
            'method':'jyycInfo',
            'maent.pripid':ent.get('pri'),
            'czmk':'czmk6',
            'random':time.time()
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>13065:break
                req= Request(
                    url='http://xygs.snaic.gov.cn/xxcx.do?method=ycmlIndex&random='+str(time.time()*1000)+'&cxyzm=no&entnameold=&djjg=&maent.entname=&page.currentPageNo='+str(pageNos)+'&yzm=',
                    headers={'User-Agent':'Magic Browser'}
                )
                result=self.gethtml(req,timeout=200)
                infolist=result.findAll('a',attrs={'onclick':re.compile(r'javascript:doOpen*')})
                regIDlist=result.findAll('li',attrs={'class':'tb-a2'})
                datelist=result.findAll('li',attrs={'class':'tb-a3'})
                del regIDlist[0]
                del datelist[0]
                l=len(datelist)
            except Exception:
                self.printpageerror(pageNos)
                traceback.print_exc()
                continue
            else:
                print('Page %d Reading' % pageNos)
                br=0
                for i in range(l):
                    try:
                        try:
                            cdate=str(datelist[i].contents[0])
                            reg_m=r'年(.*?)月'
                            reg_d=r'月(.*?)日'
                        except:
                            cdate=unicode(datelist[i].contents[0])
                            reg_m=u'年(.*?)月'
                            reg_d=u'月(.*?)日'
                        pattern=re.compile(reg_m)
                        month=int(pattern.findall(cdate)[0])
                        
                        pattern=re.compile(reg_d)
                        day=int(pattern.findall(cdate)[0])
                        cdate=date(int(cdate[0:4]),month,day)
                        if cdate<startdate:
                            br=1
                            break
                        else:
                            if cdate<=enddate:
                                Name=infolist[i].contents[0].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                regID=regIDlist[i].contents[0]
                                pri=self.dealID(infolist[i].get('onclick'))
                                entdict=dict(Name=Name,regID=regID,Date=cdate,pri=pri)
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        req=Request(
            url='http://xygs.snaic.gov.cn/ztxy.do',
            data=self.getinfopostdata(ent),
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=self.gethtml(req)
        infolist=inforesult.find('table',attrs={'id':'table_yc'}).findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='陕西'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(1900,7,1),enddate=date.today()-timedelta(days=0))