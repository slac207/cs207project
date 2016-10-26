from Timeseries import TimeSeries
import numpy as np

class ArrayTimeSeries(TimeSeries):
    """
    Inherits from TimeSeries; uses numpy arrays to store time and values data internally.

    Parameters
    ----------
    values : a sequence- data used to populate time series instance.
    times  : a sequence- time associated with each observation in `values`.

   

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


