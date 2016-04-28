# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 09:44:53 2016

@author: gong

@description:「信用中国」中图片信息的提取
"""
#import cv2

from ImageCut import ImageCut

'''
#图像处理
class ImageProcess(object):
    @staticmethod
    def foo(image_path):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
'''
    
class ImageInfoExtract(object):
    '''
    #获得工商注册号
    @staticmethod
    def get_company_number(image_path,outpath,leftx=80,lefty=0,width = 130,height=28):
        ImageCut.cut(image_path,outpath,leftx,lefty,width,height)
        return ImageCut.get_data_from_image(outpath)
    
    #获得注册资金
    @staticmethod
    def get_company_capital(image,leftx=65,lefty=65,width = 90,height=28):
        ImageCut.cut(image_path,outpath,leftx,lefty,width,height)
        return ImageCut.get_data_from_image(outpath)
        
    #获得成立时间
    @staticmethod
    def get_company_setup(image,leftx=65,lefty=130,width = 90,height=28):
        ImageCut.cut(image_path,outpath,leftx,lefty,width,height)
        return ImageCut.get_data_from_image(outpath)
    
    #获得审核时间
    @staticmethod
    def get_verifytime(image,leftx=65,lefty=260,width = 90,height=28):
        box = (leftx,lefty,leftx+width,lefty+height)
        return ImageCut.get_data_from_image(ImageCut.enhance(image.crop(box)))
    '''
    @staticmethod
    def get_company_info(image_path):
        outpath = image_path+'tmp.jpg'
        ImageCut.cut(image_path,outpath,80,10,130,12)
        number = ImageCut.get_data_from_image(outpath,True)
        
        ImageCut.cut(image_path,outpath,65,72,90,12)
        capital = ImageCut.get_data_from_image(outpath,True)
        
        ImageCut.cut(image_path,outpath,65,130,90,12)
        setuptime = ImageCut.get_data_from_image(outpath)
        
        ImageCut.cut(image_path,outpath,65,260,130,12)
        verifytime = ImageCut.get_data_from_image(outpath)
        print number,capital,setuptime,verifytime
        
        
if __name__ == '__main__':
    print ImageInfoExtract.get_company_info('/Users/gong/Desktop/basic_info_detail')
    
