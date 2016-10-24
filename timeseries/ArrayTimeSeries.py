from Timeseries import TimeSeries
import numpy as np

class ArrayTimeSeries(TimeSeries):
    """
    It is a new class ArrayTimeSeries which inherits from TimeSeries
    class and uses numpy arrays to store the data internally.

    Parameters
    ----------
    values : a sequence- data used to populate time series instance.
    times  : a sequence- time associated with each observation in `values`.

    >>> threes=range(0,1000,3)
    >>> times = range(0,1000,1)
    >>> ap=ArrayTimeSeries(times,threes)
    >>> ap[0] = 999
    >>> ap[0]
    999
    >>> ap
    ArrayTimeSeries(Length: 334, Times: array([  0,  ...97, 998, 999]), Values: array([999,  ...93, 996, 999]))
    >>> print(ap)
    ArrayTimeSeries with 334 elements (Times: array([  0,  ...97, 998, 999]), Values: array([999,  ...93, 996, 999]))
    >>> len(ap)
    334
    >>> ap = ap=ArrayTimeSeries([0,1,2,3],[5,6,7,8])
    >>> list(iter(ap))
    [5, 6, 7, 8]
    >>> list(ap.itertimes())
    [0, 1, 2, 3]
    >>> list(ap.iteritems())
    [(0, 5), (1, 6), (2, 7), (3, 8)]
    
    #Now test non-uniform time series
    >>> a = ArrayTimeSeries(times=[1,2.5,3,3.5,4],values=[0,5,10,8,7], )
    >>> a
    ArrayTimeSeries(Length: 5, Times: array([ 1. , ...,  3.5,  4. ]), Values: array([ 0,  5, 10,  8,  7]))
    >>> print(a)
    ArrayTimeSeries with 5 elements (Times: array([ 1. , ...,  3.5,  4. ]), Values: array([ 0,  5, 10,  8,  7]))

    """
    def __init__(self,times,values):
        TimeSeries.__init__(self,values,times)
        self._times = np.array(times)
        self._values = np.array(values)

    def __getitem__(self,index):
        try:
            return self._values[index]
        except IndexError:
            raise IndexError("Index out of bounds")

    def __setitem__(self,index,value):
        try:
            self._values[index] = value
        except IndexError:
            raise IndexError("Index out of bounds")

    def __len__(self):
        return super().__len__()

    def __iter__(self):
        return super().__iter__()
        
    def itertimes(self):
        return super().itertimes()

    def iteritems(self):
        return super().iteritems()
    
    


