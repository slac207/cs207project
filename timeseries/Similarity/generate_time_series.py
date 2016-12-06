import sys
import os.path
import inspect
import shutil
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]) 
import distances
import numpy as np
import random
import BinarySearchDatabase
from ArrayTimeSeries import ArrayTimeSeries as ts
import os
import pickle

global PATH
PATH = 'timeseries/Similarity/'


def generate_time_series():
    try:
        shutil.rmtree(PATH+'GeneratedTimeseries')
    except:
        pass
    os.mkdir(PATH+'GeneratedTimeseries')     
    
    #script to generate and store 1000 timeseries
    for i in range(1000):
        x = distances.tsmaker(100, 100, 1000)
        with open(PATH+"GeneratedTimeseries/Timeseries"+str(i),'wb') as f:
            pickle.dump(x, f)
        
if __name__ == "__main__":
    generate_time_series() #pragma: no cover
        