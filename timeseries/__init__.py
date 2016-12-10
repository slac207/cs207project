import pkg_resources
import sys
sys.path.append('./timeseries/')

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
