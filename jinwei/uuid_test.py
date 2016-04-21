# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 20:21:38 2016

@author: gong

@description: 这是用来生成特定编码的程序
"""

import uuid

if __name__ == '__main__':
    phone_number = "15216839275"
    nick_name = "ligong"
    print uuid.uuid1()
    name = {}
    name['phone'] = '15216839275'
    name['name'] = 'ligong'
    name['code'] = str(uuid.uuid1())
    print str(name)
    
    import qrcode
 
 
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=5,
        border=1
    )
    qr.add_data(str(name))
    qr.make(fit=True)
    img = qr.make_image()
    img.save("/Users/gong/Documents/dhqme_qrcode.png")
