import logging
from flask import Flask, request, abort, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy, DeclarativeMeta
from json import JSONEncoder
import sys
import json
import os
import inspect
#import psycopg2
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0])
from TimeseriesDB.MessageFormatting import *
from socket import socket, AF_INET, SOCK_STREAM

log = logging.getLogger(__name__)

class ProductJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            return obj.to_dict()
        return super(ProductJSONEncoder, self).default(obj)

# This can all go into a config file but is here for reference.

user = 'ubuntu'
password = 'cs207password'
#host = '172.31.56.49'
host = 'localhost'
port = '5432'
db = 'ubuntu'
url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(user, password, host, port, db)
#app.config['SQLALCHEMY_DATABASE_URI'] = url # 'sqlite:////tmp/tasks.db'
db = SQLAlchemy(app)

class Metadata(db.Model):
    """
    "id" INTEGER PRIMARY KEY NOT NULL ,
    "MEAN" DECIMAL,
    "STD" DECIMAL,
    "BLARG" DECIMAL,
    "LEVEL" VARCHAR
    """
    __tablename__ = 'metadata'

    ts_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mean = db.Column(db.Float(80))
    std = db.Column(db.Float(80))
    blarg = db.Column(db.Float(80))
    level = db.Column(db.String(80))

    def __init__(self, ts_id, mean, std, blarg, level):
        self.ts_id = ts_id
        self.mean = mean
        self.std = std
        self.blarg = blarg
        self.level = level

    def __repr__(self):
        return '<User %r>' % self.ts_id

    def to_dict(self):
        return dict(action=self.action, ts_id=self.ts_id)

def get_all_metadata():
    """
    QUERY 1:
    Sends back a json with metadata from all the time series
    """
    # Need to access the postgres table and select all
    log.info('Getting all Metadata')
    print(Metadata.query.all())
    return jsonify(dict(metadata=Metadata.query.all()))

db.create_all()
