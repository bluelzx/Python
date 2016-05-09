# -*- coding: utf-8 -*-
"""
Created on Fri May 06 09:13:35 2016

@author: LiGong

@description:这是从文本中提取公司名称的程序
"""
import os
import traceback
import pandas as pd
import jieba
import jieba.posseg as pseg
BACK_STEP = 10
jieba.load_userdict('segmentation.txt')

def gen_segmentation_dict(filename = 'company_name.xlsx',dict_name='segmentation.txt'):
    '''这是生成分词字典的函数'''
    try:
        if (os.path.exists(dict_name) and os.path.getsize(dict_name)!=0)or not os.path.exists(filename):
            return
        dataframe = pd.read_excel(filename)
        f = open(dict_name,'w')
        locations = list(dataframe[u'地名'].values)
        tails= list(dataframe[u'后缀名'].values)
      
        tails = filter(lambda x:isinstance(x,unicode),tails)
        gen_line_gs = lambda x:(x+' 2000 gs\n').encode('utf8','ignore')
        gen_line_ns = lambda x:(x+' 2000 ns\n').encode('utf8','ignore')
        total_lines = lambda x,y:x+y
       
        f.write(reduce(total_lines,map(gen_line_gs,tails)))
        f.write(reduce(total_lines,map(gen_line_ns,locations)))
        f.close()
        return tails
    except:
        traceback.print_exc()

def segmentation(content,dict_name='segmentation.txt'):
    '''这是将文本分词的函数'''
    
    words = pseg.cut(content)
    words = list(words)
    result = []
    for i,w in enumerate(words):
        if w.flag == 'gs':
            result.append(i)
    length = len(words)
    answer = []
    for r in result:
        index = r
        tmp_str = []
        exists = 0
        back_step = min(length-r,BACK_STEP)
        while index + back_step > r :
            if words[index].word in [u'(',u'（',u')',u'）']:
                exists += 1
            
            tmp_str.append(words[index])
            #遇到地方名词就停止
            if words[index].flag == 'df' and exists == 0:
                break
            index -= 1
        if len(filter(lambda x:x.flag == 'df',tmp_str)) > 0:
            tmp_str.reverse()
            answer.append(''.join(map(lambda x:x.word,tmp_str)))
    cut_list = u" [。，,！……!《》<>\"':：？\?、\|“”‘’；]{}{}【】｛｝：？！。，;、~——+％%`:“”＂'‘\n\r"
    results = set()
    for ans in answer:
        found = False
        for c in cut_list:
            if ans.find(c) >= 0:
                found = True
                break
        if not found:
            results.add(ans)
    return list(results)
        
if __name__ == '__main__':
    content = u'''
    
城南（张家港）科技有限公司
    '''
    a = segmentation(content)
    for i in a:
        print i