from socketserver import BaseRequestHandler, ThreadingTCPServer
from server import * #Deserializer
sys.path.insert(0,os.path.split(os.path.split(os.path.realpath(inspect.stack()[0][1]))[0])[0]) 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0,currentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0,parentdir+'/cs207project/timeseries/Similarity/VantagePointDatabases')
from Similarity.find_most_similar import find_most_similiar, sanity_check
from simsearch_init import initialize_simsearch_parameters

class DatabaseServer(BaseRequestHandler): 
    
    
    # def __init__(self):
        # # generate TS, pick VPs. 
        # self.deserializer = Deserializer()
        # pass
    
    # def __init__(self,*args):
        # super(self).__init__(*args)
        # print('test text added to init')
    
    def _get_data(self):
        pass
        #return data
    
    #get it on the socket, then (perhaps in a thread)
    def data_received(self, data):
        self.server.deserializer.append(data)
        if self.server.deserializer.ready():
            msg = self.server.deserializer.deserialize()
            status = TSDBStatus.OK  # until proven otherwise.
            response = TSDBOp_Return(status, None)  # until proven otherwise.
            try:
                tsdbop = TSDBOp.from_json(msg)
            except TypeError as e:
                status = TSDBStatus.INVALID_OPERATION
                response = TSDBOp_Return(status, None)
            if status is TSDBStatus.OK:
                if isinstance(tsdbop, TSDBOp_SimSearch_TS):
                    response = self._sim_with_ts(tsdbop)
                elif isinstance(tsdbop, TSDBOp_SimSearch_ID):
                    response = self._sim_with_id(tsdbop)
                elif isinstance(tsdbop, TSDBOp_TSfromID):
                    response = self._ts_with_id(tsdbop)
                else:
                    response = TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, tsdbop['op'])
            serial_response = serialize(json.dumps(response.to_json()))
            self.request.send(serial_response)
            
    def _sim_with_ts(self,tsdbop):
        id_list = find_most_similiar(tsdbop['ts'],5,self.server.data['vantage_points'],self.server.data['storage_manager'])
        result = TSDBOp_SimSearch_ID('simsearch_ts')
        result['id'] = id_list        
        print('sim_with_ts')
        return result
        
    def _sim_with_id(self,tsdbop):
        print('loc 1')
        #id_list = find_most_similiar(tsdbop['id'],tsdbop['nclosest'],self.server.data['vantage_points'],self.server.data['storage_manager'])
        id_list = find_most_similiar(tsdbop['id'],5,self.server.data['vantage_points'],self.server.data['storage_manager'])
        print('loc 2')
        result = TSDBOp_SimSearch_ID('simsearch_id')
        result['id'] = id_list
        print('sim_with_id')
        return result
        
    def _ts_with_id(self,tsdbop):
        ts = self.server.data['storage_manager'].get(tsdbop['id'])
        ts_list = [list(ts.times()),list(ts.values())]
        result = TSDBOp_SimSearch_TS('TSfromID')
        result['ts'] = ts_list
        
        print('ts_with_id')
        print(result)
        return result
        
    def handle(self):
        print('Got connection from', self.client_address) 
        #print(self.server.data)
        
        while True:
            msg = self.request.recv(2048)
            self.data_received(msg)
            if not msg:
                break
            #self.request.send(msg)
            
if __name__ == '__main__':
    z = '-----------------------------------'
    serv = ThreadingTCPServer(('', 20000), DatabaseServer) 
    print('location a',z)
    serv.data = initialize_simsearch_parameters()
    print('location b',z)
    serv.deserializer = Deserializer()
    print('location c',z)
    serv.serve_forever()
    
