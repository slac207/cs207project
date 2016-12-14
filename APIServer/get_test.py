import sys
import os
import json, requests
import unittest

ip_url = 'http://54.173.105.55'
url1 = ip_url+'/simquery?id=3&topn=2'
q = requests.get(url1)
print("Status",q.status_code,url1)
assert q.status_code<400
print(q.text)
