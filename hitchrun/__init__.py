from hitchrun import commandline
from path import Path
from hitchrun.maintenance import hitch_maintenance
import os


cwd = Path(os.getcwd())


def this_dir(filename):
    """
    Use like so:

      keypath = this_dir(__file__)
    """
    return Path(filename).abspath().dirname()
