#coding=utf-8
__author__ = 'Chen'
########################################################
#修改：2016-04-21
#修改人：李龚
#原因：主要是为了兼容python2.*和python3.*
########################################################
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
            'pageNo':'%d'% pageNos,
            'gjz':''
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            pageNos+=1
            if pageNos>19337:break
            try:
                req= Request(
                    url='http://www.ahcredit.gov.cn/exceptionInfoSelect.jspx',
                    data=self.getpostdata(pageNos),
                    headers={'User-Agent':'Magic Browser'}
                )
                result=self.gethtml(req)
                infolist=result.findAll('a',attrs={'target':'_blank'})
                regIDlist=result.findAll('li',attrs={'class':'tb-a2'})
                datelist=result.findAll('li',attrs={'class':'tb-a3'})
                del regIDlist[0]
                del datelist[0]
                l=len(datelist)
            except Exception:
                self.printpageerror(pageNos)
                continue
            else:
                print('Page %d Reading' % pageNos)
                br=0
                for i in range(l):
                    try:
                        ####################################################
                        #原因：在python3.*中不存在编码问题了，在python2.*中依然有编码问题
                        #修改：李龚
                        ####################################################
                        try:
                            cdate= str(datelist[i].contents[0])
                            reg_m=r'年(.*?)月'
                            reg_d=r'月(.*?)日'
                        except:
                            cdate = unicode(datelist[i].contents[0])
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
                                regID=self.dealID(regID)
                                href=infolist[i].get('href')
                                entdict=dict(Name=Name,regID=regID,Date=cdate,href=href)
                                self.PrintInfo(entdict)
                    except Exception as e:
                        print e
                        print traceback.print_exc()
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        req=Request(
            url='http://www.ahcredit.gov.cn'+ent.get('href'),
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=self.gethtml(req)
        infolist=inforesult.find('table',attrs={'id':'excTab'}).findAll('td')
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='安徽'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,01,1),enddate=date.today())
