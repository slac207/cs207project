# APIServer Documentation

## Purpose
This directory contains the files to populate the Postgres database and create the REST API. It uses a Storage Manager (timeseries/StorageManager.py) in order to access the timeseries database and create metadata from those time series in a Postgres database. We then use a Flask-SQLAlchemy implementation for the REST API.

## Installation
Before testing any files, the Amazon EC2 instance must be completely set up with all provisioning scripts.

## Contents
* rest.py
  * Sets up Flask, connects to Postgres, and defines six queries.
  - /timeseries GET sends back a json with metadata from all the time series
  - /timeseries POST adds a new timeseries into the database given a json which has a key for an id and a key for the timeseries, and returns the timeseries
  - /timeseries/id sends back metadata and the timeseries itself for a given ID in a JSON payload
  - /timeseries?mean_in=1.5,1.53 type queries send back only metadata. For continuous variables only range queries are supported with string mean_in=1.5,1.53 whereas for discrete variables(level here) queries such as level_in=A,B,C or level=A are supported. Only one query at a time is supported. NOTE: This is slightly different than the spec, and allows us to easily support negative values, e.g. mean_in=-100,-5
  - /simquery GET takes an id=the_id querystring and use that as an id into the database to find the timeseries that are similar, sending back the ids of the top N.
  - /simquery POST takes a timeseries as an input in a JSON, carries out a similarity query, and returns the appropriate ids as well.



## Testing
There are three testing files for the code in this module and they are all contained in the directory. These files can be run from the top directory (cs207project) inside the virtual environment by first entering the virtual environment with `source ~/venvs/flaskproj/bin/activate` and then  running `python APIServer/postgres_test_metadata.py` or `python3 APIServer/test_post_requests.py` or `python APIServer/test_get_requests.py`.

1. postgres_test_metadata.py: tests the ability to connect to the postgres database and create a table of metadata for each time series.
2. test_post_requests.py: tests for the correct behavior in the 4 GET queries.
3. test_get_requests.py: tests for the correct behavior in the 2 POST queries.
