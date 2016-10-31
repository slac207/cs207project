from pytest import raises
import unittest
import lazy
import numpy as np
from Simulatedtimeseries import SimulatedTimeSeries, StreamTimeSeriesInterface
import collections
import itertools
from random import normalvariate, random

class SimulatedTimeSeriesTest(unittest.TestCase):
    def set_up(self):
        pass
        
    def test_test(self):
        a = SimulatedTimeSeries(iter(range(10)))
        a = 10
        assert 5+2+3==a