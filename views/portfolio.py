'''
Created on 28/10/2013

@author: carlos
'''

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask.globals import request, current_app
import logging
from flask.helpers import flash, url_for
from cfg.data import MARKETS
from domain.portfolio import Portfolio
from werkzeug.utils import redirect

portfolios_bp = Blueprint('portfolios', __name__, template_folder='templates')

@portfolios_bp.route('/save', defaults={'name': None}, methods=['POST'])
@portfolios_bp.route('/save/<name>', methods=['POST','GET'])
@login_required
def save(name):
    uid=current_user.get_id()
    new_name = request.form['name']
    new_market = request.form['market']
    new_shared_uids = request.form.getlist('shared_with')
    logging.debug(new_shared_uids)
    if new_name and new_market:
        if name: #update
            pf = current_app.portfolio_manager.get(uid, name)
            if pf:
                pf.update(new_name, new_market, new_shared_uids)
            else:
                logging.warn('The portfolio %s does not exist. Cannot update it.' % (name,))
                flash('The portfolio %s does not exist. Cannot update it.' % (name,), 'error')
                return render_template('pages/portfolio_form.html', uid=uid, markets=MARKETS, selected_market=new_market, uids=current_app.uids, selected_uids=new_shared_uids)

        else: #create
            pf = Portfolio(new_name, new_market, uid)
            pf.users = new_shared_uids
            current_app.portfolio_manager.add(pf)
    # todo save portfolios
    flash('Saved portfolio %s' % (new_name, ))
    return redirect(url_for(portfolios_bp.name + '.view', name=new_name))
            
    
@portfolios_bp.route('/update/<name>')
@login_required
def update(name):    
    uid=current_user.get_id()
    pf = current_app.portfolio_manager.get(uid, name)
    if pf:
        return render_template('pages/portfolio_form.html', 
                           uid=uid, 
                           markets=MARKETS, selected_market=pf.market, 
                           uids=current_app.uids, selected_uids=pf.users)
    else:
        flash('Cannot modify the portfolio %s, the owner is %s. You can only modify your own portfolios.' % (name, uid), 'error')
        return redirect(url_for('index'))
    
    
@portfolios_bp.route('/create')
@login_required
def create():
    return render_template('pages/portfolio_form.html', uid=current_user.get_id(), markets=MARKETS, uids=current_app.uids)

@portfolios_bp.route('/view/<name>')
@login_required
def view(name):
    uid=current_user.get_id()
    pf = current_app.portfolio_manager.get(uid, name)
    return render_template('pages/view_portfolio.html', portfolio=pf, uid=uid, name=name)


    