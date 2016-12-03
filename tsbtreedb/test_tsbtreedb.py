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
import lab10


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

'''
Functions Being Tested: Lab 10 -> connect, set, commit, close, get
Summary: Test set and get for a DB
'''
def test_db_get():
    dbName = "/tmp/test2.dbdb"
    if os.path.exists(dbName):
         os.remove(dbName)
    db = lab10.connect(dbName)
    db.set("rahul", "aged")
    db.set("pavlos", "aged")
    db.set("kobe", "stillyoung")
    db.commit()
    db.close()
    db = lab10.connect("/tmp/test2.dbdb")
    assert db.get("rahul") == "aged"
    db.commit()
    db.close()

'''
Functions Being Tested: Lab 10 -> set (override)
Summary: Test set (override) and get for a DB
'''
def test_db_set():
    dbName = "/tmp/test2.dbdb"
    if os.path.exists(dbName):
         os.remove(dbName)
    db = lab10.connect(dbName)
    db.set("rahul", "aged")
    db.set("pavlos", "aged")
    db.set("kobe", "stillyoung")
    db.commit()
    db.close()
    db = lab10.connect("/tmp/test2.dbdb")
    db.set("rahul", "young")
    db.get("rahul")
    assert db.get("rahul") == "young"
    db.commit()
    db.close()

'''
Functions Being Tested: Lab 10 -> get_All_LTE()
Summary: Test getting all Less than or Equal to (Keys)
'''
def test_db_get_All_LTE():
    dbName = "/tmp/test2.dbdb"
    if os.path.exists(dbName):
         os.remove(dbName)
    db = lab10.connect(dbName)
    db.set(4.4, "ts484.dat")
    db.set(0.0, "ts3.dat") #vantagePT
    db.set(1.3, "ts82.dat")
    db.set(2.9, "ts84.dat")
    db.set(2.3, "ts382.dat")
    db.set(2.1, "ts52.dat")
    db.set(1.8, "ts49.dat")
    db.set(1.1, "ts77.dat")
    db.set(5.3, "ts583.dat")
    keys, vals = db.get_All_LTE(2.9)
    assert keys == [0.0, 1.3, 2.9, 2.3, 2.1, 1.8, 1.1]
    db.commit()
    db.close()

'''
Functions Being Tested: Lab 10 -> get_All_LTE2()
Summary: Test getting all Less than or Equal to (Vals)
'''
def test_db_get_All_LTE2():
    dbName = "/tmp/test2.dbdb"
    if os.path.exists(dbName):
         os.remove(dbName)
    db = lab10.connect(dbName)
    db.set(4.4, "ts484.dat")
    db.set(0.0, "ts3.dat") #vantagePT
    db.set(1.3, "ts82.dat")
    db.set(2.9, "ts84.dat")
    db.set(2.3, "ts382.dat")
    db.set(2.1, "ts52.dat")
    db.set(1.8, "ts49.dat")
    db.set(1.1, "ts77.dat")
    db.set(5.3, "ts583.dat")
    keys, vals = db.get_All_LTE(2.9)
    assert vals == ['ts3.dat', 'ts82.dat', 'ts84.dat', 'ts382.dat', 'ts52.dat', 'ts49.dat', 'ts77.dat']
    db.commit()
    db.close()

'''
Functions Being Tested: get() -> Key Error
Summary: If key isn't there, raise KeyError
'''
def test_db_get_error():
    dbName = "/tmp/test2.dbdb"
    if os.path.exists(dbName):
         os.remove(dbName)
    db = lab10.connect(dbName)
    db.set(4.4, "ts484.dat")
    with raises(KeyError):
        db.get(3.9)
    db.commit()
    db.close()
