''''

Authors:
Sophie Hilgard
Ryan Lapcevic
Anthony Soroka
Ariel Herbert-Voss
Yamini Bansal

Date: 1 Dec 2016
Course: Project CS 207
Document: test_tsbtreedb.py
Summary: Testing tsbtreedb functionalities

Example:
    Example how to run this test
        $ source activate py35
        $ py.test test_tsbtreedb.py

'''
import os, sys
curr_dir = os.getcwd().split('/')
sys.path.append('/'.join(curr_dir[:-1]))
ts_dir = curr_dir[:-1]
ts_dir.append('timeseries')
sys.path.append('/'.join(ts_dir))
import timeseries.Timeseries as ts
import SimilaritySearch as ss
from pytest import raises
import numpy as np
import random
import math
import datetime


'''
Functions Being Tested: tsmaker
Summary: Basic Len Test
'''
def test_len_tsmaker():
    t1 = ss.tsmaker(0.5, 0.1, 0.01)
    assert len(t1) == 100

'''
Functions Being Tested: random_ts
Summary: Basic Len Test
'''
def test_len_random_ts():
    t1 = ss.random_ts(2)
    assert len(t1) == 100

'''
Functions Being Tested: kernel_corr
Summary: Basic kernel_corr
'''
def test_kernel_corr():
    t1 = ss.random_ts(2)
    assert ss.kernel_corr(t1,t1) == 1

'''
Functions Being Tested: kernel_corr
Summary: Basic kernel_corr
'''
def test_kernel_corr2():
    t1 = ss.random_ts(2)
    t2 = ss.random_ts(3)
    assert ss.kernel_corr(t1,t2) != 1
