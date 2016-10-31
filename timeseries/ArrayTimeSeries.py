from Timeseries import TimeSeries
import numpy as np
import numbers
from timeSeriesABC import SizedContainerTimeSeriesInterface 

class ArrayTimeSeries(SizedContainerTimeSeriesInterface):
    """
    Inherits from TimeSeries; uses numpy arrays to store time and values data internally.

    Parameters
    ----------
    values : a sequence- data used to populate time series instance.
    times  : a sequence- time associated with each observation in `values`.

    Notes:
    ------
    PRE: times must be a monotonically increasing sequence
    
    """
    def __init__(self,times,values):
        """
        Parameters
        ----------
        times  : a sequence 
           time associated with each observation in `values`.
        values : a sequence
           data used to populate time series instance.
        
        Examples:
        --------
        >>> ats = ArrayTimeSeries(times=[0,1,2],values=[10,20,30])
        """         
        
        # test whether values is a sequence
        try:
            self._times = np.array([_ for _ in times])
            self._values = np.array([_ for _ in values])
        except TypeError:
            raise TypeError("Non sequence passed into constructor")
            
        # make sure that times and values are the same length
        if np.size(self._times) != np.size(self._values):
            raise TypeError("Times and Values must be same length")             
         
       

    def __getitem__(self,index):
        try:
            return np.take(self._values,index) # faster than regular indexing
        except IndexError:
            raise IndexError("Index out of bounds")

    def __setitem__(self,index,value):
        try:
            np.put(self._values, index, value)
        except IndexError:
            raise IndexError("Index out of bounds")

    def __len__(self):
        return np.size(self._values)    
    
    def values(self):
        # returns a numpy array of values
        return self._values
    
    def times(self):
        # returns a numpy array of times
        return self._times
    
    def interpolate(self,times_to_interpolate):
        """
        Produces new ArrayTimeSeries with linearly interpolated values using
        piecewise-linear functions with stationary boundary conditions.
        Uses the numpy searchsorted() function.
        
        Parameters:
        -----------
        self: ArrayTimeSeries instance
        times_to_interpolate: sorted sequence of times to be interpolated
        
        Returns:
        --------
        ArrayTimeSeries instance with interpolated times
        
        Examples:
        --------
        >>> ats = ArrayTimeSeries(times=[0,1,2],values=[40,20,30])
        >>> ats.interpolate([0.5,1.5,3])
        ArrayTimeSeries(Length: 3, Times: array([ 0.5,  1.5,  3. ]), Values: array([ 30.,  25.,  30.]))
        
        """
        
        def binary_search_np(times,t):
            # uses numpy searchsorted to perform binary search
            idx = np.searchsorted(times,t)
            if np.take(times,idx) == t:
                return self._values[t]
            else:
                left_idx,right_idx = idx-1, idx
                m = float(self._values[right_idx]-self._values[left_idx])/(self._times[right_idx]-self._times[left_idx])
                return (t-self._times[left_idx])*m + self._values[left_idx]                

        tms = []
        def interp_helper(t):
            # interpolates a given time value
            tms.append(t)
            # if the time is less than all the times we have
            if t <= self._times[0]:
                return self._values[0]
            # if the time is greater than all the times we have
            elif t >= self._times[-1]:
                return self._values[-1]
            else:
                return binary_search_np(self._times,t)
        
        interpolated_values = [interp_helper(t) for t in times_to_interpolate] 
        return self.__class__(times=tms, values=interpolated_values)
    

    def __neg__(self):
        # returns: ArrayTimeSeries instance with negated values and no change to the times
        cls = type(self)
        return cls(self._times,self._values*-1)


    def __abs__(self):
        # returns: new ArrayTimeSeries instance with absolute value of the values
        # and no change to the times
        cls = type(self)
        return cls(self._times,abs(self._values))


    def __bool__(self):
        # returns: bool `False` iff all `_values` are zero
        return np.count_nonzero(self._values) > 0   
    
    
    def __add__(self, rhs):
        # if rhs is Real, add it to all elements of `_values`.
        # if rhs is a TimeSeries instance with the same times, add it element-by-element.
        # returns: a new TimeSeries instance with the same times but updated `_values`.
        cls = type(self)
        pcls = SizedContainerTimeSeriesInterface
        if isinstance(rhs, numbers.Real):
            return cls(values=self._values+rhs,times=self._times)
        elif isinstance(rhs,cls):
            if (len(self)==len(rhs)) and self._eqtimes(rhs):
                return cls(values=self._values+rhs._values,times=self._times)
            else:
                raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points.')
        else:
            return NotImplemented  
        
    
    def __mul__(self, rhs):
        # if rhs is Real, multiply it by all elements of `_values`.
        # if rhs is a TimeSeries instance with the same times, multiply it element-by-element.
        # returns: a new TimeSeries instance with the same times but updated `_values`.
        cls = type(self)
        pcls = SizedContainerTimeSeriesInterface
        if isinstance(rhs, numbers.Real):
            return cls(values=rhs*self._values,times=self._times)
        elif isinstance(rhs,cls):
            if (len(self)==len(rhs)) and self._eqtimes(rhs):
                return cls(values=self._values*rhs._values,times=self._times)
            else:
                raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
        else:
            return NotImplemented
        
    def _eqtimes(self,rhs):
        # test equality of the time components of two TimeSeries instances
        return np.array_equal(self._times, rhs._times)
    
    def _eqvalues(self,rhs):
        # test equality of the values components of two TimeSeries instances
        return np.array_equal(self._values, rhs._values)
       
    def __eq__(self,rhs):
        # True if the times and values are the same; otherwise, False
        cls = SizedContainerTimeSeriesInterface
        if isinstance(rhs, cls):
            return self._eqtimes(rhs) and self._eqvalues(rhs)
        # elif isinstance(rhs, numbers.Real):
        #    return all(v==rhs for v in self._values)
        else:
            return False
