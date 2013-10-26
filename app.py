from flask import Flask, request
import os
import cfg
from data_input import StocksInfoUpdater

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
    

def is_installed():
    return os.path.exists(cfg.DATA_DIR) 

def install():
    os.mkdir(cfg.DATA_DIR)
    
if __name__ == '__main__':
    if not is_installed():
        install()
    app.run(debug = cfg.DEBUG_MODE)
