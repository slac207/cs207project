import abc
import itertools
import numbers
from timeSeriesABC import StreamTimeSeriesInterface
from ArrayTimeSeries import ArrayTimeSeries      

        
class SimulatedTimeSeries(StreamTimeSeriesInterface):
    """
    Class for timeseries objects that have streaming
    input data arriving via an iterator.
    """
    
    def __init__(self,gen):
        """
        Input is an iterator.  
        It may be floats corresponding to values of a timeseries
        or it may tuples of floats corresponding to (time, value) pairs.
        """

        # Use the first datapoint to decide whether times are included.
        # If firstdata is real, we are only receiving values and need 
        # to attach our own times.  
        try:
            firstdata = next(gen)
            self._firstdata = firstdata
            if isinstance(firstdata,numbers.Real):
                time = itertools.count(1)
                self._items = zip(time,gen)
            elif len(firstdata)==2:
                self._items = gen
            else: 
                raise InputError('Cannot accept input of type({}) that is not length 2'.format(type(firstdata).__name__))
        except:
            raise InputError('Invalid input into StreamTimeSeries')
        
    
    def __iter__(self):
        """Generator function returning the values only"""
        for _,v in self._items:
            yield v
        
    def itertimes(self):
        """Generator function returning the times only"""
        for t,_ in self._items:
            yield t

    def iteritems(self):
        """Generator function returning (time,value) tuples"""
        for item in self._items:
            yield item
            
    def itervalues(self): 
        """Generator function returning the values only"""
        for _,v in self._items:
            yield v
    
    def produce(self,chunk=1):
        """Return (time,value) as an ArrayTimeSeries object
        with number of items equal to 'chunk'"""
        values = []
        times = []
        for _ in range(chunk):
            try:
                t,v = next(self._items)
                times.append(t)
                values.append(v)
            except StopIteration:
                break
        return ArrayTimeSeries(times,values)
        


class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message