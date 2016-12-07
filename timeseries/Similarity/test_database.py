import sys, inspect
import os
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]) 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0,currentdir)
sys.path.insert(0,parentdir+'/cs207rbtree')

import unittest
from pytest import raises
import numpy as np

from cs207rbtree import RedBlackTree #import RBTree
from TimeseriesDB.generate_SMTimeseries import generate_time_series #script to generate time series
from pick_vantage_points import pick_vantage_points #script to pick vantage pts
from find_most_similar import find_most_similiar, sanity_check #scipts that find most similiar
from SMTimeSeries import SMTimeSeries as ts #use SMTimeseries

global PATH
PATH = 'timeseries/Similarity/'


class DataBase_tests(unittest.TestCase): 
    def setUp(self):
        if os.path.isfile("/tmp/test.dbdb"):
            os.remove("/tmp/test.dbdb")
        self.db1 = RedBlackTree.connect("/tmp/test.dbdb")
        self.db1.set(2,'database1')
        self.db1.set(1,'database2')
        self.db1.set(0.5,'database3')
        self.db1.set(3.2222,'database4')
        self.db1.set(4,'database5')
        self.db1.set(5,'database6')
        self.db1.set(200,'database7')
        self.db1.commit()
        self.db1.close()    
        self.sm = generate_time_series()
        self.vp = np.array(pick_vantage_points(20,self.sm))        
        
    def tearDown(self):
        del self.db1
        del self.sm
        del self.vp
        
    def test_nodes_less_than(self):
        """tests the function that finds nodes than a certain value"""
        db1 = RedBlackTree.connect("/tmp/test.dbdb")
        assert (db1.get(3.2222) == 'database4')
        assert (db1.get_nodes_less_than(2) == ['database3', 'database2', 'database1'])
        assert (db1.get_nodes_less_than(4.5) == ['database3', 'database2', 'database1', 'database4', 'database5'])
        assert (db1.get_nodes_less_than(0.5) == ['database3'])
        assert (db1.get_nodes_less_than(0) == [])
        db1.close()
        
        
    def test_generate_time_series(self):
        """tests that the generate_time_series """
        for i in range(1000):
            ts1 = ts.from_db(self.sm,i)
            
        
    def test_pick_vantage_points(self):
        for i in self.vp:
            db = RedBlackTree.connect(PATH+"VantagePointDatabases/"+str(i)+".dbdb")
            db.close()
            
    def test_find_most_similiar(self):

        filename = 200
        n = 20
        ans = find_most_similiar(filename, n, self.vp, self.sm)
        ans2 = sanity_check(filename,n,self.sm)
        assert np.array_equal(ans,ans2)     
        
        filename = 932
        n = 3
        ans = find_most_similiar(filename, n, self.vp, self.sm)
        ans2 = sanity_check(filename,n, self.sm)
        assert np.array_equal(ans,ans2)     
        
        filename = 32
        n = 5
        ans = find_most_similiar(filename, n, self.vp, self.sm)
        ans2 = sanity_check(filename,n, self.sm)
        assert np.array_equal(ans,ans2)     
            
    
                                  
if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover