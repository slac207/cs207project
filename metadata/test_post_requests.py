# test posts
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json, requests
from timeseries.StorageManager import FileStorageManager
from timeseries.SMTimeSeries import SMTimeSeries as ts
from json import JSONEncoder
sm = FileStorageManager(directory='./TimeseriesDB/FSM_filestorage')
sm.reload_index()
url = 'http://0.0.0.0:5000/simquery'
new_ts =ts.from_db(sm,100)
data = {}
data['ts'] = [list(new_ts.times()), list(new_ts.values())]
#data['times'] = "4"
#data['values'] = "23"
payload = json.dumps(data, ensure_ascii=False)

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True
r = requests.post(url, json=payload)
print(r)
