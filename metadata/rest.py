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


app = Flask(__name__)
app.json_encoder = ProductJSONEncoder

# This can all go into a config file but is here for reference.

user = 'ubuntu'
password = 'cs207password'
host = '172.31.56.49'
port = '5432'
db = 'ubuntu'
url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(user, password, host, port, db)
app.config['SQLALCHEMY_DATABASE_URI'] = url # 'sqlite:////tmp/tasks.db'
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

def connectDBServer(requestDict):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('localhost', 20000))
    s2 = serialize(json.dumps(requestDict))
    s.send(s2)
    msg = s.recv(8192) # May not be able to fit into one packet.
    print(msg)
    ds = Deserializer()
    ds.append(msg)
    ds.ready()
    response = ds.deserialize()
    print(response)
    return response

@app.route('/timeseries', methods=['GET'])
def get_all_metadata():
    """
    QUERY 1:
    Sends back a json with metadata from all the time series
    """
    # Need to access the postgres table and select all
    log.info('Getting all Metadata')
    print(Metadata.query.all())
    return jsonify(dict(metadata=Metadata.query.all()))

# @app.route('/timeseries', methods=['POST'])
# def create_task():
#     """
#     QUERY 2:
#     Adds a new timeseries into the database given a json which has a key
#     for an id and a key for the timeseries, and returns the timeseries.
#     """
#     # Accesses the database server and adds a new timeseries
#     # Adds new metadata to the postgres table
#     # Returns the timeseries from the database server
#     if not request.json or 'action' not in request.json:
#         abort(400)
#     log.info('Creating Task with action=%s', request.json['action'])
#     prod = Task(action=request.json['action'])
#     db.session.add(prod)
#     db.session.commit()
#     return jsonify({'op': 'OK', 'task': prod}), 201

@app.route('/timeseries/<int:ts_id>', methods=['GET'])
def get_from_id(ts_id):
    """
    QUERY 3:
    Sends back metadata and the timeseries itself in a JSON payload.
    """
    # For an id, get metadata for that id from postgres and timeseries for
    # that id from database server

    requestDict = {'op':'TSfromID','id':ts_id,'courtesy':'please'}
    response = connectDBServer(requestDict)
    tsResponse = response['ts']
    log.info('Getting Timeseries from id')
    #return tsResponse
    return jsonify(response)

# @app.route('/timeseries/', methods=['GET'])
# def get_all_tasks():
#     """
#     QUERY 4???
#     Sends back only metadata.
#     """
#     # kind = request.args.get('kind', '')
#     # if kind:
#     #     prods=Product.query.filter_by(kind=kind)
#     #     return jsonify(dict(products=prods.all()))
#     # else:
#     #     return jsonify(dict(products=Product.query.all()))
#     # filters metadata in the postgres server and sends back all metatdata
#     # that meet the condition
#     log.info('Getting all Tasks')
#     return jsonify(dict(tasks=Task.query.all()))

@app.route('/simquery/<int:ts_id>', methods=['GET'])
def get_simsearch_from_id(ts_id):

    """
    QUERY 5: Takes in an id querystring and uses it as an id into the database
    to find the timeseries that are similar, sending back the ids of the top N
    (default is 5 closest).
    """
    n_closest = request.args.get('topn', 5, type=int)

    # takes an id and connects to database server to find similar time series
    # send back the ids of the top 5.
    requestDict = {'op':'simsearch_id','id':ts_id,'n_closest':n_closest,'courtesy':'please'}
    print("REQUEST IS", requestDict)
    response = connectDBServer(requestDict)
    #tsResponse = response['id']
    log.info('Getting IDs for most similar Timeseries from input id')
    #return tsResponse
    return jsonify(response)


# @app.route('/simquery', methods=['POST'])
# def create_task():
#     """
#     QUERY 6:
#     Takes a timeseries as an input in a JSON, carries out the query, and
#     returns the appropriate ids as well.
#     """
#     # d2 = {'op':'simsearch_ts','ts':[list(ts_test.times()), list(ts_test.values())],'courtesy':'please'}
#     # takes a timeseries as input in JSON. carries out query in database server.
#     # returns the ids
#     if not request.json or 'action' not in request.json:
#         abort(400)
#     log.info('Creating Task with action=%s', request.json['action'])
#     prod = Task(action=request.json['action'])
#     db.session.add(prod)
#     db.session.commit()
#     return jsonify({'op': 'OK', 'task': prod}), 201

# @app.route('/tasks/<int:task_id>', methods=['GET'])
# def get_task_by_id(task_id):
#     task = Task.query.filter_by(task_id=task_id).first()
#     if task is None:
#         log.info('Failed to get Task with task_id=%s', task_id)
#         abort(404)
#     log.info('Getting Task with task_id=%s', task_id)
#     return jsonify({'task': task})
# @app.route('/tasks/<int:task_id>', methods=['PUT'])
# def update_task(task_id):
#     if not request.json or 'action' not in request.json:
#         log.info('Could not update. Invalid params')
#         abort(400)
#
#     task = Task.query.filter_by(task_id=task_id).first()
#     if task is None:
#         log.info('Could not find Task id=%s to update', task_id)
#         abort(404)
#
#     action = request.json['action']
#     log.info('Updating Task id=%s with action %s', task_id, action)
#     task.action = action
#     db.session.commit()
#     return jsonify({'op': 'OK', 'task': task}), 201

# @app.route('/tasks/<int:task_id>', methods=['DELETE'])
# def remove_task(task_id):
#     task = Task.query.filter_by(task_id=task_id).first()
#     if task is None:
#         abort(404)
#
#     log.info('Deleting Task with id=%s', task_id)
#     db.session.delete(task)
#     db.session.commit()
#     return jsonify({'op': 'OK'})

# @app.route('/tasks', methods=['DELETE'])
# def remove_all_tasks():
#     tasks = Task.query.all()
#     for task in tasks:
#         db.session.delete(task)
#
#     log.info('Deleted all Tasks!')
#     db.session.commit()
#     return jsonify({'op': 'OK'})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    #db.create_all()
    app.run(port=5001)
