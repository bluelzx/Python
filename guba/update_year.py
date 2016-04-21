# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 10:27:18 2015

@author: gong
"""
import os
import sys
import traceback
import pandas as pd
def get_index(url):
    tmp = url[:url.find('.')]
    return int(tmp.split(',')[-1])
    
def is_able(value):
    try:
        i= 0
        if value.startswith(u'公告 '):
            i += 1
            
        if value.startswith(u'研报 '):
            i += 1
        
        if value.startswith(u'新闻 '):
            i += 1
        
        if i > 0:
            return False
        else:
            return True
    except:
        return True
        
def update_year(filename,outname):
    try:
        dataframe = pd.read_excel(filename)
        
        dataframe['yes'] = dataframe.apply(lambda row:is_able(row[u'标题']), axis=1)
        #print       dataframe['yes']
        dataframe = dataframe[dataframe.yes == True]
        
        dataframe[u'发表下标']=dataframe.apply(lambda row: get_index(row[u'文章链接']), axis=1)
            
        dates = list(dataframe.sort_values(by = u'发表下标', ascending=0)[u'发表日期'])
        urls = list(dataframe.sort_values(by = u'发表下标', ascending=0)[u'文章链接'])
        #print dates
        year = 2015
        if dates[0][0:2] == '01':
            year = 2016
            
        years = []
        years.append([urls[0],str(year)+'-'+dates[0]])
        
        for i in range(1,len(dates)):
            month_pre = int(dates[i-1][0:2])
            month_now = int(dates[i][0:2])
            if month_pre < month_now:
                year -= 1
            #print unicode(year)+'-'+dates[i]
            years.append([urls[i],unicode(year)+'-'+dates[i]])
        
        tmp = pd.DataFrame(years,columns = (u'文章链接',u'发表时间'))
        #tmp = pd.concat({u'文章链接':urls, u'发表时间': years}, axis=1)
        #print tmp
        dataframe = pd.merge(tmp,dataframe,on=(u'文章链接'))
        dataframe.to_excel(outname)
    except Exception,e:
        print e
        traceback.print_exc()
    
if __name__ == '__main__':
    #update_year('/Users/gong/Downloads/000001.xlsx','/Users/gong/Downloads/000001_1.xlsx')
    
    if len(sys.argv) != 3:
        print '输入路径,输出路径'
        sys.exit()

    inpath = sys.argv[1]
    outpath = sys.argv[2]
    
    for s in os.listdir(inpath):
        filename = os.path.join(inpath,s)
        if filename.endswith('.xlsx'):
            print 'Now processing file: %s...' % filename
            update_year(filename,os.path.join(outpath,s))
    