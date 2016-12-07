from socketserver import BaseRequestHandler, ThreadingTCPServer
from server import * #Deserializer
from Similarity.find_most_similar import find_most_similiar

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

                serial_response = serialize(TSDBOp.to_json(response))
                self.request.send(serial_response)
            
    def _sim_with_ts(self,tsdbop):
        print('sim_with_ts')
        return 'success!'
        
    def _sim_with_id(self,tsdbop):
        id_list = find_most_similiar(tsdbop['id'],tsdbop['nclosest'],self.server.data['vantage_points'],self.server.data['storage_manager'])
        result = TSDBOp_SimSearch_ID('simsearch_id')
        result['id'] = id_list
        print('sim_with_id')
        return result
        
    def _ts_with_id(self,tsdbop):
        print('ts_with_id')
        return 'success!'
        
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
    serv = ThreadingTCPServer(('', 20000), DatabaseServer) 
    serv.data = {'vantage_points':'VP','storage_manager':'SM'}
    serv.deserializer = Deserializer()
    serv.serve_forever()
    
