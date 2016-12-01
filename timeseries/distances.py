import numpy.fft as nfft
import numpy as np
#below is your module. Use your ListTimeSeries or ArrayTimeSeries..
import ArrayTimeSeries as ts
from scipy.stats import norm

def tsmaker(m, s, j):
    t = np.arange(0.0, 1.0, 0.01)
    v = norm.pdf(t, m, s) + j*np.random.randn(100)
    return ts.ArrayTimeSeries(t, v)

def random_ts(a):
    t = np.arange(0.0, 1.0, 0.01)
    v = a*np.random.random(100)
    return ts.ArrayTimeSeries(t, v)

def stand(x, m, s):
    "standardize timeseries x by mean m and std deviation s"
    return (x-m)*(1/float(s))

def ccor(ts1, ts2):
    "given two standardized time series, compute their cross-correlation using FFT"
    return np.real(nfft.ifft(nfft.fft(ts1)*np.conj(nfft.fft(ts2))))/len(ts1)


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
    print("Numerator is ", num)
    denom1 = np.sqrt(np.sum(np.exp(mult * ccor(ts1,ts1))))
    denom2 = np.sqrt(np.sum(np.exp(mult * ccor(ts2,ts2))))

    return  (num/denom1)/denom2


#this is for a quick and dirty test of these functions
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
    #print("STANDARDIZED",standts1)

    standts2 = stand(t2, t2.mean(), t2.std())

    idx, mcorr = max_corr_at_phase(standts1, standts2)
    print(idx, mcorr)
    sumcorr = kernel_corr(standts1, standts2, mult=10)
    print(sumcorr)
    t3 = random_ts(2)
    t4 = random_ts(3)
    #plt.plot(t3)
    #plt.plot(t4)
    #plt.show()
    standts3 = stand(t3, t3.mean(), t3.std())
    print("TYPE IS",type(standts1), type(t1))
    
    standts4 = stand(t4, t4.mean(), t4.std())
    idx, mcorr = max_corr_at_phase(standts3, standts4)
    print(idx, mcorr)
    sumcorr = kernel_corr(standts3, standts4, mult=10)
    print("END",sumcorr)
    
    #ts1 with ts1 look at the maximum and try to get 1 