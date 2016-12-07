import sys, inspect
import os.path
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]) 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
import unittest
from pytest import raises
from cs207rbtree.cs207rbtree import RedBlackTree
#import BinarySearchDatabase as Database
#from generate_time_series import generate_time_series
from TimeseriesDB.generate_SMTimeseries import generate_time_series
from pick_vantage_points import pick_vantage_points
#from find_most_similar import find_most_similiar, sanity_check
import numpy as np
import math
import distances
from scipy import signal
import os
import pickle
import argparse

global PATH
PATH = 'timeseries/Similarity/'


class DataBase_tests(unittest.TestCase): 
    #def setUp(self):
        #if os.path.isfile("/tmp/test.dbdb"):
            #os.remove("/tmp/test.dbdb")
        #self.db1 = RedBlackTree.connect("/tmp/test.dbdb")
        #self.db1.set(2,'database1')
        #self.db1.set(1,'database2')
        #self.db1.set(0.5,'database3')
        #self.db1.set(3.2222,'database4')
        #self.db1.set(4,'database5')
        #self.db1.set(5,'database6')
        #self.db1.set(200,'database7')
        #self.db1.commit()
        #self.db1.close()    
        ##generate_time_series()
        ##vp = np.array(pick_vantage_points(20))        
        
    #def tearDown(self):
        #del self.db1
        
    #def test_nodes_less_than(self):
        #"""tests the function that finds nodes than a certain value"""
        #db1 = RedBlackTree.connect("/tmp/test.dbdb")
        #assert (db1.get(3.2222) == 'database4')
        #assert (db1.get_nodes_less_than(2) == ['database3', 'database2', 'database1'])
        #assert (db1.get_nodes_less_than(4.5) == ['database3', 'database2', 'database1', 'database4', 'database5'])
        #assert (db1.get_nodes_less_than(0.5) == ['database3'])
        #assert (db1.get_nodes_less_than(0) == [])
        #db1.close()

        
    def test_SM_integration(self):
        sm = generate_time_series()
        vp = np.array(pick_vantage_points(20,sm))
        
    #def test_generate_time_series(self):
        #"""tests that the generate_time_series """
        #for i in range(1000):
            #with open(PATH+"GeneratedTimeseries/Timeseries"+str(i), "rb") as f:
                #pickle.load(f)
            
        #with raises(FileNotFoundError):
            #with open(PATH+"GeneratedTimeseries/Timeseries"+str(1000), "rb") as f:
                #pickle.load(f)
            
        
    #def test_pick_vantage_points(self):
        #vp = []
        #with open(PATH+'VantagePointDatabases/vp') as f:
            #for line in f:
                #vp.append(int(line.rstrip('\n')))
        #for i in range(1000):
            #db = Database.connect(PATH+"VantagePointDatabases/"+str(i)+".dbdb")
            #db.close()
            
    #def test_find_most_similiar(self):
        #vp = []
        #with open(PATH+'VantagePointDatabases/vp') as f:
            #for line in f:
                #vp.append(int(line.rstrip('\n')))

        #filename = PATH+"GeneratedTimeseries/Timeseries200"
        #n = 20
        #ans = find_most_similiar(filename, n, vp)
        #ans2 = sanity_check(filename,n)
        #print(ans)
        #print(ans2)
        #assert np.array_equal(ans,ans2)     
        
        #filename = PATH+"GeneratedTimeseries/Timeseries932"
        #n = 3
        #ans = find_most_similiar(filename, n, vp)
        #ans2 = sanity_check(filename,n)
        #print(ans)
        #print(ans2)
        #assert np.array_equal(ans,ans2)     
        
        #filename = PATH+"GeneratedTimeseries/Timeseries32"
        #n = 5
        #ans = find_most_similiar(filename, n, vp)
        #ans2 = sanity_check(filename,n)
        #print(ans)
        #print(ans2)
        #assert np.array_equal(ans,ans2)     
            
        
    #def test_command_line_program(self):
        #find_most_similar.main(['timeseries','Timeseries1','--n','1'])
        #find_most_similar.main(['timeseries','Timeseries1','--n','1','--save','True']) 
                    
                              
                                  
if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover