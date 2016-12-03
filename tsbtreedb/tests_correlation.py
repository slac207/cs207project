
''''

Authors:
Sophie Hilgard
Ryan Lapcevic
Anthony Soroka
Ariel Herbert-Voss
Yamini Bansal

Date: 2nd Dec 2016
Course: Project CS 207
Document: test_correlation.py
Summary: Testing Correlation Functions

Example:
    Example how to run this test
        $ source activate py35
        $ py.test test_correlation.py

'''

import os, sys
curr_dir = os.getcwd().split('/')
sys.path.append('/'.join(curr_dir[:-1]))
ts_dir = curr_dir[:-1]
ts_dir.append('timeseries')
sys.path.append('/'.join(ts_dir))

from pytest import raises
from timeseries import Timeseries as ts
from SimilaritySearch import *
import numpy as np
import random
import math
import datetime


'''
Functions Being Tested: stand
Summary: Standard Deviation of the timeseries
'''
def test_stand():
    ts1 = ts.TimeSeries([100,101,102,103], [1, 2, 3, 4])
    ts1_stand = stand(ts1, np.mean([100,101,102,103]), np.std([100,101,102,103]))
    assert np.std(list(iter(ts1_stand))) == 1.0

'''
Functions Being Tested: max_corr_at_phase
Summary: Correlation of a timeseries with itself
'''
def test_self_maxccor():
    ts1 = ts.TimeSeries([100,101,102,103], [1, 2, 3, 4])
    assert max_corr_at_phase(ts1, ts1)[1] == 1.0

'''
Functions Being Tested: max_corr_at_phase
Summary: Correlation of two shifted timeseries
'''
def test_maxccor():
    ts1 = ts.TimeSeries([0, 1, 2, 3, 4, 3, 2, 1, 0], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    ts2 = ts.TimeSeries([1, 2, 3, 4, 3, 2, 1, 0, 0], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert abs(max_corr_at_phase(ts1, ts2)[1] - 1.0) < 1e-5

'''
Functions Being Tested: kernel_corr
Summary: Correlation of two shifted timeseries using the exponential kernel
'''
def test_kernel_corr():
    ts1 = ts.TimeSeries([0, 1, 2, 3, 4, 3, 2, 1, 0], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    ts2 = ts.TimeSeries([1, 2, 3, 4, 3, 2, 1, 0, 0], [1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert abs(kernel_corr(ts1, ts2, 10)-1) < 1e-3

    
