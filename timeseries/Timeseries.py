import lazy
import numpy as np
import numbers
import reprlib

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
        
        >>> t = TimeSeries([1,2,3])
        >>> t = TimeSeries([1,2,3],[0,2,4])

        """
        if times == None:
            self._times = range(0,len(values))
        else:
            self._times = [x for x in times]
            
        self._values = [x for x in values]
        
        
    def __len__(self):     
        return len(self._values)
    
    
    def __getitem__(self, index):
        # returns tuple (time, value) corresponding to the data located at 
        #     `_times[index]` and `_values[index]`.
        try:
            return (self._times[index], self._values[index])
        except IndexError:
            raise("Index out of bounds.")
        
    
    def __setitem__(self, index, value):
        # sets `_values[index]` to `value`
        try:
            self._values[index] = value
        except IndexError:
            raise("Index out of bounds.")
        

    def __repr__(self):   
        r = reprlib.Repr()
        r.maxlist = 3       # max elements displayed for lists
        cls = type(self).__name__
        timesStr  = r.repr(self._times)
        valuesStr = r.repr(self._values)
        return "{}(Length: {}, Times: {}, Values: {})".format(cls, len(self._values), timesStr, valuesStr) 
        
        
    def __str__(self):          
        r = reprlib.Repr()
        r.maxlist = 3       # max elements displayed for lists
        cls = type(self).__name__
        timesStr  = r.repr(self._times)
        valuesStr = r.repr(self._values)
        return "{} with {} elements (Times: {}, Values: {})".format(cls, len(self._values), timesStr, valuesStr)                     
        
    def __iter__(self):           
        for i in self._values:
            yield i
            
            
    def __itertimes__(self):        
        for i in self._times:
            yield i             
  
            
    def __itertimes__(self):          
        for i,j in zip(self._times,self._values):
            yield i,j
    
    
    @lazy.lazy
    def identity(self): 
        # lazy implementation of the identity function
        return self
    
    
    @property
    def lazy(self):
        """
        Lazy identity property.  
        self.lazy returns a LazyOperation instance of self.identity(), so that  
        self.lazy.eval() is self.  
        
        Returns
        -------
        self.identity()  : a LazyOperation instance
        """   
        return self.identity()
    
    
    def __pos__(self):
        # returns: TimeSeries instance with no change to the values or times
        return self
        
        
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
        # if rhs is Real, subtract it from all elements of `_values`.
        # if rhs is a TimeSeries instance with the same times, subtract it element-by-element.
        # returns: a new TimeSeries instance with the same times but updated `_values`.
        try:
            return self + (-rhs)
        except TypeError:
            return NotImplemented
    
    
    def __mul__(self, rhs):
        # if rhs is Real, multiply it by all elements of `_values`.
        # if rhs is a TimeSeries instance with the same times, multiply it element-by-element.
        # returns: a new TimeSeries instance with the same times but updated `_values`.
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
        # test equality of the values components of two TimeSeries instances
        return len(self._values)==len(rhs._values) and all(a==b for a,b in zip(self._values,rhs._values))
        
        
    def __eq__(self,rhs):
        # True if the times and values are the same; otherwise, False
        cls = type(self)
        if isinstance(rhs, cls):
            return self._eqtimes(rhs) and self._eqvalues(rhs)
        # elif isinstance(rhs, numbers.Real):
        #    return all(v==rhs for v in self._values)
        else:
            return False