# -*- coding: utf-8 -*-
#modify the format of date
def process_hum(filename,outfilename):
    with open(filename, 'r') as infile:
        with open(outfilename, 'w') as outfile:
            content = infile.readlines()
            field = [9, 10, 13, 12, 17, 15, 23, 24, 11, 25, 18, 19, 26, 27, 20, 21,]
            for j in content:
                temp = j.split('|')
                temp[24] = temp[24][:4] + '-' + temp[24][4:6] + '-' + temp[24][6:]
                #print temp[21], '年'.replace('年', '-')
                temp[21] = temp[21].replace('年', '-').replace('月', '-')[:-3]
                #print temp[21], temp[24]
                for i,k in enumerate(field):
                    if i != 0:
                        outfile.write('|')
                    outfile.write(temp[k])
                outfile.write('\n')

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print 'sx_hum_chean.py outfile_hum outfilehum_cleaned'
        exit(0)
    infile = sys.argv[1]
    outfile = sys.argv[2]
    process_hum(infile,outfile)
              
