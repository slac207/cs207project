import lazy
import numpy as np
import numbers
import reprlib
from binarysearch import binary_search
from timeSeriesABC import SizedContainerTimeSeriesInterface
import math
import statistics as stat

class TimeSeries(SizedContainerTimeSeriesInterface):
    """
    Class which stores a ordered set of numerical data using lists.
    Inherits from SizedContainerTimeSeriesInterface.
    
    Attributes:
    ----------
    _times: sequence that represents time data
    _values: sequence that represents value data

    Notes:
    ------
    PRE: times must be a monotonically increasing sequence
    """

    def __init__(self, values, times=None):
        """
        Parameters
        ----------
        values : a sequence 
           data used to populate time series instance.
        times  : a sequence (optional)
           time associated with each observation in `values`.
        
        Examples:
        --------
        >>> ts = TimeSeries(values=[10,20,30])
        """    
        # test whether values is a sequence
        try:
            iter(values)
        except TypeError:
            raise TypeError("Non sequence passed into constructor")
        self._values = [x for x in values]


        if times == None: #if not provided times, need to produce them
            self._times = range(0,len(values))
        else:
            #test if times is a sequence
            try:
                iter(times)
                self._times = [x for x in times]
                if len(self._times) != len(self._values):
                    raise TypeError("Times and Values must be same length")
            except TypeError:
                raise TypeError("Non sequence passed into constructor")
            
    def __getitem__(self, index):
        """Method for indexing into TimeSeries. 
        Returns: The value of self._values at the given index. """
        try:
            return self._values[index]
        except IndexError:
            raise IndexError("Index out of bounds")

    def __setitem__(self, index, value):
        """Method for assignment into TimeSeries value storage.
        Sets the given 'index' of self._values to 'value'. """    
        try:
            self._values[index] = value
        except IndexError:
            raise IndexError("Index out of bounds")
        
    def __len__(self):
        """Method for determing length of TimeSeries self._values"""  
        return len(self._values)    

    def values(self):
        """Returns a numpy array of the TimeSeries values"""
        return np.array(self._values)

    def times(self):
        """Returns a numpy array of the TimeSeries times"""
        return np.array(self._times)

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
        TimeSeries instance with interpolated times
        
        Examples:
        --------
        >>> ts = TimeSeries(times=[0,1,2],values=[40,20,30])
        >>> ts.interpolate([0.5,1.5,3])
        TimeSeries(Length: 3, Times: [0.5, 1.5, 3], Values: [30.0, 25.0, 30])
        """

        tms = []
        interpolated_values = []
        for t in times_to_interpolate:
            tms.append(t)
            #if the time is less than all the times we have
            if t <= self._times[0]:
                interpolated_values.append(self._values[0])
            #if the time is greater than all the times we have
            elif t >= self._times[-1]:
                interpolated_values.append(self._values[-1])
            else:
                left_idx,right_idx = binary_search(self._times,t)
                m = float(self._values[right_idx]-self._values[left_idx])/(self._times[right_idx]-self._times[left_idx])
                interpolated_values.append((t-self._times[left_idx])*m + self._values[left_idx])

        return self.__class__(times=tms, values=interpolated_values)

    def __neg__(self):
        """Returns: TimeSeries instance with negated values 
        but no change to times"""
        cls = type(self)
        return cls((-v for v in self._values), self._times)

    def __abs__(self):
        """Returns: L2-norm of the TimeSeries values"""
        return math.sqrt(sum([v*v for v in self._values]))


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
        A new TimeSeries instance with the same times but updated values"""
        
        pcls = SizedContainerTimeSeriesInterface
        cls = type(self)
        if isinstance(rhs, numbers.Real):
            return cls((a + rhs for a in self._values),self._times)
        elif isinstance(rhs,pcls):
            if (len(self)==len(rhs)) and self._eqtimes(rhs):
                return cls((a + b for a, b in zip(self._values,rhs._values)),self._times)
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
        A new TimeSeries instance with the same times but updated `_values`."""
        
        pcls = SizedContainerTimeSeriesInterface
        cls = type(self)
        if isinstance(rhs, numbers.Real):
            return cls((a*rhs for a in self._values),self._times)
        elif isinstance(rhs,pcls):
            if (len(self)==len(rhs)) and self._eqtimes(rhs):
                return cls((a*b for a, b in zip(self._values,rhs._values)),self._times)
            else:
                raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
        elif isinstance(rhs,np.ndarray):
            raise TypeError('unsupported operand type(s) for +: \'{}\' and \'{}\''.format(type(self).__name__,type(rhs).__name__))
        else:
            return NotImplemented
        
    def _eqtimes(self,rhs):
        """Test equality of the times of two SizedContainerTimeSeriesInterface instances"""
        return len(self._times)==len(rhs._times) and all(a==b for a,b in zip(self._times,rhs._times))

    def _eqvalues(self,rhs):
        """Test equality of the values of two SizedContainerTimeSeriesInterface instances"""
        return len(self._values)==len(rhs._values) and all(a==b for a,b in zip(self._values,rhs._values))

    def __eq__(self,rhs):
        """Tests if two SizedContainerTimeSeriesInterface have same times and values"""
        cls = SizedContainerTimeSeriesInterface
        if isinstance(rhs, cls):
            return self._eqtimes(rhs) and self._eqvalues(rhs)
        else:
            return False
        
        
    def mean(self, chunk=None):
        return(stat.mean(self._values))
    
    
    def std(self, chunk=None):
        return(stat.stdev(self._values))