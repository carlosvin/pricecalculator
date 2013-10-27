import os
from data_input import StocksInfoUpdater
from flask import Flask, render_template, request
from apscheduler.scheduler import Scheduler        
from cfg import URL_MERCADO_CONTINUO, DEBUG_MODE, DATA_DIR, DATA_EXTENSION,\
    SCHED_MINUTES, SCHED_DAYS, SCHED_HOURS, PM_FILE_PATH, USERS_FILE_PATH,\
    USERS_FILE_PATH, SECRET_KEY, ADMIN_PASSWORD
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
        self.secret_key=SECRET_KEY
        self.sched = Scheduler()
        self._stocks_updater = StocksInfoUpdater(URL_MERCADO_CONTINUO)
        self.update_remote()
        
        try:
            self._pm = pickle.load(open( PM_FILE_PATH, "rb" ))
        except IOError:
            self._pm = PortfolioManager()
        try:        
            self._user_manager = pickle.load(open( USERS_FILE_PATH, "rb" ))
        except IOError:
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

    def add_user(self, uid, password, admin_password):
        if admin_password == ADMIN_PASSWORD and self._user_manager.add_user(uid, password):
            try:        
                pickle.dump(self._user_manager, open( USERS_FILE_PATH, "wb" ), -1)
                return True
            except IOError:
                return False
        else:
            return False
                
app = App()

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form['email']
    password = request.form['password']
    if email and password:
        user = app.login(email, password)
        if user:
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("Invalid email or password", 'error')
    return render_template("login.html",action='/login', email=email, password=password)

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html", action='/login')

@app.route("/add/user", methods=["POST"])
def add_user_post():
    admin_password = request.form['admin_password']
    email = request.form['email']
    password = request.form['password']    
    if app.add_user(email, password, admin_password):
        flash("User %s added" % (email,))
        return render_template("add_user.html", action='/add/user')
    else:
        flash("You cannot create an user", 'error')
        return render_template("add_user.html", action='/add/user', email=email)

@app.route("/add/user", methods=["GET"])
def add_user_get():
    return render_template("add_user.html", action='/add/user')


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
