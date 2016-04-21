# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 17:41:29 2016

@author: gong

@description: 这是用来读取pdf文档，生成txt文本的程序
"""
import logging
import traceback
from PyPDF2 import PdfFileReader

#日志格式设置
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')
    
class PDF_Processor(object):
    @staticmethod
    def read_pdf(filename,outname):
        try:
            f = open(outname,'w')
            pdf_file = PdfFileReader(file(filename, 'rb'))
            for page in pdf_file.pages:
                data = page.extractText()
                f.write(data.encode('utf-8','ignore'))
            f.close()
            
        except Exception,e:
            traceback.print_exc()
            logging.info('PDF_Processor -> read_pdf: %s!' % e)

if __name__ == '__main__':
    PDF_Processor.read_pdf('/Users/gong/Downloads/1201889667.pdf','/Users/gong/Downloads/1201889667.txt')