import json
import enum
import sys, os, inspect
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]) 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir+'/timeseries')
import ArrayTimeSeries as ts
# from .tsdb_error import *


LENGTH_FIELD_LENGTH = 4

def serialize(json_obj):
    '''Turn a JSON object into bytes suitable for writing out to the network.
    Includes a fixed-width length field to simplify reconstruction on the other
    end of the wire.'''
    
    json_bytes = json_obj.encode()
    json_bytes_len = len(json_bytes)
    header = int.to_bytes(json_bytes_len+LENGTH_FIELD_LENGTH,LENGTH_FIELD_LENGTH,'little')
    msg = header+json_bytes
    return msg    


class Deserializer(object):
    '''A buffering and bytes-to-json engine.
    Data can be received in arbitrary chunks of bytes, and we need a way to
    reconstruct variable-length JSON objects from that interface. This class
    buffers up bytes until it can detect that it has a full JSON object (via
    a length field pulled off the wire). To use this, shove bytes in with the
    append() function and call ready() to check if we've reconstructed a JSON
    object. If True, then call deserialize to return it. That object will be
    removed from this buffer after it is returned.'''

    def __init__(self):
        self.buf = b''
        self.buflen = -1

    def append(self, data):
        self.buf += data
        self._maybe_set_length()

    def _maybe_set_length(self):
        if self.buflen < 0 and len(self.buf) >= LENGTH_FIELD_LENGTH:
            self.buflen = int.from_bytes(self.buf[0:LENGTH_FIELD_LENGTH], byteorder="little")

    def ready(self):
        return (self.buflen > 0 and len(self.buf) >=    self.buflen)

    def deserialize(self):
        json_str = self.buf[LENGTH_FIELD_LENGTH:self.buflen].decode()
        self.buf = self.buf[(self.buflen):]
        self.buflen = -1
        # There may be more data in the buffer already, so preserve it
        self._maybe_set_length()
        try:
            #Note how now everything is assumed to be an OrderedDict
            obj = json.loads(json_str)
            #print("OBJ", obj)
            return obj
        except json.JSONDecodeError:
            print('Invalid JSON object received:\n'+str(json_str))
            return None
            
            

class TSDBError(Exception):
    pass

class TSDBOperationError(Exception):
    pass

class TSDBConnectionError(Exception):
    pass

class TSDBStatus(enum.IntEnum):
    OK = 0
    UNKNOWN_ERROR = 1
    INVALID_OPERATION = 2
    INVALID_KEY = 3
    INVALID_COMPONENT = 4
    PYPE_ERROR = 5

    @staticmethod
    def encoded_length():
        return 3

    def encode(self):
        return str.encode('{:3d}'.format(self.value))

    @classmethod
    def from_bytes(cls, data):
        return cls(int(data.decode()))
    

# Interface classes for TSDB network operations.
# These are a little clunky (extensibility is meh), but it does provide strong
# typing for TSDB ops and a straightforward mechanism for conversion to/from
# JSON objects.


class TSDBOp(dict):
    def __init__(self, op):
        self['op'] = op

    def to_json(self, obj=None):
        # json.dumps seems to be easier to work with and automatically handles
        # hierarchical data structures.
        if obj is None:
            obj = self
        try:
            json_dict = json.dumps(obj)
            return json_dict
        except:
            raise TypeError('Cannot convert object to JSON: '+str(obj))        

    @classmethod
    def from_json(cls, json_dict):
        if 'op' not in json_dict:
            raise TypeError('Not a TSDB Operation: '+str(json_dict))
        if json_dict['op'] not in typemap:
            raise TypeError('Invalid TSDB Operation: '+str(json_dict['op']))
        return typemap[json_dict['op']].from_json(json_dict)


class TSDBOp_SimSearch_TS(TSDBOp):
    def __init__(self, ts, **kwargs):
        super().__init__('simsearch_ts')
        self['ts'] = ts
        for k,v in kwargs.items():
            self[k]=v

    @classmethod
    def from_json(cls, json_dict):
        if 'n_closest' not in json_dict:
            json_dict['n_closest'] = 5
        if ('courtesy' not in json_dict) or (json_dict['courtesy'].lower()!='please'):
            print('Impolite TSDB Operation: please include the courtesy "please" (key="courtesy",value="please"')
            raise TypeError('Impolite TSDB Operation: please include the courtesy "please" (key="courtesy",value="please"')
        return cls(ts.ArrayTimeSeries(*(json_dict['ts'])),n_closest=json_dict['n_closest'])

class TSDBOp_SimSearch_ID(TSDBOp):
    def __init__(self, idee, **kwargs):
        super().__init__('simsearch_id')
        self['id'] = idee
        for k,v in kwargs.items():
            self[k]=v
        
    @classmethod
    def from_json(cls, json_dict):
        if 'n_closest' not in json_dict:
            json_dict['n_closest'] = 5
        if ('courtesy' not in json_dict) or (json_dict['courtesy'].lower()!='please'):
            print('Impolite TSDB Operation: please include the courtesy "please" (key="courtesy",value="please"')
            raise TypeError('Impolite TSDB Operation: please include the courtesy "please" (key="courtesy",value="please"')
        return cls(json_dict['id'],n_closest=json_dict['n_closest'])

class TSDBOp_TSfromID(TSDBOp):
    def __init__(self, idee):
        super().__init__('TSfromID')
        self['id'] = idee

    @classmethod
    def from_json(cls, json_dict):
        if ('courtesy' not in json_dict) or (json_dict['courtesy'].lower()!='please'):
            print('Impolite TSDB Operation: please include the courtesy "please" (key="courtesy",value="please"')
            raise TypeError('Impolite TSDB Operation: please include the courtesy "please" (key="courtesy",value="please"')
        return cls(json_dict['id'])

class TSDBOp_Return(TSDBOp):

    def __init__(self, status, op, payload=None):
        super().__init__(op)
        self['status'], self['payload'] = status, payload

    @classmethod
    def from_json(cls, json_dict):  #should not be used, this is to return to client
        return cls(json_dict['status'], json_dict['payload'])


# This simplifies reconstructing TSDBOp instances from network data.
typemap = {
  'simsearch_ts': TSDBOp_SimSearch_TS,
  'simsearch_id': TSDBOp_SimSearch_ID,
  'TSfromID': TSDBOp_TSfromID
}

