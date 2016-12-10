import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
    
__all__ = ["distances",
           "find_most_similar",
           "generate_time_series",
           "pick_vantage_points"]
           
from Similarity.distances import *
from Similarity.find_most_similar import *
from Similarity.generate_time_series import *
from Similarity.pick_vantage_points import *