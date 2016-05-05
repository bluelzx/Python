# -*- coding: utf-8 -*-
"""
Created on Wed May  4 16:05:30 2016

@author: gong

@description:   这里认为「历史会重演」，所以本文认为现在的状态在历史中也曾出现过。
                因而，在回顾历史中来预测未来走势。
"""
import pandas as pd
class Retrospect(object):
    def __init__(self,sequence):
        if isinstance(sequence,pd.DataFrame):
            self.sequence = sequence
            self.state_sequence = None
        else:
            raise 'Data Type Error: Need pandas.DataFrame!'
    
    def encode(self):
        '''生成状态串'''
        mas = [5,10,30]
        tmp = map(lambda ma:pd.rolling_mean(self.sequence, mas[0])-self.sequence,mas)
        tmp = map(lambda r:r.apply(lambda x:1 if x > 0 else 0),tmp)
        self.state_sequence = tmp[0]+tmp[1]*2+tmp[2]*4
        return self.state_sequence
        
    
    def lookback(self,back_step = 10):
        '''回顾历史'''
        assert(len(self.state_sequence) > back_step)
        sub_seq = self.state_sequence[-back_step:]
        seq_str = ''.join(map(lambda x:str(x),self.state_sequence))
        sub_str = ''.join(map(lambda x:str(x),sub_seq))
        n = len(seq_str)
        index = 0
        results = set()
        while index < n:
            tmp = seq_str.find(sub_str,index)
            if tmp < 0:
                break
            index = tmp
            if index+back_step < n:
                results.add(self.state_sequence[index+back_step])
                index += 1
            else:
                break
        self.similar_states = list(results)
        return self.similar_state


if __name__ == '__main__':
    
            
        
