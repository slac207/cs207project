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
This file is a script to generate 20 Databases
From 20 different timeseries vantage points

How to run:
python generateDB.py

Requires folders:
tsdb
tsdata

'''

if __name__ == "__main__":

	indexes = np.random.choice(1000,20, replace = False)
	vantagePtList= []

	for j in range(20):
		fileName = 'tsdata/ts'+str(indexes[j])+'.dat'
		dbName = "tsdb/db"+str(j)+".dbdb"
		x = np.loadtxt(fileName, delimiter=' ')
		vantagePt = ts.TimeSeries(x[:,1],x[:,0])
		vantagePtList.append(vantagePt)
		if os.path.exists(dbName):
   			 os.remove(dbName)

	for i in range(1000):
		fileName = 'tsdata/ts'+str(i)+'.dat'
		x = np.loadtxt(fileName, delimiter=' ')
		comparePt = ts.TimeSeries(x[:,1],x[:,0])

		for j in range(20):
			dbName = "tsdb/db"+str(j)+".dbdb"
			db = lab10.connect(dbName)
			#dist = ss.kernel_corr(vantagePtList[j],comparePt)
			dist = random.random()

			db.set(dist, fileName)

			db.commit()
			db.close()
