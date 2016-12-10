from pytest import raises
import unittest
import lazy
import numpy as np
from SimulatedTimeSeries import SimulatedTimeSeries, InputError
from ArrayTimeSeries import ArrayTimeSeries
import collections
import itertools
from random import normalvariate, random
import numbers


class SimulatedTimeSeriesTest(unittest.TestCase):
    def setUp(self):
        def make_data(m, stop=None):
            for _ in itertools.count():
                if stop and _ > stop:
                    break  # pragma: no cover
                yield normalvariate(0, m * random())

        self.make_data = make_data
        self.data = zip(itertools.count(10), self.make_data(1))
        self.ts0 = SimulatedTimeSeries(self.data)

    def tearDown(self):
        del self.make_data

    def test_init(self):
        # Construct with an iterator
        self.ts = SimulatedTimeSeries(iter(range(10)))
        assert isinstance(self.ts, SimulatedTimeSeries)
        # Construct with an itertools count method
        self.ts2 = SimulatedTimeSeries(itertools.count())
        assert isinstance(self.ts2, SimulatedTimeSeries)
        # Construct with zipped tuples of count and a generator
        assert isinstance(self.ts0, SimulatedTimeSeries)
        # Cannot construct with a list
        with raises(InputError):
            SimulatedTimeSeries([0, 1, 2])

        # Cannot have a generator yielding a tuple of length other than 2:
        def genfun_return_triplet():
            for _ in range(10):
                yield (0, 1, 2)

        gen_return_triplet = genfun_return_triplet()
        with raises(InputError):
            SimulatedTimeSeries(gen_return_triplet)

    @staticmethod
    def test_iter():
        # the iter method should return an iterable
        # that yields the values
        tsiter = iter(SimulatedTimeSeries(iter(range(10))))
        assert isinstance(tsiter, collections.Iterable)
        assert isinstance(next(tsiter), numbers.Real)

    @staticmethod
    def test_itertimes():
        ts = SimulatedTimeSeries(iter(range(10)))
        times = ts.itertimes()
        assert isinstance(times, collections.Iterable)
        assert isinstance(next(times), numbers.Real)

    @staticmethod
    def test_itervalues():
        ts = SimulatedTimeSeries(iter(range(10)))
        values = ts.itervalues()
        assert isinstance(values, collections.Iterable)
        assert isinstance(next(values), numbers.Real)

    @staticmethod
    def test_iteritems():
        ts = SimulatedTimeSeries(iter(range(10)))
        items = ts.iteritems()
        assert isinstance(items, collections.Iterable)
        assert isinstance(next(items), tuple)
        t, v = next(items)
        assert isinstance(t, numbers.Real)
        assert isinstance(v, numbers.Real)

    @staticmethod
    def test_produce():
        ts = SimulatedTimeSeries(iter(range(10)))
        ats = ts.produce(20)
        assert isinstance(ats, ArrayTimeSeries)
        assert len(ats) == 9
        assert list(ats._times) == list(range(1, 10))
        assert list(ats._values) == list(range(1, 10))

        ts = SimulatedTimeSeries(iter(range(100)))
        ats = ts.produce(20)
        assert len(ats) == 20

    def test_repr(self):
        assert repr(self.ts0) == 'Instance of a SimulatedTimeSeries with streaming input'

    def test_str(self):
        assert str(self.ts0) == 'Instance of a SimulatedTimeSeries with streaming input'

    @staticmethod
    def test_lazy():
        ts = SimulatedTimeSeries(iter(range(10)))
        tslazy = ts.lazy
        assert isinstance(tslazy, lazy.LazyOperation)
        assert isinstance(tslazy.eval(), SimulatedTimeSeries)

    @staticmethod
    def test_online_mean():
        ts = SimulatedTimeSeries(iter(range(100)))
        assert isinstance(ts.online_mean(), SimulatedTimeSeries)
        assert all(ts.online_mean().produce(10)._values == np.arange(0.5, 5.5, 0.5))

    @staticmethod
    def test_online_std():
        ts = SimulatedTimeSeries(iter(range(100)))
        assert isinstance(ts.online_std(), SimulatedTimeSeries)
        assert all(ts.online_std().produce(10)._values == np.sqrt(
            np.array([(i ** 2) / 12 + 5 * i / 12 + 0.5 for i in range(10)])))

    @staticmethod
    def test_mean():
        ts = SimulatedTimeSeries(iter(range(100)))
        assert ts.mean() == 10.5

    @staticmethod
    def test_std():
        ts = SimulatedTimeSeries(iter(range(100)))
        assert ts.std() == 5.9160797830996161
