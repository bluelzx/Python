#coding=utf-8
__author__ = 'Chen'
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
import json
import traceback

class GetYCParser(YCParser):

    def getinfopostdata(self,id,type,name,entId):
        if name:name=name.encode('utf-8')
        postdata=urlencode({
            'id':id,
            'type':type,
            'name':name,
            'seljyyl':'true',
            'entId':entId
        }).encode('utf-8')
        return postdata

    def getentlist(self,startdate,enddate):
        pageNos=0
        while True:
            try:
                pageNos+=1
                if pageNos>7824:break
                url='http://gsxt.cqgs.gov.cn/search_searchjyyc.action?currentpage='+str(pageNos)+'&itemsperpage=10'
                result=self.gethtml(url)
                result=json.loads(str(result))
                br=0
            except Exception:
                self.printpageerror(pageNos)
                continue
            else:
                print('Page %d Reading' % pageNos)
                for i,jyyc in enumerate(result['jyyclist']):
                    try:
                        cdate=jyyc['_date']
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
                                Name=jyyc.get('_name').replace('\n','').strip()
                                if self.checkname(Name)==False:continue
                                entdict=dict(Name=Name,regID=jyyc.get('_regCode'),Date=cdate,ID=jyyc.get('_pripid'),entType=jyyc.get('_entType'))
                                self.PrintInfo(entdict,self.f)
                    except Exception as e:
                        print e
                        traceback.print_exc()
                        self.printitemerror(pageNos,i)
                        continue
            if br==1:break

    def PrintInfo(self,ent,f):
        #post方法获取type值，然后采用get方法
        req=Request(
            url='http://gsxt.cqgs.gov.cn/search_ent',
            data=self.getinfopostdata(ent.get('regID'),ent.get('entType'),ent.get('Name'),ent.get('ID')),
            headers={'User-Agent':'Magic Browser'}
        )
        inforesult=self.gethtml(req).find('body',attrs={'ng-controller':'frameCtrl'})
        inforesult=str(inforesult)
        reg=r'data-type=\"(\d)*\"'
        pattern=re.compile(reg)
        type=pattern.findall(inforesult)[0]
        infourl='http://gsxt.cqgs.gov.cn/search_getEnt.action?entId='+ent.get('ID')+'&id='+ent.get('regID')+'&type='+type
        inforesult=str(self.gethtml(infourl))
        #提取Entity页面内的经营异常信息
        reg=r'"qyjy":\[(.*)\]'
        pattern=re.compile(reg)
        qyjy=pattern.findall(inforesult)[0]
        reg=r'\{(.*?)\}'
        pattern=re.compile(reg)
        infolist=pattern.findall(qyjy)
        l=len(infolist)
        for i in range(l):
            if ent.get('Name'):
                f.write(self.to_utf8(ent.get('Name'))+'|')
            else:f.write('|')
            if ent.get('regID'):
                f.write(self.to_utf8(ent.get('Name'))+'|')
            else:f.write('|')
            f.write(str(i+1)+'|')
            info=infolist[i]
            reg=r'"specause":"(.*?)"'
            pattern=re.compile(reg)
            inreason=pattern.findall(info)
            f.write(self.to_utf8(inreason[0])+'|')
            reg=r'"abntime":"(.*?)"'
            pattern=re.compile(reg)
            intime=pattern.findall(info)
            f.write(self.to_utf8(intime[0])+'|')
            reg=r'"remexcpres":"(.*?)"'
            pattern=re.compile(reg)
            outreason=pattern.findall(info)
            if outreason:f.write(self.to_utf8(outreason[0]))
            f.write('|')
            reg=r'"remdate":"(.*?)"'
            pattern=re.compile(reg)
            outtime=pattern.findall(info)
            if outtime:f.write(self.to_utf8(outtime[0]))
            f.write('|')
            reg=r'"decorg":"(.*?)"'
            pattern=re.compile(reg)
            org=pattern.findall(info)
            f.write(self.to_utf8(org[0])+'|')
            f.write('\n')


if __name__=='__main__':
    location='重庆'
    YCParser=GetYCParser()
    YCParser.GetYC(location,startdate=date(2015,11,1),enddate=date.today())
