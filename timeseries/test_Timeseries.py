from pytest import raises
import unittest
import lazy
import numpy as np
from Timeseries import TimeSeries
from ArrayTimeSeries import ArrayTimeSeries
from StorageManager import SMTimeSeries, FileStorageManager
import numbers
import collections
import timeSeriesABC


class SizedContainerTimeSeriesInterfaceTest(unittest.TestCase):

    """ Test any time series that adheres to the SizedContainerTimeSeriesInterface"""
    def setUp(self):
        self.ts=None
        
    def tearDown(self):
        del self.ts
        
    def test_length(self):
        if self.ts is None:
            return
        assert len(self.ts) == 4

    def test_getitem(self):
        if self.ts is None:
            return
        with raises(IndexError):
            self.ts[12]
        assert self.ts[3] == 3

    def test_setitem(self):
        if self.ts is None:
            return
        with raises(IndexError):
            self.ts[200] = 0
        self.ts[2] = -10
        assert self.ts[2] == -10

    def test_iter(self):
        if self.ts is None:
            return
        assert isinstance(iter(self.ts), collections.Iterable) == True
        assert list(iter(self.ts)) == [0,1,2,3]

    def test_itertimes(self):
        if self.ts is None:
            return
        assert isinstance(self.ts.itertimes(), collections.Iterable) == True
        assert list(self.ts.itertimes()) == [10,11,12,13]

    def test_iteritems(self):
        if self.ts is None:
            return
        assert isinstance(self.ts.iteritems(), collections.Iterable) == True
        assert list(self.ts.iteritems()) == [(10, 0), (11, 1), (12, 2), (13, 3)]

    def test_times(self):
        if self.ts is None:
            return
        assert self.ts.items() == list(zip(self.ts.times(),self.ts.values()))
    
    def test_contains(self):
        if self.ts is None:
            return
        assert self.ts.__contains__(3) == True
        assert self.ts.__contains__(13) == False

    def test_itervalues(self):
        if self.ts is None:
            return
        assert isinstance(self.ts.itervalues(), collections.Iterable) == True
        assert list(self.ts.itervalues()) == [0,1,2,3]

    def test_interpolate(self):
        if self.ts is None:
            return
        # check class, times, values equal.
        ts_interp = self.ts.interpolate([10.5])
        assert type(ts_interp) == type(self.ts)
        assert ts_interp.times() == [10.5]
        assert ts_interp.values() == [0.5]
        
        ts_extrap = self.ts.interpolate([-100,100])
        assert type(ts_extrap) == type(self.ts)
        assert (ts_extrap.times() == [-100,100]).all()
        assert (ts_extrap.values() == [0,3]).all()

        # # extrapolate right on the endpoints.
        # ts_extrap = self.ts.interpolate([11])
        # assert type(ts_extrap) == type(self.ts)
        # assert (ts_extrap.times() == [11]).all()
        # assert (ts_extrap.values() == [1]).all()


    def test_lazy(self):
        if self.ts is None:
            return
        'lazy property should be an instance of LazyOperation'
        assert isinstance(self.ts.lazy,lazy.LazyOperation)==True
        'self.ts.lazy.eval() should be the same as self.ts'
        assert self.ts is self.ts.lazy.eval()

    def test_pos(self):
        if self.ts is None:
            return
        # Values should be the same
        assert list((+self.ts)._values)==list(self.ts._values)
        # Times should be the same
        assert list((+self.ts)._times)==list(self.ts._times)
        # A new instance should be created that is equal to the old.
        assert +self.ts==self.ts

    def test_neg(self):
        if self.ts is None:
            return
        # Values should be negated
        assert list((-self.ts)._values)==[-v for v in self.ts._values]
        # Times should be the same
        assert list((-self.ts)._times)==list(self.ts._times)
        # Negating twice should return to the start
        assert -(-self.ts)==self.ts

    def test_abs(self):
        if self.ts is None:
            return
        # absolute value of an instance and its negative should be the same.
        assert abs(self.ts)>0
        assert abs(self.ts)==abs(-self.ts)
        assert abs(self.ts)==3.7416573867739413
        
    def test_eq(self):
        if self.ts is None:
            return
        assert self.ts2==self.ts3
        assert self.ts2 is not self.ts3
        assert self.ts !=self.ts2
        assert self.ts2 != self.ts4
        assert self.ts != 'a'
            
    def test_bool(self):
        if self.ts is None:
            return
        assert not bool(self.ts*0)
        assert bool(self.ts)
        assert bool(-self.ts)

    def test_add(self):
        if self.ts is None:
            return
        ts_add = self.ts_a+self.ts_b
        # Class should be preserved, times maintained, values added
        assert isinstance(ts_add,type(self.ts_a))
        assert (ts_add.times()==self.ts_a.times()).all()
        assert (ts_add.values() == [0,2,4,6,8]).all()
        
        ts_add_c = self.ts+5
        # Class should be preserved, times maintained, values added
        assert isinstance(ts_add_c,type(self.ts))
        assert (ts_add_c.times()==self.ts.times()).all()
        assert (ts_add_c.values() == self.ts.values()+5).all()
        
        # Time series with different times should return a value error
        with raises(ValueError):
            self.ts+self.ts2
        # Time series with different lengths should return a value error
        with raises(ValueError):
            self.ts2+self.ts4
        # addition with other types is not implemented
        with raises(TypeError):
            assert self.ts+'a'
        with raises(TypeError):
            assert 'a'+self.ts
        # addition with numpy arrays should fail:
        with raises(TypeError):
            self.ts+np.arange(4)

    def test_sub(self):
        if self.ts is None:
            return
        ts_sub = self.ts_a-self.ts_b
        # Class should be preserved, times maintained, values subtracted
        assert isinstance(ts_sub,type(self.ts_a))
        assert (ts_sub.times()==self.ts_a.times()).all()
        assert (ts_sub.values() == [4,4,4,4,4]).all()
        
        ts_sub_c = self.ts-5
        # Class should be preserved, times maintained, values subtracted
        assert isinstance(ts_sub_c,type(self.ts))
        assert (ts_sub_c.times()==self.ts.times()).all()
        assert (ts_sub_c.values() == self.ts.values()-5).all()
        
        # Time series with different times should return a value error
        with raises(ValueError):
            self.ts-self.ts2
        # Time series with different lengths should return a value error
        with raises(ValueError):
            self.ts2-self.ts4
        # subtraction with other types is not implemented
        with raises(TypeError):
            self.ts-'a'
        with raises(TypeError):
            'a'-self.ts
        # subtraction with numpy arrays should fail:
        with raises(TypeError):
            self.ts-np.arange(4)
            
        assert self.ts_a-self.ts_b==self.ts_a+(-self.ts_b)
            
    def test_mul(self):
        if self.ts is None:
            return
        ts_mul = self.ts_a*self.ts_b
        # Class should be preserved, times maintained, values multiplied
        assert isinstance(ts_mul,type(self.ts_a))
        assert (ts_mul.times()==self.ts_a.times()).all()
        assert (ts_mul.values() == [-4,-3,0,5,12]).all()
        
        ts_mul_c = self.ts*5
        # Class should be preserved, times maintained, values multiplied
        assert isinstance(ts_mul_c,type(self.ts))
        assert (ts_mul_c.times()==self.ts.times()).all()
        assert (ts_mul_c.values() == self.ts.values()*5).all()
        
        # Time series with different times should return a value error
        with raises(ValueError):
            self.ts*self.ts2
        # Time series with different lengths should return a value error
        with raises(ValueError):
            self.ts2*self.ts4
        # multiplication with other types is not implemented
        with raises(TypeError):
            self.ts*'a'
        with raises(TypeError):
            'a'*self.ts            
        # multiplication with numpy arrays should fail:
        with raises(TypeError):
            self.ts*np.arange(4)

    def test_mean(self):
        if self.ts is None:
            return
        assert self.ts.mean() == 1.5
        
    def test_std(self):
        if self.ts is None:
            return
        assert self.ts.std() == 1.2909944487358056

