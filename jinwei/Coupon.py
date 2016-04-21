# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 11:41:49 2016

@author: gong

@description: 这是用来生成券的程序
"""
import md5
import traceback
from PIL import Image, ImageFont, ImageDraw

class Coupon(object):
    def __init__(self,seller,seller_qr):
        '''
        这是初始化函数:
        seller:卖家微信号
        seller_qr:卖家微信二维码路径
        '''
        self.seller = seller
        self.seller_qr = seller_qr
        self.width = 386
        self.logo_img = 'logo.png'
    
    def gen_code(self,phone_num,buyer,price):
        '''
        这是生成信息编号的函数
        phone_num:买家手机号
        buyer:买家名字
        price:产品价格
        '''
        try:
            tmp_md5 = md5.new()
            #生成号码的MD5
            tmp_md5.update(str(phone_num))
            n_code = tmp_md5.hexdigest()
            
            #生成买家的MD5
            tmp_md5.update(str(buyer))
            b_code= tmp_md5.hexdigest()
            
            #生成卖家的MD5
            tmp_md5.update(str(self.seller))
            s_code= tmp_md5.hexdigest()
            
            #成价格的MD5
            tmp_md5.update(str(price))
            p_code= tmp_md5.hexdigest()
            
            
            tmp_md5.update(str(n_code+b_code+s_code+p_code))
            total_code = tmp_md5.hexdigest()
            result = unicode()
            for i in range(len(total_code)/2):
                result += unicode(hex(int(total_code[i*2:i*2+2],16) % 16))[2:]
            
            answer = unicode()
            for i in range(len(result)):
                answer += result[i]
                if i % 4 == 3 and i != len(result)-1:
                    answer += u'-'
            return answer.upper()
        except Exception,e:
            traceback.print_exc()
            print 'gen_code error: %s !' % e
            return None
            
            
    def gen_code_image(self,code,price):
        '''
        生活码的图片
        '''
        try:
            im = Image.open('product.jpg')
            #im = Image.new("RGB", (self.width, 200), (255, 255, 255))
            dr = ImageDraw.Draw(im)
            font = ImageFont.truetype('华文楷体.ttf', 28)
            text_product = unicode(price)
            text_seller = unicode(self.seller)
            text_code = unicode(code)
            dr.text((self.width*0.22, 25), text_code, font=font, fill="#000000")
            dr.text((self.width*0.22, 118), text_seller, font=font, fill="#000000")
            dr.text((self.width*0.38, 70), text_product, font=ImageFont.truetype('华文行楷.ttf', 40), fill="#ff0000")
            return im
        except Exception,e:
            traceback.print_exc()
            print 'gen_code_image error: %s !' % e
            return None
    
    
    def gen_total_image(self,code,price,out):
        '''
        这是用来生成最后图片的程序
        code,price:用来生成编码的图片
        logo_img:logo的图片
        seller_img:卖家的二维码
        '''
        try:
            logo = Image.open(self.logo_img)
            seller = Image.open(self.seller_qr)
            code = self.gen_code_image(code,price)
            
            hight_1 = logo.size[1]
            box_1 = (0, 0, logo.size[0], logo.size[1])
            
            hight_2 = code.size[1]
            box_2 = (0, logo.size[1], code.size[0], code.size[1]+logo.size[1])
             
            hight  = int(float(seller.size[1])/float(seller.size[0])*self.width*0.8)
            total_hight = hight_1 + hight_2 + hight + 20
            
            
            img = Image.new("RGB", (self.width, total_hight), (255, 255, 255))
            
            img.paste(logo,box_1)
            img.paste(code,box_2)
            
            width = int(self.width*0.8)
            
            seller = seller.resize((width,hight))
            left = (self.width - width)/2
            up = code.size[1]+logo.size[1]
            right = left+seller.size[0]
            down = up+seller.size[1]
            box_3 = (left,up,right,down)
            img.paste(seller,box_3)
            #img.show()
            img.save(out)
        except Exception,e:
            traceback.print_exc()
            print 'gen_total_image error: %s !' % e
            
if __name__ == '__main__':
    cp = Coupon('ligong1992','seller.png')
    print cp.gen_code(1,2,3)
    cp.gen_total_image('907C-6BE9-BEF0-7F5F',299,'/Users/gong/Documents/aa.jpg')
