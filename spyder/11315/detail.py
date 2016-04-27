# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 16:00:52 2016

@author: gong

@description:这是解析11315征信系统详情页面的程序
http://09024488.11315.com/
"""
from bs4 import BeautifulSoup
class ParseDetail(object):
    #从style中提取必要的信息
    @staticmethod
    def __get_data_from_style__(style):
        values = style.split(';')
        values = filter(lambda x:len(x) > 5,values)
        tmp_dict = {}
        for v in values:
            tmp_index = v.find(':')
            tmp = [v[:tmp_index],v[tmp_index+1:]]
            tmp_dict[tmp[0].strip()] = tmp[1].strip()
        image = tmp_dict['background-image']
        
        position = tmp_dict['background-position']
        width = tmp_dict['width']
        height = tmp_dict['height']
        width = int(width[:width.find('px')].strip())
        height = int(height[:height.find('px')].strip())
        tmp = position.split(' ')
        bgd_x = int(tmp[0][:tmp[0].find('px')])
        bgd_y = int(tmp[1][:tmp[1].find('px')])
        image = image[image.find('http'):image.find('\')')]
        return (image,bgd_x,bgd_y,width,height)
        
    @staticmethod
    def parse_datail(html):
        soup = BeautifulSoup(html,'lxml')
        table = soup.find('table',attrs={'class':'v1Table01'})
        trs = table.findAll('tr')
        
        #公司名称
        company_name = unicode(trs[0].find('th',attrs={'class':'th01'}).string.strip())
        ps = trs[1].findAll('p')
        
        #企业法人
        try:
            owner = ParseDetail.__get_data_from_style__(ps[0].attrs['style'])
        except:
            owner = ''
        
        #注册资本
        try:
            capital = ParseDetail.__get_data_from_style__(ps[1].attrs['style'])
        except:
            capital = ''
        
        #行业  
        try:
            industry = unicode(trs[2].find('td').string.strip())
        except:
            industry = ''
        
        #号码   
        phones = []
        try:
            for p in trs[3].findAll('p'):
                phones.append(ParseDetail.__get_data_from_style__(p.attrs['style']))
        except:
            pass
          
        #区域
        try:
            area = ParseDetail.__get_data_from_style__(trs[5].findAll('p')[0].attrs['style'])
        except:
            area = ''
        #地址
        try:
            location = unicode(trs[6].findAll('td')[0].contents[0] .strip())
        except:
            location = ''
        #主营产品
        try:
            products = ParseDetail.__get_data_from_style__(trs[7].findAll('p')[0].attrs['style'])
        except:
            products = ''
        #链接
        try:
            href = trs[8].findAll('a')[0].attrs['href'] 
        except:
            href = ''
        result = {}
        result[u'公司名称'] = company_name
        result[u'企业法人'] = owner
        result[u'注册资本'] = capital
        result[u'行业'] = industry
        result[u'号码'] = phones
        result[u'区域'] = area
        result[u'地址'] = location
        result[u'主营产品'] = products
        result[u'更多信息'] = href
        return result
    
    @staticmethod
    def deep_detail(html):
        soup = BeautifulSoup(html,'lxml')
        contents = unicode(soup.find('div',attrs={'class','text_box'}).findAll('p')[0].get_text().strip())
        products = soup.findAll('table',attrs={'class','table02'})[1].findAll('tr')[4].get_text()       
        result = {}
        result[u'主营产品'] = products
        result[u'公司介绍'] = contents
        return result

if __name__ == '__main__':
    f = open('/Users/gong/Desktop/a.html','r')
    html = f.read()
    f.close()
    #print html
    print ParseDetail.parse_datail(html)
