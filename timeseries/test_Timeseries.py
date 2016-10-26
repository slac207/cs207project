from pytest import raises
import unittest
import lazy
import numpy as np
from Timeseries import TimeSeries
from ArrayTimeSeries import ArrayTimeSeries
import collections

class ArrayTimeSeriesTest(unittest.TestCase):
    def setUp(self):
        self.ats = ArrayTimeSeries(values=[0,5,10,8,7], times=[1,2.5,3,3.5,4])

    def test_input_range(self):
        t = ArrayTimeSeries(values = range(1,10),times=range(10,19))

    def test_input_list(self):
        t = ArrayTimeSeries(values=[1,2,3,4],times=[10,20,30,40])

    def test_input_string(self):
        t = ArrayTimeSeries('abcd',[0,10,20,30])
        t = ArrayTimeSeries('abcd','edsa')

    def test_input_nonseq(self):
        with raises(TypeError):
            t = ArrayTimeSeries(3)
        with raises(TypeError):
            t = ArrayTimeSeries(range(0,2),3)

    def test_input_tuple(self):
        t = ArrayTimeSeries((2,3),(1,2))
        t = ArrayTimeSeries((),())

    def test_len(self):
        assert len(self.ats) == 5

    def test_getitem(self):
        with raises(IndexError):
            self.ats[12]
        assert self.ats[2] == 10

    def test_setitem(self):
        self.ats[4] = 100
        with raises(IndexError):
            self.ats[6] = 203

    def test_iter(self):
        assert isinstance(iter(self.ats), collections.Iterable) == True
        assert list(iter(self.ats)) == [0,5,10,8,7]

    def test_iteritems(self):
        assert isinstance(self.ats.iteritems(), collections.Iterable) == True
        assert list(self.ats.iteritems()) == [(1.0, 0.0), (2.5, 5.0), (3.0, 10.0), (3.5, 8.0), (4.0, 7.0)]

    def test_itertimes(self):
        assert isinstance(self.ats.itertimes(), collections.Iterable) == True
        assert list(self.ats.itertimes()) == [1.0,2.5,3.0,3.5,4.0]

    def test_string_repr(self):
        assert str(ArrayTimeSeries((2,3),(1,2))) == "ArrayTimeSeries with 2 elements (Times: array([2, 3]), Values: array([1, 2]))"
        assert repr(ArrayTimeSeries((2,3),(1,2))) == "ArrayTimeSeries(Length: 2, Times: array([2, 3]), Values: array([1, 2]))"

