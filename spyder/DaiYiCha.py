# -*- coding: utf-8 -*-
"""
Created on Mon May 09 14:01:10 2016

@author: gong

@description:这是下载http://www.daiyicha.com/上面P2P平台数据的程序
"""
import json
import traceback
from WebSpyder import WebSpyder
import urllib
import pandas as pd
class DaiYiCha(object):
    def __init__(self):
        self.spyder = WebSpyder()
    
    #下载详细数据
    def get_ajax_info(self,p2p_name,outpath='p2p_info/'):
        assert(isinstance(p2p_name,unicode))
        url = 'http://www.daiyicha.com/cha.php?view=show&word=' + urllib.quote(str(p2p_name.encode('gb2312')))
        data = self.spyder.get_data(url)
        start = data.find('jq.getJSON("plugin.php?id=lonvoy_siteinfo:ax", ')+len('jq.getJSON("plugin.php?id=lonvoy_siteinfo:ax", ')
        tmp_data = data[start:]
        tmp_data = tmp_data[:tmp_data.find(', function (json)')]
        del data
        tmp_data = tmp_data.replace(':','":')
        tmp_data = tmp_data.replace(',',',"')
        tmp_data = tmp_data.replace('{','{"')
        
        data_dict = json.loads(tmp_data)
        data_url = 'http://www.daiyicha.com/plugin.php?id=lonvoy_siteinfo:ax'
        for k,v in data_dict.iteritems():
            data_url += '&'+str(k).strip()+'='+urllib.quote(str(v.encode('gb2312')))
        
        total_data = self.spyder.get_data(data_url)
        f = open(outpath+p2p_name+'.txt','w')
        f.write(total_data)
        f.close()
  
if __name__ == '__main__':
    dataframe = pd.read_excel('P2P.xlsx')
    data = dataframe[u'平台'].values
    
    import os
    dyc = DaiYiCha()
  
    for item in data:
        print 'processing ',item
        try:
            short_name = item.strip()
            
            if os.path.exists('p2p_info/'+short_name+'.txt'):
                continue
            dyc.get_ajax_info(short_name)
        except:
            print item,'error!'
    
            
    