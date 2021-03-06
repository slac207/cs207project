import sys, os, shutil, inspect
from Similarity import distances
import numpy as np
import random
import argparse
from cs207rbtree import RedBlackTree as Database 
from timeseries.StorageManager import FileStorageManager
from timeseries.SMTimeSeries import SMTimeSeries as ts 

global PATH
PATH = os.path.dirname(os.path.abspath(__file__))+'/'

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