class TimeSeriesTest(unittest.TestCase):

    """ Test time series methods """
    def setUp(self):
        self.ts = TimeSeries(range(0,4),range(1,5))

    def tearDown(self):
        del self.ts
        
    def test_input_diff_len(self):
        with raises(TypeError):
            t = TimeSeries([1,2,3],[3,1,3,4])
            
    def test_input_range(self):
        t = TimeSeries(range(0,5))

    def test_input_string(self):
        t = TimeSeries('abcd')

    def test_input_list(self):
        t = TimeSeries([3,4,5])
        t = TimeSeries([])

    def test_input_tuple(self):
        t = TimeSeries((2,3))
        t = TimeSeries(())

    def test_input_nonseq(self):
        with raises(TypeError):
            t = TimeSeries(3)
        with raises(TypeError):
            t = TimeSeries(range(0,2),3)

    def test_string(self):
        assert str(TimeSeries((2,3))) == "TimeSeries with 2 elements (Times: range(0, 2), Values: [2, 3])"

    def test_repr(self):
        assert repr(TimeSeries((2,3))) == "TimeSeries(Length: 2, Times: range(0, 2), Values: [2, 3])"

    def test_length(self):
        assert len(self.ts) == 4

    def test_getitem(self):
        with raises(IndexError):
            self.ts[12]
        assert self.ts[3] == 3

    def test_setitem(self):
        with raises(IndexError):
            self.ts.__setitem__(200,0)

        t = TimeSeries([1,2,3])
        t[1] = 5
        assert t[1] == 5

    def test_iter(self):
        assert isinstance(iter(self.ts), collections.Iterable) == True
        assert list(iter(self.ts)) == [0,1,2,3]

    def test_itertimes(self):
        assert isinstance(self.ts.itertimes(), collections.Iterable) == True
        assert list(self.ts.itertimes()) == [1,2,3,4]

    def test_iteritems(self):
        assert isinstance(self.ts.iteritems(), collections.Iterable) == True
        assert list(self.ts.iteritems()) == [(1, 0), (2, 1), (3, 2), (4, 3)]
        assert self.ts[3] == 3

    def test_contains(self):
        assert self.ts.__contains__(2) == True
        assert self.ts.__contains__(15) == False

    def test_itervalues(self):
        assert isinstance(self.ts.itervalues(), collections.Iterable) == True
        assert list(self.ts.itervalues()) == [0,1,2,3]

    def test_times(self):
        assert (self.ts.times() == [1,2,3,4]).all()

    def test_items(self):
        assert self.ts.items() == [(1, 0), (2, 1), (3, 2), (4, 3)]

    def test_values(self):
        assert (self.ts.values() == [0,1,2,3]).all()

    def test_interpolate(self):
        a = TimeSeries(times=[0,5,10],values=[1,2,3])
        b = TimeSeries(times=[2.5,7.5],values=[100,-100])
        assert(a.interpolate([1]) == TimeSeries(times=[1],values=[1.2]))
        assert(a.interpolate(b.itertimes()) == TimeSeries(times=[2.5,7.5],values=[1.5,2.5]))
        assert(a.interpolate([-100,100]) == TimeSeries(times=[-100,100],values=[1,3]))   
        
    def test_lazy(self):
        'lazy property should be an instance of LazyOperation'
        assert isinstance(self.ts.lazy,lazy.LazyOperation)==True
        'self.ts.lazy.eval() should be the same as self.ts'
        assert self.ts is self.ts.lazy.eval()

    def test_lazy_smoketest(self):
        '''An involved use of lazy operations on the lazy property
        to ensure the layers can work together'''
        @lazy.lazy
        def check_length(a,b):
            return len(a)==len(b)
        thunk = check_length(TimeSeries(range(0,4),range(1,5)).lazy, TimeSeries(range(1,5),range(2,6)).lazy)
        assert thunk.eval()==True

    def test_pos(self):
        # Values should be the same
        assert (+self.ts)._values==self.ts._values
        # Times should be the same
        assert (+self.ts)._times==list(self.ts._times)
        # A new instance should be created that is equal to the old.
        assert +self.ts==self.ts

    def test_neg(self):
        # Values should be negated
        assert (-self.ts)._values==[-v for v in self.ts._values]
        # Times should be the same
        assert (-self.ts)._times==list(self.ts._times)
        # Negating twice should return to the start
        assert -(-self.ts)==self.ts

    def test_abs(self):
        # absolute value of an instance with negative and positive values
        # should have only positive values
        self.ts2 = TimeSeries(range(-10,10))
        assert min(abs(self.ts2)._values)>=0
        # Times should be the same
        assert abs(self.ts2)._times == list(self.ts2._times)

    def test_eq(self):
        self.ts3 = TimeSeries(range(10))
        self.ts4 = TimeSeries(range(10))
        self.ts5 = TimeSeries(range(9))
        self.ts6 = [0,1,2]
        assert self.ts3==self.ts4
        assert self.ts3 is not self.ts4
        assert self.ts3!=self.ts5
        assert self.ts3 != self.ts6

    def test_bool(self):
        assert not bool(TimeSeries([0,0,0]))
        assert bool(TimeSeries([0,0,1]))
        assert bool(TimeSeries([-1,0,0]))


    def test_add(self):
        self.ts_long = TimeSeries(range(9))
        assert self.ts+self.ts==TimeSeries((2*v for v in self.ts._values),self.ts._times)
        # Addition with a constant is defined
        assert self.ts+5==TimeSeries((5+v for v in self.ts._values),self.ts._times)
        # Different-length timeseries should return a value error
        with raises(ValueError):
            self.ts+self.ts_long
        # Time series with different values should return a value error
        with raises(ValueError):

            self.ts+TimeSeries(range(0,4),range(0,4))
        # addition with other types is not implemented
        with raises(TypeError):
            assert self.ts+'a'
        with raises(TypeError):
            assert 'a'+self.ts

    def test_sub(self):
        self.ts_long = TimeSeries(range(9))
        assert self.ts-self.ts==TimeSeries((0 for v in self.ts._values),self.ts._times)
        assert self.ts-self.ts==self.ts+(-self.ts)
        # Subtraction with a constant is defined
        assert self.ts-5==TimeSeries((v-5 for v in self.ts._values),self.ts._times)
        # Different-length timeseries should return a value error
        with raises(ValueError):
            self.ts-self.ts_long
        # Time series with different values should return a value error
        with raises(ValueError):
            self.ts-TimeSeries(range(0,4),range(0,4))
        # subtraction with other types is not implemented
        with raises(TypeError):
            assert self.ts-'a'
        with raises(TypeError):
            assert 'a'-self.ts

    def test_mul(self):
        self.ts_long = TimeSeries(range(9))
        assert self.ts*self.ts==TimeSeries((v**2 for v in self.ts._values),self.ts._times)
        # Multiplication with a constant is defined
        assert self.ts*5==TimeSeries((5*v for v in self.ts._values),self.ts._times)
        # Different-length timeseries should return a value error
        with raises(ValueError):
            self.ts*self.ts_long
        # Time series with different values should return a value error
        with raises(ValueError):
            self.ts*TimeSeries(range(0,4),range(0,4))
        # multiplication with other types is not implemented
        with raises(TypeError):
            assert self.ts*'a'
        with raises(TypeError):
            assert 'a'*self.ts

if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover
