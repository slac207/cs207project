# Timeseries Module Documentation

## Purpose
Creates an interface for the Timeseries class and creates all the classes that inherit from this interface

## Installation
Before running any files, `python setup.py install` must be run from the top level directory, cs207project. 

## Contents
* timeSeriesABC.py: implements the base Timeseries class, TimeSeriesInterface, and the two classes that directly inherit from it
  1. SizedContainerTimeSeriesInterface: timeseries which contain a notion of "containerness"
  2. StreamTimeSeriesInterface: timeseries with no underlying storage
* Timeseries.py: implements the basic Timeseries class which stores timeseries times and values as arrays. Inherits from the SizedContainerTimeSeriesInterace which inherits from the TimeSeriesInterface
* ArrayTimeSeries.py: implements a timeseries class whose storage is numpy arrays. Inherits from SizedContainerTimeSeriesInterace.
* SimulatedTimeSeries.py: timeseries which uses a generator as data. Inherits from StreamTimeSeriesInterface.
* SMTimeSeries.py: combines the ArrayTimeSeries implementation with a storage manager. Inherits from SizedContainerTimeSeriesInterace.
* binarysearch.py: Modified binary search implementation used for producing linearly interpolated values in the Timeseries class
* lazy.py: allows for lazy operations, isolating the function class for the function execution.
* StorageManger.py: interface and implementation for storing and retrieving timeseries objects on disk

## Usage

Creating different types of timeseries
```
#Create Timeseries
timeseries = TimeSeries(range(0,4),range(10,14))
#Create Array Timeseries
array_timeseries = ArrayTimeSeries(range(10,14),range(0,4))
#Create SMTimeSeries (and the FileStorageManager it uses to store them)
sm = FileStorageManager(directory='./temp_dir1')
sm_timeseries = SMTimeSeries(range(10,14),range(0,4),id=1,SM=sm)
#Create Simulated Timeseries
simulated_timeseries = SimulatedTimeSeries(iter(range(10)))
```
Useful timeSeriesABC Operations (which apply to any ts that inherit from timeSeriesABC)
```
ts.mean() #calculates the mean of the timeseries values
ts.std() #calculates the std of the timeseries values
ts.lazy #creates lazyOperation instance
iter(ts) #iterate over values
ts.itervalues() #alternate way to iterate over values
ts.itertimes() #iterate over times
ts.iteritems() #iterate over (time, value) pairs
```
Useful SizedContainerTimeSeriesInterface Operations:
```
ts.items() # returns (time, value) tuples
ts1-ts2 #subtract timeseries values, times of ts1 and ts2 must match 
ts1+ts2 #add timeseries values, times of ts1 and ts2 must match 
ts1*ts2 #multiply timeseries values, times of ts1 and ts2 must match 
len(ts)
ts.values() 
ts.times()
ts[1] #returns the value at index supplied
ts[2] = 4
ts1 = ts2 #equal if have the same times and values
ts.interpolate([10, 12, 14]) #linearly interpolates the times values supplied
```
Useful StreamTimeSeriesInterface Operations:
```
ts = SimulatedTimeSeries(iter(range(10)))
ats = ts.produce(20) #returns list of (times,values) tuples of length specified
ts.online_std() #provides running std
ts.online_mean() #provides running mean
```

Useful StorageManager Operations:
```
sm = FileStorageManager()
sm.store(12,ts) #store timeseries with given id as its identifier. If no index provided, generates one
sm.size(10) #length of a timeseries at given id
sm.get(10) #returns timeseries for given id
```

## Testing 
There are 5 testing files for the code in this module and they are all contained in the [test folder](https://github.com/slac207/cs207project/tree/master/tests). These files can be run using `python setup.py test`. 

1. test_binarysearch.py: tests our modified binary_search implementation used in interpolating the Timeseries class
2. test_FileStorageManager: tests the functionality of the FileStorageManager
3. test_lazy: tests the ability to create lazy operations
4. test_SimulatedTimeseries: test the functionality of the SimulatedTimeSeries class
5. test_Timeseries: tests the functionality of the different SizedContainerTimeSeriesInterface classes and their interactions

