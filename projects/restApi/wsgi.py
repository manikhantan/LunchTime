import os, sys
dir_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(dir_path)
from projects.restApi.app import app as application