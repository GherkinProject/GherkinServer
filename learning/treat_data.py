#!/usr/bin/python

import sys

def treat_data(fileLoc, featLoc):
    """read data from csv and simplify them"""
    extBase = []
    with open(featLoc) as featFile:
        for line in featFile.readlines():
            extBase.append(line.split(":")[0])
   
    #print "extensions loaded"
    with open(fileLoc) as fileFile:
        for line in fileFile.readlines():
            line = line.split("\n")[0]
            line = line[1:]
            with open('constant.csv', 'a+') as constFile:
                #print "csv file loaded"
                constFile.write(line)
                for ext in extBase:
                    with open("data/" + line + "." + ext + ".csv") as f:
                        #print ext + " csv file loaded"
                        c = 0
                        r = []
            	        for row in f.readlines():
            	            if row[0] != '%':
                                row = row.split(',')
                                c = c + 1
                                try:
                                    for i in xrange(len(row)):
                                        r[i] = r[i] + float(row[i])
                                except:
                                    r = [float(i) for i in row]
            	        r = [i / c for i in r]
            	        for i in r:
            	            constFile.write('$'+str(i))
        	        
                constFile.write('\n')
            

#print treat_data("", "featureplan")
treat_data(sys.argv[1], sys.argv[2])
