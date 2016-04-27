# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 10:08:31 2016

@author: gong

@description: 这是一个下载网页内容的程序
"""

import urllib2,urllib,cookielib
#from urllib2 import Request,HTTPError
from urllib2 import build_opener
from urllib2 import HTTPRedirectHandler
from urllib2 import HTTPCookieProcessor

'''
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
        return Request(newurl,headers=newheaders,
                       origin_req_host=req.origin_req_host,unverifiable=True)

proxy_support =
urllib2.ProxyHandler({'http':'http://XX.XX.XX.XX:XXXX'})
'''

class WebSpyder(object):
    def __init__(self,timeout=10):
        self.headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8,ja;q=0.6,en;q=0.4,zh-TW;q=0.2",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
            "Cookie":""
        }
        urllib2.socket.setdefaulttimeout(timeout)
        self.cookies = cookielib.CookieJar()
        self.opener = build_opener(HTTPRedirectHandler,HTTPCookieProcessor(self.cookies))
        urllib2.install_opener(self.opener)
    
    
    def gen_postdata(self,data_dict):
        '''生成post data'''
        return urllib.urlencode(data_dict).encode('utf-8')
    
    def get_cookies(self):
        '''获得cookies'''
        cookies_str = ''
        for cookie in self.cookies:
            cookies_str += cookie.name+'='+cookie.value+';'
        return cookies_str
    
    
    def get_htmldata(self,url,post_data=None,retries=3):
        '''返回HTML的数据'''
        result = None
        
        #设置http请求头
        self.headers['Cookie'] = self.get_cookies()
        self.opener.addheaders = [(k,v) for k,v in self.headers.iteritems()]
        try:
            if post_data:
                result = self.opener.open(url,self.gen_postdata(post_data)).read()
            else:
                result = self.opener.open(url).read()
            return result
        except Exception as err:
            if retries == 0:raise err
            return self.get_htmldata(url,post_data,retries-1)

if __name__ == '__main__':
    a= WebSpyder()
    a.get_htmldata('http://www.taobao.com')
    print a.get_cookies()
