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

# Create the app and set it's json encoder
app = Flask(__name__)
app.json_encoder = ProductJSONEncoder

# Config information for the postgres database
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


class MetaTable(db.Model):
    """
    Reflect the "metadata" table from postgres.
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
        "Set all attributes for each column"
        for k,v in kw.items():
            setattr(self,k,v)
    def __repr__(self):
        return '<ID %r>' % self.id
    def to_dict(self):
        "Define a dict that includes all metadata fields"
        return dict(id=self.id, mean=self.mean, level=self.level, blarg=self.blarg,std=self.std)

def connectDBServer(requestDict):
    "Connect to the custom similarity server. Send and receive a request"
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
    QUERY 1 and 4:
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
        # split with ","
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
    Connects to both the metadata Postgres table and the similarity database.
    Sends back metadata and the timeseries itself in a JSON payload.
    """
    # For an id, get metadata for that id from postgres and timeseries for
    # that id from database server
    md_from_id = MetaTable.query.filter_by(id= timeseries_id).all()
    requestDict = {'op':'TSfromID','id':timeseries_id,'courtesy':'please'}
    response = connectDBServer(requestDict)
    tsResponse = response['ts']
    response['metadata'] = md_from_id
    log.info('Getting Timeseries from id')
    #return tsResponse
    return jsonify(response)

@app.route('/simquery/<int:ts_id>', methods=['GET'])
def get_simsearch_from_id(ts_id):

    """
    QUERY 5: Takes in an id querystring and uses it as an id into the
    similarity database to find the timeseries that are similar.
    Sends back the ids of the top N which is passed in as an argument
    (default is 5 closest).
    """
    n_closest = request.args.get('topn', 5, type=int)
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
    Takes a timeseries as an input in a JSON, carries out the similarity query,
    and returns the appropriate ids to timeseries.
    """
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

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0")
