import lazy
import numpy as np
import numbers

class TimeSeries:
    
    """
    Purpose of the class.
    Things the user should keep in mind when using an instance
        of this object.
    """
    
    def __init__(self, values, times=None):
        """
        Parameters
        ----------
        values : a sequence 
           data used to populate time series instance.
        times  : a sequence (optional)
           time associated with each observation in `values`.
        
        Notes
        -----
        PRE: 
           - 
           -
        POST: 
           - 
           -
        INVARIANTS: 
           -
           -
        WARNINGS:
           -
           -
        """

        if times == None:
            self._times = range(0,len(values))
        else:
            self._times = [x for x in times]
            
        self._values = [x for x in values]
        
        
    def __len__(self):
        return len(self._values)
    
    
    def __getitem__(self, time):
        """
        Reports the data value located at `self[time]`, where
            `self` is a TimeSeries instance.
        Note: `time` is a list index, not an actual observed time
            in the series.
        """        
        try:
            return self._values[self._times.index(time)]
        except IndexError:
            raise("Index out of bounds.")
        
    
    def __setitem__(self, time, value):
        """
        Note: `time` is a list index, not an actual observed time
            in the series.
        """         
        try:
            self._values[self._times.index(time)] = value
        except IndexError:
            raise("Index out of bounds.")
        
    def __repr__(self):
        """
        Prints a string representation of a TimeSeries instance.
        - For a TimeSeries instance with > 10 elements:
             returns a string with name of the class, length of the instance, 
             and list containing the first element and the last element 
             separated by an ellipsis. 
        - For a TimeSeries instance with <= 10 elements: 
             returns a string with name of the class, length of the instance, 
             and the full list representation of the data.        
        """           
        class_name = type(self).__name__
        print(type(self))
        if len(self._values) > 10:
            if np.ndim(self._values)==1:
                return '{}(Length: {}, Contents:[({},{}), ... ,({},{})])'.format(class_name, len(self._values), self._times[0], self._values[0], self._times[-1],self._values[-1]) 
            else:
                return '{}(Length: {}, Contents:[({}), ... ,({})])'.format(class_name, len(self._values), self._values[0], self._values[-1])                 
        else:
            if np.ndim(self._values)==1:               
                return '{}(Length: {}, Contents:[{}])'.format(class_name, len(self._values), ','.join([str(z) for z in zip(self._times, self._values)]))      
            else:
                return '{}(Length: {}, Contents:[{}])'.format(class_name, len(self._values), ','.join([str(z) for z in self._values]))                      
        
    def __str__(self):
        """
        Prints a string representation of a TimeSeries instance.
        - For a TimeSeries instance with > 10 elements:
             prints a string with a list containing the first element 
             and the last element separated by an ellipsis. 
        - For a TimeSeries instance with <= 10 elements: 
             prints the full list representation of the data.        
        """           
        class_name = type(self).__name__
        if len(self._values) > 10:
            if np.ndim(self._values)==1:
                return 'Length: {} [({},{}), ... ,({},{})]'.format(len(self._values), self._times[0], self._values[0], self._times[-1],self._values[-1]) 
            else:
                return 'Length: {} [({}), ... ,({})]'.format(len(self._values), self._values[0],self._values[-1]) 
        else:
            if np.ndim(self._values)==1:
                return 'Length: {} [{}]'.format(len(self._values), ','.join([str(z) for z in zip(self._times, self._values)]))      
            else:
                return 'Length: {} [{}]'.format(len(self._values), ','.join([str(z) for z in  self._values]))                      
        
    def __iter__(self):           
        for i in self._values:
            yield i
            
    def __itertimes__(self):        
        for i in self._times:
            yield i    
            
    def __iteritems__(self):          
        for i,j in zip(self._times,self._values):
            yield i,j
    
    @lazy.lazy
    def identity(self): 
        return self
    
    @property
    def lazy(self):
        return self.identity()
    
    def __pos__(self):
        # Returns: TimeSeries instance with no change to the values or times
        return self
        
    def __neg__(self):
        # Returns: TimeSeries instance with negated values and no change to the times
        cls = type(self)
        return cls((-v for v in self._values), self._times)
        
    def __abs__(self):
        # Returns: new TimeSeries instance with absolute value of the values
        #     and no change to the times
        cls = type(self)
        return cls((abs(v) for v in self._values), self._times)
    
    def __bool__(self):
        # Returns: bool `False` iff all `_values` are zero
        return bool(any(self._values))
        
    def __add__(self, rhs):
        # If rhs is Real, add it to all elements of `_values`.
        # If rhs is a TimeSeries instance with the same times, add it element-by-element.
        # Returns: a new TimeSeries instance with the same times but updated `_values`.
        cls = type(self)
        try:
            if isinstance(rhs, numbers.Real):
                return cls((a + rhs for a in self._values),self._times) 
            elif isinstance(rhs,cls):
                if (len(self)==len(rhs)) and self._eqtimes(rhs): 
                    return cls((a + b for a, b in zip(self._values,rhs._values)),self._times)
                else:
                    raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points.')
            else:
                return NotImplemented
        except TypeError:
            return NotImplemented
            
    def __sub__(self, rhs):
        # If rhs is Real, subtract it from all elements of `_values`.
        # If rhs is a TimeSeries instance with the same times, subtract it element-by-element.
        # Returns: a new TimeSeries instance with the same times but updated `_values`.
        try:
            return self + (-rhs)
        except TypeError:
            return NotImplemented
    
    def __mul__(self, rhs):
        # If rhs is Real, multiply it by all elements of `_values`.
        # If rhs is a TimeSeries instance with the same times, multiply it element-by-element.
        # Returns: a new TimeSeries instance with the same times but updated `_values`.
        cls = type(self)
        try:
            if isinstance(rhs, numbers.Real):
                return cls((a*rhs for a in self._values),self._times) 
            elif isinstance(rhs,cls):
                if (len(self)==len(rhs)) and self._eqtimes(rhs): 
                    return cls((a*b for a, b in zip(self._values,rhs._values)),self._times)
                else:
                    raise ValueError(str(self)+' and '+str(rhs)+' must have the same time points')
            else:
                return NotImplemented
        except TypeError:
            return NotImplemented
    
    def _eqtimes(self,rhs):
        # test equality of the time components of two TimeSeries instances
        return len(self._times)==len(rhs._times) and all(a==b for a,b in zip(self._times,rhs._times))

    def _eqvalues(self,rhs):
        # Test equality of the values components of two TimeSeries instances
        return len(self._values)==len(rhs._values) and all(a==b for a,b in zip(self._values,rhs._values))
        
    def __eq__(self,rhs):
        # True if the times and values are the same; otherwise, False
        cls = type(self)
        if isinstance(rhs, cls):
            return self._eqtimes(rhs) and self._eqvalues(rhs)
        #elif isinstance(rhs, numbers.Real):
        #    return all(v==rhs for v in self._values)
        else:
            return False
            