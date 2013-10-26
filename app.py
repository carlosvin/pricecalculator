import os
import cfg
from data_input import StocksInfoUpdater
from flask import Flask, request, logging
from apscheduler.scheduler import Scheduler        
        
sched = Scheduler()
app = Flask(__name__)
stocks_updater = StocksInfoUpdater(cfg.URL_MERCADO_CONTINUO)

@app.route('/')
def list_our_stocks():
    stocks_files = []
    for files in os.listdir(cfg.DATA_DIR):
        if files.endswith(cfg.DATA_EXTENSION):
            stocks_files.append(files)
            
    return unicode(stocks_files)

@app.route('/load_remote_stocks')
def load_remote_stocks():
    stocks = stocks_updater.update()
    ret = ""
    for v in stocks:
        ret += "<br>" + unicode(v)
    return ret
    

#@sched.interval_schedule(minutes=1, hour='8-17', day='0-6')
@sched.cron_schedule(minute='0,15,30,45', day_of_week='0-4', hour='8-17')
def update_remote_data():
    stocks_updater.update()

def is_installed():
    return os.path.exists(cfg.DATA_DIR) 

def install():
    os.mkdir(cfg.DATA_DIR)
    
if __name__ == '__main__':
    if not is_installed():
        install()
    sched.start()
    sched.print_jobs()
    stocks_updater.update()
    app.run(debug = cfg.DEBUG_MODE)
