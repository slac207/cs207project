import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
                      
from timeseries.lazy import *                      
from timeseries.timeSeriesABC import *             
from timeseries.ArrayTimeSeries import *
from timeseries.binarysearch import *
from timeseries.SimulatedTimeSeries import *
from timeseries.SMTimeSeries import *
from timeseries.StorageManager import *
from timeseries.Timeseries import * 