# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 16:34:22 2016

@author: gong

@description: 这是用来计算词语相似度的程序
"""
import os
import gensim
class Sentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
        
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

class WordSimirality(object):
    def __init__(self,dirname,model = 'word2vec.model'):
        self.dirname = dirname
        if not os.path.exists(model):
            if os.path.isdir(self.dirname):
                self.sentences = Sentences(self.dirname)
            if os.path.isfile(self.dirname):
                self.sentences = map(lambda x:x.split(),open(self.dirname,'r').read().decode('utf8','ignore').split('\n'))
            self.sentences = filter(lambda x:len(x) > 0,self.sentences)
            self.model = gensim.models.Word2Vec(self.sentences,min_count = 5,size=100,workers=1)
            self.model.save(model)
        else:
            self.model = gensim.models.Word2Vec.load(model)
    
    
    def simirality(self,word1,word2):
        return self.model.similarity(word1,word2)

if __name__ == '__main__':
    a = WordSimirality('/Users/gong/Desktop/ccc.txt')
    print a.simirality(u'银联',u'银联卡')