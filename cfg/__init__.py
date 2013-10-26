import os

DATA_DIR_NAME = "data"
DATA_DIR = os.path.join(os.curdir, DATA_DIR_NAME)
DATA_EXTENSION = ".%s" % (DATA_DIR_NAME,)

DEBUG_MODE = True

URL_MERCADO_CONTINUO="http://www.invertia.com/mercados/bolsa/indices/mdo-continuo/acciones-ib011continu"

SCHED_DAYS='0-4'
SCHED_HOURS='8-17'
SCHED_MINUTES='0,15,30,45'
