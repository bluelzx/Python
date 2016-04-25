#coding=utf-8
__author__ = 'Chen'

#有时存在重定向问题
#页数或无限增加
#如果遇到页面出错要刷新网页

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
#import http.cookiejar
import re
from datetime import *
from YCParser import YCParser
import traceback


class GetYCParser(YCParser):

    def getpostdata(self,pageNos):
        postdata=urlencode({
            'pageNo':'%d'% pageNos,
            'gjz':''
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>26619:break
                req=Request(
                    url='http://222.143.24.157/exceptionInfoSelect.jspx',
                    data=self.getpostdata(pageNos),
                    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'}
                )
                result=self.gethtml(req)
                infolist=result.findAll('a',attrs={'target':'_blank'})
                regIDlist=result.findAll('li',attrs={'class':'tb-a2'})
                datelist=result.findAll('li',attrs={'class':'tb-a3'})
                del regIDlist[0]
                del datelist[0]
                l=len(datelist)
            except Exception as err:
                self.printpageerror(pageNos)
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
                                regID=self.dealID(regIDlist[i].contents[0])
                                href=infolist[i].get('href')
                                entdict=dict(Name=Name,regID=regID,Date=cdate,href=href)
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        traceback.print_exc()
                        continue
                if br==1:break

    def PrintInfo(self,ent):
        req=Request(
            url='http://222.143.24.157'+ent.get('href'),
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'}
        )
        inforesult=self.gethtml(req)
        infolist=inforesult.find('table',attrs={'id':'excTab'}).findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='河南'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,11,1),enddate=date.today()-timedelta(days=0))


