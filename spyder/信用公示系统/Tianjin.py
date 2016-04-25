#coding=utf-8
__author__ = 'Chen'

#如果读取post异常，使用浏览器刷新网页或“编辑与重发”
####################################################
#修改：李龚
#兼容2.*和3.*两个版本，同时处理字符串的编码问题
#tobe continue
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

    def changedate(self,fdate):   #处理日期格式
        if (fdate.find(u'年')==-1)&(fdate.find('-')==-1):
            cdate=date(int(fdate[0:4]),int(fdate[4:6]),int(fdate[6:8]))
        else:
            if fdate.find('-')!=-1:
                fdate=fdate.replace('-',u'年',1)
                fdate=fdate.replace('-',u'月',1)
                fdate=fdate+u'日'
            
            reg=u'年(.*?)月'
            pattern=re.compile(reg)
            month=int(pattern.findall(fdate)[0])
            reg=u'月(.*?)日'
            pattern=re.compile(reg)
            day=int(pattern.findall(fdate)[0])
            cdate=date(int(fdate[0:4]),month,day)
        return cdate

    def getpostdata(self,pageNos):
        postdata= urlencode({
            'searchContent':'',
            'page':'%d'% pageNos
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>18678:break
                req= Request(
                    url='http://tjcredit.gov.cn/platform/saic/exclist.ftl',
                    data=self.getpostdata(pageNos),
                    headers={'User-Agent':'Magic Browser'}
                )
                result=self.gethtml(req)
                infolist=result.findAll('li',attrs={'class':'tb-a1'})
                datelist=result.findAll('li',attrs={'class':'tb-a3'})
                l=len(datelist)
                del infolist[0]
                del datelist[0]
            except Exception:
                self.printpageerror(pageNos)
                traceback.print_exc()
                continue
            else:
                print('Page %d Reading' % pageNos)
                k=0
                for i in range(l):
                    try:
                        try:
                            cdate=str(datelist[i].contents[0])
                        except:
                            cdate=unicode(datelist[i].contents[0])
                        cdate=self.changedate(cdate)
                        if (cdate>=startdate)&(cdate<=enddate):
                            Name=infolist[i].find('a').contents[0].replace('\n','').strip()
                            if self.checkname(Name)==False:continue
                            href=infolist[i].find('a').get('href')
                            reg=r'entId=(.*)'
                            pattern=re.compile(reg)
                            entId=pattern.findall(href)[0]
                            entdict=dict(Name=Name,entId=entId)
                            self.PrintInfo(entdict,self.f)
                        if cdate<startdate:
                            k=1
                            break
                    except Exception:
                        self.printitemerror(pageNos,i)
                        traceback.print_exc()
                        continue
            if k==1:break

    def PrintInfo(self,ent,f):
        #取得注册号
        infourl='http://tjcredit.gov.cn/platform/saic/viewBaseExc.ftl?entId='+ent.get('entId')
        inforesult=self.gethtml(infourl)
        id=inforesult.findAll('span')[1].contents[0][5:]
    #取得经营异常信息
        infourl='http://tjcredit.gov.cn/platform/saic/baseInfo.json?entId='+ent.get('entId')+'&departmentId=scjgw&infoClassId=qyjyycmlxx'
        inforesult=self.gethtml(infourl)
        infolist=inforesult.findAll('td',attrs={'class':''})
        l=int(len(infolist)/6)
        for j in range(l):
            f.write(self.to_utf8(ent.get('Name'))+'|')
            f.write(id+'|')
            for k in range(6):
                i=j*6+k
                infostr=infolist[i].contents
                if infostr:
                    infostr=infostr[0]
                    #if isinstance(infostr,)
                    if i==2:
                        tmp = str(self.changedate(unicode(infostr)))
                        f.write(tmp)
                    else:f.write(self.to_utf8(infostr.replace('\n','').strip()))
                f.write('|')
            f.write('\n')
            f.flush()


if __name__=='__main__':
    location='天津'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2013,11,1),enddate=date.today()-timedelta(days=0))
