import sys, os, inspect, shutil
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]) 
import Similarity.distances as distances
import numpy as np
import random
from StorageManager import FileStorageManager

def generate_time_series():
    #make the FileStorageManager where we'll store all the Timeseries
    PATH = os.path.dirname(os.path.abspath(__file__))+'/'
    fsm = FileStorageManager(directory=PATH+'FSM_filestorage')
    
    #script to generate and store 1000 timeseries
    for i in range(1000):
        x = distances.tsmaker(100, 100, 1000)
        fsm.store(i, x, overwrite=True) #overwrite if they already exist
     
    return fsm #return the Storage Manager for future use 
            
            
if __name__ == "__main__":
    generate_time_series() #pragma: no cover
