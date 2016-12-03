import os
import sys

curr_dir = os.getcwd().split('/')
sys.path.append('/'.join(curr_dir[:-1]))
ts_dir = curr_dir[:-1]
ts_dir.append('timeseries')
sys.path.append('/'.join(ts_dir))
import timeseries.Timeseries as ts
import SimilaritySearch as ss
import numpy as np
import lab10

'''
SCRIPT 3, Milestone 2 Part 7

This file is a script to return
the 10 most similar timeseries to argv[1]

How to run:
python genSimilarity.py tsdata/ts899.dat

Returns (Prints):
#### Nearest Timeseries ####
tsdata/ts899.dat

Example 2:
python genSimilarity.py ts_test.dat

Returns (Prints):
#### Nearest Timeseries ####
tsdata/ts398.dat


Requires folder:
tsdb

'''

if __name__ == "__main__":
    # Load in the TS to Evaluate
    filename = sys.argv[1]
    x = np.loadtxt(filename, delimiter=' ')
    origTs = ts.TimeSeries(x[:, 1], x[:, 0])
    time = np.arange(0.0, 1.0, 0.01)
    testTs = origTs.interpolate(time)

    # Find the Nearest vantagePt
    minDist = float('inf')
    for j in range(20):
        dbName = "tsdb/db" + str(j) + ".dbdb"
        db = lab10.connect(dbName)
        vantagePtFile = db.get(0)
        x = np.loadtxt(vantagePtFile, delimiter=' ')
        comparePt = ts.TimeSeries(x[:, 1], x[:, 0])
        dist = 2 * (1 - ss.kernel_corr(comparePt, testTs))
        if dist < minDist:
            minDist = dist
            minDbName = dbName
            minVantagePtFile = vantagePtFile

    # Connect to DB Referencing the Nearest vantagePT
    db = lab10.connect(minDbName)
    keys, filenames = db.get_All_LTE(float(2) * minDist)
    nFiles = len(filenames)

    # Dictionary Key File, Val = Distance to testTs
    distDict = {}

    # Get dist between testTs and all TS within key below 2*minDist
    for i in range(nFiles):
        x = np.loadtxt(filenames[i], delimiter=' ')
        comparePt = ts.TimeSeries(x[:, 1], x[:, 0])
        dist = 2 * (1 - ss.kernel_corr(comparePt, testTs))
        # dist = random.random()
        distDict[filenames[i]] = dist

    # Commented out these prints that return up to 10 of the nearest TS
    # Print 10 Nearest Distances (Assuming you have reviewed at least 10 TS)
    # print(sorted(distDict.values())[:10])
    # Print 10 nearest TS FIles (Assuming you have reviewed at least 10 TS)
    # print(sorted(distDict, key=distDict.__getitem__)[:10])

    # Return Nearest Timeseries
    nearest = sorted(distDict, key=distDict.__getitem__)[0]
    print("#### Nearest Timeseries ####")
    print(nearest)
    file_path = 'Results/results.txt'
    text_file = open(file_path, "w")
    text_file.write(nearest)
    text_file.close()
