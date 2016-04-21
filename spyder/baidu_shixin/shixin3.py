# -*- coding: utf-8 -*-
import sys,urllib, urllib2, time, random, json
import string

def getPage(ch, order, area = '', retries = 3):
    '''
    返回一个网页html
    ch:表示搜索的常用汉字，unicode编码
    order:下载的页数
    area:表示区域，这里是各个省份，unicode编码
    retries:下载失败后，需要重试的次数
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}
    url_f = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E5%A4%B1%E4%BF%A1%E8%A2%AB%E6%89%A7%E8%A1%8C%E4%BA%BA%E5%90%8D%E5%8D%95&cardNum=&iname="
    url_m1 = "&areaName="       #区域的名字
    url_m2 = "&pn="             #page number
    url_l = "&rn=10&ie=utf-8&oe=utf-8&format=json"
    
    #url的前后部分，第一页为空，之后的第i页的order为i-1
    keyword = urllib.quote(ch.encode('utf-8'))
    areaName = urllib.quote(area.encode('utf-8'))
    
    url = url_f + keyword + url_m1 + areaName + url_m2 + str(order) + url_l
    req = urllib2.Request(url, headers = headers)
    order = order/10 + 1

    try:
        content = urllib2.urlopen(req, timeout = 5).read()
        print "page got %s %s %s!" %(ch.encode('utf8'),area.encode('utf8'),str(order))
        return content
    except:
        if retries > 0:
            order = 10 * (order - 1)
            return getPage(ch, order, '',retries - 1)
        else:
            print "miss %s %s !" %(ch.encode('utf8') ,str(order))
            return ''
            
#检验是否需要分省市爬虫
def tryAnalyze(ch): 
    temp = getPage(ch, 1950, '')
    if len(temp) < 100:
        return 0
    return 1
    

#解析下载到的json
def AnalyzeJson(ch, order,company_file,human_file,area=''):
    '''
    ch:汉字
    order:页面数
    company_file:公司文件的写入操作符
    human_file:个人文件的写入操作符
    area:区域
    '''
    temp = getPage(ch, order, area)
    
    #return temp

    order = order/10 + 1

    if temp == '':
        with open('miss.txt', 'a') as outfile:
            outfile.write(ch.encode('utf8') +'|'+ area.encode('utf8')+'|' + str(order) + '\n')
        return 1

    try:
        content = json.loads(temp)
    except:
        #做一些非法json格式的处理
        for i in range(len(temp)):
            if temp[i]=='\\' and (not temp[i+1] in string.printable):
                temp = temp[:i] + '/' + temp[i+1:]
        content = json.loads(temp)

    if len(content['data']) == 0: return 0

    #这个是返回的json的key，个人
    field_comp = ['iname', 'cardNum', 'caseCode', 'areaName', 'businessEntity', 'courtName', 'duty', 'performance', 'disruptTypeName', 'publishDate', 'gistId', 'regDate', 'gistUnit', 'performedPart', 'unperformPart']
    
    #这个是返回的json的key，公司
    field_hum = ['StdStg', 'StdStl', '_update_time', 'loc', 'lastmod', 'changefreq', 'priority', 'type', 'sitelink', 'iname', 'cardNum', 'caseCode', 'age', 'sexy', 'focusNumber', 'areaName', 'businessEntity', 'courtName', 'duty', 'performance', 'disruptTypeName', 'publishDate', 'partyTypeName', 'gistId', 'regDate', 'gistUnit', 'performedPart', 'unperformPart', 'publishDateStamp', 'SiteId']
    
    for i in content["data"][0]["result"]:
        if i['partyTypeName'] == '1': #公司
            field = field_comp
            outfile = company_file
        else: #个人
            field = field_hum
            outfile = human_file

        for j in field:
            tmp = i[j]
            if isinstance(tmp,int):
                tmp = unicode(tmp)
            outfile.write(tmp.encode('utf-8') + '|')
        outfile.write('\n')
        outfile.flush()
    return 1


#封装起来的主函数
def main(outfile_company = 'outfile_company.txt',outfile_human = 'outfile_human.txt',
        over_txt ='over_txt.txt',ch_list_file = 'ch_list.txt',sleep=False):
    '''
    outfile_company:公司的输出
    outfile_human:个人的输出
    over_txt:问成的
    ch_list_file:常用汉字的文本
    sleep:是否暂停sleep
    '''
    province = [u'北京',u'天津',u'重庆',u'上海',u'河北',u'山西',u'吉林',u'辽宁',u'黑龙江',
    u'陕西',u'甘肃',u'青海',u'山东',u'福建',u'浙江',u'河南',u'湖北',u'湖南',u'江西',u'江苏',
    u'安徽',u'广东',u'海南',u'四川',u'贵州',u'云南',u'内蒙古',u'新疆',u'宁夏',u'广西',u'西藏']
   
    company_file = open(outfile_company, 'a')
    human_file = open(outfile_human, 'a')
    
    with open(ch_list_file, 'r') as infile:
        ch_list = infile.read()
    
    #判断一下字符编码类型
    if not isinstance(ch_list,unicode):
        try:
            ch_list = ch_list.decode('utf8')
        except:
            try:
                ch_list = ch_list.decode('gb2312')
            except:
                ch_list = ch_list.decode('gbk')
    
    ch_list = ch_list.split('\n')

    page_index = 0
    for ch in ch_list:
        if tryAnalyze(ch):
            for k in province:
                while(AnalyzeJson(ch, page_index,company_file,human_file,area = k)):
                    if sleep:
                        interm = random.randrange(0, 20)
                        time.sleep(interm/10.0)                    
                    page_index += 50
                if page_index == 2000:
                    with open(over_txt, 'a') as outfile:
                        outfile.write("%s %s \n" % (ch.encode('utf8'),k.encode('utf8')))
        else:
            page_index = 0
            while(AnalyzeJson(ch, page_index,company_file,human_file)):
                if sleep:
                    interm = random.randrange(0, 20)
                    time.sleep(interm/10.0)
                page_index += 50
            with open(over_txt, 'a') as outfile:
                outfile.write("%s\n" % ch.encode('utf8'))
    company_file.close()
    human_file.close()

'''
AnalyzeJson(ch_list[1464: 1466], 50)
'''

if __name__ == '__main__':
    outfile_company = 'outfile_company.txt'
    outfile_human = 'outfile_human.txt'
    over_txt ='over_txt.txt'
    ch_list_file = 'ch_list2.txt'
    sleep=False
    
    argv_nb = len(sys.argv)
    if argv_nb > 6:
        print 'python shixin3.py outfile_company outfile_human over_txt ch_list_file sleep'
        exit(0)
        
    #获得outfile_company
    if argv_nb >= 2:
        outfile_company = sys.argv[1]
    
    #outfile_human
    if argv_nb >= 3:
        outfile_human = sys.argv[2]
        
    #over_txt
    if argv_nb >= 4:
        over_txt = sys.argv[3]
        
    #over_txt
    if argv_nb >= 5:
        ch_list_file = sys.argv[4]
    
    #sleep
    if argv_nb >= 6:
        sleep = sys.argv[5]
        if int(sleep) != 0:
            sleep = True
        else:
            sleep = False

    main(outfile_company+'.tmp' ,outfile_human+'.tmp',over_txt,ch_list_file,sleep)
    
    #以下是用来清洗的程序
    from sx_comp_clean import process_comany
    process_comany(outfile_company+'.tmp',outfile_company)
    from sx_hum_clean import process_hum
    process_hum(outfile_human+'.tmp',outfile_human)