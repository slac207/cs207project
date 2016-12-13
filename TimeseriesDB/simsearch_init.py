import sys, inspect, os
from Similarity.pick_vantage_points import pick_vantage_points
from TimeseriesDB.generate_SMTimeseries import generate_time_series


def initialize_simsearch_parameters():
    sm = generate_time_series()
    vp = pick_vantage_points(20,sm)
    d = dict({'vantage_points':vp,'storage_manager':sm})
    return d

if __name__ == "__main__":
    initialize_simsearch_parameters()