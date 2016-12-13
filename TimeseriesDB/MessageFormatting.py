import json
import enum
import sys, os, inspect
import timeseries as ts
from TimeseriesDB.tsdb_error import *


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
        """Appends data to the buf"""
        self.buf += data
        self._maybe_set_length()

    def _maybe_set_length(self):
        """Extract the length of the buffer"""
        if self.buflen < 0 and len(self.buf) >= LENGTH_FIELD_LENGTH:
            self.buflen = int.from_bytes(self.buf[0:LENGTH_FIELD_LENGTH], byteorder="little")

    def ready(self):
        """If we read in the full message, can proceed"""
        return (self.buflen > 0 and len(self.buf) >=    self.buflen)

    def deserialize(self):
        """Turns bytes into json object"""
        json_str = self.buf[LENGTH_FIELD_LENGTH:self.buflen].decode()
        self.buf = self.buf[(self.buflen):]
        self.buflen = -1
        # There may be more data in the buffer already, so preserve it
        self._maybe_set_length()
        try:
            #Note how now everything is assumed to be an OrderedDict
            obj = json.loads(json_str)
            return obj
        #raise a Decode error if invalid JSON object
        except json.JSONDecodeError: 
            print('Invalid JSON object received:\n'+str(json_str))
            return None
        
    

class TSDBOp(dict):
    """Base Class for the different TSDB operations that inherits from a dictionary
    and requires a dictionary 'op' key with a valid operation in typemap"""
    
    def __init__(self, op):
        self['op'] = op

    def to_json(self, obj=None):
        """Converts a TSDBOp objects into a JSON object """
        if obj is None:
            obj = self
        try:
            json_dict = json.dumps(obj)
            return json_dict
        except:
            raise TypeError('Cannot convert object to JSON: '+str(obj))        

    @classmethod
    def from_json(cls, json_dict):
        """Converts a JSON object into a TSDBOp object"""
        
        #json_dict must contain key 'op'
        if 'op' not in json_dict: 
            raise TypeError('Not a TSDB Operation: '+str(json_dict))
        #can only support ops in our typemap
        if json_dict['op'] not in typemap: 
            raise TypeError('Invalid TSDB Operation: '+str(json_dict['op']))
        return typemap[json_dict['op']].from_json(json_dict)


class TSDBOp_SimSearch_TS(TSDBOp):
    """Class for performing similarity searches with a new timeseries"""    
    def __init__(self, ts, **kwargs):
        super().__init__('simsearch_ts')
        self['ts'] = ts
        for k,v in kwargs.items():
            self[k]=v

    @classmethod
    def from_json(cls, json_dict):
        """Converts a JSON object into a TSDBOp_SimSearch_TS object"""
        
        if 'n_closest' not in json_dict:
            json_dict['n_closest'] = 5
        if ('courtesy' not in json_dict) or (json_dict['courtesy'].lower()!='please'):
            print('Impolite TSDB Operation: please include the courtesy "please" (key="courtesy",value="please"')
            raise TypeError('Impolite TSDB Operation: please include the courtesy "please" (key="courtesy",value="please"')
        return cls(ts.ArrayTimeSeries(*(json_dict['ts'])),n_closest=json_dict['n_closest'])

class TSDBOp_SimSearch_ID(TSDBOp):
    """Class for performing similarity searches with an existing timeseries"""  
    def __init__(self, idee, **kwargs):
        super().__init__('simsearch_id')
        self['id'] = idee
        for k,v in kwargs.items():
            self[k]=v
        
    @classmethod
    def from_json(cls, json_dict):
        """Converts a JSON object into a TSDBOp_Simsearch_ID object"""
        
        if 'n_closest' not in json_dict:
            json_dict['n_closest'] = 5
        if ('courtesy' not in json_dict) or (json_dict['courtesy'].lower()!='please'):
            print('Impolite TSDB Operation: please include the courtesy "please" (key="courtesy",value="please"')
            raise TypeError('Impolite TSDB Operation: please include the courtesy "please" (key="courtesy",value="please"')
        return cls(json_dict['id'],n_closest=json_dict['n_closest'])

class TSDBOp_TSfromID(TSDBOp):
    """Class for fetching timeseries based on ID"""  
    def __init__(self, idee):
        super().__init__('TSfromID')
        self['id'] = idee

    @classmethod
    def from_json(cls, json_dict):
        """Converts a JSON object into a TSDBOp_TSfromID object"""
         
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

