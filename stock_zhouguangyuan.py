# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 11:54:41 2016

@author: gong
"""

#统计数据for周光远
import os
import sys
import pandas as pd

def statistic_for_stock(filename,outname):
    dataframe = pd.read_excel(filename)
    grouped = dataframe.groupby(u'发表时间')
    
    read_num = grouped[u'阅读'].sum()
    cmt_num = grouped[u'评论'].sum()
    eassy_num = grouped[u'文章链接'].nunique()
    author_num = grouped[u'作者'].nunique()

    
    answer = [read_num,cmt_num,eassy_num,author_num]
    
   
    
    pd.DataFrame(answer).T.to_excel(outname)
    

if __name__ == '__main__':
    statistic_for_stock('/Users/gong/Downloads/000006.xlsx')
    if len(sys.argv) != 3:
        print '输入路径,输出路径'
        sys.exit()

    inpath = sys.argv[1]
    outpath = sys.argv[2]
    
    for s in os.listdir(inpath):
        filename = os.path.join(inpath,s)
        if filename.endswith('.xlsx'):
            print 'Now processing file: %s...' % filename
            statistic_for_stock(filename,os.path.join(outpath,s))