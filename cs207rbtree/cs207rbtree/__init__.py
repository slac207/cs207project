import pkg_resources
import sys
sys.path.append('../cs207rbtree/')

from cs207rbtree import *

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
