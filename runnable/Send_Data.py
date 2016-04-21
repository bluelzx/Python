# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 20:56:51 2016

@author: gong

@description: 这是用来发邮件的程序，在初期可以用来备份数据
"""
import base64
import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Send_Data(object):
    def __init__(self,smtp_server,username,password,sender = 'admin'):
        #初始化基本值
        self.smtp_server = smtp_server
        self.username = username
        self.password = password
        self.sender = sender
    
    #发送数据
    def send_message(self,subject,data,receiver='ligong19@qq.com',filename = None):
        try:
            msg_root = MIMEMultipart('related')
            msg_root['Subject'] = subject#邮件标题
            msg_root['From'] = self.sender
            msg_root['To'] = receiver
            msg_text = MIMEText('%s'% data,'html','utf-8')#你所发的文字信息将以html形式呈现
            msg_root.attach(msg_text)
            if filename:
                att = MIMEText(open('%s'%filename, 'rb').read(), 'base64', 'utf-8')#添加附件
                att['Content-Type'] = 'application/octet-stream'
                att['Content-Disposition'] = "attachment; filename='%s'" % filename
                msg_root.attach(att)
            smtp = smtplib.SMTP()
            send_num = 0
            while send_num < 100:#持续尝试发送，直到发送成功
                send_num += 1
                try:
                    smtp.sendmail(self.sender, receiver, msg_root.as_string())#发送邮件 
                    break
                except:
                    try:
                        smtp.connect(self.smtp_server)#连接至邮件服务器
                        smtp.login(base64.decodestring(self.username), base64.decodestring(self.password))#登录邮件服务器
                    except:
                        print "failed to login to smtp server"#登录失败
            smtp.quit()
        except Exception,e:
            traceback.print_exc()
            print e

if __name__ == '__main__':
    sd = Send_Data('smtp.qq.com','bGlnb25nMTk=','MTk5Mi4wMS4wNGxpZ29uZw==','ligong19@qq.com')
    sd.send_message('交易','你好')