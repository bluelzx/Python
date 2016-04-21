# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 16:45:58 2016

@author: gong

@description:这是运行爬虫的程序
"""
import Queue
from WebSpyder import WebSpyder

#运行下载程序的爬虫 
class Spyder_Runner(object):
    def __init__(self,parser,name='Spyder_Runner'):
        self.name = name
        #列表也页面的任务
        self.list_jobs = Queue.Queue(maxsize = 100)
        
        #详情页面的任务
        self.detail_jobs = Queue.Queue(maxsize = 10000)
        
        #下载的爬虫
        self.downloader = WebSpyder()
        
        #解析的程序
        self.parser = parser
        
    #添加任务
    def add_list_job(self,list_url):
        if self.parser.is_myurl(list_url):
            self.list_jobs.put(list_url)
    
    #是否要加入list表
    def __is_add_to_list_job__(self,list_url):
        return True
    
    #添加详情页面任务
    def add_detail_job(self,details):
        for detail in filter(lambda x:self.parser.is_myurl(x),details):
            self.add_detail_job.put(detail)
            
    #运行
    def run(self):
        while True:
            #处理列表页
            try:
                list_url = self.list_jobs.get(timeout = 5)
                if list_url:
                    htmldata = self.downloader.get_htmldata(list_url)
                    self.add_detail_job(self.parser.parse_list(htmldata))
                    
                    #获得下一个列表网址
                    next_list_url = self.parser.next_list_url(list_url)
                    
                    #判断是不是需要加入的下载列表中去
                    if self.__is_add_to_list_job__(next_list_url):
                        self.add_list_job(next_list_url)
            except Exception as e:
                print e
            
            #处理详情页
            try:
                while self.detail_jobs.qsize() > 0:
                    detail = self.detail_jobs.get(timeout=5)
                    if detail:
                        print self.parser.parse_detail(detail)
                    
            except Exception as e:
                print e
                
        
if __name__ == '__main__':
    pass
