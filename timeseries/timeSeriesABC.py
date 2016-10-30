import abc
import lazy


class TimeSeriesInterface(abc.ABC):
    """
    TO DO
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