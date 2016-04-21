# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:08:58 2016

@author: gong

@description: 这是用来定义模型输入的数据结构
"""
import numpy
from sklearn import preprocessing

class DataSet(object):
    def __init__(self, samples, labels, scale = False,fake_data=False):
        if fake_data:
            self._num_samples = 10000
        else:
            #检查数据的长度与标签的长度是否一致
            assert samples.shape[0] == labels.shape[0], (
              "samples.shape: %s labels.shape: %s" % (samples.shape,labels.shape))
            self._num_samples = samples.shape[0]
            
            
            #这里把数据进行归一化
            if scale:
                min_max_scaler = preprocessing.MinMaxScaler()
                samples = samples.astype(numpy.float32)
                shape = samples.shape
                tmp_shape = (shape[0],reduce(lambda x,y:x*y,shape[1:]))
                samples = samples.reshape(tmp_shape)
                samples = min_max_scaler.fit_transform(samples)
                #samples = samples.reshape(shape)
            else:
                samples = samples.reshape(samples.shape[0],
                              samples.shape[1] * samples.shape[2])
                samples = samples.astype(numpy.float32)
                samples = numpy.multiply(samples, 1.0 / 255.0)
            self._samples = samples
            self._labels = labels
            self._epochs_completed = 0
            self._index_in_epoch = 0
    
    @property
    def samples(self):
        return self._samples
  
    @property
    def labels(self):
        return self._labels
        
    @property
    def num_samples(self):
        return self._num_samples
    
    @property
    def epochs_completed(self):
        return self._epochs_completed
    
    def next_batch(self, batch_size, fake_data=False):
        """Return the next `batch_size` samples from this data set."""
        if fake_data:
            fake_image = [1.0 for _ in xrange(self._samples.shape[1])]
            fake_label = 0
            return [fake_image for _ in xrange(batch_size)], [
                fake_label for _ in xrange(batch_size)]
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_samples:
            # Finished epoch
            self._epochs_completed += 1
            
            # Shuffle the data
            perm = numpy.arange(self._num_samples)
            numpy.random.shuffle(perm)
            self._samples = self._samples[perm]
            self._labels = self._labels[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_samples
        end = self._index_in_epoch
        return self._samples[start:end], self._labels[start:end]
        
