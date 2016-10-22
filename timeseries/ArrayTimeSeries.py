from Timeseries import TimeSeries
import numpy as np

class ArrayTimeSeries(TimeSeries):
    """
    It is a new class ArrayTimeSeries which inherits from TimeSeries
    class and uses numpy.array to store the data internally.

    Parameters
    ----------
    values : a sequence
    data used to populate time series instance.
    times  : a sequence (optional)
    time associated with each observation in `values`.

    >>> threes=range(0,1000,3)
    >>> ap=ArrayTimeSeries(threes)
    >>> ap[0]=999
    >>> ap[0]
    array([  0, 999])
    >>> ap
    ArrayTimeSeries(Length: 334, Contents:[([  0 999]), ... ,([333 999])])
    >>> print(ap)
    Length: 334 [([  0 999]), ... ,([333 999])]

    Now test non-uniform time series
    >>> a = ArrayTimeSeries(values=[0,5,10,8,7], times=[1,2.5,3,3.5,4])
    >>> a
    ArrayTimeSeries(Length: 5, Contents:[[ 1.  0.],[ 2.5  5. ],[  3.  10.],[ 3.5  8. ],[ 4.  7.]])
    >>> print(a)
    Length: 5 [[ 1.  0.],[ 2.5  5. ],[  3.  10.],[ 3.5  8. ],[ 4.  7.]]

    """
    def __init__(self,values,times=None):
        TimeSeries.__init__(self,values,times)
        self._values=np.column_stack((self._times, values))

    def __getitem__(self,time):
        try:
            return self._values[self._times.index(time),]
        except IndexError:
            raise("Index out of bounds")

    def __setitem__(self,time,value):
        try:
            self._values[self._times.index(time),1] = value
        except IndexError:
            raise("Index out of bounds")

    def __len__(self):
        return len(self._values)

    def __itertimes__(self):
        super().__itertimes__()

    def __iteritems__(self):
        for i,j in self._values:
            yield i,j
