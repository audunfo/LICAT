#!/usr/bin/env python
# Implementation of extended learning curve model - ELCM
# Project thesis, NTNU 2011
# Author: Audun Follegg
####
# if line.find('Dataset') == 0:
#                                                 setname = line.split(':')[1].strip()
#                                                 sets[setname] = []

from math import log, e, floor, ceil
from lcurvemodel import learningCurve, collectionCurve, readConfig as lcurveConf
import csv
import xlwt

def readConfig():
    # Holder of datasets  {i: (q,c)}
    components = []
    # Get the Data
    file = "costdata.conf"
    infile = open(file,"r")
    line = infile.readline()

    while line:
        line = infile.readline()
        if line.find('#') == 0 or line == '\n' or line == '':
            continue
        else:
            item = line.split(':')
            name, q, c, e, l = item
            components.append(( name, int(q), float(c), float(e),int(l)))

    infile.close()
    return components


    # Fixed component purchase cost
def fixedCostSum(components):
    costs = [ q*c for name, q, c, _, _ in components]
    return sum(costs)

def fixedCost(components):
    return [(name,q*c) for name,q,c,_,_ in components]        

    # Components costs(t)
def variableCostSum(components,t):
        # Name, q, e for each component. If c==0: calc cost from learning curve
    var_comp = [ (name,q,e) for name, q, c,e,_ in components if c == 0]
        # Collections of components modelled usin ELC
    lcurveComps = lcurveConf()
    costs = []
    for name,q,e in var_comp:
        colname = lcurveComps[name]
        cost_t = collectionCurve(colname, t)
        costs.append((cost_t,q))
    return sum([c*q for c,q in costs])

def variableCostList(components,t):
    var_comp = [ (name,q,e,l) for name, q, c,e,l in components if c == 0]
          # Collections of components modelled usin ELC
    lcurveComps = lcurveConf()
    costs = {}
    for name,q,e,l in var_comp:
        costs[name] =[]
        colname = lcurveComps[name]
        for n in range(t):
            cost_n = collectionCurve(colname, n)
            costs[name].append((n,cost_n,q,l))
    return costs
    
    # Returns list[(name,e_cost)]
def energyCost(components,hrs,e_price):
    e_costs = [(name,q*e*hrs*e_price) for name,q,c,e,_ in components]
    return e_costs

    # Returns dict[name] = [(hour,quantity,cost)]
def maintenenceCost(components,hrs):
    m_data     = [(name,q,c,l) for name,q,c,e,l in components]
    lcurveComps = lcurveConf()
    result     = []
    
    for name,q,c,l in m_data:
        ltmp = l
        h=0
        print "-- > "+name+"< --"
        print "component length: " + str(len(components))
        for h in range(hrs):       
            if h>=l:
                if c==0:
                    colname = lcurveComps[name]
                    c = collectionCurve(colname,hoursInYears(h))
                y = hoursInYears(h)
                print y
                result.append((name,y,h,q,c))
                l += ltmp
    return result

def yearsInHours(t):
    return int(round(t*365*24))
def hoursInYears(t):
    return int(round(t/8765,0))
def daysInWeeks(t):
    return int((round(t/7),0))
def hoursInDays(t):
    return int(round(t/24,0))
            
"""
END MODEL FUNCTIONS
"""            
###         Energy Costs         ###
   #__________________________________#
   # hrs     = hours of operation     #
   # e_price = average price of 1 KWh #
   # ->> returns list of costs        #

def getCostModelResults(t):
    components = readConfig()
    curveComponents = lcurveConf()
    f_costs = fixedCostSum(components)
    m_costs = []
    e_costs = []
    c_sum   = []
    # ADD PURCHASE COST
    i=0
    init_cost = float(f_costs) + float(variableCostSum(components,0))
   
    e_cost_sum = 0
    m_cost_sum = 0
    total_sum = 0
    m = maintenenceCost(components,yearsInHours(t))
    for i in range(t):
        e = energyCost(components,yearsInHours(1),0.24106)
       
        e_unit_sum = sum([c for name,c in e])
        e_cost_sum += e_unit_sum
       
        e_costs.append(e_cost_sum)
        # print "Ecost for t="+str(i)
        # print e_costs
        
        m_unit_sum = sum([q*c for name,y,h,q,c in m if y==i])
        # print "unit m cost sum"
        # print m_unit_sum
        m_cost_sum += m_unit_sum
        m_costs.append(m_cost_sum)
        # print "Mcost for t="+str(i)
        # print m_costs
       
        if i ==0: 
            total_sum += e_unit_sum + m_unit_sum + init_cost
            c_sum.append(total_sum)
            # c_sum.append(e_costs[i] + m_costs[i] + init_cost)
        else:
            total_sum += e_unit_sum + m_unit_sum
            c_sum.append(total_sum)
            # c_sum.append(e_costs[i] + m_costs[i])
        # print "Csum , ecost , mcost"
        # print c_sum,e_costs[i], m_costs[i],init_cost
        
    result = {'Sum':c_sum,'Energy':e_costs,'Maintenence':m_costs}
    return result
    
def readXLS():
    
    book = xlrd.open_workbook("results.xls")
    print "The number of worksheets is", book.nsheets
    print "Worksheet name(s):", book.sheet_names()
    sh = book.sheet_by_index(0)

def writeXLS(results,t,sheet):
    book = xlwt.Workbook()
    cmodel_sheet = book.add_sheet('Cost Model Results')
    lmodel_sheet = book.add_sheet('Learning Curve Results')
    
    cmodel_sheet.write(0,0,'t')
    cmodel_sheet.write(0,1,'Fixed purchase cost')
    cmodel_sheet.write(0,2,'LCurve purchase cost')
    cmodel_sheet.write(0,3,'Energy')
    cmodel_sheet.write(0,4,'Maintenence')
    cmodel_sheet.write(0,5,'Total cost')
    
    e = results["Energy"]
    m = results["Maintenence"]
    s = results["Sum"]
    
    for i in range(t):
        print i
        print e[i]
        print m[i]
        print s[i]
    
    for i in range(t):
        cmodel_sheet.write(i+1,0,i)
        cmodel_sheet.write(i+1,3,e[i])
        cmodel_sheet.write(i+1,4,m[i])
        cmodel_sheet.write(i+1,5,s[i])
    book.save('coool.xls')

    
if __name__ == '__main__':
    t=15
    x = getCostModelResults(t)
    writeXLS(x,t,0) 
    
    print "20000 timer i aar"+ str(hoursInYears(70000))
    