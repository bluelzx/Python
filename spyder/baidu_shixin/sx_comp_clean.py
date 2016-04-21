# -*- coding: utf-8 -*-
'''-3
高安市三伢仔汽修饭店|
L3812698X|
(2013)高法执字第00182号|
江西|
喻琨|
高安市人民法院|
劳动争议|
全部未履行|
其他有履行能力而拒不履行生效法律文书确定义务|
2015年12月30日|
（2012）宜中民四终字第114号|
20130408|
宜春市中级人民法院|
|
|
'''
import time
def process_comany(filename,outfilename):
    day = time.strftime("%Y%m%d",time.localtime(time.time()))
    with open(filename, 'r') as infile:
        with open(outfilename, 'w') as outfile:
            content = infile.readlines()
            for j in content:
                temp = j.split('|')
                outfile.write(temp[0] + '|' + temp[0] + '|')
                outfile.write(temp[3] + '|' + '不良信用' + '|')
                outfile.write(temp[9] + '|' + '3' + '|')
                outfile.write(temp[12] + '|' + '1' + '||||||')
                outfile.write(day + '||' + day + '|||')
                outfile.write('|' + temp[1] + '\n')

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print 'sx_comp_chean.py outfile_company outfile_company_cleaned'
        exit(0)
    infile = sys.argv[1]
    outfile = sys.argv[2]
    process_comany(infile,outfile)