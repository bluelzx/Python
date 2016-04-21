# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 18:12:48 2016

@author: gong

@description: 这是用来分割text文档的程序
"""
import logging
import traceback
class TextSpliter(object):
    def __init__(self,logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        
    def split(self,filename,path):
        try:
            f = open(filename,'r')
            data = f.read()
            f.close()
            for i,myfile in enumerate(data.split('▲Top')):
                myfilename = path+'/data_'+str(i)+'.txt'
                f = open(myfilename,'w')
                f.write(myfile)
                f.close()
        except Exception,e:
            self.logger.log(self.log_level, e)
            traceback.print_exc()

if __name__ == '__main__':
    TextSpliter(None).split('/Users/gong/Desktop/aaa.txt','/Users/gong/Desktop/bb')