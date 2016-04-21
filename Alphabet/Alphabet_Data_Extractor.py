# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 18:25:29 2016

@author: gong

@description: 这是从不同文本中抽取数据的类
"""
import os
class Alphabet_Data_Extractor(object):
    def __init__(self,jar_path='Alphatbet_Data_Extractor.jar'):
        self.name = 'Alphabet Data Extractor'
        self.path = jar_path
        
    def extract_data(self,infile,outfile):
        command = 'java -jar Alphatbet_Data_Extractor.jar %s %s' % (infile,outfile)
        tmp = os.popen(command).readlines()
        print tmp


if __name__ == '__main__':
    Alphabet_Data_Extractor().extract_data('/Users/gong/Downloads/16ggkkj_zzfrm_006_0402_j.doc','/Users/gong/Documents/a.txt')

