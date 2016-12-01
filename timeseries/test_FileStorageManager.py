import unittest
from pytest import raises
from StorageManager import FileStorageManager
from ArrayTimeSeries import ArrayTimeSeries
from timeSeriesABC import SizedContainerTimeSeriesInterface
import numpy as np

class FileStorageManagerTest(unittest.TestCase):
    def setUp(self):
        self.sm = FileStorageManager()
        temp = np.arange(20).reshape(-1,2)
        self.ts = ArrayTimeSeries(temp[:,0],temp[:,1])
        self.sm.store(10,self.ts)
        
    def tearDown(self):
        del self.sm
        del self.ts
    
    def test_storing(self):
        assert isinstance(self.sm.store(12,self.ts),SizedContainerTimeSeriesInterface)
        assert len(self.sm._index)==2
        
    def test_storing_noid(self):
        assert isinstance(self.sm.store(None,self.ts),SizedContainerTimeSeriesInterface)
        assert len(self.sm._index)==2
    
    def test_storing_charid(self):
        '''We aren't explicitly supporting non-integer IDs, but they should work fine.'''
        assert isinstance(self.sm.store('string',self.ts),SizedContainerTimeSeriesInterface)
        assert len(self.sm._index)==2
        
    def test_id(self):
        assert self.sm.id == 10
        assert self.sm.store(12,self.ts)
        assert self.sm.id == 12
        
    def test_size(self):
        assert self.sm.size(10)==len(self.ts)
        with raises(KeyError):
            self.sm.size(1)
        
    def test_get(self):
        for i in range(5):
            self.sm.store(i,self.ts+i)
        assert self.sm.get(10)==self.ts
        assert self.sm.id==10
        assert self.sm.get(4)==self.ts+4
        assert self.sm.id==4
        