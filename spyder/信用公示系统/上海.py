#coding=utf-8
__author__ = 'Han'

#只能获取50页的信息
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
import traceback
class GetYCParser(YCParser):

    def getpostdata(self,pageNos):
        postdata=urlencode({
            'captcha':'',
            'condition.pageNo':'%d'% pageNos,
            'condition.insType':'',
            'session.token':'9cf1c6b3-ed46-4eed-8acf-9421bf4e3e66',
            'condition.keyword':''
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>50:break
                req= Request(
                    url='https://www.sgs.gov.cn/notice/search/ent_except_list',
                    data=self.getpostdata(pageNos),
                        headers={
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding':'gzip, deflate',
                        'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4,zh-TW;q=0.2',
                        'Cache-Control':'max-age=0',
                        'Connection':'keep-alive',
                        'Content-Length':116,
                        'Content-Type':'application/x-www-form-urlencoded',
                        'Cookie':'JSESSIONID=0000JJz6VVLnhmrE_A_giMRfPqT:19307hbmg',
                        'Host':'www.sgs.gov.cn',
                        'Origin':'https://www.sgs.gov.cn',
                        'Referer':'https://www.sgs.gov.cn/notice/search/ent_except_list',
                        'Upgrade-Insecure-Requests':1,
                        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
                    }
                )
                result=self.gethtml(req)
                table=result.find('table')
                infolist=table.findAll('td')
                l=len(infolist)
            except Exception:
                self.printpageerror(pageNos)
                traceback.print_exc()
                continue
            else:
                print('Page %d Reading' % pageNos)
                br=0
                for i in range(2,l,3):
                    try:
                        try:
                            cdate=str(infolist[i].contents[0])
                            reg_m=r'年(.*?)月'
                            reg_d=r'月(.*?)日'
                        except:
                            cdate=unicode(infolist[i].contents[0])
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
                                Name=infolist[i-2].find('a').contents[0].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                regID=infolist[i-1].contents[0]
                                href=infolist[i-2].find('a').get('href')
                                entdict=dict(Name=Name,regID=regID,href=href)
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        infourl=ent.get('href')
        inforesult=self.gethtml(infourl)
        infolist=inforesult.find('table',attrs={'id':'exceptTable'}).findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='上海'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(1900,10,8),enddate=date.today()-timedelta(days=0),fmode='a')