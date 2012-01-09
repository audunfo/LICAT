#!/usr/bin/env python
# Implementation of extended learning curve model - ELCM 
# Project thesis, NTNU 2011 
# Author: Audun Follegg
####

from math import log, e

# input/output

def readConfig():
	# Holder of datasets (Dictionary)
	collections = {}
	# Get the Data
	file = "learningcurve.conf"
	infile = open(file,"r")
	line = infile.readline()
	while line:
		line = infile.readline()
		if line.find('#') == 0 or line == '\n' or line == '':
			continue
		elif line.find('Collection') == 0:
			colname = line.split(':')[1].strip()
			collections[colname] = {}
		elif line.find('Dataset') == 0:
			setname = line.split(':')[1].strip()
			myset = collections[colname][setname] = []
		else:
			myset.append(float(line.split(':')[1].strip()))
	infile.close()
	return collections

# Models		

def learningCurve(P_0, dT, nr_inv, K, t):
	t = float(t)
	P_of_t = P_0 * (nr_inv * (1 + e**(log(nr_inv - 1) - log(81)*t/dT ) )**(-1) )**(log(K)/log(2))
	return P_of_t
# Calculate the aggregated cost evolution of a product composed of n components

def collectionCurve(sets,t):
	# Calculate learningCurve for each set and add result
	C_sum_of_t = 0
	for s in sets:
		v = sets[s]
		C_sum_of_t += learningCurve(v[0],v[1],v[2]**(-1),v[3],t)
	return C_sum_of_t

# Returns list of cost for one component for t = [0,t]
def learningCurveList(P_0,dT,nr_inv,K,t):
    result =[]
    print P_0
    for i in range(t):
        result.append(learningCurve(P_0,dT,nr_inv,K,i))
        print result
    return result
    
# Returns list of cost for one collection of components for t = [0,t]    
def collectionCurveList(sets,t):
    result = []
    for i in range(t):
        result.append(collectionCurve(sets,i))
    return result

# Method that returns both collection curve and the individual curves for each dataset
def getLearningCurveResults(t):
    data = readConfig()
    
    result = {} # {colname: sets[]--> results}
    # colname -> collection name
    # First k/v pair in result[colname] is an array with the name "colname + result"
    for colname in data.keys():
        print "---- Collection name: " + colname + " ----"
        result[colname] = {}
        # Add the collection curve to the result first
        result[colname][colname +' result'] = collectionCurveList(data[colname],t)
        setnames = data[colname].keys()
        print "length of setnames in getLearningResults: "+str(len(setnames))
        # Add the results for each data set in the collection
        for set in setnames:
            result[colname][set] = []
            print "---- Dataset name: " + set + " ----"
            v = data[colname][set]
            result[colname][set].append(v)
            print learningCurveList(v[0],v[1],v[2]**(-1),v[3],t)
            result[colname][set].extend(learningCurveList(v[0],v[1],v[2]**(-1),v[3],t))
        
    return result
            

def printFunction():
	print "Follegg's Forecasting Model:"
	print " ========================= "
	collections = readConfig()
	
	for sets in collections.keys():
		print "\n----"
		print "---- Collection name: " + sets + " ----"
		print "----"
		
		setnames = collections[sets].keys()
		for s in setnames:
			v = collections[sets][s]
			print "\n"
			print '* ' + s + ' *'
			print ""
			print "-> Settings overview:"
			print v 
			print ""

			print "-> Results:"
			for t in range(30):
				print learningCurve(v[0],v[1],v[2]**(-1),v[3],t)
		print "\n Accumulated result:"	
		print collectionCurve(collections[sets],5)

if __name__ == '__main__':
    getLearningCurveResults(30)
    printFunction()
		#for t in range (20):
			#print collectionCurve(sets,t)
	#		print "Colname: "+ c +"Sets: "
	#		print collections[c]
  