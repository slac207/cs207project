from pytest import raises
import unittest
import lazy
import numpy as np
from Timeseries import TimeSeries
import collections

class TimeSeriesTest(unittest.TestCase):
    def setUp(self):
        self.ts = TimeSeries(range(0,4),range(1,5))
        
class LazyTest(unittest.TestCase):

    def setUp(self):
        self.ts = TimeSeries(range(0,4),range(1,5))

    def tearDown(self):
        del self.ts

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

    def test_length(self):
        assert len(self.ts) == 4

    def test_getitem(self):
        assert self.ts[3] == (4,3)

    def test_setitem(self):
        t = TimeSeries([1,2,3])
        t[1] = 5
        assert t[1] == (1,5)

    def test_iter(self):
        assert isinstance(iter(self.ts), collections.Iterable) == True
        assert list(iter(self.ts)) == [0,1,2,3]

    def test_itertimes(self):
        assert isinstance(self.ts.__itertimes__(), collections.Iterable) == True
        #assert list(self.ts.__itertimes__()) == [1,2,3,4]

    #def test_iteritems(self):
    #    assert isinstance(self.ts.__iteritems__(), collections.Iterable) == True
    #    assert list(self.ts.__iteritems__()) == [(1, 0), (2, 1), (3, 2), (4, 3)]


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
        assert self.ts3==self.ts4
        assert self.ts3 is not self.ts4
        assert self.ts3!=self.ts5

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


unittest.main()
