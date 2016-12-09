import numpy as np
import pandas as pd
import time
from sqlite3 import dbapi2 as sq3
import os
import pickle
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from timeseries.StorageManager import FileStorageManager
from SMTimeSeries import SMTimeSeries as ts

sm = FileStorageManager()
level_options = ['A','B','C','D','E','F']
metadata = np.zeros((10,5)).astype(str)
for i in range(15,20):
    ts1 = ts.from_db(sm,i)
    ts_id = i
    ts_std = ts.std()
    ts_mean = ts.mean()
    blarg = np.random.uniform()
    level = level_options[np.random.randint(0,high=6)]
    metadata[i,:] = np.array([ts_id, ts_mean, ts_std, blarg, level])
all_metadata = pd.DataFrame(metadata, columns=['id', 'mean', 'std', 'blarg', 'level'])
ourschema="""
DROP TABLE IF EXISTS "metadata";
DROP TABLE IF EXISTS "contributors";
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
all_metadata.to_sql("metadata", db, if_exists="append", index=False)

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
