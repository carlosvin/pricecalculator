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

class ViewCfg:
    def __init__(self, name, endpoint, childs=()):
        self.name = name
        self.endpoint = endpoint
        self.childs = childs

    @property
    def has_childs(self):
        return len(self.childs) > 0

MENU_PORTFOLIO = (
         ViewCfg('Create', 'portfolio.create'),
         ViewCfg('Propios', 'portfolio.list_own'),
         ViewCfg('Compartidos', 'portfolio.list_shared'),
        )

class Application:
    APP_NAME = "Tuntun"

    VIEWS_MENU = (
         ViewCfg('Calculator', 'calculator.calculate'),
         ViewCfg('Portfolio', None, MENU_PORTFOLIO),

        )