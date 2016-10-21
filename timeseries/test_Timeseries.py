from pytest import raises
import lazy
from Timeseries import TimeSeries

ts = TimeSeries(range(0,4),range(1,5))

def test_lazy():
    'lazy property should be an instance of LazyOperation'
    assert isinstance(ts.lazy,lazy.LazyOperation)==True
    'ts.lazy.eval() should be the same as ts'
    assert ts is ts.lazy.eval()

def test_lazy_smoketest():
    '''An involved use of lazy operations on the lazy property
    to ensure the layers can work together'''
    @lazy.lazy
    def check_length(a,b):
      return len(a)==len(b)
    thunk = check_length(TimeSeries(range(0,4),range(1,5)).lazy, TimeSeries(range(1,5),range(2,6)).lazy)
    assert thunk.eval()==True

def test_pos():
    # Values should be the same
    assert (+ts)._values==ts._values
    # Times should be the same
    assert (+ts)._times==list(ts._times)
    # A new instance should be created that is equal to the old.
    assert +ts==ts
    
def test_neg():
    # Values should be negated
    assert (-ts)._values==[-v for v in ts._values]
    # Times should be the same
    assert (-ts)._times==list(ts._times)
    # Negating twice should return to the start
    assert -(-ts)==ts
    
def test_abs():
    # absolute value of an instance with negative and positive values
    # should have only positive values
    ts2 = TimeSeries(range(-10,10))
    assert min(abs(ts2)._values)>=0
    # Times should be the same
    assert abs(ts2)._times == list(ts2._times)

def test_eq():
    ts3 = TimeSeries(range(10))
    ts4 = TimeSeries(range(10))
    ts5 = TimeSeries(range(9))
    assert ts3==ts4
    assert ts3 is not ts4
    assert ts3!=ts5
    
def test_bool():
    assert not bool(TimeSeries([0,0,0]))
    assert bool(TimeSeries([0,0,1]))
    assert bool(TimeSeries([-1,0,0]))
    
    
def test_add():
    ts_long = TimeSeries(range(9))
    assert ts+ts==TimeSeries((2*v for v in ts._values),ts._times)
    # Addition with a constant is defined
    assert ts+5==TimeSeries((5+v for v in ts._values),ts._times)
    # Different-length timeseries should return a value error
    with raises(ValueError):
        ts+ts_long
    # Time series with different values should return a value error
    with raises(ValueError):
    
        ts+TimeSeries(range(0,4),range(0,4))
    # addition with other types is not implemented    
    with raises(TypeError):
        assert ts+'a'
    with raises(TypeError):
        assert 'a'+ts
            
def test_sub():
    ts_long = TimeSeries(range(9))
    assert ts-ts==TimeSeries((0 for v in ts._values),ts._times)
    assert ts-ts==ts+(-ts)
    # Subtraction with a constant is defined
    assert ts-5==TimeSeries((v-5 for v in ts._values),ts._times)
    # Different-length timeseries should return a value error
    with raises(ValueError):
        ts-ts_long
    # Time series with different values should return a value error
    with raises(ValueError):
        ts-TimeSeries(range(0,4),range(0,4))
    # subtraction with other types is not implemented    
    with raises(TypeError):
        assert ts-'a'
    with raises(TypeError):
        assert 'a'-ts

def test_mul():
    ts_long = TimeSeries(range(9))
    assert ts*ts==TimeSeries((v**2 for v in ts._values),ts._times)
    # Multiplication with a constant is defined
    assert ts*5==TimeSeries((5*v for v in ts._values),ts._times)
    # Different-length timeseries should return a value error
    with raises(ValueError):
        ts*ts_long
    # Time series with different values should return a value error
    with raises(ValueError):
        ts*TimeSeries(range(0,4),range(0,4))
    # multiplication with other types is not implemented    
    with raises(TypeError):
        assert ts*'a'
    with raises(TypeError):
        assert 'a'*ts
    

