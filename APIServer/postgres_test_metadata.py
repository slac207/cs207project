import psycopg2
import numpy as np
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import *
import pandas as pd
import sys
import os
import inspect
#sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0])
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from timeseries.StorageManager import FileStorageManager
from timeseries.SMTimeSeries import SMTimeSeries as ts
from timeseries.Similarity import distances

sm = FileStorageManager(directory='./TimeseriesDB/FSM_filestorage')
sm.reload_index()
print("ALL INDICES", sm._index)
level_options = ['A','B','C','D','E','F']
metadata = np.zeros((1000,5)).astype(str)
for i in range(1000):
    ts1 = ts.from_db(sm,i)
    ts_id = i
    ts_std = ts1.std()
    ts_mean = ts1.mean()
    blarg = np.random.uniform()
    level = level_options[np.random.randint(0,high=6)]
    metadata[i,:] = np.array([ts_id, ts_mean, ts_std, blarg, level])
all_metadata = pd.DataFrame(metadata, columns=['id', 'mean', 'std', 'blarg', 'level'])

all_metadata['id'] = all_metadata['id'].astype(int)
all_metadata['std'] = all_metadata['std'].astype(float)
all_metadata['blarg'] = all_metadata['blarg'].astype(float)
all_metadata['level'] = all_metadata['level'].astype(str)
all_metadata['mean'] = all_metadata['mean'].astype(float)

print(all_metadata)
connection = None
# open a connection to our database
user = 'ubuntu'
password = 'cs207password'
host = 'localhost'
#host = '172.31.56.49' # try 127.0.0.0
port = '5432'
db = 'ubuntu'
url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(user, password, host, port, db)
connection = psycopg2.connect("dbname=ubuntu user=ubuntu password=cs207password")
engine = create_engine('postgresql://ubuntu:cs207password@localhost:5432/ubuntu')
cursor = connection.cursor()


ourschema="""
DROP TABLE IF EXISTS "metadata";
CREATE TABLE metadata (
    id INTEGER PRIMARY KEY NOT NULL,
    MEAN REAL NOT NULL,
    STD REAL NOT NULL,
    BLARG REAL NOT NULL,
    LEVEL CHAR(1) NOT NULL);"""
cursor.execute(ourschema)
connection.commit()
print("executed")
# insert data into the random_numbers table
#for n in range(10000):
#	cursor.execute("INSERT INTO random_numbers(rn) VALUES (%s)", np.random.rand(1))
all_metadata.to_sql("metadata", engine, if_exists="replace", index=False)
print("added to psql")

# commit the transaction - ensure that what was inserted persists in the database
# query the random_numbers table and obtain data as Python objects
cursor.execute("SELECT * FROM metadata;")

# show the floats
#print("POSTGRES DATA")
for record in cursor:
	print (record)
# close and cleanup the db connection
cursor.close()
connection.close()
