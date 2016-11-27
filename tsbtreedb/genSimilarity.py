import os, sys
curr_dir = os.getcwd().split('/')
sys.path.append('/'.join(curr_dir[:-1]))
ts_dir = curr_dir[:-1]
ts_dir.append('timeseries')
sys.path.append('/'.join(ts_dir))
import timeseries.Timeseries as ts
import SimilaritySearch as ss
import numpy as np
import random
import lab10

'''
This file is a script to return
the 10 most similar timeseries to argv[1]

How to run:
python genSimilarity.py ts_test.dat

Requires folder:
tsdb

'''

def connect(dbname):
    try:
        f = open(dbname, 'r+b')
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    return DBDB(f)

if __name__ == "__main__":
	filename = sys.argv[1]
	x = np.loadtxt(filename, delimiter=' ')
	testPt = ts.TimeSeries(x[:,1],x[:,0])
	
	# Need to compare testPt against all Vantage pts
	# And find closest vantagePt

	#dbName = "tsdb/db"+str(j)+".dbdb"
	dbName = "tsdb/db0.dbdb"
	db = lab10.connect(dbName)


	#dist = ss.kernel_corr(vantagePtList[j],testPt)
	dist = random.random()
	keys, filenames = db.getAll_LTE(dist)
	distDict = {}

	for i in range(len(filenames)):
		x = np.loadtxt(filenames[i], delimiter=' ')
		comparePt = ts.TimeSeries(x[:,1],x[:,0])
		#dist = ss.kernel_corr(comparePt,testPt)
		dist = random.random()

		distDict[filenames[i]] = dist


	print(sorted(distDict.values())[:10])
	print(sorted(distDict, key=distDict.__getitem__)[:10])
