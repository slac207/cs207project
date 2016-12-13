import logging
from flask import Flask, request, abort, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy, DeclarativeMeta
from json import JSONEncoder
from sqlalchemy import *
import sys
import json
import os
import inspect
from sqlalchemy.dialects.postgresql import INTEGER, REAL, CHAR

# from sqlalchemy.dialects.postgresql import \
#     ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
#     DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
#     INTERVAL, JSON, JSONB, MACADDR, NUMERIC, OID, REAL, SMALLINT, TEXT, \
#     TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
#     DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR
#import psycopg2
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0])
from TimeseriesDB.MessageFormatting import *
from socket import socket, AF_INET, SOCK_STREAM
from timeseries.StorageManager import FileStorageManager
from timeseries.SMTimeSeries import SMTimeSeries as ts


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
#host = 'localhost'
port = '5432'
db = 'ubuntu'
url = 'postgresql://{}:{}@{}:{}/{}'
url = url.format(user, password, host, port, db)
app.config['SQLALCHEMY_DATABASE_URI'] = url # 'sqlite:////tmp/tasks.db'
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)
#engine1 = create_engine('postgresql://ubuntu:cs207password@localhost:5432/ubuntu')
class MetaTable(db.Model):
    """
    "id" INTEGER PRIMARY KEY NOT NULL ,
    "MEAN" DECIMAL,
    "STD" DECIMAL,
    "BLARG" DECIMAL,
    "LEVEL" VARCHAR
    """
    metadata1=MetaData(db.engine)
    print(metadata1)
    __table__ = Table('metadata', metadata1,
        Column('id', INTEGER, primary_key=True),
        Column('mean', FLOAT),
        Column('std', FLOAT),
        Column('blarg', FLOAT),
        Column('level', CHAR(1)),
        autoload=True, autoload_with=db.engine

    )
    def __init__(self,**kw):
        for k,v in kw.items():
            setattr(self,k,v)
    def __repr__(self):
        return '<ID %r>' % self.id
    def to_dict(self):
        return dict(id=self.id, mean=self.mean, level=self.level, blarg=self.blarg,std=self.std)
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
    print(MetaTable.query.all())
    #return jsonify(dict(metadata=5))
    id = request.args.get('id_in', type=str)
    mean = request.args.get('mean_in', type=str)
    blarg = request.args.get('blarg_in', type=str)
    level = request.args.get('level_in', type=str)
    std = request.args.get('std_in', type=str)
    log.info('Getting all Tasks')
    # filters metadata in the postgres server and sends back all metatdata
    # that meet the condition

    for metadata_var in [id,mean,blarg,std]:
        if metadata_var:
            # split with -
            lower = float(metadata_var.split("-")[0])
            upper = float(metadata_var.split("-")[1])
            if mean:
                table = MetaTable.mean
            elif blarg:
                table = MetaTable.mean
            elif id:
                table = MetaTable.id
                lower = int(lower)
                upper = int(upper)
            elif std:
                table = MetaTable.std
            result=MetaTable.query.filter(and_(table>=lower,table<=upper))
            return jsonify(dict(metadata=result.all()))
    if level:
        all_options = level.split(",")
        result=MetaTable.query.filter(MetaTable.level.in_(all_options))
        return jsonify(dict(metadata=result.all()))
    return jsonify(dict(metadata=MetaTable.query.all()))

@app.route('/timeseries', methods=['POST'])
def add_timeseries():
    """
    QUERY 2:
    Adds a new timeseries into the database given a json which has a key
    for an id and a key for the timeseries, and returns the timeseries.
    """
    # Accesses the database server and adds a new timeseries
    # Adds new metadata to the postgres table
    # Returns the timeseries from the database server
    if not request.json or 'ts' not in request.json:
        print("not json!")
        abort(400)
    log.info('Adding Timeseries to Database')
    ts_dict = json.loads(request.json)
    print(ts_dict)
    sm = FileStorageManager(directory='./TimeseriesDB/FSM_filestorage')
    sm.reload_index()
    print("got sm")
    new_ts = ts(times=ts_dict['ts'][0],values=ts_dict['ts'][1])
    sm.store(t=new_ts,id=1000,overwrite=True)
    print("CHECKING",sm.get(1000))
    return request.json, 201
    #except:
    #    abort(400)
    #return jsonify({'op': 'OK', 'task': prod}), 201

@app.route('/timeseries/<int:timeseries_id>', methods=['GET'])
def get_from_id(timeseries_id):
    """
    QUERY 3:
    Sends back metadata and the timeseries itself in a JSON payload.
    """
    # For an id, get metadata for that id from postgres and timeseries for
    # that id from database server
    #print(MetaTable['metadata'])
    print("metadata")
    md_from_id = MetaTable.query.filter_by(id= timeseries_id).all()
    requestDict = {'op':'TSfromID','id':timeseries_id,'courtesy':'please'}
    response = connectDBServer(requestDict)
    tsResponse = response['ts']
    response['metadata'] = md_from_id
    log.info('Getting Timeseries from id')
    #return tsResponse
    return jsonify(response)

@app.route('/timeseries')
def filter_by_metadata():
    """
    QUERY 4
    Filter by metadata field and send back filtered metadata.
    """
    id = request.args.get('id', type=str)
    mean = request.args.get('mean', type=str)
    blarg = request.args.get('blarg', type=str)
    level = request.args.get('level', type=str)
    std = request.args.get('std', type=str)
    log.info('Getting all Tasks')
    # filters metadata in the postgres server and sends back all metatdata
    # that meet the condition
    for metadata_var in [id,mean,blarg,std]:
        if metadata_var:
            # split with -
            lower = str(metadata_var.split("-")[0])
            upper = str(metadata_var.split("-")[1])
            result=MetaTable.query.filter(metadata_var==DecimalInterval(lower,upper))
            return jsonify(dict(metadata=result.all()))
    if level:
        all_options = level.split(",")
        result=MetaTable.query.filter(MetaTable.level.in_(all_options))
        return jsonify(dict(metadata=result.all()))
    return jsonify(dict(metadata=Task.query.all()))

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
    return jsonify(response),201


@app.route('/simquery', methods=['POST'])
def get_simsearch_from_json():
    """
    QUERY 6:
    Takes a timeseries as an input in a JSON, carries out the query, and
    returns the appropriate ids as well.
    """
    # takes a timeseries as input in JSON. carries out query in database server.
    # returns the ids
    if not request.json or 'ts' not in request.json:
        print("not json!")
        abort(400)
    log.info('Getting IDs for most similar Timeseries from input id')
    ts_dict = json.loads(request.json)
    print(ts_dict)
    requestDict = {'op':'simsearch_ts','ts':ts_dict['ts'],'courtesy':'please'}
    response = connectDBServer(requestDict)
    #tsResponse = response['id']
    #return tsResponse
    return jsonify(response), 201

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
    app.run(host="0.0.0.0")
