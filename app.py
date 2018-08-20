import os
from data_input import StocksInfoUpdater
from flask import Flask, render_template, request
import sched, time
import pickle
from urllib.error import URLError
from domain.portfolio import PortfolioManager
from flask_login import LoginManager, login_user, logout_user,login_required,\
    current_user
from domain.user import UserManager
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
import logging
from cfg import Log, Paths, Extensions
from cfg.data import Secrets, Enums, Alerts, Application
from views.portfolio import portfolio
from views.calculator import calculator

class App(Flask):
    def __init__(self):
        super(App, self).__init__(__name__)
        self.secret_key=Secrets.KEY
        self.config.from_object(Enums)
        self.config.from_object(Application)
        
        if not self.is_installed():
            self.install()
        
        logging.basicConfig(filename=Paths.LOG , level=Log.LEVEL)
        
        self.load_portfolio_manager()
        
        try:        
            self._user_manager = pickle.load(open( Paths.USERS, "rb" ))
        except IOError:
            self._user_manager = UserManager()
        
        self._login_manager = LoginManager()
        self._login_manager.init_app(self)
        self._login_manager.user_loader(self._user_manager.get)
        
        
        # TODO when we have more markets, then we'll create and stocks upater by market
        self.sched = sched.scheduler(time.time, time.sleep)
        self._stocks_updater = StocksInfoUpdater(Enums.MARKETS[0].url)
        self.update_remote()
    
    def update_remote(self):
        try:
            self.sched.enter(3600, 1, self.update_remote)
            self._stocks_updater.update()
        except URLError:
            logging.error('Cannot get URL: ' + self._stocks_updater.url)
    
    @property
    def stocks(self):
        return self._stocks_updater.stocks
    
    @staticmethod
    def is_installed():
        return os.path.exists(Paths.DATA_DIR) 

    @staticmethod
    def install():
        os.mkdir(Paths.DATA_DIR)
    
    def login(self, uid, password):
        return self._user_manager.login(uid, password)

    def add_user(self, uid, password, admin_password):
        if admin_password == Secrets.ADMIN_PW and self._user_manager.add_user(uid, password):
            try:        
                pickle.dump(self._user_manager, open( Paths.USERS, "wb" ), -1)
                return True
            except IOError:
                return False
        else:
            return False
  
    def _get_uids(self):
        return self._user_manager.uids
    uids = property(_get_uids)
    
    def load_portfolio_manager(self):
        try:
            self.portfolio_manager = pickle.load(open( Paths.PORTFOLIOS, "rb" ))
        except IOError:
            self.portfolio_manager = PortfolioManager()
    
    def save_portfolio_manager(self):
        try:
            pickle.dump(self.portfolio_manager, open( Paths.PORTFOLIOS, "wb" ), -1)
            return True
        except IOError as e:
            logging.error(e)
            return False
                
app = App()
app.register_blueprint(portfolio)
app.register_blueprint(calculator, url_prefix='/calculator')


@app.route("/login", methods=["POST"])
def login_post():
    email = request.form['email']
    password = request.form['password']
    if email and password:
        user = app.login(email, password)
        if user:
            login_user(user, remember=True)
            flash("Logged in successfully.", Alerts.SUCCESS)
        else:
            flash("Invalid email or password", Alerts.ERROR)
    return redirect(request.args.get("next") or url_for("index"))
    #return render_template("login.html", action='/login', email=email, password=password)

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("pages/login.html", uid=current_user.get_id())

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/add/user", methods=["POST"])
def add_user_post():
    admin_password = request.form['admin_password']
    email = request.form['email']
    password = request.form['password']    
    if app.add_user(email, password, admin_password):
        flash("User %s added" % (email,))
        return render_template("pages/add_user.html", action='/add/user')
    else:
        flash("You cannot create an user", Alerts.ERROR)
        return render_template("pages/add_user.html", action='/add/user', email=email)

@app.route("/add/user", methods=["GET"])
def add_user_get():
    return render_template("pages/add_user.html", action='/add/user')

@app.route('/stocks')
def list_our_stocks():
    stocks_files = []
    for files in os.listdir(Paths.DATA_DIR):
        if files.endswith(Extensions.DATA):
            stocks_files.append(files)
    return str(stocks_files, 'utf-8')

@app.route('/prices')
def list_prices():
    return render_template('pages/instruments_select.html', stocks=app.stocks)

@app.route('/')
def index():
    uid = current_user.get_id()
    return render_template("pages/index.html", 
                           uid=uid, 
                           own_pfs=app.portfolio_manager.get_own(uid).values(), shared_pfs=app.portfolio_manager.get_shared(uid).values())

if __name__ == '__main__':
    app.run()
