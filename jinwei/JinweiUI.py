# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 14:57:04 2016

@author: gong

@description: 这是用来制作界面的程序
"""
from Tkinter import *
import tkMessageBox
top = Tk()
top.geometry('270x270+500+300')
#按钮生成图像的函数
def gen_image_callback():
   tkMessageBox.showinfo( "Hello Python", "Hello World")

L1 = Label(top, text=u'电话号码:')
L1.place(x = 0,y = 25,anchor = NW)

E1 = Entry(top, bd =5)
E1.place(x = 60,y = 20,anchor = NW)
gen_coupon = Button(top, text =u'生成券', command = gen_image_callback)
gen_coupon.pack()
top.mainloop()
