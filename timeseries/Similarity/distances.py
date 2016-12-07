import sys
import os.path
import inspect
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]) 
import numpy.fft as nfft
import numpy as np
from ArrayTimeSeries import ArrayTimeSeries as ts
#from SMTimeSeries import SMTimeSeries as ts
from scipy.stats import norm

def tsmaker(m, s, j):
    """Makes a TimeSeries whose values are approximately normally distributed
    m: location parameter for normal pdf
    s: scale parameter for normal pdf
    j: coefficient for extra randomness added to normally distributed values
    """
    t = np.arange(0.0, 1.0, 0.01)
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return ts(t, v)

def random_ts(a):
    """Creates a TimeSeries with random values
    a: scaling term to generate random values for time series
    """
    t = np.arange(0.0, 1.0, 0.01)
    v = a*np.random.random(100)
    return ts(t, v)

def stand(x, m, s):
    "standardize timeseries x by mean m and std deviation s"
    return (x-m)*(1/float(s))

def ccor(ts1, ts2):
    "given two standardized time series, compute their cross-correlation using FFT"
    return nfft.fftshift(np.real(nfft.ifft(nfft.fft(ts1)*np.conj(nfft.fft(ts2)))))/len(ts1)

# this is just for checking the max correlation with the
#kernelized cross-correlation
def max_corr_at_phase(ts1, ts2):
    ccorts = ccor(ts1, ts2)
    idx = np.argmax(ccorts)
    maxcorr = ccorts[idx]
    return idx, maxcorr

#The equation for the kernelized cross correlation is given at
#http://www.cs.tufts.edu/~roni/PUB/ecml09-tskernels.pdf
#normalize the kernel there by np.sqrt(K(x,x)K(y,y)) so that the correlation
#of a time series with itself is 1. We'll set the default multiplier to 1.
def kernel_corr(ts1, ts2, mult=1):
    "compute a kernelized correlation so that we can get a real distance"
    num = np.sum(np.exp(mult * ccor(ts1,ts2)))
    denom1 = np.sqrt(np.sum(np.exp(mult * ccor(ts1,ts1))))
    denom2 = np.sqrt(np.sum(np.exp(mult * ccor(ts2,ts2))))
    return  (num/denom1)/denom2

def distance(ts1,ts2,mult=1):
    """Calculates the distance metric using the kernal coefficient"""
    return 2*(1-kernel_corr(ts1, ts2, mult))


