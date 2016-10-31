import abc
import itertools
import numbers

class StreamTimeSeriesInterface(abc.ABC):
    """
    Abstract Base Class for timeseries data
    that arriving streaming.
    """
    
    @abc.abstractmethod
    def produce(self,chunk=1)->list:
        """
        Output a list of (time,value) tuples of length chunk
        """
        

        
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
        firstdata = next(gen)
        print(type(firstdata))
        self.firstdata = firstdata
        try:
            if isinstance(firstdata,numbers.Real):
                time = itertools.count()
                self._items = zip(time,gen)
            elif len(firstdata)==2:
                self._items = gen
            else: 
                raise InputError('Cannot accept input of type({}) that is not length 2'.format(type(firstdata)))
        except:
            raise InputError('Invalid input into StreamTimeSeries')
        
        
    def produce(self,chunk=1):
        """Return (time,value) tuples in a list of length chunk"""
        return [next(self._items) for d in range(chunk)]
        


class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message