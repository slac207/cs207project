import abc
import lazy
import reprlib


class TimeSeriesInterface(abc.ABC):
    """
    Documentation of the interface.
    """
    
    @abc.abstractmethod
    def __iter__(self):
        """pass"""
        
    @abc.abstractmethod
    def itertimes(self):
        """pass"""
        

    @abc.abstractmethod
    def iteritems(self):
        """pass"""
        
            
    @abc.abstractmethod
    def itervalues(self):
        """pass"""
        
    
    @abc.abstractmethod
    def __repr__(self):
        """
        TO DO
        """
        
        
    @abc.abstractmethod
    def __str__(self): 
        """
        TO DO
        """
        
        
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
        self.identity() : a LazyOperation instance
        """
        return self.identity() 
        



class SizedContainerTimeSeriesInterface(TimeSeriesInterface):
    """
    Documentation of the interface.
    Need to say that times are stored in _times and values in _values
    """

    def __iter__(self):
        # iterate over values
        for i in self._values:
            yield i

            
    def itertimes(self):
        for i in self._times:
            yield i

            
    def iteritems(self):
        for i,j in zip(self._times,self._values):
            yield i,j

            
    def itervalues(self):
        for j in self._values:
            yield j
        
    def __contains__(self,item):
        return item in self._values
    
    def __repr__(self):
        r = reprlib.Repr()
        r.maxlist = 3       # max elements displayed for lists
        cls = type(self).__name__
        timesStr  = r.repr(self._times)
        valuesStr = r.repr(self._values)
        return "{}(Length: {}, Times: {}, Values: {})".format(cls, len(self._values), timesStr, valuesStr)
    
    def __str__(self):
        """
        Returns a string representation of a TimeSeries instance, of the form

        "TimeSeries with 'n' elements (Times: 't', Values: 'v')"

        where n is the length of `self`
              t displays the first three elements of _times
              v displays the first three elements of _values
        """
        r = reprlib.Repr()
        r.maxlist = 3       # max elements displayed for lists
        cls = type(self).__name__
        timesStr  = r.repr(self._times)
        valuesStr = r.repr(self._values)
        return "{} with {} elements (Times: {}, Values: {})".format(cls, len(self._values), timesStr, valuesStr) 
    

    def items(self):
        # returns a list of time, value pairs
        return list(zip(self._times,self._values))
    
    def __pos__(self):
        # returns: TimeSeries instance with no change to the values or times
        return self

    def __sub__(self, rhs):
        # if rhs is Real, subtract it from all elements of `_values`.
        # if rhs is a TimeSeries instance with the same times, subtract it element-by-element.
        # returns: a new TimeSeries instance with the same times but updated `_values`.
        return self + (-rhs) 
    
    @abc.abstractmethod
    def __getitem__(self):
        """
        TO DO
        """   
        
    @abc.abstractmethod
    def __setitem__(self):
        """
        TO DO
        """ 
        
    @abc.abstractmethod
    def __len__(self):
        """
        TO DO
        """ 
        
    @abc.abstractmethod
    def values(self):
        """
        TO DO
        """    
        
    @abc.abstractmethod
    def times(self):
        """
        TO DO
        """  
        
    @abc.abstractmethod
    def interpolate(self):
        """
        TO DO
        """ 
        
    @abc.abstractmethod
    def __neg__(self):
        """
        TO DO
        """   
        
    @abc.abstractmethod
    def __abs__(self):
        """
        TO DO
        """ 
        
    @abc.abstractmethod
    def __bool__(self):
        """
        TO DO
        """   
        
    @abc.abstractmethod
    def __add__(self):
        """
        TO DO
        """       
        
    @abc.abstractmethod
    def __mul__(self):
        """
        TO DO
        """   
        
    @abc.abstractmethod    
    def __eq__(self,rhs):
        """
        TO DO
        """   
        
class StreamTimeSeriesInterface(TimeSeriesInterface):
    """
    Abstract Base Class for timeseries data
    that arrive streaming.
    """
    
    @abc.abstractmethod
    def produce(self,chunk=1)->list:
        """
        Output a list of (time,value) tuples of length chunk
        """
    
    def __repr__(self):
        cls = type(self)
        return "Instance of a {} with streaming input".format(cls.__name__)

    def __str__(self):
        return repr(self)
        
    