class SizedContainerTimeSeriesInterfaceTestInteractions(unittest.TestCase):

    def setUp(self):
        self.ts1 = None
                
    def tearDown(self):
        del self.ts1
        
    def test_eq_interaction(self):
        if self.ts1 is None:
            return
        assert self.ts1 == self.ts2c
        assert self.ts2c == self.ts1
        assert self.ts1 is not self.ts2c
        assert self.ts2c is not self.ts1
        assert self.ts1 != self.ts2
        assert self.ts2 != self.ts1
    
    def test_add_interaction(self):
        if self.ts1 is None:
            return
        ts_sum = self.ts1+self.ts2
        assert isinstance(ts_sum,timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert type(ts_sum)==type(self.ts1)
        assert (ts_sum.times()==self.ts1.times()).all()
        # All values should be the same, but the interface does not specify the format
        # for returning them.  Therefore, we just do three spot-checks.
        assert ts_sum.values()[0]==self.ts1.values()[0]+self.ts2.values()[0]
        assert ts_sum.values()[2]==self.ts1.values()[2]+self.ts2.values()[2]
        assert ts_sum.values()[-1]==self.ts1.values()[-1]+self.ts2.values()[-1]
        
        ts_sum = self.ts2+self.ts1
        assert isinstance(ts_sum,timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert type(ts_sum)==type(self.ts2)
        assert (ts_sum.times()==self.ts2.times()).all()
        # All values should be the same, but the interface does not specify the format
        # for returning them.  Therefore, we just do three spot-checks.
        assert ts_sum.values()[0]==self.ts1.values()[0]+self.ts2.values()[0]
        assert ts_sum.values()[2]==self.ts1.values()[2]+self.ts2.values()[2]
        assert ts_sum.values()[-1]==self.ts1.values()[-1]+self.ts2.values()[-1]
        
        # These have different times so should fail
        with raises(ValueError):
            self.ts1+self.ts2b
        with raises(ValueError):
            self.ts2b+self.ts1
            
    def test_sub_interaction(self):
        if self.ts1 is None:
            return
        ts_sub = self.ts1-self.ts2
        assert isinstance(ts_sub,timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert type(ts_sub)==type(self.ts1)
        assert (ts_sub.times()==self.ts1.times()).all()
        # All values should be the same, but the interface does not specify the format
        # for returning them.  Therefore, we just do three spot-checks.
        assert ts_sub.values()[0]==self.ts1.values()[0]-self.ts2.values()[0]
        assert ts_sub.values()[2]==self.ts1.values()[2]-self.ts2.values()[2]
        assert ts_sub.values()[-1]==self.ts1.values()[-1]-self.ts2.values()[-1]
        
        ts_sub = self.ts2-self.ts1
        assert isinstance(ts_sub,timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert type(ts_sub)==type(self.ts2)
        assert (ts_sub.times()==self.ts2.times()).all()
        # All values should be the same, but the interface does not specify the format
        # for returning them.  Therefore, we just do three spot-checks.
        assert ts_sub.values()[0]==self.ts2.values()[0]-self.ts1.values()[0]
        assert ts_sub.values()[2]==self.ts2.values()[2]-self.ts1.values()[2]
        assert ts_sub.values()[-1]==self.ts2.values()[-1]-self.ts1.values()[-1]
        
        # These have different times so should fail
        with raises(ValueError):
            self.ts1-self.ts2b
        with raises(ValueError):
            self.ts2b-self.ts1
        
    def test_multiply_interaction(self):
        if self.ts1 is None:
            return
        ts_mul = self.ts1*self.ts2
        assert isinstance(ts_mul,timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert type(ts_mul)==type(self.ts1)
        assert (ts_mul.times()==self.ts1.times()).all()
        # All values should be the same, but the interface does not specify the format
        # for returning them.  Therefore, we just do three spot-checks.
        assert ts_mul.values()[0]==self.ts1.values()[0]*self.ts2.values()[0]
        assert ts_mul.values()[2]==self.ts1.values()[2]*self.ts2.values()[2]
        assert ts_mul.values()[-1]==self.ts1.values()[-1]*self.ts2.values()[-1]
        
        ts_mul = self.ts2*self.ts1
        assert isinstance(ts_mul,timeSeriesABC.SizedContainerTimeSeriesInterface)
        assert type(ts_mul)==type(self.ts2)
        assert (ts_mul.times()==self.ts2.times()).all()
        # All values should be the same, but the interface does not specify the format
        # for returning them.  Therefore, we just do three spot-checks.
        assert ts_mul.values()[0]==self.ts1.values()[0]*self.ts2.values()[0]
        assert ts_mul.values()[2]==self.ts1.values()[2]*self.ts2.values()[2]
        assert ts_mul.values()[-1]==self.ts1.values()[-1]*self.ts2.values()[-1]
        
        # These have different times so should fail
        with raises(ValueError):
            self.ts1*self.ts2b
        with raises(ValueError):
            self.ts2b*self.ts1
            
class test_TimeSeries(SizedContainerTimeSeriesInterfaceTest):
    def setUp(self):
        self.ts = TimeSeries(range(0,4),range(10,14))
        self.ts2 = TimeSeries(range(4))
        self.ts3 = TimeSeries(list(range(4)))
        self.ts4 = TimeSeries(range(5))
        self.ts_a = TimeSeries([2,3,4,5,6],range(10,15))
        self.ts_b = TimeSeries([-2,-1,0,1,2],range(10,15))

    def tearDown(self):
        del self.ts
        del self.ts2
        del self.ts3
        del self.ts4
        del self.ts_a
        del self.ts_b
        
    def test_init(self):
        # Takes (values, times[optional]) as inputs
        
        # each of these should succeed
        ts = TimeSeries(range(0,4),range(10,14))
        ts = TimeSeries([0,1,2,3],[10,11,12,13])
        ts = TimeSeries(np.arange(4),np.arange(10,14))
        ts = TimeSeries(range(0,4))
        ts = TimeSeries([0,1,2,3])
        ts = TimeSeries(np.arange(4))
        ts = TimeSeries(range(0,4),np.arange(10,14))
        ts = TimeSeries([0,1,2,3],np.arange(10,14))
        
        # Times and Values must have the same lengths.
        with raises(TypeError):
            ts = TimeSeries(range(0,4),range(0,5))
 
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
    
    def test_string(self):
        assert str(TimeSeries((2,3))) == "TimeSeries with 2 elements (Times: range(0, 2), Values: [2, 3])"

    def test_repr(self):
        assert repr(TimeSeries((2,3))) == "TimeSeries(Length: 2, Times: range(0, 2), Values: [2, 3])"
    
class test_ArrayTimeSeries(SizedContainerTimeSeriesInterfaceTest):
    def setUp(self):
        self.ts = ArrayTimeSeries(range(10,14),range(0,4))
        self.ts2 = ArrayTimeSeries(range(4),range(4))
        self.ts3 = ArrayTimeSeries(list(range(4)),list(range(4)))
        self.ts4 = ArrayTimeSeries(range(5),range(5))
        self.ts_a = ArrayTimeSeries(range(10,15),[2,3,4,5,6])
        self.ts_b = ArrayTimeSeries(range(10,15),[-2,-1,0,1,2])

    def tearDown(self):
        del self.ts
        del self.ts2
        del self.ts3
        del self.ts4
        del self.ts_a
        del self.ts_b

    def test_init(self):
        # Takes (time, values) as inputs; both required
        
        # each of these should succeed
        ts = ArrayTimeSeries(range(0,4),range(10,14))
        ts = ArrayTimeSeries([0,1,2,3],[10,11,12,13])
        ts = ArrayTimeSeries(np.arange(4),np.arange(10,14))
        ts = ArrayTimeSeries(range(0,4),np.arange(10,14))
        ts = ArrayTimeSeries([0,1,2,3],np.arange(10,14))
        
        # Times and Values must both be given
        with raises(TypeError):
            ts = ArrayTimeSeries(range(0,4))
        # Times and Values must have the same lengths.
        with raises(TypeError):
            ts = ArrayTimeSeries(range(0,4),range(0,5))

    def test_input_string(self):
        t = ArrayTimeSeries('abcd',[0,10,20,30])
        t = ArrayTimeSeries('abcd','edsa')

    def test_input_list(self):
        t = ArrayTimeSeries(values=[1,2,3,4],times=[10,20,30,40])

    def test_input_tuple(self):
        t = ArrayTimeSeries((2,3),(1,2))
        t = ArrayTimeSeries((),())

    def test_input_nonseq(self):
        with raises(TypeError):
            t = ArrayTimeSeries(4,3)
    
    def test_string(self):
        assert str(ArrayTimeSeries((2,3),(1,2))) == "ArrayTimeSeries with 2 elements (Times: array([2, 3]), Values: array([1, 2]))"

    def test_repr(self):
        assert repr(ArrayTimeSeries((2,3),(1,2))) == "ArrayTimeSeries(Length: 2, Times: array([2, 3]), Values: array([1, 2]))"

            
class test_SMTimeSeries(SizedContainerTimeSeriesInterfaceTest):
    def setUp(self):
        self.sm = FileStorageManager()

        self.ts = SMTimeSeries(range(10,14),range(0,4),id=1,SM=self.sm)
        self.ts2 = SMTimeSeries(range(4),range(4),id=2,SM=self.sm)
        self.ts3 = SMTimeSeries(list(range(4)),list(range(4)),id=3,SM=self.sm)
        self.ts4 = SMTimeSeries(range(5),range(5),id=4,SM=self.sm)
        self.ts_a = SMTimeSeries(range(10,15),[2,3,4,5,6],id=5,SM=self.sm)
        self.ts_b = SMTimeSeries(range(10,15),[-2,-1,0,1,2],id=6,SM=self.sm)
        
        self.sm.store(100,self.ts)
        self.sm.store(101,self.ts2)

    def tearDown(self):
        del self.ts
        del self.ts2
        del self.ts3
        del self.ts4
        del self.ts_a
        del self.ts_b

    def test_init_times_values(self):
        # The call signature for SMTimeSeries is 
        # (times=None,values=None,id=None,SM=None,get_from_SM=False)
        
        # It should succeed with only (times,values) given
        ts = SMTimeSeries(range(0,4),range(0,4))
        ts = SMTimeSeries(times=range(0,4),values=range(0,4))
        ts = SMTimeSeries([0,1,2,3],np.arange(10,14))
        
        # It should succeed with (times,values) given, plus an id
        ts = SMTimeSeries(range(0,4),range(0,4),id=12)
        assert ts.id==12
        
        # It should succeed with (times,values) given, plus a storage manager
        ts = SMTimeSeries(range(0,4),range(0,4),SM=self.sm)
        
        # It should succeed with (times,values) given, plus a storage manager and id
        ts = SMTimeSeries(range(0,4),range(0,4),id=12,SM=self.sm)
        assert ts.id==12
        
        # Times and Values must both be given
        with raises(TypeError):
            ts = SMTimeSeries(range(0,4))
        # Times and Values must have the same lengths.
        with raises(TypeError):
            ts = SMTimeSeries(range(0,4),range(0,5))
        
    def test_init_from_db(self):
        # from_db has a call signature (SM,id)
        
        ts = SMTimeSeries.from_db(self.sm,100)
        assert ts.id==100
        assert ts==self.ts
        
        ts = SMTimeSeries.from_db(self.sm,101)
        assert ts.id==101
        assert ts==self.ts2

        with raises(KeyError):
            ts = SMTimeSeries.from_db(self.sm,102)
        
    def test_init_from_ts(self):
        # from_ts has a call signature (ts,SM=None,id=None)
        
        # Can be called with just a time series
        ts = SMTimeSeries.from_ts(TimeSeries(range(5)))
        ts = SMTimeSeries.from_ts(self.ts)
        assert ts==self.ts
        assert ts.id==1

        # Can be called with a storage manager 
        ts = SMTimeSeries.from_ts(self.ts,SM=self.sm)
        assert ts==self.ts
        assert len(self.sm._index)==9

        # Can be called with an id
        ts = SMTimeSeries.from_ts(self.ts,id=3)
        assert ts==self.ts
        assert ts.id==3

        # Can be called with a storage manager and id
        ts = SMTimeSeries.from_ts(self.ts,SM=self.sm,id=13)
        assert ts==self.ts
        assert ts.id==13
        # 4 because this is the second time we've added to it
        assert len(self.sm._index)==10
        
class test_TimeSeries_ArrayTimeSeries_Interactions(SizedContainerTimeSeriesInterfaceTestInteractions):
        
    def setUp(self):
        self.ts1 = TimeSeries(range(1,6),range(11,16))
        self.ts2 = ArrayTimeSeries(range(11,16),range(-2,3))
        # With different times, this one should fail
        self.ts2b = ArrayTimeSeries(range(1,6),range(-2,3))
        # This should be equal to ts1
        self.ts2c = ArrayTimeSeries(range(11,16),range(1,6))
                
    def tearDown(self):
        del self.ts1
        del self.ts2
        del self.ts2b
        del self.ts2c

class test_SMTimeSeries_ArrayTimeSeries_Interactions(SizedContainerTimeSeriesInterfaceTestInteractions):
        
    def setUp(self):
        self.ts1 = SMTimeSeries(range(11,16),range(1,6) )
        self.ts2 = ArrayTimeSeries(range(11,16),range(-2,3))
        # With different times, this one should fail
        self.ts2b = ArrayTimeSeries(range(1,6),range(-2,3))
        # This should be equal to ts1
        self.ts2c = ArrayTimeSeries(range(11,16),range(1,6))
                
    def tearDown(self):
        del self.ts1
        del self.ts2
        del self.ts2b
        del self.ts2c
        
class test_TimeSeries_SMTimeSeries_Interactions(SizedContainerTimeSeriesInterfaceTestInteractions):
        
    def setUp(self):
        self.ts1 = TimeSeries(range(1,6),range(11,16))
        self.ts2 = SMTimeSeries(range(11,16),range(-2,3))
        # With different times, this one should fail
        self.ts2b = SMTimeSeries(range(1,6),range(-2,3))
        # This should be equal to ts1
        self.ts2c = SMTimeSeries(range(11,16),range(1,6))
                
    def tearDown(self):
        del self.ts1
        del self.ts2
        del self.ts2b
        del self.ts2c