import lazy
import numpy as np
import numbers
import reprlib
from binarysearch import binary_search
from timeSeriesABC import SizedContainerTimeSeriesInterface


class TimeSeries(SizedContainerTimeSeriesInterface):
    """
    Purpose of the class.
    Things the user should keep in mind when using an instance
        of this object.

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

        """
        # test whether values is a sequence
        try:
            iter(values)
        except TypeError:
            raise TypeError("Non sequence passed into constructor")
        self._values = [x for x in values]


        if times == None:
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


    def __len__(self):
        return len(self._values)


    def __getitem__(self, index):
        # returns value corresponding to the data located at
        #  `_values[index]`.
        try:
            return self._values[index]
        except IndexError:
            raise IndexError("Index out of bounds")


    def __setitem__(self, index, value):
        # sets `_values[index]` to `value`
        try:
            self._values[index] = value
        except IndexError:
            raise IndexError("Index out of bounds")

    





    def values(self):
        #  a numpy array of values
        return np.array(self._values)

    def times(self):
        # returns a numpy array of times
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

        """

        tms = []
        def interp_helper(t):
            tms.append(t)
            #if the time is less than all the times we have
            if t <= self._times[0]:
                return self._values[0]
            #if the time is greater than all the times we have
            elif t >= self._times[-1]:
                return self._values[-1]
            else:
                left_idx,right_idx = binary_search(self._times,t)
                m = float(self._values[right_idx]-self._values[left_idx])/(self._times[right_idx]-self._times[left_idx])
                return (t-self._times[left_idx])*m + self._values[left_idx]

        interpolated_values = [interp_helper(t) for t in times_to_interpolate]
        return self.__class__(times=tms, values=interpolated_values)


    def __eq__(self,rhs):
        # True if the times and values are the same; otherwise, False
        if isinstance(rhs, type(self)) or isinstance(self, type(rhs)):
            return self._eqtimes(rhs) and self._eqvalues(rhs)
        # elif isinstance(rhs, numbers.Real):
        #    return all(v==rhs for v in self._values)
        else:
            return False



    def __neg__(self):
        # returns: TimeSeries instance with negated values and no change to the times
        cls = type(self)
        return cls((-v for v in self._values), self._times)


    def __abs__(self):
        # returns: new TimeSeries instance with absolute value of the values
        #     and no change to the times
        cls = type(self)
        return cls((abs(v) for v in self._values), self._times)


    def __bool__(self):
        # returns: bool `False` iff all `_values` are zero
        return bool(any(self._values))


    def __add__(self, rhs):
        # if rhs is Real, add it to all elements of `_values`.
        # if rhs is a TimeSeries instance with the same times, add it element-by-element.
        # returns: a new TimeSeries instance with the same times but updated `_values`.
        cls = type(self)
        pcls = SizedContainerTimeSeriesInterface
        if isinstance(rhs, numbers.Real):
            return cls((a + rhs for a in self._values),self._times)
        elif isinstance(rhs,pcls):
            if (len(self)==len(rhs)) and self._eqtimes(rhs):
                return cls((a + b for a, b in zip(self._values,rhs._values)),self._times)
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
            return cls((a*rhs for a in self._values),self._times)
        elif isinstance(rhs,pcls):
            if (len(self)==len(rhs)) and self._eqtimes(rhs):
                return cls((a*b for a, b in zip(self._values,rhs._values)),self._times)
            else:
                raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
        else:
            return NotImplemented
        
        
    def _eqtimes(self,rhs):
        # test equality of the time components of two TimeSeries instances
        return len(self._times)==len(rhs._times) and all(a==b for a,b in zip(self._times,rhs._times))


    def _eqvalues(self,rhs):
        # test equality of the values components of two TimeSeries instances
        return len(self._values)==len(rhs._values) and all(a==b for a,b in zip(self._values,rhs._values))


    def __eq__(self,rhs):
        # True if the times and values are the same; otherwise, False
        cls = SizedContainerTimeSeriesInterface
        if isinstance(rhs, cls):
            return self._eqtimes(rhs) and self._eqvalues(rhs)
        # elif isinstance(rhs, numbers.Real):
        #    return all(v==rhs for v in self._values)
        else:
            return False