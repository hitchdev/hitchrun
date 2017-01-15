from hitchrun import commandline
from path import Path
import os


cwd = Path(os.getcwd())
keypath = Path(os.path.abspath(os.path.dirname(__file__)))
