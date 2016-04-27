# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:46:15 2016

@author: gong

@description:这是用浏览器来抓取数据的程序
"""

#########################################################
#这里需要安装对应的浏览器驱动，并添加到路径
#笔者已经安装了chromedriver和phantomjs
#brew install chromedriver
#brew install phantomjs
#########################################################
import os
from selenium import webdriver
class BrowserSpyder(object):
    def __init__(self,brower_type='chromedriver'):
        self.brower_type = brower_type
        self.driver = None
        if 'chromedriver' == brower_type.lower():
            #添加chromedriver的路径
            chromedriver = '/usr/local/bin/chromedriver'
            os.environ['webdriver.chrome.driver'] = chromedriver
            self.driver = eval('webdriver.Chrome(chromedriver)')
        elif 'phantomjs' == brower_type.lower():
            #添加phantomjs的路径
            phantomjs = '/usr/local/bin/phantomjs'
            os.environ['webdriver.phantomjs.driver'] = phantomjs
            self.driver = eval('webdriver.PhantomJS(phantomjs)')
        elif 'firefox' == brower_type.lower():
            self.driver = eval('webdriver.Firefox()')
    #获得内容
    def get_htmldata(self,url):
        self.driver.get(url)
        return self.driver.page_source
    
    #退出
    def quit(self):
        self.driver.quit()

if __name__ == '__main__':
    b = BrowserSpyder('PhantomJS')
    print b.get_htmldata('http://www.11315.com/newSearch?regionMc=%E5%8C%97%E4%BA%AC%E5%B8%82&searchType=1&regionDm=110000&searchTypeHead=1&name=%E4%B8%AD%E5%9B%BD%E5%B9%B3%E5%AE%89')
    b.quit()
