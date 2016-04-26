# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 10:43:43 2016

@author: gong

@description:生成目标格式的文本，编码方式gbk
"""
import os
import time
from datetime import date
import traceback
from Classify import Classify

class GenFile:
    
    @staticmethod
    def __gen_last_record__(rlist):
        c_max = (None,None)
        r_max = (None,None)
        for i,r in enumerate(rlist):
            if c_max[0]:
                if c_max[0] < r[0]:
                    c_max = (r[0],i)
            else:
                c_max = (r[0],i)
                
                
            if r_max[0] and r[1] and r_max[0] < r[1]:
                r_max = (r[1],i)
            elif r[1] and r_max[0] == None:
                r_max = (r[1],i)
                
        if r_max[0]:
            if r_max[0] > c_max[0]:
                return None
        return rlist[c_max[1]][2]
        
        
        
    #整理成统一的日期格式yyyy-mm-dd
    @staticmethod
    def dealdate(cdate):
        try:
            cdate = cdate.replace(u'年','-')
            cdate = cdate.replace(u'月','-')
            cdate = cdate.replace(u'日','')
            tmp = cdate.split('-')
            year = int(tmp[0])
            month = int(tmp[1])
            day = int(tmp[2])
            return date(year,month,day)
        except:
            return None
    
    
    
    @staticmethod
    def remove_duplicate(inputfile):
        if not os.path.exists(inputfile):
            print 'No Such File: %s!' % inputfile
            return None
        line_dict = {}
        fopen = open(inputfile,'r')
        line = fopen.readline()
        while line:
            if len(line) < 10:
                line = fopen.readline()
                continue
            tmp_line = line.decode('utf8','ignore')
            words = tmp_line.split('|')
            if len(words) != 9:
                continue
            cdate = GenFile.dealdate(words[4])
            cnum = words[1]
            remove = GenFile.dealdate(words[6])
            #已经存在了
            if line_dict.has_key(cnum):
                line_dict[cnum].append((cdate,remove,tmp_line))
            else:
                line_dict[cnum] = [(cdate,remove,tmp_line)]
            line = fopen.readline()
        fopen.close()
        
        result = []
        for k,v in line_dict.iteritems():
            if len(v) == 1:
                #移除了
                if v[0][1] and v[0][0] < v[0][1]:
                    continue
                result.append(v[0][2])
            else:
                line = GenFile.__gen_last_record__(v)
                if line:
                    result.append(line)
        del line_dict
        return result
        
    @staticmethod
    def gen_line(line,province,touch_time,spliter = u'/**********/'):
        words = line.split('|')
        if len(words) != 9:
            return None
        result = (u'%s'+spliter)*21+u'\n'
        compname = words[0]
        compkeyname = words[0]
        province = province
        TPYE = Classify.predict(words[3])
        postdate = words[4]
        level = Classify.get_risk_score(words[3])
        channel = u'全国企业信用公示系统（'+province+u'）'
        rank = ''
        TPYE_2 = ''
        postdate_2 = ''
        level_2=''
        channel_2=''
        rank_2=''
        updatetime = unicode(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(touch_time)))
        
        subcomp	= words[0]
        createtime	= updatetime
        
        privince_field = ''
        city_field = ''
        id = ''
        reg_no = words[1]
        comp_no = ''
        result = result % (compname,compkeyname,province,TPYE,postdate,level,channel,rank,TPYE_2,postdate_2,level_2,channel_2,rank_2,updatetime,subcomp,createtime,privince_field,city_field,id,reg_no,comp_no)
        result = result.encode('gbk','ignore')  
        return result
    
    @staticmethod
    def gen_file(inputfile,outputfile,province):
        if not os.path.exists(inputfile):
            print 'No Such File: %s!' % inputfile
            return None
        touch_time = os.path.getmtime(inputfile)
        #fopen = open(inputfile,'r')
        fout = open(outputfile,'w')
        try:
            lines = GenFile.remove_duplicate(inputfile)
        except:
            traceback.print_exc()
            lines = []
            
        for line in lines:
            if len(line) < 10:
                continue
            #line = line.decode('utf8','ignre')
            try:
                result = GenFile.gen_line(line,province,touch_time)
                fout.write(result)
            except Exception,e:
                traceback.print_exc()
                print e
        #fopen.close()
        fout.close()


if __name__ == '__main__':
    GenFile.gen_file(u'/Users/gong/Documents/工作/other_code/抓取代码/信用公示系统/安徽.txt',
                     u'/Users/gong/Documents/工作/other_code/抓取代码/信用公示系统/安徽_2.txt',u'安徽')
    
        
    

