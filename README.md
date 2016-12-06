# CS207 Project

[![Build Status](https://travis-ci.org/slac207/cs207project.svg?branch=master)](https://travis-ci.org/slac207/cs207project)

[![Coverage Status](https://coveralls.io/repos/github/slac207/cs207project/badge.svg?branch=master)](https://coveralls.io/github/slac207/cs207project?branch=master)

# CS207 Final Project

## Contents

### `cs207rbtree` (directory) 
Contains a `pip install`able implementation of a Red Black Tree.

- [ ] describe directory contents.

### `timeseries` 
Contains our time series implementation.

- [ ] describe directory contents.


--------
 *(below is documentation internal to the group)*

# Project Workflow

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