import unittest, os
from pytest import raises
from timeseries.StorageManager import FileStorageManager
from timeseries.ArrayTimeSeries import ArrayTimeSeries
from timeseries.timeSeriesABC import SizedContainerTimeSeriesInterface
import numpy as np

class FileStorageManagerTest(unittest.TestCase):
    """ 
    Test the FileStorageManager class.  
    It should implement everything from the FileStorageManagerInterface.
    Additionally, test its initialization functionality.    
    """

    def setUp(self):
        # make a storage manager at the default location
        self.sm = FileStorageManager()
        temp = np.arange(20).reshape(-1,2)
        
        # Put a timeseries into the storage manager.
        self.ts = ArrayTimeSeries(temp[:,0],temp[:,1])
        self.sm.store(10,self.ts)
        
        # define a directory for a second storage manager
        self.dir2 = './temp_filestorage'
        
    def tearDown(self):
        del self.sm
        del self.ts
    
    def test_index_on_disk(self):
        assert os.path.exists(self.sm._idx_file)
    
    def test_storing(self):
        # storing should work and return something that adheres to the SizedContainerTimeSeriesInterface
        assert isinstance(self.sm.store(12,self.ts),SizedContainerTimeSeriesInterface)
        
        # check that the file exist on disk
        (_,filename) = self.sm._index[12]
        assert os.path.exists(filename)
        
        # Check that there are two files in the storage manager now
        assert len(self.sm._index)==2
        
    def test_storing_noid(self):
        # storing should work when no id is given (a random one is generated).
        assert isinstance(self.sm.store(None,self.ts),SizedContainerTimeSeriesInterface)
        assert len(self.sm._index)==2
    
    def test_storing_charid(self):
        # We aren't explicitly supporting non-integer IDs, but they should work fine.
        assert isinstance(self.sm.store('string',self.ts),SizedContainerTimeSeriesInterface)
        assert len(self.sm._index)==2
        
    def test_id(self):
        # The id attribute should reflect the most recently written or accessed timeseries.
        assert self.sm.id == 10
        assert self.sm.store(12,self.ts)
        assert self.sm.id == 12
        
    def test_size(self):
        # The size method returns the length of a timeseries at a given id.
        assert self.sm.size(10)==len(self.ts)
        # it fails if the id is not present.
        with raises(KeyError):
            self.sm.size(1)
        
    def test_get(self):
        # return a timeseries for a given id.
        for i in range(5):
            self.sm.store(i,self.ts+i)
        assert self.sm.get(10)==self.ts
        assert self.sm.id==10
        assert self.sm.get(4)==self.ts+4
        assert self.sm.id==4
        
        # it fails if the id is not present.
        with raises(KeyError):
            self.sm.get(22)
            
    def test_duplicate_id(self):
        # storing the same thing twice should fail
        self.sm.store(12,self.ts)
        with raises(KeyError):
            self.sm.store(12,self.ts)

        # however, you an overwrite by explicitly saying so
        self.sm.store(12,self.ts,overwrite=True)
        
    def test_making_directory(self):
        # FileStorageManager makes a new directory if it does not exist.
        dir2 = self.dir2
        if os.path.exists(dir2):
            [ os.remove(dir2+'/'+f) for f in os.listdir(dir2) ]
            os.rmdir(dir2)
        sm2 = FileStorageManager(directory=dir2)
        
    def test_repr(self):
        assert self.sm.__repr__()=='FileStorageManager(1 ids: [10])'
        
    def test_idx_reload(self):
        # If, for some reason, the index is lost in memory, it can be reloaded from disk.
        idx1 = self.sm._index
        self.sm._index = None
        self.sm.reload_index()
        idx2 = self.sm._index
        assert idx1==idx2
        
    def test_zzz_teardowndir(self):
        """this test runs at the end and removes the directories and files made for the testing"""
        dir = self.sm._dir
        assert dir=='./FSM_filestorage'
        if os.path.exists(dir):
            [ os.remove(dir+'/'+f) for f in os.listdir(dir) ]
            os.rmdir(dir)
        dir2 = self.dir2
        if os.path.exists(dir2):
            [ os.remove(dir2+'/'+f) for f in os.listdir(dir2) ]
            os.rmdir(dir2)
            