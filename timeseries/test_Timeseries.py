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

