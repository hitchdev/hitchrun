from hitchrun import commandline
from path import Path
from hitchrun.maintenance import hitch_maintenance
from hitchrun.decorators import expected
import os
import sys


cwd = Path(os.getcwd())


def this_dir(filename):
    """
    Use like so:

      keypath = this_dir(__file__)
    """
    return Path(filename).abspath().dirname()


genpath = Path(sys.executable).parent.parent.abspath()
