# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 18:36:37 2016

@author: gong

@description: 这是从word文档里面抽取数据的程序，继承Alphabet_Data_Extractor类

"""
import logging
import zipfile
import traceback
import xml


from Alphabet_Data_Extractor import Alphabet_Data_Extractor
class Word_Alphabet_Data_Extractor(Alphabet_Data_Extractor):
    def __init__(self,logger, log_level=logging.INFO):
        self.name = 'Word Alphabet Data Extractor'
        self.logger = logger
        self.log_level = log_level
        
    def extract_data(self,infile,outfile = None):
        try:
            document = zipfile.ZipFile(infile)

            xml_content = document.read('word/document.xml')
            reparsed = xml.dom.minidom.parseString(xml_content)
            print reparsed.toprettyxml(indent="   " , encoding="utf-8")
        
        except Exception,e:
            #self.logger.log(self.log_level, e)
            print traceback.print_exc()

if __name__ == '__main__':
    word = Word_Alphabet_Data_Extractor(None)
    
    word.extract_data(u'/Users/gong/Documents/论文终极材料/上海交通大学硕士学位论文——终稿.docx')