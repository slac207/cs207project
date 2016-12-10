import os, sys

curr_dir = os.getcwd().split('/')
sys.path.append('/'.join(curr_dir[:-1]))
ts_dir = curr_dir[:-1]
ts_dir.append('timeseries')
sys.path.append('/'.join(ts_dir))
import numpy.fft as nfft
import numpy as np
# below is your module. Use your ListTimeSeries or ArrayTimeSeries..
from timeseries import Timeseries as ts
from scipy.stats import norm

'''

Code to calculate distances from vantage points which you can then use to do similarity search,

How to run:
python SimilaritySearch.py

Output:
HI
0.999071058544 1.3566298197725897 0.999380338186 1.3570526700214758
0.994987437107 0.994987437107
99 0.999942119235
0.999970386717
19 0.209255165854
0.00670302226967

'''


def tsmaker(m, s, j):
    t = np.arange(0.0, 1.0, 0.01)
    v = norm.pdf(t, m, s) + j * np.random.randn(100)
    return ts.TimeSeries(v, t)


def random_ts(a):
    t = np.arange(0.0, 1.0, 0.01)
    v = a * np.random.random(100)
    return ts.TimeSeries(v, t)


def stand(x, m, s):
    """Standardize timeseries x by mean m and std deviation s

    Args:
    x: Timeseries that is beign standardized
    m: Mean of the timeseries after standardization
    s: Standard deviation of the timeseries after standardization

    Output:
    A timeseries with mean 0 and standard deviation 1
    """
    vals = np.array(list(iter(x)))
    vals = (vals - m) / s
    return ts.TimeSeries(vals, list(x.itertimes()))


def ccor(ts1, ts2):
    """given two standardized time series, compute their cross-correlation using FFT

    Args:
    ts1, ts2: Timeseries whose correlation has to be checked

    Output: Value of dot product of the timeseries for different shifts of the second timeseries

    """
    f1 = nfft.fft(list(iter(ts1)))
    f2 = nfft.fft(np.flipud(list(iter(ts2))))
    cc = np.real(nfft.ifft(f1 * f2)) / (abs(ts1) * abs(ts2))
    return cc


# this is just for checking the max correlation with the
# kernelized cross-correlation
def max_corr_at_phase(ts1, ts2):
    """Calculates the maximum value of the correlation for different shifts

    Args:
    ts1, ts2: Timeseries whose correlation is to be calculated

    Output:
    idx: Index of maximum correlation
    maxcorr: Value of maximum correlation"""
    ccorts = ccor(ts1, ts2)
    cidx = np.argmax(ccorts)
    maxcorr = ccorts[cidx]
    return cidx, maxcorr


# The equation for the kernelized cross correlation is given at
# http://www.cs.tufts.edu/~roni/PUB/ecml09-tskernels.pdf
# normalize the kernel there by np.sqrt(K(x,x)K(y,y)) so that the correlation
# of a time series with itself is 1. We'll set the default multiplier to 1.
def kernel_corr(ts1, ts2, mult=1):
    """Kernelized correlation calculated with an exponential kernel.
        The correlation value may be slightly greater than 1 due to precision issues in the calculation

    Args:
    ts1, ts2: Timeseries whose correlation is to be caluclated
    mult: Kernel constant

    Output:
    Value of the correlation as a float"""
    # your code here.
    ccorts = ccor(ts1, ts2)
    cc1 = ccor(ts1, ts1)
    cc2 = ccor(ts2, ts2)
    exp_ccorts = np.exp(mult * ccorts)
    exp_ts1 = np.exp(mult * cc1)
    exp_ts2 = np.exp(mult * cc2)
    return sum(exp_ccorts) / np.sqrt(sum(exp_ts1) * sum(exp_ts2))


# this is for a quick and dirty test of these functions
if __name__ == "__main__":
    print("HI")
    t1 = tsmaker(0.5, 0.1, 0.01)
    t2 = tsmaker(0.5, 0.1, 0.01)
    print(t1.mean(), t1.std(), t2.mean(), t2.std())
    import matplotlib.pyplot as plt

    plt.plot(t1)
    plt.plot(t2)
    plt.show()
    standts1 = stand(t1, t1.mean(), t1.std())
    standts2 = stand(t2, t2.mean(), t2.std())
    print(np.std(list(iter(standts1))), np.std(list(iter(standts2))))

    idx, mcorr = max_corr_at_phase(standts1, standts2)
    print(idx, mcorr)
    sumcorr = kernel_corr(standts1, standts2, mult=10)
    print(sumcorr)
    t3 = random_ts(2)
    t4 = random_ts(3)
    plt.plot(t3)
    plt.plot(t4)
    plt.show()
    standts3 = stand(t3, t3.mean(), t3.std())
    standts4 = stand(t4, t4.mean(), t4.std())
    idx, mcorr = max_corr_at_phase(standts3, standts4)
    print(idx, mcorr)
    sumcorr = kernel_corr(standts3, standts4, mult=10)
    print(sumcorr)
