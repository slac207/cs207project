import sys, inspect, os
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]) 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir)
print(sys.path)
#parentdir = os.path.dirname(currentdir)
#print("SIMSEARCH",parentdir)
#sys.path.insert(0,parentdir+'/timeseries')

from Similarity.pick_vantage_points import pick_vantage_points
from generate_SMTimeseries import generate_time_series


def initialize_simsearch_parameters():
    sm = generate_time_series()
    vp = pick_vantage_points(20,sm)
    d = dict({'vantage_points':vp,'storage_manager':sm})
    return d

if __name__ == "__main__":
    initialize_simsearch_parameters()