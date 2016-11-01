import numpy as np
import numbers
from timeSeriesABC import SizedContainerTimeSeriesInterface

class ArrayTimeSeries(SizedContainerTimeSeriesInterface):
    """
    Class which stores a ordered set of numerical data using numpy arrays.
    Inherits from SizedContainerTimeSeriesInterface.

    Attributes:
    ----------
    _times: sequence that represents time data
    _values: sequence that represents value data

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
        """Method for indexing into ArrayTimeSeries. 
        Returns: The value of self._values at the given index. """
        try:
            return np.take(self._values,index) 
        except IndexError:
            raise IndexError("Index out of bounds")

    def __setitem__(self,index,value):
        """Method for assignment into ArrayTimeSeries value storage.
        Sets the given 'index' of self._values to 'value'. """        
        try:
            np.put(self._values, index, value)
        except IndexError:
            raise IndexError("Index out of bounds")

    def __len__(self):
        """Method for determing length of ArrayTimeSeries self._values"""         
        return np.size(self._values)    
    
    def values(self):
        """Returns a numpy array of ArrayTimeSeries values, i.e. self._values"""
        return self._values
    
    def times(self):
        """Returns a numpy array of ArrayTimeSeries times, i.e. self._times"""
        return self._times
    
    def _binary_search_np(self,times,t):
        """Helper function for interpolate() that finds extrapolated value
        for a given time, t, using numpy binarysearch (np.searchsorted())
        Returns: linearly extrapolated value for a given time """
        
        idx = np.searchsorted(times,t) # implements binary search
        #if the value is already in times, return its (known) value
        if np.take(times,idx) == t:
            return self._values[idx]
        #otherwise, extrapolate
        else:
            left_idx,right_idx = idx-1, idx
            m = float(self._values[right_idx]-self._values[left_idx])/(self._times[right_idx]-self._times[left_idx])
            return (t-self._times[left_idx])*m + self._values[left_idx]
        
    def interpolate(self,times_to_interpolate):
        """
        Produces new ArrayTimeSeries with linearly interpolated values using
        piecewise-linear functions with stationary boundary conditions.
        
        Parameters:
        -----------
        self: ArrayTimeSeries instance
        times_to_interpolate: sorted sequence of times to be interpolated
        
        Returns:
        --------
        ArrayTimeSeries instance with interpolated values
        
        Examples:
        --------
        >>> ats = ArrayTimeSeries(times=[0,1,2],values=[40,20,30])
        >>> ats.interpolate([0.5,1.5,3])
        ArrayTimeSeries(Length: 3, Times: array([ 0.5,  1.5,  3. ]), Values: array([ 30.,  25.,  30.]))
        """                
        tms = []
        interpolated_values = []
        for t in times_to_interpolate:
            # interpolates a given time value
            tms.append(t)
            # if the time is less than all the times we have
            if t <= self._times[0]:
                interpolated_values.append(self._values[0])
            # if the time is greater than all the times we have
            elif t >= self._times[-1]:
                interpolated_values.append(self._values[-1])
            else:
                interpolated_values.append(self._binary_search_np(self._times,t))
        
        return self.__class__(times=tms, values=interpolated_values)

    def __neg__(self):
        """Returns: ArrayTimeSeries instance with negated values 
        but no change to times"""
        cls = type(self)
        return cls(self._times,self._values*-1)

    def __abs__(self):
        """Returns: L2-norm of the ArrayTimeSeries values"""
        return np.linalg.norm(self._values)

    def __bool__(self):
        """Returns: Returns True if all values in self._values are 
        zero. False, otherwise"""
        return bool(abs(self))
    
    def __add__(self, rhs):
        """
        Description
        -------------
        If rhs is Real, add it to all elements of `_values`.
        If rhs is a SizedContainerTimeSeriesInterface instance with the same
        times, add the values element-wise.
        
        Returns:
        --------
        A new ArrayTimeSeries instance with the same times but updated values"""
        
        pcls = SizedContainerTimeSeriesInterface
        cls = type(self)
        if isinstance(rhs, numbers.Real):
            return cls(values=self._values+rhs,times=self._times)
        elif isinstance(rhs,pcls):
            if (len(self)==len(rhs)) and self._eqtimes(rhs):
                return cls(values=self._values+rhs._values,times=self._times)
            else:
                raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points.')
        elif isinstance(rhs,np.ndarray):
            raise TypeError('unsupported operand type(s) for +: \'{}\' and \'{}\''.format(type(self).__name__,type(rhs).__name__))
        else:
            return NotImplemented  
    
    def __mul__(self, rhs):
        """
        Description:
        -----------
        If rhs is Real, multiply it by all elements of `_values`.
        If rhs is a TimeSeries instance with the same times, multiply values element-wise.
        
        Returns:
        --------
        A new ArrayTimeSeries instance with the same times but updated `_values`."""
        
        pcls = SizedContainerTimeSeriesInterface
        cls = type(self)
        if isinstance(rhs, numbers.Real):
            return cls(values=rhs*self._values,times=self._times)
        elif isinstance(rhs,pcls):
            if (len(self)==len(rhs)) and self._eqtimes(rhs):
                return cls(values=self._values*rhs._values,times=self._times)
            else:
                raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
        elif isinstance(rhs,np.ndarray):
            raise TypeError('unsupported operand type(s) for +: \'{}\' and \'{}\''.format(type(self).__name__,type(rhs).__name__))
        else:
            return NotImplemented
        
    def _eqtimes(self,rhs):
        """Test equality of the times of two SizedContainerTimeSeriesInterface instances"""
        return np.array_equal(self._times, rhs._times)
    
    def _eqvalues(self,rhs):
        """Test equality of the values of two SizedContainerTimeSeriesInterface instances"""
        return np.array_equal(self._values, rhs._values)
       
    def __eq__(self,rhs):
        """Tests if two SizedContainerTimeSeriesInterface have same times and values"""
        if isinstance(rhs,SizedContainerTimeSeriesInterface):
            return self._eqtimes(rhs) and self._eqvalues(rhs)
        else:
            return False
