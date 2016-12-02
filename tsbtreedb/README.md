# CS207 Project - Milestone 2 - Team 1 Evaluates Team 3

# How To

### Script 1
** Where: **
generateTS.py

** What: **
Generates (using tsmaker) a set of 1000 time series, each stored in a file (stored in /tsdata)
Interpolated the tsmaker TS from 0.01 to 0.99 with 1024 points to set up a regular sampling.

** How: **
python generateTS.py

### Script 2
** Where: **
generateDB.py

** What: **
Randomly choose 20 vantage points, and create 20 database indexes (stored in /tsdb)

** How: **
python generateDB.py

### Script 3
** Where: **
genSimilarity.py

** What: **
 Takes the name of a new data file as input, and returns the name of an existing
data file whose time series is the most similar.

Compares the passed timeseries (in the first argument) the timeseries stored in
the folder /tsdb

** How: **
python genSimilarity.py tsdata/ts899.dat
Returns:
tsdata/ts899.dat
