# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 20:37:25 2015

@author: gong
"""
from lxml import etree
import traceback
def read_file(filename = '/Volumes/Untitled/ProsperDataExport.xml'):
    try:
        f = open(filename,'r')
        f1 = open('/Users/gong/Documents/bid.txt','w')
        start = False
        end = False
        line = f.readline()
        print line
        while line:
            line = f.readline()
            #print line
            if line.find('<Bids>') >= 0:
                start = True
            if line.find('</Bids>') >= 0:
                end = True
            if start and not end:
                f1.write(line)
        f.close()
        f1.close()
    except Exception,e:
        traceback.print_exc()
        print e


def parse_xml(filename = '/Users/gong/Downloads/ProsperDataExportBids.xml'):
    doc = etree.parse(filename)
    
    #root = doc.Element("Marketplaces")
    Marketplaces = doc.xpath(u'//Bid')
    result = []
    print len(Marketplaces)
    for Marketplace in Marketplaces:
        tmp = {}
        for c in list(Marketplace):
            tmp[c.tag] = c.text
        result.append(tmp)
    
    keys = result[0].keys()
    print keys
    f = open('/Users/gong/Documents/bids.csv','w')
    f.write(','.join(keys)+'\n')
    for tmp in result:
        line = ''
        for key in keys:
            line += ','+str(tmp[key])
        line = line[1:]+'\n'
        f.write(line)
    f.close()
        
if __name__ == '__main__':
    #read_file()
    parse_xml()