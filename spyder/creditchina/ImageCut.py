# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 17:33:17 2016

@author: gong

@description:这是用来截取图片的程序
"""
import commands
import os
from PIL import Image
from PIL import ImageEnhance
import traceback
class ImageCut(object):
    def __gen_crop_box__(width,):
        pass
    '''
    image_path: 输入文件
    outpath:输出文件
    background-position-x: -314px(一般小于0)
    background-position-y: -29px
    width: 77px
    height: 15px
    '''
    @staticmethod
    def cut(image_path,outpath,bgd_x,bgd_y,width,height):
        try:
            if not os.path.exists(image_path):
                print 'Image %s not exists!' % image_path
                return None
            image = Image.open(image_path)
            i_width,i_height = image.size
            left_x = abs(bgd_x)
            left_y = abs(bgd_y)
            right_x = left_x + width
            right_y = left_y + height
            box = (left_x,left_y,right_x,right_y)
            ImageCut.enhance(image).crop(box).save(outpath)
        except Exception,e:
            print e
            traceback.print_exc()
    
    
    #图像增强
    @staticmethod
    def enhance(image,factor=50.0):  
        image_contrast = ImageEnhance.Contrast(image).enhance(factor)  
        image_sharpness = ImageEnhance.Sharpness(image_contrast).enhance(factor)  
        return image_sharpness 
    
    #二值化
    @staticmethod
    def binarization(image,reverse = True):
        #灰度化
        image = image.convert("L") 
        pixsels = image.load()
        for x in range(1,image.width-1):
            for y in range(1,image.height-1):
                if reverse:
                    pixsels[x, y] = 0 if pixsels[x, y] < 25 else 255
                else:
                    pixsels[x, y] = 255 if pixsels[x, y] < 25 else 0
               
                
        return image
    
    #从图像中提取数字
    @staticmethod
    def get_data_from_image(image_path,enhance=False):
        image = Image.open(image_path)
        if enhance:
            image = ImageCut.binarization(image)
            image = ImageCut.enhance(image)
            image.save(image_path)
        
        command = '/usr/local/bin/tesseract %s %s' % (image_path,image_path+'tmp')
        commands.getoutput(command)
        f= open(image_path+'tmp.txt','r')
        data = f.read()
        f.close()
        os.remove(image_path+'tmp.txt')
        return data

if __name__ == '__main__':
    ImageCut.cut('/Users/gong/Desktop/qpema.jpg','/Users/gong/Desktop/qpema_2.jpg',-314,-29,77,15)
    print ImageCut.get_data_from_image('/Users/gong/Desktop/qpema_2.jpg',True)