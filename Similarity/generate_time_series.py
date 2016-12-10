import sys
import os.path
from Similarity import distances
import numpy as np
import random
from timeseries.SMTimeSeries import SMTimeSeries as ts
from timeseries.StorageManager import FileStorageManager
import os
import pickle

global PATH
PATH = os.path.dirname(os.path.abspath(__file__))+'/'


def generate_time_series():
    fsm = FileStorageManager(directory='./FSM_filestorage')
    
    #script to generate and store 1000 timeseries
    for i in range(1000):
        x = distances.tsmaker(100, 100, 1000)
        fsm.store(i, x, overwrite=True)
        
        
if __name__ == "__main__":
    generate_time_series() #pragma: no cover
        