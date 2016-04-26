# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 17:33:17 2016

@author: gong

@description:这是用来截取图片的程序
"""
import os
from PIL import Image
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
            left_x = -bgd_x
            left_y = -bgd_y
            right_x = left_x + width
            right_y = left_y + height
            box = (left_x,left_y,right_x,right_y)
            image.crop(box).save(outpath)
            
        except Exception,e:
            print e
            traceback.print_exc()
            
    def get_data_from_image(image_path):
        

if __name__ == '__main__':
    ImageCut.cut()