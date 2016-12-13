import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
    
__all__ = ["DatabaseServer",
           "generate_SMTimeseries",
           "MessageFormatting",
           "simsearch_init"]
           
from TimeseriesDB.DatabaseServer import *
from TimeseriesDB.generate_SMTimeseries import *
from TimeseriesDB.MessageFormatting import *
from TimeseriesDB.simsearch_init import *        
