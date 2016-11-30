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
SCRIPT 2, Milestone 2 Part 7

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
	dbList = []

	#Create TS Referencing
	#The 20 randomally selected vantagePtFiles
	for j in range(20):
		fileName = 'tsdata/ts'+str(indexes[j])+'.dat'
		dbName = "tsdb/db"+str(j)+".dbdb"
		x = np.loadtxt(fileName, delimiter=' ')
		vantagePt = ts.TimeSeries(x[:,1],x[:,0])
		vantagePtList.append(vantagePt)
		##Remove DB if it has previously been created
		if os.path.exists(dbName):
   			 os.remove(dbName)
		db = lab10.connect(dbName)
		dbList.append(db)

	#For all 20 Databases
	#Loop through 1000 TimeSeries
	#Add Key = Distance(vantagePt, comparePt)
	#Value = comparePT's fileName
	for i in range(1000):
		fileName = 'tsdata/ts'+str(i)+'.dat'
		x = np.loadtxt(fileName, delimiter=' ')
		comparePt = ts.TimeSeries(x[:,1],x[:,0])

		# Add Key,Value for ComparePt for all 20 Databases
		for j in range(20):
			dist = 2*(1-ss.kernel_corr(vantagePtList[j],comparePt))

			'''
			dbName = "tsdb/db"+str(j)+".dbdb"
			db = lab10.connect(dbName)
			db.set(dist, fileName)
			db.commit()
			db.close()
			'''

			dbList[j].set(dist, fileName)

	for j in range(20):
		dbList[j].commit()
		dbList[j].close()
