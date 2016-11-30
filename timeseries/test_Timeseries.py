from pytest import raises
import unittest
import lazy
import numpy as np
from Timeseries import TimeSeries
from ArrayTimeSeries import ArrayTimeSeries
import numbers
import collections
import timeSeriesABC


class TimeSeriesTest(unittest.TestCase):

    """ Test time series and array time series methods """
    def setUp(self):
        self.ts = TimeSeries(range(0,4),range(1,5))
        self.ats = ArrayTimeSeries(values=[0,5,10,8,7], times=[1,2.5,3,3.5,4])

    def tearDown(self):
        del self.ts
        del self.ats

    def test_input_diff_len(self):
        with raises(TypeError):
            t = TimeSeries([1,2,3],[3,1,3,4])
        with raises(TypeError):
            t = ArrayTimeSeries([1,2,3],[3,1,3,4])

    def test_input_range(self):
        t = TimeSeries(range(0,5))
        t = ArrayTimeSeries(values = range(1,10),times=range(10,19))

    def test_input_string(self):
        t = TimeSeries('abcd')
        t = ArrayTimeSeries('abcd',[0,10,20,30])
        t = ArrayTimeSeries('abcd','edsa')

    def test_input_list(self):
        t = TimeSeries([3,4,5])
        t = TimeSeries([])
        t = ArrayTimeSeries(values=[1,2,3,4],times=[10,20,30,40])

    def test_input_tuple(self):
        t = TimeSeries((2,3))
        t = TimeSeries(())
        t = ArrayTimeSeries((2,3),(1,2))
        t = ArrayTimeSeries((),())

    def test_input_nonseq(self):
        with raises(TypeError):
            t = TimeSeries(3)
        with raises(TypeError):
            t = TimeSeries(range(0,2),3)
        with raises(TypeError):
            t = ArrayTimeSeries(3)
        with raises(TypeError):
            t = ArrayTimeSeries(range(0,2),3)

    def test_string(self):
        assert str(TimeSeries((2,3))) == "TimeSeries with 2 elements (Times: range(0, 2), Values: [2, 3])"
        assert str(ArrayTimeSeries((2,3),(1,2))) == "ArrayTimeSeries with 2 elements (Times: array([2, 3]), Values: array([1, 2]))"

    def test_repr(self):
        assert repr(TimeSeries((2,3))) == "TimeSeries(Length: 2, Times: range(0, 2), Values: [2, 3])"
        assert repr(ArrayTimeSeries((2,3),(1,2))) == "ArrayTimeSeries(Length: 2, Times: array([2, 3]), Values: array([1, 2]))"

    def test_length(self):
        assert len(self.ts) == 4
        assert len(self.ats) == 5

    def test_getitem(self):
        with raises(IndexError):
            self.ts[12]
        assert self.ts[3] == 3
        with raises(IndexError):
            self.ats[12]
        assert self.ats[2] == 10

    def test_setitem(self):
        with raises(IndexError):
            self.ts.__setitem__(200,0)
        t = TimeSeries([1,2,3])
        t[1] = 5
        assert t[1] == 5
        ats = ArrayTimeSeries(times=[1,2,3],values=[3,6,8])
        ats[2] = 100
        assert ats[2] == 100
        with raises(IndexError):
            self.ats[6] = 203

    def test_iter(self):
        assert isinstance(iter(self.ts), collections.Iterable) == True
        assert list(iter(self.ts)) == [0,1,2,3]
        assert isinstance(iter(self.ats), collections.Iterable) == True
        assert list(iter(self.ats)) == [0,5,10,8,7]

    def test_itertimes(self):
        assert isinstance(self.ts.itertimes(), collections.Iterable) == True
        assert list(self.ts.itertimes()) == [1,2,3,4]
        assert isinstance(self.ats.itertimes(), collections.Iterable) == True
        assert list(self.ats.itertimes()) == [1.0,2.5,3.0,3.5,4.0]

    def test_iteritems(self):
        assert isinstance(self.ts.iteritems(), collections.Iterable) == True
        assert list(self.ts.iteritems()) == [(1, 0), (2, 1), (3, 2), (4, 3)]
        assert self.ts[3] == 3
        assert isinstance(self.ats.iteritems(), collections.Iterable) == True
        assert list(self.ats.iteritems()) == [(1.0, 0.0), (2.5, 5.0), (3.0, 10.0), (3.5, 8.0), (4.0, 7.0)]

    def test_contains(self):
        assert self.ts.__contains__(2) == True
        assert self.ts.__contains__(15) == False
        assert self.ats.__contains__(5) == True
        assert self.ats.__contains__(15) == False

    def test_itervalues(self):
        assert isinstance(self.ts.itervalues(), collections.Iterable) == True
        assert list(self.ts.itervalues()) == [0,1,2,3]
        assert isinstance(self.ats.itervalues(), collections.Iterable) == True
        assert list(self.ats.itervalues()) == [0,5,10,8,7]

    def test_times(self):
        assert (self.ts.times() == [1,2,3,4]).all()
        assert (self.ats.times() == [1,2.5,3,3.5,4]).all()

    def test_items(self):
        assert self.ts.items() == [(1, 0), (2, 1), (3, 2), (4, 3)]
        assert self.ats.items() == [(1.0, 0), (2.5, 5), (3.0, 10), (3.5, 8), (4.0, 7)]

    def test_values(self):
        assert (self.ts.values() == [0,1,2,3]).all()
        assert (self.ats.values() == [0,5,10,8,7]).all()

    def test_interpolate(self):
        a = TimeSeries(times=[0,5,10],values=[1,2,3])
        b = TimeSeries(times=[2.5,7.5],values=[100,-100])
        assert(a.interpolate([1]) == TimeSeries(times=[1],values=[1.2]))
        assert(a.interpolate(b.itertimes()) == TimeSeries(times=[2.5,7.5],values=[1.5,2.5]))
        assert(a.interpolate([-100,100]) == TimeSeries(times=[-100,100],values=[1,3]))
        assert(a.interpolate([5]) == TimeSeries(times=[5],values=[2]))
        assert(b.interpolate([0,2.5,7.5,10]) == TimeSeries(times=[0,2.5,7.5,10],values=[100,100,-100,-100]))

        a = ArrayTimeSeries(times=[0,5,10],values=[1,2,3])
        b = ArrayTimeSeries(times=[2.5,7.5],values=[100,-100])
        assert(a.interpolate([1]) == ArrayTimeSeries(times=[1],values=[1.2]))
        assert(a.interpolate(b.itertimes()) == ArrayTimeSeries(times=[2.5,7.5],values=[1.5,2.5]))
        assert(a.interpolate([-100,100]) == ArrayTimeSeries(times=[-100,100],values=[1,3]))
        assert(a.interpolate([5]) == ArrayTimeSeries(times=[5],values=[2]))
        assert(b.interpolate([0,2.5,7.5,10]) == ArrayTimeSeries(times=[0,2.5,7.5,10],values=[100,100,-100,-100]))

    def test_lazy(self):
        'lazy property should be an instance of LazyOperation'
        assert isinstance(self.ts.lazy,lazy.LazyOperation)==True
        assert isinstance(self.ats.lazy,lazy.LazyOperation)==True
        'self.ts.lazy.eval() should be the same as self.ts'
        assert self.ts is self.ts.lazy.eval()
        assert self.ats is self.ats.lazy.eval()

    def test_lazy_smoketest(self):
        '''An involved use of lazy operations on the lazy property
        to ensure the layers can work together'''
        @lazy.lazy
        def check_length(a,b):
            return len(a)==len(b)
        thunk = check_length(TimeSeries(range(0,4),range(1,5)).lazy, TimeSeries(range(1,5),range(2,6)).lazy)
        assert thunk.eval()==True
        @lazy.lazy
        def check_length(a,b):
            return len(a)==len(b)
        thunk = check_length(ArrayTimeSeries(values=range(0,4),times=range(1,5)).lazy, ArrayTimeSeries(values=range(1,5),times=range(2,6)).lazy)
        assert thunk.eval()==True

    def test_pos(self):
        # Values should be the same
        assert (+self.ts)._values==self.ts._values
        # Times should be the same
        assert (+self.ts)._times==list(self.ts._times)
        # A new instance should be created that is equal to the old.
        assert +self.ts==self.ts
        # Values should be the same
        assert np.all((+self.ats)._values==self.ats._values)
        # Times should be the same
        assert np.all((+self.ats)._times==list(self.ats._times))
        # A new instance should be created that is equal to the old.
        assert +self.ats==self.ats

    def test_neg(self):
        # Values should be negated
        assert (-self.ts)._values==[-v for v in self.ts._values]
        # Times should be the same
        assert (-self.ts)._times==list(self.ts._times)
        # Negating twice should return to the start
        assert -(-self.ts)==self.ts
        # Values should be negated
        assert np.all((-self.ats)._values==[-v for v in self.ats._values])
        # Times should be the same
        assert np.all((-self.ats)._times==list(self.ats._times))
        # Negating twice should return to the start
        assert -(-self.ats)==self.ats


    def test_abs(self):
        # absolute value of an instance and its negative should be the same.
        ts = TimeSeries(range(10))
        assert abs(ts)>0
        assert abs(ts)==abs(-ts)
        assert abs(ts)==16.881943016134134
        
        # test on ArrayTimeSeries
        ats = ArrayTimeSeries(range(10),range(10))
        assert abs(ats)>0
        assert abs(ats)==abs(-ats)
        assert abs(ats)==16.881943016134134
        
        
    def test_eq(self):
        self.ts3 = TimeSeries(range(10))
        self.ts4 = TimeSeries(range(10))
        self.ts5 = TimeSeries(range(9))
        self.ts6 = [0,1,2]
        assert self.ts3==self.ts4
        assert self.ts3 is not self.ts4
        assert self.ts3!=self.ts5
        assert self.ts3 != self.ts6
        self.ats3 = ArrayTimeSeries(values=range(10),times=range(10))
        self.ats4 = ArrayTimeSeries(values=range(10),times=range(10))
        self.ats5 = ArrayTimeSeries(values=range(9),times=range(9))
        self.ats6 = [0,1,2]
        assert self.ats3==self.ats4
        assert self.ats3 is not self.ats4
        assert self.ats3!=self.ats5
        assert self.ats3 != self.ats6
        
        # A TimeSeries should be able to equal an ArrayTimeSeries
        assert self.ts3==self.ats3
        
    def test_eq_ArrayTimeSeries_TimeSeries(self):
        self.ts7 = TimeSeries(range(10))
        self.ts8 = TimeSeries([10,34,23])
        self.ats7 = ArrayTimeSeries(values=range(10),times=range(10))
        self.ats8 = ArrayTimeSeries(values=range(8),times=range(8))
        # ArrayTimeSeries and TimeSeries objects should be the same if they have the same times and values
        assert self.ts7==self.ats7
        assert self.ats7==self.ts7
        assert self.ts7 is not self.ats8
        assert self.ats7!=self.ts8

    def test_add_ArrayTimeSeries_TimeSeries(self):
        ts1 = TimeSeries(range(10))
        ts2 = TimeSeries([10,34,23])
        ats1 = ArrayTimeSeries(values=range(10),times=range(10))
        ats2= ArrayTimeSeries(values=range(8),times=range(8))
        sumTS1 = ts1 + ats1
        # Check that the result is an instance of sized Container
        # Check that the size of times has not changed
        # Check that the elements have been added
        assert isinstance(sumTS1, timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert len(sumTS1.times())==len(ts1.times())
        assert sumTS1.values()[4] == ts1.values()[4] + ats1.values()[4]
        assert sumTS1.times()[-1] == ats1.times()[-1]
        sumTS2 = ats1 + ts1
        assert isinstance(sumTS2, timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert len(sumTS2.times())==len(ts1.times())
        assert sumTS2.values()[2] == ts1.values()[2] + ats1.values()[2]
        assert sumTS2.times()[-1] == ats1.times()[-1]
        
        # addition with numpy arrays should fail:
        with raises(TypeError):
            ts1+np.arange(10)
        with raises(TypeError):
            ats1+np.arange(10)
            
            
    def test_sub_TimeSeries_ArrayTimeSeries(self):
        ts1 = TimeSeries(range(10))
        ts2 = TimeSeries([0,1,2,3,4,5,6,7,8,9])
        ats1 = ArrayTimeSeries(values=range(10),times=range(10))
        subTS1 = ts1 - ats1
        subTS2 = ats1 - ts1
        subTS3 = ts2 - ats1
        # Check that the result is an instance of sized Container
        # Check that the size of times has not changed
        # Check that the elements have been subtracted
        assert isinstance(subTS1, timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert len(subTS1.times())==len(ts1.times())
        assert subTS1.values()[4] == ts1.values()[4] - ats1.values()[4]
        assert subTS1.times()[-1] == ats1.times()[-1]
        assert isinstance(subTS2, timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert len(subTS2.times())==len(ts1.times())
        assert subTS2.values()[2] == ts1.values()[2] - ats1.values()[2]
        assert subTS2.times()[-1] == ats1.times()[-1]
        assert isinstance(subTS3, timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert len(subTS3.times())==len(ts2.times())
        assert subTS3.values()[2] == ts2.values()[2] - ats1.values()[2]
        assert subTS3.times()[-1] == ats1.times()[-1]

        # subtraction with numpy arrays should fail:
        with raises(TypeError):
            ts1-np.arange(10)
        with raises(TypeError):
            ats1-np.arange(10)

    def test_multiply_Array_TimeSeries_TimeSeries(self):
        ts1 = TimeSeries(range(10))
        ts2 = TimeSeries([10,34,23])
        ats1 = ArrayTimeSeries(values=range(10),times=range(10))
        ats2= ArrayTimeSeries(values=range(8),times=range(8))
        mulTS1 = ts1.__mul__(ats1)
        mulTS2 = ats1 * ts1
        # Check that the result is an instance of sized Container
        # Check that the size of times has not changed
        # Check that the elements have been multiplied
        assert isinstance(mulTS1, timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert len(mulTS1.times())==len(ts1.times())
        assert mulTS1.values()[2] == ts1.values()[2] * ats1.values()[2]
        assert mulTS1.times()[-1] == ats1.times()[-1]
        assert isinstance(mulTS2, timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert len(mulTS2.times())==len(ts1.times())
        assert mulTS2.values()[2] == ts1.values()[2] * ats1.values()[2]
        assert mulTS2.times()[-1] == ats1.times()[-1]
        
        # multiplication with numpy arrays should fail:
        with raises(TypeError):
            ts1*np.arange(10)
        with raises(TypeError):
            ats1*np.arange(10)

            
    def test_bool(self):
        assert not bool(TimeSeries([0,0,0]))
        assert bool(TimeSeries([0,0,1]))
        assert bool(TimeSeries([-1,0,0]))
        assert not bool(ArrayTimeSeries(values=[0,0,0],times=range(3)))
        assert bool(ArrayTimeSeries(values=[0,0,1],times=range(3)))
        assert bool(ArrayTimeSeries(values=[-1,0,0],times=range(3)))


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
        self.ts_long = ArrayTimeSeries(values=range(9),times=range(9))
        assert self.ats+self.ats==ArrayTimeSeries(values=(2*v for v in self.ats._values),times=self.ats._times)
        # Addition with a constant is defined
        assert self.ats+5==ArrayTimeSeries(values=(5+v for v in self.ats._values),times=self.ats._times)
        # Different-length timeseries should return a value error
        with raises(ValueError):
            self.ats+self.ts_long
        # Time series with different values should return a value error
        with raises(ValueError):
            self.ats+ArrayTimeSeries(range(0,4),range(0,4))
        # addition with other types is not implemented
        with raises(TypeError):
            assert self.ats+'a'
        with raises(TypeError):
            assert 'a'+self.ats

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

        self.ats_long = ArrayTimeSeries(values=range(9),times=range(9))
        assert self.ats-self.ats==ArrayTimeSeries(values=(0 for v in self.ats._values),times=self.ats._times)
        assert self.ats-self.ats==self.ats+(-self.ats)
        # Subtraction with a constant is defined
        assert self.ats-5==ArrayTimeSeries(values=(v-5 for v in self.ats._values),times=self.ats._times)
        # Different-length timeseries should return a value error
        with raises(ValueError):
            self.ats-self.ats_long
        # Time series with different values should return a value error
        with raises(ValueError):
            self.ats-ArrayTimeSeries(values=range(0,4),times=range(0,4))
        # subtraction with other types is not implemented
        with raises(TypeError):
            assert self.ats-'a'
        with raises(TypeError):
            assert 'a'-self.ats

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

        self.ts_long = ArrayTimeSeries(range(9),range(9))
        assert self.ats*self.ats==ArrayTimeSeries(values=(v**2 for v in self.ats._values),times=self.ats._times)
        # Multiplication with a constant is defined
        assert self.ats*5==ArrayTimeSeries(values=(5*v for v in self.ats._values),times=self.ats._times)
        # Different-length timeseries should return a value error
        with raises(ValueError):
            self.ats*self.ts_long
        # Time series with different values should return a value error
        with raises(ValueError):
            self.ats*ArrayTimeSeries(values=range(0,4),times=range(0,4))
        # multiplication with other types is not implemented
        with raises(TypeError):
            assert self.ats*'a'
        with raises(TypeError):
            assert 'a'*self.ats
            

    def test_mean(self):
        self.ts  = TimeSeries(range(0,4),range(1,5))
        self.ats = ArrayTimeSeries(values=[0,5,10,8,7], times=[1,2.5,3,3.5,4])
        assert self.ts.mean() == 1.5
        assert self.ats.mean() == 6.0

        
    def test_std(self):
        self.ts  = TimeSeries(range(0,4),range(1,5))
        self.ats = ArrayTimeSeries(values=[0,5,10,8,7], times=[1,2.5,3,3.5,4])
        assert self.ts.std() == 1.2909944487358056
        assert self.ats.std() == 3.8078865529319543

        
        

if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover
