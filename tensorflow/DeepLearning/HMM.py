# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 15:59:17 2016

@author: gong

@description:这是HMM模型
"""
#from sklearn.hmm import GaussianHMM
from sklearn import hmm
X=[0,1,2,1,1,2,0,3,9]

model = hmm.MultinomialHMM(n_components=4)
model.n_symbols=10
model.fit([X],n_iter=100)
print model.predict(X)
#print model.eval(X)
