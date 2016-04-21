# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:02:27 2016

@author: gong

@description:这是搭建的一个CNN深度神经网络模型
"""
import tensorflow as tf

class CNN_DeepLearning(object):
    def __init__(self,input_shape,label_shape):
        self._input_shape = list(input_shape)               #输入的维度
        self._label_shape = list(label_shape)               #输出的维度
        self._session = tf.InteractiveSession()
        self._input_shape[0] = None
        self._label_shape[0] = None
        #输入
        self.x = tf.placeholder("float", shape=self._input_shape)
        
        #分类
        self.y_ = tf.placeholder("float", shape=self._label_shape)
        
        #dropout value        
        self.keep_prob = tf.placeholder("float")
        #用来存放层的list
        self._layers = []
        
    def weight_variable(self,shape):
        '''生成一个权重矩阵W'''
        initial = tf.truncated_normal(shape,stddev=0.1)
        return tf.Variable(initial)
    
    def bias_variable(self,shape):
        '''生成一个bias的矩阵b'''
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)
    
    #padding can be VALID or SAME
    def pooling(self,x,ksize=[1, 2, 2, 1],strides = [1, 2, 2, 1],padding = 'SAME',pooling='max'):
        '''池化'''     
        if 'average' == pooling.lower():
            return tf.nn.avg_pool(x, ksize=ksize,strides=strides, padding=padding)
        if 'max' == pooling.lower():
            return tf.nn.max_pool(x, ksize=ksize,strides=strides, padding=padding)
    
    def hide_layer(self,input_value,weight_value,bias_value,conv_strides = [1, 1, 1, 1],pooling_strides = [1, 2, 2, 1],ksize = [1, 2, 2, 1],padding = 'SAME',pooling = 'max'):
        '''新建一个隐藏层的网络'''  
        tmp_conv = tf.nn.relu(tf.nn.conv2d(input_value,weight_value,conv_strides,padding)+bias_value)     
        return self.pooling(tmp_conv,ksize=ksize,strides = pooling_strides,padding=padding,pooling=pooling)
    
    def dense_layer(self,input_value,weight_value,bias_value):
        '''密集连接层'''
        return tf.nn.relu(tf.matmul(input_value, weight_value) + bias_value)
        
    def dropout(self,input_value):
        '''dropout'''
        return tf.nn.dropout(input_value, self.keep_prob)
        
    
    def output_layer(self,input_value,weight_value,bias_value):
        '''新建一个输出层'''
        return tf.nn.softmax(tf.matmul(self.dropout(input_value), weight_value) + bias_value)
    
    
    def train(self,output_value,train_data,iteration=10,keep_prob=0.5):
        '''训练网络'''
        #交叉熵作为损失函数
        cross_entropy = -tf.reduce_sum(self.y_*tf.log(output_value))
        
        #优化函数
        train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
        correct_prediction = tf.equal(tf.argmax(output_value,1), tf.argmax(self.y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        self._session.run(tf.initialize_all_variables())
        
        
        for i in range(iteration):
            batch = train_data.next_batch(50)
            
            if i%100 == 0:
                train_accuracy = accuracy.eval(feed_dict={self.x:batch[0], self.y_: batch[1],self.keep_prob:keep_prob})
                print "step %d, training accuracy %g"%(i, train_accuracy)
            train_step.run(feed_dict={self.x: batch[0], self.y_: batch[1],self.keep_prob:keep_prob})
        return accuracy
    
    #测试数据
    def test(self,test_data,accuracy,keep_prob = 1.0):
        if accuracy:
            return accuracy.eval(feed_dict={self.x: test_data.samples, self.y_: test_data.labels, self.keep_prob: keep_prob})

    #预测
    def predict(self,predict_data,keep_prob = 1.0):
        layer = self._layers[-1]
        return layer.eval(feed_dict={self.x: predict_data.samples, self.keep_prob: keep_prob})

if __name__ == '__main__':
    import input_data
    from DataSet import DataSet
    train_images = input_data.extract_images('MNIST_data/train-images-idx3-ubyte.gz')
    test_images = input_data.extract_images('MNIST_data/t10k-images-idx3-ubyte.gz')
    train_labels = input_data.extract_labels('MNIST_data/train-labels-idx1-ubyte.gz',one_hot=True)
    test_labels = input_data.extract_labels('MNIST_data/t10k-labels-idx1-ubyte.gz',one_hot=True)
    train = DataSet(train_images,train_labels)
    test = DataSet(test_images,test_labels)
    cnn = CNN_DeepLearning(train.samples.shape,train.labels.shape)
    
    
    #建立网路
    layer1 = cnn.hide_layer(tf.reshape(cnn.x,[-1,28,28,1]),cnn.weight_variable([5,5,1,32]),cnn.bias_variable([32]))
    layer2 = cnn.hide_layer(layer1,cnn.weight_variable([5,5,32,64]),cnn.bias_variable([64]))
    layer3 = cnn.dense_layer(tf.reshape(layer2,[-1,7*7*64]),cnn.weight_variable([7*7*64,1024]),cnn.bias_variable([1024]))
    output = cnn.output_layer(layer3,cnn.weight_variable([1024,10]),cnn.bias_variable([10]))
    a = cnn.train(output,train)
    value = layer1.eval(feed_dict={cnn.x:test.samples})
    print output.eval(feed_dict={cnn.x:test.samples,cnn.keep_prob:1}).shape
    print cnn.test(test,a)
    
    
    