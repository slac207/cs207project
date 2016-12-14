# TimeseriesDB Module Documentation

## Purpose
This module contains the methods for creating a multi-threaded socket server to recieve and respond to 3 different types of queries:
1. Find the n most similiar timeseries to timeseries already in our database 
2. Find the n most similiar timeseries to a new timeseries provided
3. Given the id of a timeseries, return it from the FileStorageManager 

We use a ThreadingTCPServer, and use the [similarity module](https://github.com/slac207/cs207project/tree/master/Similarity) in order to return the similarity results.

## Installation
Before running any files, `pip install -e .` must be run from the top level directory, cs207project. 

## Contents
* DatabaseServer.py: contains our socket server implementation 
* MessageFormatting.py: contains the functions/classes for serializing and deserializing in order to pass data over the wire. Also contains the class definitions for the different types of operations our server carries out. 
* generate_SMTimeseries.py: contains the code to generate random ArrayTimeSeries and store them using the FileStorageManager

## Usage
* Run DatabaseServer.py file from a terminal
* Decide on operation, op, you want to run:
```
from MessageFormatting import *
from socket import socket, AF_INET, SOCK_STREAM
op_1 = {'op':'TSfromID','id':12,'courtesy':'please'} #get timeseries from id
op_2 = {'op':'simsearch_id','id':12,'n_closest':2,'courtesy':'please'} #get similiar timeseries from id 
op_3 = {'op':'simsearch_ts','ts':new_ts,'courtesy':'please} #get similiar timeseries from new (provided) timeseries
```
* Convert the operation into bytes
```
input = serialize(json.dumps(op))
```
* Connect socket 
```
s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 20000)) #the latter is the port we use in our DatabaseServer
s.send(input)
```
* Recieve and deserialize output
```
msg = s.recv(8192)
ds = Deserializer()
ds.append(msg)
ds.ready()
response = ds.deserialize() #response is now in dictionary form like the original message that was passed in
```

## Testing 
There is one testing file for the code in this module and it is contained in the [test folder](https://github.com/slac207/cs207project/tree/master/tests). These files can be run using `python setup.py test`. 

1. test_server.py: tests for accuracy of the three queries we support as well as tests the serializer/deserializer

