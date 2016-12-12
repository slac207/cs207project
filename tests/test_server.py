from TimeseriesDB.MessageFormatting import *
import importlib
import unittest
from pytest import raises
import numpy as np
from TimeseriesDB.tsdb_error import *
from TimeseriesDB import DatabaseServer
from TimeseriesDB.MessageFormatting import * #Deserializer
from Similarity.find_most_similar import find_most_similiar, sanity_check
from TimeseriesDB.simsearch_init import initialize_simsearch_parameters
from socketserver import BaseRequestHandler, ThreadingTCPServer, TCPServer
from timeseries.ArrayTimeSeries import ArrayTimeSeries as ts
import threading
from socket import socket, AF_INET, SOCK_STREAM
import sys
from scipy.stats import norm
import multiprocessing


class Server_Tests(unittest.TestCase):
    
    def setUp(self):
        ThreadingTCPServer.allow_reuse_address = True
        self.port = 20000
        try:
            self.serv = ThreadingTCPServer(('', port), DatabaseServer)
        except:
            self.port += 1
            self.serv = ThreadingTCPServer(('', self.port), DatabaseServer)
                
        self.serv.data = initialize_simsearch_parameters()
        self.serv.deserializer = Deserializer()        
        self.serv_thread = threading.Thread(target=self.serv.serve_forever)
        self.serv_thread.setDaemon(True)
        self.serv_thread.start()   
        self.serv_thread2 = threading.Thread(target=self.serv.serve_forever)
        self.serv_thread2.setDaemon(True)
        self.serv_thread2.start()           
        
    def tearDown(self):
        self.serv.socket.close()
        self.serv.server_close()

        
    def test_serializer_deserializer(self):
        #test the serializing
        msg = {'op':'TSfromID','id':12,'courtesy':'please'}
        serialized = serialize(json.dumps(msg))
        assert isinstance(serialized, bytes) #check that bytes are passed back
        
        ds = Deserializer()
        ds.append(serialized)
        ds.ready()
        response = ds.deserialize()
        #check that serializing and then deserializing leaves us with the original message  
        assert response == msg   
        
    def test_queries(self):
        s = socket(AF_INET, SOCK_STREAM)        
        s.connect(('localhost', self.port))
        
        #query for similarity search with an ID
        d2 = {'op':'simsearch_id','id':12,'n_closest':2,'courtesy':'please'}
        s2 = serialize(json.dumps(d2))        
        s.send(s2)
        msg = s.recv(8192)
        ds = Deserializer()
        ds.append(msg)
        ds.ready()
        response = ds.deserialize()  
        assert len(response['id']) == 2 #returned back two ids
        assert type(response['id'][0]) == type(response['id'][1]) == int 
        
        #query for similarity search with a new timeseries
        t = np.arange(0.0, 1.0, 0.01)
        v = norm.pdf(t, 100, 100) + 1000*np.random.randn(100)
        ts_test = ts(t, v)

        d2 = {'op':'simsearch_ts','ts':[list(ts_test.times()), list(ts_test.values())],'courtesy':'please'}
        s2 = serialize(json.dumps(d2))        
        s.send(s2)
        msg = s.recv(8192)
        ds = Deserializer()
        ds.append(msg)
        ds.ready()
        response = ds.deserialize()  
        assert len(response['id']) == 5 #returned back five ids
        assert type(response['id'][0]) == type(response['id'][1]) == int         
        
        #query for timeseries based on id
        d2 = {'op':'TSfromID','id':12,'courtesy':'please'}
        s2 = serialize(json.dumps(d2))        
        s.send(s2)
        msg = s.recv(8192)
        ds = Deserializer()
        ds.append(msg)
        ds.ready()
        response = ds.deserialize() 
        assert len(response['ts']) == 2 #returned back times and values
        
        #nonpolite query test, passes back a none operation
        d2_impolite = {'op':'simsearch_id','id':12,'n_closest':2}
        s2_impolite = serialize(json.dumps(d2_impolite))  
        s.send(s2_impolite)              
        msg_impolite = s.recv(8192)  
        ds = Deserializer()
        ds.append(msg_impolite)
        ds.ready()
        response_impolite = ds.deserialize()  
        assert 'payload' in response_impolite
            
        s.close()
        
    def test_multiple_queries(self):
        def query_1():
            #function to compute simsearch
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(('localhost', self.port))
            d2 = {'op':'simsearch_id','id':12,'n_closest':2,'courtesy':'please'}
            s2 = serialize(json.dumps(d2))    
            s.send(s2)
            msg = s.recv(8192)
            ds = Deserializer()
            ds.append(msg)
            ds.ready()
            response = ds.deserialize()
            assert type(response['id'][0]) == type(response['id'][1]) == int 
            s.close()
            return
        
        def query_2():
            #function to return timeseries from id
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(('localhost', self.port))
            d2 = {'op':'TSfromID','id':12,'courtesy':'please'}
            s2 = serialize(json.dumps(d2)) 
            s.send(s2)
            msg = s.recv(8192)
            ds = Deserializer()
            ds.append(msg)
            ds.ready()
            response = ds.deserialize()
            assert len(response['ts']) == 2 
            s.close()
            return
            
        self.p = multiprocessing.Process(target=query_1) 
        self.p2 = multiprocessing.Process(target=query_2) 
        self.p.start()
        self.p2.start() 
        self.p.join()
        self.p2.join()
          
        
if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover
