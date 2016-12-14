import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json, requests
from timeseries.StorageManager import FileStorageManager
from json import JSONEncoder
import unittest
from timeseries.ArrayTimeSeries import ArrayTimeSeries as ts
import numpy as np
from scipy.stats import norm


class Rest_API_tests(unittest.TestCase):
    def setUp(self):
        #r = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4')
        #self.ip_url = "http://"+r.text #'http://54.173.105.55'
        self.ip_url = "http://localhost:5000"

    def test_query2(self):
        """
        Test Query 2:
        Adds a new timeseries into the database given a json which has a key
        for an id and a key for the timeseries, and returns the timeseries.
        """
        t = np.arange(0.0, 1.0, 0.01)
        v = norm.pdf(t, 100, 100) + 1000*np.random.randn(100)
        ts_test = ts(t, v)
        data = {}
        data['ts'] = [list(ts_test.times()), list(ts_test.values())]
        data['id'] = 1000
        payload = json.dumps(data, ensure_ascii=False)
        print("Executing query2")
        url = self.ip_url+'/timeseries'
        r = requests.post(url, json=payload)
        print("Status",r.status_code,url)
        print(r.text[0:50])
        assert r.status_code<400

    def test_query6(self):
        """
        Test Query 6:
        Takes a timeseries as an input in a JSON, carries out the similarity query,
        and returns the appropriate ids to timeseries.
        """
        #payload = json.dumps(data, ensure_ascii=False)
        t = np.arange(0.0, 1.0, 0.01)
        v = norm.pdf(t, 100, 100) + 1000*np.random.randn(100)
        ts_test = ts(t, v)
        data = {}
        data['ts'] = [list(ts_test.times()), list(ts_test.values())]
        print("waiting for query6")
        url = self.ip_url+'/simquery'
        r = requests.post(url, json=data)
        print("Status",r.status_code,url)
        assert r.status_code<400
        print(r.text[0:50])

if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover
