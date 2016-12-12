import sys, os
import numpy as np
import random

from cs207rbtree import RedBlackTree as Database
from timeseries.SMTimeSeries import SMTimeSeries as ts
from Similarity.pick_vantage_points import pick_vantage_points
from Similarity import distances
from timeseries.timeSeriesABC import SizedContainerTimeSeriesInterface 
 
global PATH
PATH = os.path.dirname(os.path.abspath(__file__))+'/'

def sanity_check(filename,n,sm):
    """
    Function that manually finds the n most similiar timeseries to the given
    timeseries. Serves as a check of the vantage point method
    
    Returns: list of n most similiar filenames 
    """
    ans = []
    d = []
    
    if isinstance(filename,SizedContainerTimeSeriesInterface):
        ts1 = filename 
    else:
        try:
            #load the given file
            ts1 = ts.from_db(sm,int(filename))
        except KeyError: #if the id is invalid
            raise KeyError    
        
    for i in range(1000):
        ts2 = ts.from_db(sm,i)  
        dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
        d.append([dist,i])
        
    d.sort(key=lambda x: x[0])
    for i in range(1,n+1):
        ans.append(d[i][1])
        
    return ans


def find_similarity_of_points_in_radius(closest_vantage_pt, ts1, radius, sm):
    """
    Given a vantage point and a radius, find the points that fall within the
    circle around the vantage point. Then calculates the distance from all of these
    points to the timeseries of interest.
    
    closest_vantage_pt: number of the vantage point being considered
    ts1: timeseries of interest
    radius: radius of circle to consider
    
    Returns: list of tuples (distance, timeseries id) in sorted order
    
    """
    #open database for that vantage point
    db = Database.connect(PATH+"VantagePointDatabases/"+str(closest_vantage_pt)+".dbdb")
    
    #find all light curves within 2d of the vantage point
    light_curves_in_radius = db.get_nodes_less_than(radius)
    
    light_curves_in_radius.append(str(closest_vantage_pt)) # add in the vantage pt
    db.close()    
    
    #find similiarity between these light curves and given light curve
    distance = []
    for l in light_curves_in_radius:
        ts2 = ts.from_db(sm,int(l))
        dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
        distance.append([dist,int(l)]) 
    return distance

    
def find_most_similiar(filename,n, vantage_pts, sm):
    """
    Finds n most similiar time series to the time series of interest (filename)
    by using the supplied vantage points
    
    filename: timeseries of interest
    n: number of similiar timeseries to return (n must be between 1 and 20)
    vantage_pts: a list of the vantage point numbers 
    
    Returns: list of n most similiar filenames
    
    Notes: Correct behavior is not gaurenteed when n > the number of vantage points 
    """
    
    file_names = []
    
    if isinstance(filename,SizedContainerTimeSeriesInterface):
        ts1 = filename
    else:
        try:
            #load the given file
            ts1 = ts.from_db(sm,filename)
        except KeyError: #if the id is invalid
            raise KeyError
       
    #find the most similiar vantage point = d by calculating the distance from
    #the given TS to each vantage point 
    vantage_pts_dist = []
    for i in vantage_pts:
        ts2 = ts.from_db(sm,i)
        dist = distances.distance(distances.stand(ts1,ts1.mean(),ts1.std()), distances.stand(ts2,ts2.mean(),ts2.std()), mult=1)
        vantage_pts_dist.append([dist,i])
    
    vantage_pts_dist.sort(key=lambda x: x[0])
    
    all_pts_to_check = []
    for i in range(n):
        closest_vantage_pt = vantage_pts_dist[i][1]
        radius = 2*vantage_pts_dist[i][0]
        pts_in_radius = find_similarity_of_points_in_radius(closest_vantage_pt, ts1, radius, sm)
        for j in pts_in_radius:
            if j not in all_pts_to_check:
                all_pts_to_check.append(j)
                
    all_pts_to_check.sort(key=lambda x: x[0])
    
    for i in range(1,n+1): #ignore given timeseries 
        file_names.append(all_pts_to_check[i][1])  
        
    return file_names

