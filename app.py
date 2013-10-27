import os
from data_input import StocksInfoUpdater
from flask import Flask, render_template, request
from apscheduler.scheduler import Scheduler        
from cfg import URL_MERCADO_CONTINUO, DEBUG_MODE, DATA_DIR, DATA_EXTENSION,\
    SCHED_MINUTES, SCHED_DAYS, SCHED_HOURS, PM_FILE_PATH, USERS_FILE_PATH
import pickle
from domain.portfolio import PortfolioManager
from domain.filters import factory
from flask_login import LoginManager, login_user
from domain.user import User, UserManager
from flask.helpers import flash, url_for
from werkzeug.utils import redirect

class App(Flask):
    def __init__(self):
        super(App, self).__init__(__name__)
        self.sched = Scheduler()
        self._stocks_updater = StocksInfoUpdater(URL_MERCADO_CONTINUO)
        self.update_remote()
        
        self._pm = pickle.load(open( PM_FILE_PATH, "rb" ))
        if self._pm == None:
            self._pm = PortfolioManager()
        
        self._user_manager = pickle.load(open( USERS_FILE_PATH, "rb" ))
        if self._user_manager == None:
            self._user_manager = UserManager()
        
        self._login_manager = LoginManager()
        self._login_manager.init_app(self)
        self._login_manager.user_loader(self._user_manager.get)
            
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
        
    def append_filter(self, filter, portfolio):
        portfolio.add_filter(filter)
    
    def login(self, uid, password):
        return self._user_manager.login(uid, password)
                
app = App()

@app.route("/login", methods=["POST"])
def login():
    login = request.form['login']
    password = request.form['password']
    if login and password:
        user = app.login(login, password)
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", login=login, password=password)

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

@app.route('/portfolio/update', methods=['POST'])
def update_filter():
    type=request.form['type']
    value = request.form['value']
    filter = factory(type, value)
    if filter:
        app.append_filter(filter)

@app.sched.cron_schedule(minute=SCHED_MINUTES, day_of_week=SCHED_DAYS, hour=SCHED_HOURS)
def update_remote_data():
    app.update_remote()

if __name__ == '__main__':
    app.run()
