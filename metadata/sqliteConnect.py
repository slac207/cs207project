import numpy as np
import pandas as pd
from sqlite3 import dbapi2 as sq3
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0])
from timeseries.StorageManager import FileStorageManager
from SMTimeSeries import SMTimeSeries as ts
from timeseries.Similarity import distances
import numpy as np
from StorageManager import FileStorageManager
import os

sm = FileStorageManager(directory='./FSM_filestorage')
sm.reload_index()
#script to generate and store 1000 timeseries
#for i in range(50):
#    x = distances.tsmaker(100, 100, 1000)
#    sm.store(i, x, overwrite=True)
print(sm._dir)
print(sm)
print(os.getcwd())
#sm2=FileStorageManager()
level_options = ['A','B','C','D','E','F']
metadata = np.zeros((1000,5)).astype(str)
for i in range(50):
    ts1 = ts.from_db(sm,i)
    #ts = sm.get(id=i)
    ts_id = i
    ts_std = ts1.std()
    ts_mean = ts1.mean()
    blarg = np.random.uniform()
    level = level_options[np.random.randint(0,high=6)]
    metadata[i,:] = np.array([ts_id, ts_mean, ts_std, blarg, level])
all_metadata = pd.DataFrame(metadata, columns=['id', 'mean', 'std', 'blarg', 'level'])
ourschema="""
DROP TABLE IF EXISTS "metadata";
CREATE TABLE "metadata" (
    "id" INTEGER PRIMARY KEY NOT NULL ,
    "MEAN" DECIMAL,
    "STD" DECIMAL,
    "BLARG" DECIMAL,
    "LEVEL" VARCHAR
);

"""

PATHSTART="."
def get_db(dbfile):
    sqlite_db = sq3.connect(os.path.join(PATHSTART, dbfile))
    return sqlite_db

def init_db(dbfile, schema):
    """Creates the database tables."""
    db = get_db(dbfile)
    db.cursor().executescript(schema)
    db.commit()
    return db


print(all_metadata.head())
db=init_db("/tmp/metadata_test.db", ourschema)
all_metadata.to_sql("metadata", db, if_exists="replace", index=False)

selection="""
SELECT * FROM metadata;
"""
c=db.cursor().execute(selection)
print(c.fetchall())

rem="""
DELETE FROM metadata;
"""
c=db.cursor().execute(rem)
db.commit()
os.remove('/tmp/metadata_test.db')
