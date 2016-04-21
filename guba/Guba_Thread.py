# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 21:18:58 2015

@author: gong
"""
import sys
import time 
import Queue
#import random
import threading
import traceback
import pandas as pd
from Eastmoney_Guba import Eastmoney_Guba

#全局任务
JOB_QUEUE = Queue.Queue(maxsize = 10000)

class Guba_Thread(threading.Thread):
    def __init__(self,thread_id,interval = 10):
        threading.Thread.__init__(self)  
        self.thread_id = thread_id  
        self.interval = interval  
        self.thread_stop = False
        self.jobs = Queue.Queue(maxsize = 10000)
        self.results = []
    
    def run(self):
        print 'Thread %s is running....' % self.thread_id
        global JOB_QUEUE
        while not self.thread_stop:
            try:
                #job数量为0，则跳出循环
                if self.jobs.qsize() == 0:
                    #没有任务可做
                    self.get_job(JOB_QUEUE)
                    continue
                #执行任务
                func,params = self.jobs.get()
                try:
                    print 'Now Thread %s is processing job %s ...' % (self.thread_id,str(params))
                    result = func(**params)
                    if result != None:
                        self.results.append(result)
                    time.sleep(self.interval)
                except:
                    print 'Processing job %s ERROR! Add to job queue to continue!' % str(params)
                    JOB_QUEUE.put((func,params))
                
                #没有任务做了就停止
                if JOB_QUEUE.qsize() == 0:
                    break
            except Exception,e:
                traceback.print_exc()
                print e
    
    def get_results(self):
        try:
            return pd.concat(self.results)
        except Exception,e:
            traceback.print_exc()
            print e
    '''
    #停止
    def stop(self):  
        self.thread_stop = True 
    '''
    
    #添加任务
    def add_job(self,func,params):
        self.jobs.put((func,params))
        
    #获得job
    def get_job(self,job_queue):
        if job_queue.qsize() == 0:
            return
        else:
            func,params = job_queue.get()
            self.add_job(func,params)

def stockid_process(stockid):
    tmp = str(stockid)
    while len(tmp) < 6:
        tmp = '0'+tmp
    return tmp


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print '线程数量,股票代码文件,输出文件路径'
        sys.exit()
    thread_num = int(sys.argv[1])
    filename = sys.argv[2]
    path = sys.argv[3]
    
    threads = []
    for i in range(thread_num):
        threads.append(Guba_Thread(i))

    #获取任务
    stockids = map(stockid_process,pd.read_excel(filename)['stockid'])
    for stockid in stockids:
        tmp_job = {'stockid':stockid,'path':path}
        JOB_QUEUE.put(Eastmoney_Guba.__process__,tmp_job)
    '''
    aas = [i for i in range(50)]
    bbs = [i*i for i in range(50)]
    for i in range(50):
        tmp_job = {'a':aas[i],'b':bbs[i]}
        JOB_QUEUE.put((add,tmp_job))
    threads = []
    for i in range(3):
        threads.append(Guba_Thread(i))
    
    times = len(stockids)/thread_num
    for i in range(times):
        for j in range(thread_num):
            tmp_job = {'stockid':stockids[i*thread_num+j],'path':path}
            threads[j].add_job(Eastmoney_Guba.__process__,tmp_job)
    
    for i in range(times*thread_num,len(stockids)):
        tmp_job = {'stockid':stockids[i],'path':path}
        tmp = random.randint(0,thread_num-1)
        threads[tmp].add_job(Eastmoney_Guba.__process__,tmp_job)
    '''
    
    #运行线程
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    