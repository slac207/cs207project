import sys, os, shutil, inspect
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]) 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0,currentdir)
sys.path.insert(0,parentdir)
#sys.path.insert(0,parentdir+'/timeseries/Similarity')

import distances
import numpy as np
import random
import argparse

from cs207rbtree import RedBlackTree as Database
from StorageManager import FileStorageManager
from SMTimeSeries import SMTimeSeries as ts

global PATH
#PATH = 'timeseries/Similarity/'
PATH = '../timeseries/Similarity/'
#PATH = './'#./timeseries/Similarity/'

def pick_vantage_points(arg, sm):
    """
    Code which picks 20 vantage points and produces a database for each one.
    The database stores (key,value) pairs where:
    key = distance from timeseries to vantage point (kernel coefficient)
    value = id of timeseries (0-999)
    
    returns: list of vantage points (integers from 0-999)
    """
    try:
        parser = argparse.ArgumentParser(description="vantage points")
        parser.add_argument('--n', help='number of vantage points', type=int, default=20)
            
        args = parser.parse_args(arg)
        num = args.n
    except:
        num = arg
    
    print("P",parentdir)
    print("C", currentdir)

    try:
        shutil.rmtree(PATH+'VantagePointDatabases')
        os.mkdir(PATH+'VantagePointDatabases')    
    except:
        os.mkdir(PATH+'VantagePointDatabases')    
        
    
    vantage_pts = random.sample(range(0,1000),num)

    for vantage_point in vantage_pts:
        try:
            os.remove(PATH+"VantagePointDatabases/"+str(vantage_point)+".dbdb")
            db1 = Database.connect(PATH+"VantagePointDatabases/"+str(vantage_point)+".dbdb")
        except:
            db1 = Database.connect(PATH+"VantagePointDatabases/"+str(vantage_point)+".dbdb")
        
        ts2 = ts.from_db(sm,vantage_point) #load in the timeseries from the Storage Manager 

        for i in range(1000):
            if i != vantage_point:
                ts1 = ts.from_db(sm,i) #load in the timeseries from the Storage Manager 
                dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
                db1.set(dist,str(i))
    
        db1.commit()
        db1.close()
        
        f = open(PATH+'VantagePointDatabases/vp', 'w')
        for i in vantage_pts:
            f.write(str(i)+"\n")
        f.close()
        
    return vantage_pts    
