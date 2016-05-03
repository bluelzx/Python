# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:38:32 2016

@author: gong

@description:截取图像
box = (179,156,1476,1133)
box = (179,1209,1476,977+1209)

"""
import os
from PIL import Image
import traceback

def cut_pic(image_path,box,index=1,path='/Users/gong/Documents/tmp/'):
    try:
        image = Image.open(image_path)
        image.crop(box).save(path+str(index)+'.jpg')
    except:
        traceback.print_exc()
    
if __name__ == '__main__':
    #box = (89,605,650+89,488+605)
    root = u'/Users/gong/Desktop/pic2/'
    #cut_pic(root+u'28号资料_页面_065.jpg',box)

    
    index = 119
    for i in os.listdir(root):
        if os.path.isfile(os.path.join(root,i)) and i.endswith('.jpg'):
            f = os.path.join(root,i)
            box1 = (89,79,650+89,488+79)
            #box1 = (179,156,1476,1133)
            #box2 = (179,1209,1476,977+1209)
            box2 = (89,605,650+89,488+605)
            cut_pic(f,box1,index)
            index += 1
            cut_pic(f,box2,index)
            index+=1

