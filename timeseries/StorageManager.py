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
    """Implementation of the StorageManagerInterface.
    """
    
    #  ---  Design Decisions:  ----
    #Stores the timeseries objects as separate numpy files.
    #Maintains an index of the ids in memory and a copy on-disk.
    #As values, the index contains the length and filename of the timeseries.
    """$$ NEED TO SAVE THE INDEX EVERY TIME IT IS MODIFIED, OR HAVE IT LOADED FROM DISK AS AN OPEN FILE..."""
    
    def __init__(self,directory='./filestorage'):
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
        that adherest to the SizedContainerTimeSeriesInterface"""
        return ArrayTimeSeries(ts[:,0],ts[:,1])
        
    def _make_id(self):
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
        
        if id is None:
            id = self._make_id()
        
        if (id in self._index) and (overwrite == False):
            raise KeyError('There already a time series with id {}; if you want to overwrite, set overwrite=True'.format(id))
        else:
            filename = self._dir+'/ts_{}.npy'.format(id)        
            self._index[id] = (len(times),filename)
            np.save(filename,ts)
            with open(self._idx_file,'wb') as f:
                pickle.dump(self._index,f)

            
        self._id = id
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
    
class SMTimeSeries(SizedContainerTimeSeriesInterface):
    """$$own docstring here.  Include some examples."""
    # Maybe make there be one thing loaded in memory in the FSM, with ID and TS a property.
    # If I link a storage manager then change it, does it change the internal one too?

    def __init__(self,times=None,values=None,id=None,SM=None,get_from_SM=False):
        if SM:
            self._sm = SM
        else:
            self._sm = FileStorageManager()
        
        if get_from_SM:
            self._ts = self._sm.get(id)
            self._id = id
        else:
            if (times is None) or (values is None):
                raise TypeError('Require Times and Values; at least one was missing')
            else:
                # Write to the Storage Manager, but it takes an input that 
                # adheres to the SizedContainerTimeSeriesInterface.
                ts_temp = ArrayTimeSeries(times,values)
                if id:
                    self._ts = self._sm.store(id,ts_temp)
                    self._id = id
                else:
                    # Make a new ID
                    self._ts = self._sm.store(None,ts_temp)
                    self._id = self._sm.id
            
    @classmethod
    def from_db(cls,SM,id):
        return cls(id=id,SM=SM,get_from_SM=True)
    
    @classmethod
    def from_ts(cls,ts,SM=None,id=None):
        return cls(times=ts.times(),values=ts.values(),SM=SM,id=id)
    
    @property
    def SM(self):
        return self._sm
        
    @property
    def id(self):
        return self._id
    
    @property
    def _times(self):
        return self._ts._times
    
    @property
    def _values(self):
        return self._ts._values

    def __getitem__(self, index):
        """Method for indexing into TimeSeries. 
        Returns: The value of self._values at the given index. """
        return self._ts.__getitem__(index)

    def __setitem__(self, index, value):
        """Method for assignment into TimeSeries value storage.
        Sets the given 'index' of self._values to 'value'. """    
        return self._ts.__setitem__(index, value)
        
    def __len__(self):
        """Method for determing length of TimeSeries self._values"""  
        return self._ts.__len__()

    def values(self):
        """Returns a numpy array of the TimeSeries values"""
        return self._ts.values()

    def times(self):
        """Returns a numpy array of the TimeSeries times"""
        return self._ts.times()

    def interpolate(self,times_to_interpolate):
        """
        Produces new TimeSeries with linearly interpolated values using
        piecewise-linear functions with stationary boundary conditions

        Parameters:
        -----------
        self: TimeSeries instance
        times_to_interpolate: sorted sequence of times to be interpolated

        Returns:
        --------
        TimeSeries instance with interpolated times and values
        
        """
        cls = type(self)
        return cls.from_ts(self._ts.interpolate(times_to_interpolate),SM=self.SM)

    def __neg__(self):
        """Returns: TimeSeries instance with negated values 
        but no change to times"""
        cls = type(self)
        return cls.from_ts(-self._ts,SM=self.SM)

    def __abs__(self):
        """Returns: L2-norm of the TimeSeries values"""
        return abs(self._ts)


    def __bool__(self):
        """Returns: Returns True if all values in self._values are 
        zero. False, otherwise"""
        return bool(self._ts)

    def __add__(self, rhs):
        """
        Description
        -------------
        If rhs is Real, add it to all elements of `_values`.
        If rhs is a SizedContainerTimeSeriesInterface instance with the same
        times, add the values element-wise.
        
        Returns:
        --------
        A new TimeSeries instance with the same times but updated values"""
        cls = type(self)
        return cls.from_ts(self._ts+rhs,SM=self.SM)

    def __mul__(self, rhs):
        """
        Description:
        -----------
        If rhs is Real, multiply it by all elements of `_values`.
        If rhs is a TimeSeries instance with the same times, multiply values element-wise.
        
        Returns:
        --------
        A new TimeSeries instance with the same times but updated `_values`."""
        cls = type(self)
        return cls.from_ts(self._ts*rhs,SM=self.SM)
        
    def __eq__(self,rhs):
        """Tests if two SizedContainerTimeSeriesInterface have same times and values"""
        return self._ts == rhs
        
        
    def mean(self, chunk=None):
        return self._ts.mean(chunk=chunk)
    
    
    def std(self, chunk=None):
        return self._ts.std(chunk=chunk)
