#!/usr/bin/env python
# encoding: utf-8
"""
licat.py
Created by Audun Follegg on 2011-11-05.
A part of the spesialization project at NTNU 2011
####

"""
import sys
import getopt

import learningcurve as lc
import costmodel as cm
import xlrd,xlwt


help_message = '''
Velcome to Li-Fi Cost Analysis Tool.
Here are a list of the commands to use:
-l : calculates the learningcurve
-c : calculates the costmodel

'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv

    commands = []
    inputfiles =[]
    output = ""
    cmodel = False
    lcurve = False
    outputFile = False
    t = 0

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:lcf:vt:", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)

        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
                print "runnng verbose \n"
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
            if option in ("-l","--lcurve"):
                lcurve = True
                commands.append('l')
                print "lcurve with specified file: "+value
            if option in ("-c", "--cmodel"):
                cmodel = True
                commands.append('c')
                print " Using "+ value+" for lcurve config"
            if option in ("-f", "--cmodel"):
                inputfiles.append(value)
                print " Using inputfile: "+ value
            if option in ("-t", "--time"):
                t=value

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2

    print commands
    print inputfiles
    print t
    lcurveResult = {}
    cmodelResult = {}

    if cmodel:
        if t>0:
            cmodelResult = cm.getCostModelResults(int(t))
        else:
            cmodelResult = cm.getCostModelResults(30)

    elif lcurve:
        if t>0:
            lcurveResult = lc.getLearningCurveResults(int(t))
        else:
            lcurveResult = lc.getLearningCurveResults(30)
    else: 
        if t>0:
            lcurveResult = lc.getLearningCurveResults(int(t))
            cmodelResult = cm.getCostModelResults(int(t))
        else: 
            lcurveResult = lc.getLearningCurveResults(30)
            cmodelResult = cm.getCostModelResults(30)
            
   # printResults(lcurveResult,cmodelResult,t)
    writeXLS(lcurveResult,cmodelResult,t,output)
    printResults(lcurveResult,cmodelResult,1)

def writeXLS(l_result,c_result,t,filename):

    book = xlwt.Workbook()
    cmodel_sheet = book.add_sheet('Cost Model Results')
    lmodel_sheet = book.add_sheet('Learning Curve Results')

    if len(l_result)>0:
        # lmodel_sheet.write(0,0,'t')
        #        lmodel_sheet.write(0,1,'Fixed purchase cost')
        #        lmodel_sheet.write(0,2,'LCurve purchase cost')
        #        lmodel_sheet.write(0,3,'Energy')
        #        lmodel_sheet.write(0,4,'Maintenence')
        #        lmodel_sheet.write(0,5,'Total cost')

        # write_merge(r1,r2,c1,c2,label,style)


        # result[colname][set].extend(learningCurveList(v[0],v[1],v[2]**(-1),v[3],t))
        # i= row counter, j = column counter
        j = 3
        i= 3
        colnames = l_result.keys()
        for colname in colnames:

            lmodel_sheet.write(i,j,str(colname))
            setnames = l_result[colname].keys()
            for set in setnames:
                i+=2
                lmodel_sheet.write(i,j,str(set))
                for v in l_result[colname][set]:
                    i+=1
                    lmodel_sheet.write(i,j,str(v))
            i=3
            j+=4
        if len(filename)>0:
            book.save(filename)
        else:
            book.save('result.xls')

    if len(c_result)>0:
        print "lets do even more writing"
    print "writing to file "+filename
    print l_result

     # cmodel_sheet.write(0,0,'t')
     #       cmodel_sheet.write(0,1,'Fixed purchase cost')
     #       cmodel_sheet.write(0,2,'LCurve purchase cost')
     #       cmodel_sheet.write(0,3,'Energy')
     #       cmodel_sheet.write(0,4,'Maintenence')
     #       cmodel_sheet.write(0,5,'Total cost')
     #
    #  e = results["Energy"]
    #  m = results["Maintenence"]
    #  s = results["Sum"]
    #
    #  for i in range(t):
    #      cmodel_sheet.write(i+1,0,i)
    #      cmodel_sheet.write(i+1,3,e[i])
    #      cmodel_sheet.write(i+1,4,m[i])
    #      cmodel_sheet.write(i+1,5,s[i])
    #      book.save('result3.xls')

def printResults(l_result,c_result,t):

    print intro +"\n"
    
    # if len(l_result.keys)>0:
    print lc_intro

    # Print Learning Curve results
    colnames = l_result.keys()
    for colname in colnames:
        print "\nCollection: " + str(colname)
        setnames = l_result[colname].keys()
        for set in setnames:
            print "\nDataSet: " + str(set) +"\n"
            for v in l_result[colname][set]:
                print v


# Syntax of LearningCurveRes:
# result[colname][set].extend(learningCurveList(v[0],v[1],v[2]**(-1),v[3],t))


intro = ''' ############  LICAT - Li-Fi Cost Analysis Tool ############
'''

lc_intro = ''' ############           Learning curve results        ############
'''
cm_intro = ''' ############           Ownership cost results        ############
'''

if __name__ == "__main__":
    sys.exit(main())

