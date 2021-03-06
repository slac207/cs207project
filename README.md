# CS207 Project

[![Build Status](https://travis-ci.org/slac207/cs207project.svg?branch=master)](https://travis-ci.org/slac207/cs207project)

[![Coverage Status](https://coveralls.io/repos/github/slac207/cs207project/badge.svg?branch=master)](https://coveralls.io/github/slac207/cs207project?branch=master)

# CS207 Final Project

## Purpose
This package contains the code to create a Web UI which supports similarity searches of timeseries by id, similarity searches of newly provided timeseries, timeseries metadata queries, timeseries retrieval based on id. The underlying REST API includes functionality for additional queries.

See [this website](http://54.147.79.65/) for a demo of our working project (on a pre-existing instance)

## Instructions for Running our Project in an EC2 Instance
1. Create an Ubuntu 16.04 instance on Amazon EC2.
2. Make sure the security group allows HTTP access on port 80.
3. Connect via ssh:
```
$ chmod 0400 pair.sem 
$ sudo ssh -i "pair.sem" ubuntu@public_ip
```
4. Run the following commands to provision the system:
```
git clone https://github.com/slac207/cs207project.git
cd ~/cs207project/provisioners
chmod a+x run.sh
./run.sh
``` 
5. When prompted by postgres=#, paste:
`alter user postgres password 'password'; create user ubuntu createdb createuser password 'cs207password'; create database ubuntu owner ubuntu; \q`

## Installation
To install our package, run pip install -e . from the top level directory, cs207project. Along with the dependencies, this installs all 4 sub-packages: cs207rbtree, timeseries, Similarity, and TimeseriesDB.

These sub-packages are usable independently of this project, although they do depend on each other to some degree. However, we do not currently support installing only a subset of the sub-packages; instead, it is best to install all sub-packages using the above command.


## Contents

### `cs207rbtree` (directory)
Contains our implementation of a Red Black Tree.

- See README in [cs207rbtree](https://github.com/slac207/cs207project/tree/master/cs207rbtree) for directory contents

### `timeseries` (directory)
Contains our time series implementation.

- See [timeseries README](https://github.com/slac207/cs207project/blob/master/timeseries/README.md) for directory contents, usage, and testing

### `Similarity`(directory)
Contains our similarity search implementation
- See [Similarity README](https://github.com/slac207/cs207project/blob/master/Similarity/README.md) for directory contents, usage, and testing

### `TimeseriesDB`(directory)
Contains our multi-threaded socket server implementation
- See [TimeseriesDB README](https://github.com/slac207/cs207project/blob/master/TimeseriesDB/README.md) for directory contents, usage, and testing

### `APIServer`(directory)
Contains our REST API, Postgres, and Flask implementation
- See [APIServer README](https://github.com/slac207/cs207project/blob/master/APIServer/README.md) for directory contents, usage, and testing

### `tests` (directory)
Contains our test suite. Each test file is pointed to in the respective module README linked above.

## Testing 
Run `python setup.py` tests from the main directory and all our main test files should run. Where appropriate, in the underlying READMEs we give further instruction for running additional tests.

We performed a smoke test in our demo instance, uploading a file containing the same data as timeseries 33 into the similarity search and making sure that our UI returned 33 as the most similar timeseries (which it does!). We included the smoke_test_33.json file in the main directory in case others want to try this smoke test as well (in the demo instance, as timeseries are regenerated for each instance). 

## Command Line Note
Note that we understood the directions differently and thought that we were taking out the command line program and replacing with the server implementation. You can see our command line program from Milestone 2 at [this previous commit](https://github.com/slac207/cs207project/commit/f0bd843357f0e626ec1b9451f3224b924d7e2214). Note that this does not include a link through the socket server, instead it talks directly to the BinarySearchTree.

## Known Bugs

### Web UI
- Intermittently, the metadata table will drop 1-2 rows and append them unparsed to the end of the table. However, timeseries are always plotted. [We think this might be related to the asynchronous nature of the AJAX calls.]
- The web UI displays unusual behavior on Windows machines, despite the browser. 

--------
 *(below is documentation internal to the group)*

# Project Workflow

![Workflow](https://github.com/slac207/cs207project/raw/master/www/html/files/workflow.png)

## Code Review

For substantial project tasks, two people will be assigned.

*Person 1* is the actual implementer, and will write basic test functions for their code.

*Person 2* will review the code of *Person 1*, and write additional test functions as needed.


## Comment Standards

According to  [PEP 8](https://www.python.org/dev/peps/pep-0008/#code-lay-out) **docstrings** should be included
> for all public modules, functions, classes, and methods. Docstrings are not necessary for non-public methods, but you should have a comment that describes what the method does. This comment should appear after the `def` line.

At our October 21 group meeting, we decided to make sure we have comments

1. at the start of a class definition (to explain the purpose of the class)
2. within the constructor (i.e., the `__init__()` definition (to explain nonobvious aspects of object construction)
3. at the start of user-facing functions (to explain nonobvious aspects of function construction)

**Regular comments** (i.e., those preceded by `#`) are brief in-line comments to fellow developers to help understand how the code works.
