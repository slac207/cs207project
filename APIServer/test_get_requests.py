# test posts
import sys
import os
import json, requests
import unittest
class Rest_API_tests(unittest.TestCase):
    def setUp(self):
        self.ip_url = 'http://54.173.105.55'

    def test_query1(self):
        """
        Test Query 1:
        Sends back a json with metadata from all the time series
        """
        url = self.ip_url+'/timeseries'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400

    def test_query3(self):
        """
        Test Query 3:
        Connects to both the metadata Postgres table and the similarity database.
        Sends back metadata and the timeseries itself in a JSON payload.
        """
        url = self.ip_url+'/timeseries/12'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400
        url = self.ip_url+'/timeseries/-12'
        r = requests.get(url)
        print("Status",r.status_code,url)
        #assert r.status_code==400
        url = self.ip_url+'/timeseries/54353'
        r = requests.get(url)
        print("Status",r.status_code,url)
        #assert r.status_code==400
        url = self.ip_url+'/timeseries/54.3'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code==404

    def test_query4(self):
        """
        Test Query 4:
        Supports timeseries?mean_in=1.5,1.53 type queries sends back only metadata.
        For continuous variables only range queries are supported with
        string mean_in=1.5,1.53 whereas for discrete variables(level here)
        queries such as level_in=A,B,C or level=A are supported.
        Only one query at a time is supported.
        """
        url = self.ip_url+'/timeseries?mean_in=30,50'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400
        url = self.ip_url+'/timeseries?std_in=3,5'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400
        url = self.ip_url+'/timeseries?level_in=B,C'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400
        url = self.ip_url+'/timeseries?level_in=D'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400
        url = self.ip_url+'/timeseries?blarg_in=3,5'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400
        url = self.ip_url+'/timeseries?id_in=1,5'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400
        url = self.ip_url+'/timeseries?mean_in=-100,-45'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400
        url = self.ip_url+'/timeseries?mean_in=-100.4,-45.2'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400
        url = self.ip_url+'/timeseries?mean_in=-100.4--45.2'
        r = requests.get(url)
        print("Status",r.status_code,url)
        #assert r.status_code==400

    def test_query5(self):
        """
        Test Query 5:
         Takes in an id querystring and uses it as an id into the
        similarity database to find the timeseries that are similar.
        Sends back the ids of the top N which is passed in as an argument
        (default is 5 closest).
        """
        url = self.ip_url+'/simquery?id=5&?topn=8'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400
        url = self.ip_url+'/simquery?id=20&topn=200'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400
        print(r.text)
        assert "null" in r.text
        url = self.ip_url+'/simquery?id=5'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code<400
        url = self.ip_url+'/simquery?id=-10'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code==400
        url = self.ip_url+'/simquery?id=2000'
        r = requests.get(url)
        print("Status",r.status_code,url)
        assert r.status_code==400


if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover
