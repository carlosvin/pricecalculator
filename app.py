import os
from data_input import StocksInfoUpdater
from flask import Flask, render_template
from apscheduler.scheduler import Scheduler        
from cfg import URL_MERCADO_CONTINUO, DEBUG_MODE, DATA_DIR, DATA_EXTENSION,\
    SCHED_MINUTES, SCHED_DAYS, SCHED_HOURS

class App(Flask):
    def __init__(self):
        super(App, self).__init__(__name__)
        self.sched = Scheduler()
        self._stocks_updater = StocksInfoUpdater(URL_MERCADO_CONTINUO)
        self.update_remote()
            
    def run(self):
        if not self.is_installed():
            self.install()
        self.sched.start()
        self.sched.print_jobs()
        super(App, self).run(debug = DEBUG_MODE)
    
    def update_remote(self):
        self._stocks_updater.update()
        
    def _get_stocks(self):
        return self._stocks_updater.stocks
    stocks=property(_get_stocks)

    @staticmethod
    def is_installed():
        return os.path.exists(DATA_DIR) 

    @staticmethod
    def install():
        os.mkdir(DATA_DIR)

app = App()

@app.route('/')
def list_our_stocks():
    stocks_files = []
    for files in os.listdir(DATA_DIR):
        if files.endswith(DATA_EXTENSION):
            stocks_files.append(files)
    return unicode(stocks_files)

@app.route('/prices')
def list_prices():
    return render_template('instruments_select.html', stocks=app.stocks)


@app.sched.cron_schedule(minute=SCHED_MINUTES, day_of_week=SCHED_DAYS, hour=SCHED_HOURS)
def update_remote_data():
    app.update_remote()

if __name__ == '__main__':
    app.run()
