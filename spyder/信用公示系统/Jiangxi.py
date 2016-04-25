#coding=utf-8
__author__ = 'Chen'

####################################################
#修改：李龚
#兼容2.*和3.*两个版本，同时处理字符串的编码问题
#江西省下载的程序作了较大的修改，原因是江西省下载的网址发生变化
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
import urlparse

class GetYCParser(YCParser):
    def getpostdata(self,pageNos):
        postdata=urlencode({
            'qymcandzch':'请输入企业名称、统一社会信用代码或注册号',
            'limit':'100',
            'page':'%d'% pageNos,
            'yzmSearch':''
        }).encode('utf-8')
        return postdata
    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>27492:break
                req= Request(
                    url='http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/ccjcgs_jyycmlIndex.pt',
                    data=self.getpostdata(pageNos),
                    headers={'User-Agent':'Magic Browser'}
                )
                result=self.gethtml(req)
                infolist=result.findAll('div',attrs={'class':'tb-b'})
                l=len(infolist)
                urllist=[info.find('a').get('href') for info in infolist]
                Namelist = [info.find('a').contents[0] for info in infolist]
                
            
                regIDlist=[info.find('li',attrs={'class':'tb-a2'}).contents[0] for info in infolist]
                datelist=[info.find('li',attrs={'class':'tb-a3'}).contents[0] for info in infolist]
                #nbxhlist=[info.find('input',attrs={'id':re.compile('nbxh')}).get('value') for info in infolist]
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
                            cdate=str(datelist[i]).strip()
                            reg_m=r'年(.*?)月'
                            reg_d=r'月(.*?)日'
                        except:
                            cdate=unicode(datelist[i]).strip()
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
                                href = urllist[i]
                                Name=Namelist[i].replace('\n','').strip()
                                if self.checkname(Name)==False:
                                    continue
                                entdict=dict(Name=Name,regID=regIDlist[i],Date=cdate,href=href)
                                self.PrintInfo(entdict)
                    except Exception:
                        self.printitemerror(pageNos,i)
                        traceback.print_exc()
                        continue
            if br==1:break

    def PrintInfo(self,ent):
        infourl='http://gsxt.jxaic.gov.cn/ECPS/ccjcgs/gsgs_viewJyycxx.pt?qyid=%s&zch=%s&qylx=%s'
    
        result = urlparse.urlparse(ent.get('href'))
        tmp = urlparse.parse_qs(result.query,True) 
        if not tmp.has_key('qylx'):
            tmp['qylx'] = ['']
        infourl = infourl %(tmp['qyid'][0],tmp['zch'][0],tmp['qylx'][0])
        req= Request(
            url=infourl,
            headers={'User-Agent':'Magic Browser'}
        )
        
        inforesult=self.gethtml(req)
        #print inforesult
        infolist=inforesult.find('table').findAll('td')
        #print ent.get('href'),infourl,infolist
        self.gendown(ent,infolist)

if __name__=='__main__':
    location='江西'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2013,11,1),enddate=date.today())