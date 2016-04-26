# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 10:49:35 2016

@author: gong

@description: 这是从网络上爬去上市公司新闻、公告数据的程序
"""
class CompanyTextDataDownloader(object):
    def __init__(self,name = 'CompanyTextDataDownloader'):
        self._name = name
    
    def is_myurl(self,url):
        '''判断是不是应该这个类来处理的网址链接'''
        return False

    def parse_list(self,html_data):
        '''这是解析列表页的函数，返回文章的链接列表'''
        pass
    
    def parse_detail(self,html_data):
        '''这是解析列表详情的函数，返回标题，时间，文本'''
        pass
    
    def next_list_url(self,url):
        '''获得下一个列表页的链接'''
        pass
    
