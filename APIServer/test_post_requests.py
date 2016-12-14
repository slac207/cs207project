import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json, requests
from timeseries.StorageManager import FileStorageManager
from timeseries.SMTimeSeries import SMTimeSeries as ts
from json import JSONEncoder


class Rest_API_tests(unittest.TestCase):
    def setUp(self):
        r = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4')
        self.ip_url = r.text #'http://54.173.105.55'

    def test_query2(self):
        """
        Test Query 2:
        Adds a new timeseries into the database given a json which has a key
        for an id and a key for the timeseries, and returns the timeseries.
        """
        sm = FileStorageManager(directory='./TimeseriesDB/FSM_filestorage')
        sm.reload_index()
        new_ts =ts.from_db(sm,100)
        data = {}
        data['ts'] = [list(new_ts.times()), list(new_ts.values())]
        payload = json.dumps(data, ensure_ascii=False)
        url = self.ip_url+'/simquery'
        r = requests.post(url, json=payload)
        print("Status",r.status_code,url)
        print(r.text[0:50])
        #assert r.status_code<400

    def test_query6(self):
        """
        Test Query 6:
        Takes a timeseries as an input in a JSON, carries out the similarity query,
        and returns the appropriate ids to timeseries.
        """
        sm = FileStorageManager(directory='./TimeseriesDB/FSM_filestorage')
        sm.reload_index()
        new_ts =ts.from_db(sm,100)
        data = {}
        data['ts'] = [list(new_ts.times()), list(new_ts.values())]
        payload = json.dumps(data, ensure_ascii=False)
        url = self.ip_url+'/simquery'
        r = requests.post(url, json=payload)
        print("Status",r.status_code,url)
        #assert r.status_code<400
        print(r.text[0:50])
