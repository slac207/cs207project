# CS207 Project - Milestone 2 - Team 1 Evaluates Team 3

# How To

### Script 1
**Where:**
generateTS.py

**What:**
Generates (using tsmaker) a set of 1000 time series, each stored in a file (stored in /tsdata)
Interpolated the tsmaker TS from 0.01 to 0.99 with 1024 points to set up a regular sampling.

**How:**
python generateTS.py

### Script 2
**Where:**
generateDB.py

**What:**
Randomly choose 20 vantage points, and create 20 database indexes (stored in /tsdb)

**How:**
python generateDB.py

### Script 3
**Where:**
genSimilarity.py

**What:**
 Takes the name of a new data file as input, and returns the name of an existing
data file whose time series is the most similar.

Compares the passed timeseries (in the first argument) to the timeseries stored in
folder /tsdata presuming databases in folder /tsdb are databases referencing /tsdata
timeseries.

**How:**
python genSimilarity.py tsdata/ts899.dat

**Returns:**
tsdata/ts899.dat
Saves string into Results/results.txt

## Additional files

### Tests
**Where:**
test_tsbtreedb.py

**What:**
Tests for SimilaritySearch.py and lab10.py

**How:**
py.test test_tsbtreedb.py

**Returns:**
13 passed in 0.92 seconds

### Similarity Search
**Where:**
SimilaritySearch.py

**What:**
Code to calculate distances from vantage points which you can then use to do similarity search

**How:**
python SimilaritySearch.py

**Returns:**
Some test script results

### Lab 10
**Where:**
lab10.py

**What:**
A Database class DBDB that implements a simple key/value database.
It lets you associate a key with a value, and store that association
on disk for later retrieval.
