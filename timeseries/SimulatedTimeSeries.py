import abc
import itertools
import numbers
from timeSeriesABC import StreamTimeSeriesInterface
from ArrayTimeSeries import ArrayTimeSeries
import math


class SimulatedTimeSeries(StreamTimeSeriesInterface):
    """
    Class for timeseries objects that have streaming
    input data arriving via an iterator.
    """

    def __init__(self, gen):
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
            if isinstance(firstdata, numbers.Real):
                time = itertools.count(1)
                self._items = zip(time, gen)
                self._firstitem = (0, self._firstdata)
            elif len(firstdata) == 2:
                self._items = gen
                self._firstitem = self._firstdata
            else:
                raise InputError(
                    'Cannot accept input of type({}) that is not length 2'.format(type(firstdata).__name__))
        except:
            raise InputError('Invalid input into StreamTimeSeries')

        # Initialize the mean and standard deviation trackers
        self._running_mean = (self._firstitem[1], 1)  # tuple of current mean, number of observations included.
        self._running_std = (self._firstitem[1], 1,
                             0)  # tuple of current mean, number of observations included, sum of squared errors around the mean

    def __iter__(self):
        """Generator function returning the values only"""
        return self.itervalues()

    def itertimes(self):
        """Generator function returning the times only"""
        for t, _ in self._items:
            yield t

    def iteritems(self):
        """Generator function returning (time,value) tuples"""
        for item in self._items:
            yield item

    def itervalues(self):
        """Generator function returning the values only"""
        for _, v in self._items:
            yield v

    def produce(self, chunk=1):
        """Return (time,value) as an ArrayTimeSeries object
        with number of items equal to 'chunk'"""
        values = []
        times = []
        for _ in range(chunk):
            try:
                t, v = next(self._items)
                times.append(t)
                values.append(v)
            except StopIteration:
                break
        return ArrayTimeSeries(times, values)

    def _online_mean_genfun(self):
        # Helper function to online_mean.
        # This is a generator function used as the input to 
        # construct the online_mean SimulatedTimeSeries object.  
        # It returns (time,value) tuples
        # where the value is the mean of the present time series object.
        yield self._firstitem
        for item in self._items:
            t, v = item
            mu, n = self._running_mean
            n += 1
            delta = v - mu
            mu = mu + delta / n
            self._running_mean = (mu, n)
            yield (t, mu)

    def online_mean(self):
        """Return a SimulatedTimeSeries of the running mean.
        Note that this is computed only over the samples that 
        are called from this method.
        """
        return SimulatedTimeSeries(self._online_mean_genfun())

    def _online_std_genfun(self):
        # Helper function to online_std.
        # This is a generator function used as the input to 
        # construct the online_std SimulatedTimeSeries object.  
        # It returns (time,value) tuples
        # where the value is the std of the present time series object.
        yield self._firstitem[0], 0
        for item in self._items:
            t, v = item
            mu, n, S = self._running_std
            n += 1
            mu_last, mu = mu, mu + (v - mu) / n
            S += (v - mu_last) * (v - mu)
            self._running_std = mu, n, S
            stdev = math.sqrt(S / (n - 1))
            yield (t, stdev)

    def online_std(self):
        """Return a SimulatedTimeSeries of the running std.
        Note that this is computed only over the samples that 
        are called from this method.
        """
        return SimulatedTimeSeries(self._online_std_genfun())

    def mean(self, chunk=20):
        """Return the mean of the next chunk values of the generator.
        Returns a float.  Does not include previous values."""

        return self.produce(chunk=chunk).mean()

    def std(self, chunk=20):
        """Return the standard deviation of the next chunk values of the generator.
        Returns a float.  Does not include previous values."""
        return self.produce(chunk=chunk).std()


class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
