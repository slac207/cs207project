import abc
import lazy
import reprlib


class TimeSeriesInterface(abc.ABC):
    """
    Interface for TimeSeries class which inherits from ABC
    """
    
    @abc.abstractmethod
    def __iter__(self):
        """Iterate over values."""
        """pass"""

            
    def itertimes(self):
        """Iterate over times."""
        """pass"""

        
    @abc.abstractmethod
    def itertimes(self):
        """pass"""
        

    @abc.abstractmethod
    def iteritems(self):
        """Iterate over (time, value) pairs."""
        """pass"""
        
            
    @abc.abstractmethod
    def itervalues(self):
        """Iterate over values."""
        """pass"""
    
    @abc.abstractmethod
    def __repr__(self):
        """
        All TimeSeries must support a repr function
        """
        
        
    @abc.abstractmethod
    def __str__(self): 
        """
        All TimeSeries must support a str function
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
    Interface for sized-container based TimeSeries.
    Inherits from TimeSeriesInterface.
    Times for TimeSeries stored in _times
    Values for TimeSeries stored in _values

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
        """Returns boolean of whether given 'item' is contained in _.values"""
        return item in self._values
    
    def __repr__(self):
        """
        Returns a string representation of a SizedContainerTimeSeriesInterface
        instance, of the form

        "Class_name(Length: 'n', Times: 't', Values: 'v')"

        where n is the length of `self`
              t displays the first three elements of _times
              v displays the first three elements of _values
        """        
        r = reprlib.Repr()
        r.maxlist = 3       # max elements displayed for lists
        cls = type(self).__name__
        timesStr  = r.repr(self._times)
        valuesStr = r.repr(self._values)
        return "{}(Length: {}, Times: {}, Values: {})".format(cls, len(self._values), timesStr, valuesStr)
    
    def __str__(self):
        """
        Returns a string representation of a SizedContainerTimeSeriesInterface
        instance, of the form

        "Class_name with 'n' elements (Times: 't', Values: 'v')"

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
        """Returns a list of (time, value) pairs"""
        return list(zip(self._times,self._values))
    
    def __pos__(self):
        """Returns: TimeSeries instance with no change to the values or times"""
        return self

    def __sub__(self, rhs):
        """
        Description
        -------------
        If rhs is Real, subtract it from all elements of `_values`.
        If rhs is a SizedContainerTimeSeriesInterface instance with the same
        times, subtract the values element-wise.
        
        Returns:
        --------
        A new instance of type(self) with the same times but updated values"""
        
        return self + (-rhs) 
    
    @abc.abstractmethod
    def __getitem__(self):
        """
        Require indexing for sized-container based TimeSeries.
        """   
        
    @abc.abstractmethod
    def __setitem__(self):
        """
        Require assignment for sized-container based TimeSeries.
        """ 
        
    @abc.abstractmethod
    def __len__(self):
        """
        Require notion of size for sized-container based TimeSeries.
        """ 
        
    @abc.abstractmethod
    def values(self):
        """
        Require ability to return stored values for sized-container based TimeSeries.
        """    
        
    @abc.abstractmethod
    def times(self):
        """
        Require ability to return stored values for sized-container based TimeSeries.
        """  
        
    @abc.abstractmethod
    def interpolate(self):
        """
        Require notion of value interpolation for times not present originally
        for sized-container based TimeSeries.
        """ 
        
    @abc.abstractmethod
    def __neg__(self):
        """
        Require ability to negate values for sized-container based TimeSeries.
        """   
        
    @abc.abstractmethod
    def __abs__(self):
        """
        Require notion of 2-norm over values for sized-container based TimeSeries.
        """ 
        
    @abc.abstractmethod
    def __bool__(self):
        """
        Require ability to test if self._values is all zeros
        """   
        
    @abc.abstractmethod
    def __add__(self):
        """
        Require ability to add together two SizedContainerTimeSeriesInterface
        instances, assuming that their times are equivalent pairwise.
        """       
        
    @abc.abstractmethod
    def __mul__(self):
        """
        Require ability to multiply two SizedContainerTimeSeriesInterface
        instances, assuming that their times are equivalent pairwise.
        """   
        
    @abc.abstractmethod    
    def __eq__(self,rhs):
        """
        Require notion of equality between two SizedContainerTimeSeriesInterface
        instances.
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
        
    