import numpy as np
from timeseries.timeSeriesABC import SizedContainerTimeSeriesInterface
from timeseries.ArrayTimeSeries import ArrayTimeSeries
from timeseries.StorageManager import FileStorageManager

class SMTimeSeries(SizedContainerTimeSeriesInterface):
    """
    SMTimeSeries is an implementation of the SizedContainerTimeSeriesInterface.
    It uses a FileStorageManager to store the timeseries.  
    
    A SMTimeSeries instance can be made in one of three ways:
    1. giving times and values, optionally with an id and a storage manager:
        SMTimeSeries(times,values,id=id,SM=SM)
    2. from an existing storage manager:
        SMTimeSeries.from_db(SM,id)
    3. from a timeseries implementing the SizedContainerTimeSeriesInterface:
        SMTimeSeries.from_ts(ts,id=id,SM=SM)
    """

    def __init__(self,times=None,values=None,id=None,SM=None,get_from_SM=False,nosave=False):
        # Set the storage manager; make a new one if not given.
        if SM:
            self._sm = SM
        else:
            self._sm = FileStorageManager()
        
        # If the call came from from_db, get the ts from the storage manager.
        if get_from_SM:
            self._ts = self._sm.get(id)
            self._id = id
        elif nosave:
            # Initialize elsewhere (get self._ts and self._id), without saving into the database.
            pass
            
        
        # If not, a timeseries was given.  It needs to be stored.
        else:
            if (times is None) or (values is None):
                raise TypeError('Require Times and Values; at least one was missing')
            else:
                # Write to the Storage Manager, but it takes an input that 
                # adheres to the SizedContainerTimeSeriesInterface.
                # We make an intermediate ArrayTimeSeries object.
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
        """return a SMTimeSeries instance with timeseries from a storage manager at the given id, """
        return cls(id=id,SM=SM,get_from_SM=True)
    
    @classmethod
    def from_ts(cls,ts,SM=None,id=None):
        """return a SMTimeSeries instance from a given timeseries that implements the SizedContainerTimeSeriesInterface."""
        return cls(times=ts.times(),values=ts.values(),SM=SM,id=id)
    
    @classmethod
    def from_ops(cls,ts,SM=None):
        """return a SMTimeSeries instance from operations among SMTimeSeries instances; do not save it."""
        new_ts = cls(SM=SM,nosave=True)
        new_ts._ts = ts
        new_ts._id = None
        return new_ts

    @property
    def SM(self):
        """Return the storage manager used by the SMTimeSeries instance."""
        return self._sm
        
    @property
    def id(self):
        """Return the id of the SMTimeSeries instance within its storage manager."""
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
        return cls.from_ops(self._ts.interpolate(times_to_interpolate),SM=self.SM)
        #return cls.from_ts(self._ts.interpolate(times_to_interpolate),SM=self.SM)

    def __neg__(self):
        """Returns: TimeSeries instance with negated values 
        but no change to times"""
        cls = type(self)
        return cls.from_ops(-self._ts,SM=self.SM)
        #return cls.from_ts(-self._ts,SM=self.SM)

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
        return cls.from_ops(self._ts+rhs,SM=self.SM)
        #return cls.from_ts(self._ts+rhs,SM=self.SM)

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
        return cls.from_ops(self._ts*rhs,SM=self.SM)
        #return cls.from_ts(self._ts*rhs,SM=self.SM)
        
    def __eq__(self,rhs):
        """Tests if two SizedContainerTimeSeriesInterface have same times and values"""
        return self._ts == rhs
        
        
    def mean(self, chunk=None):
        """ Return the mean of the values."""
        return self._ts.mean(chunk=chunk)
    
    
    def std(self, chunk=None):
        """ Return the standard deviation of the values."""
        return self._ts.std(chunk=chunk)
