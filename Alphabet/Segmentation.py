# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:38:28 2016

@author: gong

@description:这是用jieba分词来将文本进行分词的类
"""
import jieba
import traceback
import jieba.posseg as pseg
from Sentiment import Sentiment

class Segmentation(object):
    def __init__(self,):
        '''
        logger:日志
        stop_dict:停用词字典
        user_dict：用户自定义字典
        '''
        self.stop_dict = 'stop_word.txt'
        
        #加载自定义字典
        jieba.load_userdict('stock_list.txt')
        jieba.load_userdict('sentiment_dict.txt')
        
        
        
        #加载停用词
        if self.stop_dict:
            self.stop_word = set(open(self.stop_dict,'r').read().decode('utf8','ignore').split())
        else:
            self.stop_word = set()
    
    def cut_to_sentence(self,infile):
        try:
            '''
            infile:将文本分割成句子
            '''
            cut_list = "[。，,！……!《》<>\"':：？\?、\|“”‘’；]{}（）{}【】()｛｝（）：？！。，;、~——+％%`:“”＂'‘\n\r".decode('utf8','ignore')
            
            content = open(infile,'r').read().decode('utf8','ignore')
            for mark in cut_list:
                content = content.replace(mark,'\n')
            sentences = content.split('\n')
            sentences = map(lambda x:x.strip(),sentences)
            
            return sentences
        except Exception,e:
            traceback.print_exc()
            print 'cut to sentence %s ' % e
            
    def cut(self,infile,word_outile = None,nominal_outfile = None):
        '''
        infile:输入文件
        word_outfile:分词的输出文件
        nominal_outfile:词性的输出结果
        '''
        try:
            contents = self.cut_to_sentence(infile)
            writer_word = None
            writer_nominal = None
            if word_outile:
                writer_word = open(word_outile,'w')
            if nominal_outfile:
                writer_nominal = open(nominal_outfile,'w')
            sentiment = [0,0,0]
            if writer_word:
                for content in contents:
                    words = list(set(jieba.cut(content,cut_all = True)) - self.stop_word)
                    words = filter(lambda x:len(x) > 0,words)
                    if len(words) > 0:
                        tmp = reduce(lambda x,y:(x[0]+y[0],x[1]+y[1],x[2]+y[2]),map(lambda x:Sentiment.get_sentiment(x),words))                        
                        sentiment[0] += tmp[0]
                        sentiment[1] += tmp[1]
                        sentiment[2] += tmp[2]
                        writer_word.write(' '.join(map(lambda w:w.encode('utf8','ignore'),words))+'\n')
                writer_word.close()
                
            stop_flag = set(['p','x','m','d','c','a'])
            
            if writer_nominal:
                for content in contents:
                    words = pseg.cut(content)
                    for w in words:
                        if (w.word not in self.stop_word) and (w.flag not in stop_flag):
                            writer_nominal.write(w.word.encode('utf8','ignore')+' '+w.flag.encode('utf8','ignore')+' '+unicode(hash(content)).encode('utf8','ignore')+'\n')

                writer_nominal.close()
            return sentiment
        except Exception,e:
            traceback.print_exc()
            print 'cut error: %s !' % e

if __name__ == '__main__':
    print Segmentation().cut('/Users/gong/Desktop/aaa.txt','/Users/gong/Desktop/ccc.txt','/Users/gong/Desktop/ddd.txt')

