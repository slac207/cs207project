import abc, os, pickle, reprlib
import numpy as np
from timeSeriesABC import SizedContainerTimeSeriesInterface
from ArrayTimeSeries import ArrayTimeSeries

class StorageManagerInterface():
    """An interface for storing timeseries objects on disk
    and retrieving them from disk.
    """

    @abc.abstractmethod
    def store(id:int, t:SizedContainerTimeSeriesInterface)->SizedContainerTimeSeriesInterface:
        """Store a given timeseries, with unique id provided. 
        The timeseries uses the SizedContainerTimeSeriesInterface.
        Return the given timeseries as an object
        that adheres to the SizedContainerTimeSeriesInterface."""
    
    @abc.abstractmethod
    def size(id:int)->int:
        """Retrieve the size of a stored timeseries
        at the provided unique id.
        """
    
    @abc.abstractmethod
    def get(id:int)->SizedContainerTimeSeriesInterface:
        """Retrieve a stored timeseries at the provided unique id.
        Return a representation of the timeseries as an object
        that adheres to the SizedContainerTimeSeriesInterface.
        """
    

class FileStorageManager(StorageManagerInterface):
    """Implementation of the StorageManagerInterface that stores
    the timeseries on disk as numpy's .npy format.
    """
    
    #  ---  Design Decisions:  ----
    #Stores the timeseries objects as separate numpy files.
    #Maintains an index of the ids in memory and a copy on-disk.
    #As values, the index contains the length and filename of the timeseries.
    
    def __init__(self,directory='./FSM_filestorage'):
        # define an index, directory, and save the index.
        self._index = dict()
        if not os.path.exists(directory):
            os.makedirs(directory)
        self._dir = directory
        self._id = None
        self._idx_file = self._dir+'/index.p'
        with open(self._idx_file,'wb') as f:
            pickle.dump(self._index,f)
        
    @staticmethod
    def _make_ts(ts):
        """Transform an n x 2 numpy array into a timeseries object
        that adheres to the SizedContainerTimeSeriesInterface"""
        return ArrayTimeSeries(ts[:,0],ts[:,1])
        
    def _make_id(self):
        """if no ID is given, assign a uniqe one randomly."""
        
        # choose from the integers 100x bigger than the current size.
        # repeat until an unused one is found (shouldn't take long!)
        n = len(self._index)
        N = 100*len(self._index)
        if N==0:
            id_prop = 1
            return id_prop
        # Get the first value
        id_prop = next(iter(self._index))
        while id_prop in self._index:
            id_prop = np.random.randint(0,N)
        return id_prop
            
    
    def store(self, id:int, t:SizedContainerTimeSeriesInterface, overwrite=False)->SizedContainerTimeSeriesInterface:
        """Store a given timeseries, with unique id provided. 
        The timeseries uses the SizedContainerTimeSeriesInterface.
        Return the given timeseries as an object
        that adheres to the SizedContainerTimeSeriesInterface."""
        times = np.asarray(t.times(),dtype='float64').reshape(-1,1)
        values = np.asarray(t.values(),dtype='float64').reshape(-1,1)
        ts = np.concatenate((times,values),axis=1)
        
        # if no id is given, generate a unique one
        if id is None:
            id = self._make_id()
        
        # if id is already taken and we are not overwriting, throw an error
        # otherwise, store the timeseries, update the index, and store the index.
        if (id in self._index) and (overwrite == False):
            raise KeyError('There already a time series with id {}; if you want to overwrite, set overwrite=True'.format(id))
        else:
            filename = self._dir+'/ts_{}.npy'.format(id)        
            self._index[id] = (len(times),filename)
            np.save(filename,ts)
            with open(self._idx_file,'wb') as f:
                pickle.dump(self._index,f)

        # update the id property
        self._id = id
        
        # return a timeseries object.
        return self._make_ts(ts)
        
    def size(self, id:int)->int:
        """Retrieve the size of a stored timeseries
        at the provided unique id.
        """
        if id in self._index:
            size,filename = self._index[id]
            self._id = id
            return size
        else:
            raise KeyError('There is no time series with id {}'.format(id))

    def get(self, id:int  )->SizedContainerTimeSeriesInterface:
        """Retrieve a stored timeseries at the provided unique id.
        Return a representation of the timeseries as an object
        that adheres to the SizedContainerTimeSeriesInterface.
        """  
        # return the timeseries and update the id property
        if id in self._index:
            size,filename = self._index[id]
            ts = np.load(filename)
            self._id = id
            return self._make_ts(ts)
        else:
            raise KeyError('There is no time series with id {}'.format(id))

    @property
    def id(self):
        """ID of the most recently stored or accessed record"""
        return self._id
    
    def reload_index(self):
        # if the index is somehow lost in memory, reload it from disk
        with open(self._idx_file,'rb') as f:
            self._index = pickle.load(f)
            
    def __repr__(self):
        # Use reprlib for repr formatting
        r = reprlib.Repr()
        r.maxlist = 5
        cls = type(self).__name__
        tmp = list(self._index.keys())
        tmp.sort()
        key_str = r.repr(tmp)
        return '{}({} ids: {})'.format(cls,len(self._index),key_str)
    
