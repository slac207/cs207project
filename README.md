# CS207 Project

[![Build Status](https://travis-ci.org/slac207/cs207project.svg?branch=master)](https://travis-ci.org/slac207/cs207project)

[![Coverage Status](https://coveralls.io/repos/github/slac207/cs207project/badge.svg?branch=master)](https://coveralls.io/github/slac207/cs207project?branch=master)

# CS207 Final Project

## Purpose
This package contains the code to create a Web UI which supports similarity searches of timeseries by id, similarity searches of newly provided timeseries, timeseries metadata queries, timeseries retrieval based on id, and addition of a new timeseries into our database.

See [this website](http://54.157.228.231) for a demo of our working project (on a pre-existing instance)

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
git clone https://github.com/slac207/cs207project.git`
cd ~/cs207project/provisioners`
chmod a+x run.sh
./run.sh
``` 
5. When prompted by postgres=#, paste:
`alter user postgres password 'password'; create user ubuntu createdb createuser password 'cs207password'; create database ubuntu owner ubuntu; \q`

## Installation
Before running any files, `pip install -e .` must be run from the top level directory, cs207project. 

## Contents

### `cs207rbtree` (directory)
Contains a `pip install`able implementation of a Red Black Tree.

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
