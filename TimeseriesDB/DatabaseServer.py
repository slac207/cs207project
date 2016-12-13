from socketserver import BaseRequestHandler, ThreadingTCPServer
from TimeseriesDB.MessageFormatting import * 
from Similarity.find_most_similar import find_most_similiar, sanity_check
from TimeseriesDB.simsearch_init import initialize_simsearch_parameters

class DatabaseServer(BaseRequestHandler): 
    """Server that receives data and performs 3 operations based on the request:
    1. Finds the n most similiar timeseries to an existing timeseries 
    2. Finds the n most similiar timeseries to a new timeseries
    3. Returns the timeseries from its ID
    
    """
    def _get_data(self):
        pass
    #get it on the socket
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
            #depending on type of TSDPOp, call appropriate function
            if status is TSDBStatus.OK:
                if isinstance(tsdbop, TSDBOp_SimSearch_TS):
                    response = self._sim_with_ts(tsdbop)
                elif isinstance(tsdbop, TSDBOp_SimSearch_ID):
                    response = self._sim_with_id(tsdbop)
                elif isinstance(tsdbop, TSDBOp_TSfromID):
                    response = self._ts_with_id(tsdbop)
                else:
                    response = TSDBOp_Return(TSDBStatus.UNKNOWN_ERROR, tsdbop['op'])
            
            #convert back to bytes in order to send it back
            serial_response = serialize(response.to_json())
            self.request.send(serial_response)

    def _sim_with_ts(self,tsdbop):
        """Returns the n most similiar timeseries given a new ts"""
        id_list = find_most_similiar(tsdbop['ts'],tsdbop['n_closest'],self.server.data['vantage_points'],self.server.data['storage_manager'])
        result = TSDBOp_SimSearch_ID('simsearch_ts')
        result['id'] = id_list    
        return result

    def _sim_with_id(self,tsdbop):
        """Returns the n most similiar timeseries given a id of an existing ts"""
        id_list = find_most_similiar(tsdbop['id'],tsdbop['n_closest'],self.server.data['vantage_points'],self.server.data['storage_manager'])
        result = TSDBOp_SimSearch_ID('simsearch_id')
        result['id'] = id_list
        return result

    def _ts_with_id(self,tsdbop):
        """Returns a timeseries from the Storage Manager given the ID"""
        ts = self.server.data['storage_manager'].get(tsdbop['id'])
        ts_list = [list(ts.times()),list(ts.values())]
        result = TSDBOp_TSfromID('TSfromID') ##just changed this
        result['ts'] = ts_list
        return result

    def handle(self):
        """Handler for all incoming messages"""
        print('Got connection from', self.client_address)         
        while True:
            msg = self.request.recv(2048)
            self.data_received(msg)
            if not msg:
                break
            

if __name__ == '__main__':
    z = '-----------------------------------'
    ThreadingTCPServer.allow_reuse_address = True
    serv = ThreadingTCPServer(('', 20000), DatabaseServer) 
    serv.data = initialize_simsearch_parameters()
    serv.deserializer = Deserializer()
    print('Ready',z)
    serv.serve_forever()
