# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 14:40:05 2015

@author: gong

@description: 这是用来在中国地图上面天色的程序
"""
import pandas as pd
import matplotlib.pyplot as plt


def get_cities(filename = '/Users/gong/Documents/city'):
    f = open(filename,'r')
    cities = f.read().split('\n')
    f.close()
    return cities

def issame(city1,city2):
    #print city1,city2
    if city1.find(city2) >= 0:
        return True
    return False

def get_index(city,mycity):
    for i,v in enumerate(mycity):
        if issame(city.decode('utf8','ignore'),v):
            print i
            return i
    return -1
def gen_data(data,cities,infile = u'/Users/gong/Documents/论文资料/地区数据.xlsx',filename = '/Users/gong/Documents/out.xls'):
    dataframe = pd.read_excel(infile)
    mycity = list(dataframe['city'])
    mydata = list(dataframe[data])
    result = []
    outcities = []
    for city in cities:
        index = get_index(city,mycity)
        outcities.append(city.decode('utf8','ignore'))
        if index < 0:
            result.append(0)
        else:
            result.append(mydata[index])
    pd.DataFrame({'city':outcities, data: result}).to_excel(filename)
    #pd.DataFrame([cities,result])

def plot_pic(infile = u'/Users/gong/Documents/论文资料/地区数据.xlsx'):
    dataframe = pd.read_excel(infile)
    x = dataframe[u'城镇化率']
    y = dataframe[u'人均gdp']
    plt.plot(x, y,'o')
    #plt.title(’Plot of y vs. x’)# give plot a title
    plt.xlabel('lat')# make axis labels
    plt.ylabel('gdp')

def get_cities(infile = u'/Users/gong/Documents/论文资料/地区数据.xlsx'):
    dataframe = pd.read_excel(infile)
    data = dataframe[['city',u'省份']]
    #print data
    mydict = {}
    
    for d in data.iterrows():
        if not mydict.has_key(d[1][u'省份']):
            mydict[d[1][u'省份']] = []
        mydict[d[1][u'省份']].append(d[1]['city'])
    tmp = []
    for key in mydict.keys():
        tmp.append([key,','.join(mydict[key])])
    pd.DataFrame(tmp).to_excel(u'/Users/gong/Documents/a.xls')
    
if __name__ == '__main__':
    #cities = get_cities()
    #gen_data(u'人均gdp',cities)
    #plot_pic()
    get_cities()