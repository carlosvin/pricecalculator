'''
Created on 28/10/2013

@author: Carlos

Configurable parameters

'''
from domain.market import Market
from domain.filters import FilterLessThan, FilterMoreThan

class FileNames:
    DATA_DIR =  'data'
    PORTFOLIOS = 'portfolios.saved'
    USERS = 'users.saved'
    LOG_FILE_NAME = 'output.log'
    
class SchedCfg:
    DAYS='0-4'
    HOURS='8-17'
    MINUTES='0,15,30,45'
    
# --------------- Secrets:
class Secrets:
    KEY = 'fjsDFDeseJIKL675yu67321f--lfgLd'
    """ TODO You must change this password """
    ADMIN_PW = "admin"

class Enums:
    MARKETS = (
               Market('Continuo', "http://www.invertia.com/mercados/bolsa/indices/mdo-continuo/acciones-ib011continu"),
               )
    
    FILTERS=(
        FilterLessThan.NAME, 
        FilterMoreThan.NAME, 
)

class Alerts:
    SUCCESS = 'success'
    INFO = 'info'
    WARN = 'warning'
    ERROR = 'danger'

class Application:
    APP_NAME = "Tuntun"