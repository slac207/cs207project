from socketserver import BaseRequestHandler, ThreadingTCPServer
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
            self.deserializer.append(data)
            if self.deserializer.ready():
                msg = self.deserializer.deserialize()
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

                serial_response = serialize(response.to_json())
                self.request.send(serial_response)
            
    def _sim_with_ts(self,tsdbop):
        pass
        
    def _sim_with_id(self,tsdbop):
        pass
        
    def _ts_sith_id(self,tsdbop):
        pass
        
        
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
    serv.data = ['input data goes here']
    serv.serve_forever()
    
