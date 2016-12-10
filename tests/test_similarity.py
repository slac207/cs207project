import sys, inspect
import os.path
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]) 
import unittest
from pytest import raises
from ArrayTimeSeries import ArrayTimeSeries as ts
import numpy as np
import math
import distances
from scipy import signal

class SimilarityTest(unittest.TestCase):   
        
    def test_tsmakers(self):
        t1 = distances.tsmaker(0.5, 0.1, 0.01)
        assert type(t1) == ts #make sure tsmaker returns correct type
        t2 = distances.random_ts(0.5)
        assert type(t2) == ts #make sure random_ts returns correct type 
        
    def test_standardize(self):
        t0 = ts(times=[0,1,2,4,5,6],values=[3,4,5,6,7,8])
        assert t0.mean() == 5.5 #check mean
        assert t0.std() == np.sqrt(7/2.0) #check sqrt
        
        standardized_values = distances.stand(t0,t0.mean(),t0.std()).values()
        assert (str(standardized_values) == str(np.array([-1.33630621,-0.80178373,-0.26726124 ,0.26726124 ,0.80178373 ,1.33630621]))) #check that standardized values are correct
        
    def test_ccor(self): #checks that the ccor function returns the correct result
        t0 = ts(times=[0,1,2,3],values=[1,2,3,4])
        t0_stand = distances.stand(t0,t0.mean(),t0.std())
        t1 = ts(times=[0,1,2,3],values=[-1,2,1,-1])
        t1_stand = distances.stand(t1,t1.mean(), t1.std())
        d = distances.ccor(t0_stand,t1_stand)
        assert (str(d) == str(np.array([ 0.19364917,-0.71004695,-0.06454972 ,0.5809475 ])))
        
    def test_maxcorratphase(self): #checks that maxcorratphase returns the correct result
        t0 = ts(times=[0,1,2,3],values=[1,2,3,4])
        t0_stand = distances.stand(t0,t0.mean(),t0.std())
        t1 = ts(times=[0,1,2,3],values=[-1,2,1,-1])
        t1_stand = distances.stand(t1,t1.mean(), t1.std()) 
        assert (distances.max_corr_at_phase(t0_stand,t1_stand)) == (3, 0.58094750193111244)
        
    def test_kernelcorr(self): 
        """tests that the kernelized cross correlation is 1 when
        the two timeseries are identical and that the kernel corr is <= 1"""
        
        t0 = ts(times=[0,1,2,4,5,6],values=[3,4,5,6,7,8])
        t0_stand = distances.stand(t0,t0.mean(),t0.std())
        t1 = ts(times=[0,1,2,4,5,6],values=[3,4,5,6,7,8])
        t1_stand = distances.stand(t1,t1.mean(), t1.std())
        ans = distances.kernel_corr(t1_stand, t0_stand)
        assert str(ans) == str(1.0)
        
        t3 = ts(times=[0,1,2,4,5,6],values=[3,7,9,10,16,20])
        t3_stand = distances.stand(t3,t3.mean(), t3.std())          
        assert (distances.kernel_corr(t1_stand, t3_stand) < 1)
        
    def test_distance(self):
        """tests that the distance from identical timeseries is 0"""
        t0 = ts(times=[0,1,2,4,5,6],values=[3,4,5,6,7,8])
        t0_stand = distances.stand(t0,t0.mean(),t0.std())
        t1 = ts(times=[0,1,2,4,5,6],values=[3,4,5,6,7,8])
        t1_stand = distances.stand(t1,t1.mean(), t1.std())        
        assert distances.distance(t0_stand, t1_stand) < 10**(-16)
        
        
        
if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover