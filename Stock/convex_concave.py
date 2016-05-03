# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 09:58:33 2016

@author: gong

@description:判断是不是有凸和凹的形态
"""

def has_convex(high_seq,max_step = 10):
    '''最近判断是不是有凸，跨度最大是max_ste'''
    max_step = min(max_step,len(high_seq))
    for i in xrange(3,max_step):
        delta = float(high_seq[-i] - high_seq[-1])/float(i-1)
        for j in xrange(1,i):
            if high_seq[-1]+delta*(j-1) < high_seq[-j]:
                return False
        return True

def has_concave(low_seq,max_step = 10):
    '''最近判断是不是有凹，跨度最大是max_ste'''
    max_step = min(max_step,len(low_seq))
    for i in xrange(3,max_step):
        delta = float(low_seq[-i] - low_seq[-1])/float(i-1)
        for j in xrange(1,i):
            if low_seq[-1]+delta*(j-1) > low_seq[-j]:
                return False
        return True

if __name__ == '__main__':
    x = [5,4,3,1]
    print has_concave(x)
