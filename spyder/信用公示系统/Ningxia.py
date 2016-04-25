#coding=utf-8
__author__ = 'Chen'

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

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>1772:break
                req=Request(
                    url='http://gsxt.ngsh.gov.cn/ECPS/enterpriseAbnAction_enterpriseList.action?curr_Page='+str(pageNos),
                    headers={'User-Agent':'Magic Browser'}
                )
                result=self.gethtml(req)
                infolist=result.findAll('div',attrs={'class':'tb-b'})
                l=len(infolist)
                Namelist=[info.find('a').contents[0] for info in infolist]
                regIDlist=[info.find('li',attrs={'class':'tb-a2'}).contents[0] for info in infolist]
                datelist=[info.find('li',attrs={'class':'tb-a3'}).contents[0] for info in infolist]
                nbxhlist=[info.find('input',attrs={'id':re.compile('nbxh\d*')}).get('value') for info in infolist]
            except Exception:
                self.printpageerror(pageNos)
                continue
            else:
                print('Page %d Reading' % pageNos)
                br=0
                for i in range(l):
                    try:
                        try:
                            cdate=str(datelist[i])
                            reg_m=r'年(.*?)月'
                            reg_d=r'月(.*?)日'
                        except:
                            cdate=unicode(datelist[i])
                            reg_m=u'年(.*?)月'
                            reg_d=u'月(.*?)日'
                        print cdate
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
                                Name=Namelist[i].replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                entdict=dict(Name=Name,regID=regIDlist[i],Date=cdate,nbxh=nbxhlist[i])
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        traceback.print_exc()
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        infourl='http://gsxt.ngsh.gov.cn/ECPS/jyycxxAction_init.action?nbxh='+ent.get('nbxh')
        inforesult=self.gethtml(infourl)
        infolist=inforesult.find('table').findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='宁夏'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(1900,10,10),enddate=date.today()-timedelta(days=0))