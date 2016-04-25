# -*- coding: utf-8 -*-
__author__ = 'Chen'

########################################################
#修改：2016-04-21
#修改人：李龚
#原因：主要是为了兼容python2.*和python3.*
########################################################
'''
import urllib.request
from urllib.error import HTTPError
from urllib.request import Request
'''
import bs4
from bs4 import BeautifulSoup
import re

try:
    from urllib.request import build_opener,HTTPRedirectHandler,Request
    from urllib.error import HTTPError
except:
    from urllib2 import build_opener,HTTPRedirectHandler,Request
    from urllib2 import HTTPError
    

class YCParser():

    def __init__(self):
        ################################################
        #做到兼容，同时加入cookies的模块
        ################################################
        try:
            from http.cookiejar import CookieJar
            from urllib.request import HTTPCookieProcessor
        except:
            from cookielib import CookieJar
            from urllib2 import HTTPCookieProcessor
        self.cookies = CookieJar()
        self.opener = build_opener(self.RedirectHandler,HTTPCookieProcessor(self.cookies))
        self.namecheck=[u'摊']
        self.DEBUG = True

    #解决自动重定向问题
    class RedirectHandler(HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            m = req.get_method()
            if (not (code in (301, 302, 303, 307) and m in ("GET", "HEAD")
                or code in (301, 302, 303, 307) and m == "POST")):
                raise HTTPError(req.full_url, code, msg, headers, fp)
            newurl = newurl.replace(' ', '%20')
            CONTENT_HEADERS = ("content-length", "content-type")
            newheaders = dict((k, v) for k, v in req.headers.items()
                              if k.lower() not in CONTENT_HEADERS)
            return Request(newurl,
                           headers=newheaders,
                           origin_req_host=req.origin_req_host,
                           unverifiable=True)

    def gethtml(self,req,retries=3,timeout=15):
        try:
            page=self.opener.open(req,timeout=timeout)
            
            html=BeautifulSoup(page.read(),"html.parser")
            return html
        except Exception as err:
            if retries>0:return self.gethtml(req, retries-1)
            else:raise err

    def GetYC(self,location,startdate,enddate,fmode='w',pagemode='w',itemmode='w'):
        self.f=open('D:\\GSXT\\'+location+'.txt',fmode)
        self.pageerror=open('D:\\GSXT\\ErrorPages\\'+location+'.txt',pagemode)
        self.itemerror=open('D:\\GSXT\\ErrorItems\\'+location+'.txt',itemmode)
        self.pageerrornum=0
        self.itemerrornum=0
        self.getentlist(startdate,enddate)
        self.f.close()
        self.pageerror.close()
        print('pageerrornum=',self.pageerrornum)
        print('itemerrornum=',self.itemerrornum)

    def printpageerror(self,pageNos):
        print('Page %d Failed' % pageNos)
        self.pageerrornum+=1
        self.pageerror.write(str(pageNos)+'\n')
        
        #ADD by LiGong
        if self.DEBUG:
            self.pageerror.flush()
    def printitemerror(self,pageNos,i):
        print('page %s item %s error!' %(pageNos,i))
        self.itemerrornum+=1
        self.itemerror.write(str(pageNos)+','+str(i)+'\n')
        
        #ADD by LiGong
        if self.DEBUG:
            self.itemerror.flush()

    def dealID(self,regID):
        reg=r'(\d+)'
        pattern=re.compile(reg)
        regID=pattern.findall(regID)[0]
        return regID

    def gendown(self,ent,infolist):
        l=int(len(infolist)/6)
        for j in range(l):
            ####################################
            #兼容python2.*的编码
            ####################################
        
            self.f.write(self.to_utf8(ent.get('Name'))+'|')
         
            self.f.write(self.to_utf8(ent.get('regID').strip())+'|')
            for k in range(6):
                i=j*6+k
                infostr=infolist[i].contents
                if infostr:
                    infostr=infostr[0]
                    
                    ###############################
                    #兼容python2.*的编码
                    ###############################
                    tmp = infostr.replace('\n','').strip()
                    if isinstance(tmp,unicode):
                        tmp = tmp.encode('utf8')
                    self.f.write(tmp+'|')
                else:
                    self.f.write('|')
            self.f.write('\n')
            
        #ADD by LiGong
        if self.DEBUG:
            self.f.flush()

    def checkname(self,name):
        if (len(name)<=3) or (name[-1] in self.namecheck):
            return False
        else:
            return True
    
    #add by Ligong
    def gen_cookie(self):
        '''获得cookies'''
        cookies_str = ''
        for cookie in self.cookies:
            cookies_str += cookie.name+'='+cookie.value+';'
        return cookies_str
        
    def to_utf8(self,mystr):
        if isinstance(mystr,int):
            return str(mystr)
        if isinstance(mystr,unicode):
            return mystr.encode('utf8','ignore')
        if isinstance(mystr,bs4.element.NavigableString):
            return unicode(mystr).encode('utf8','ignore')
        return mystr
        
