import os
import logging
from codegen.reversewrapper import DEBUG_MODE
from cfg.data import *

class Paths:
    DATA_DIR = os.path.join(os.curdir, FileNames.DATA_DIR)
    PORTFOLIOS = os.path.join(DATA_DIR, FileNames.PORTFOLIOS)
    USERS = os.path.join(DATA_DIR, FileNames.USERS)
    LOG = os.path.join(DATA_DIR, FileNames.LOG_FILE_NAME)

class Extensions:
    DATA= ".%s" % (FileNames.DATA_DIR,)

class Log:
    LEVEL = logging.DEBUG
    MODE = (LEVEL == logging.DEBUG)


