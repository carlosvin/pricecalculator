'''
Created on 28/10/2013

@author: carlos
'''

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask.globals import request, current_app
import logging
from flask.helpers import flash, url_for
from domain.portfolio import Portfolio
from werkzeug.utils import redirect
from domain.filters import Filter
from cfg.data import Alerts

portfolio = Blueprint('portfolio', __name__, template_folder='templates/')

def save_portfolio_manager():
    if current_app.save_portfolio_manager():
        flash( 'Saved portfolio manager', Alerts.SUCCESS)
    else:
        flash('Saving portfolio manager: Error', Alerts.ERROR)

@portfolio.route('/save', defaults={'name': None}, methods=['POST'])
@portfolio.route('/save/<name>', methods=['POST','GET'])
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
                flash('The portfolio %s does not exist. Cannot update it.' % (name,), Alerts.ERROR)
                return render_template('portfolio/pages/form.html', uid=uid, selected_market=new_market, uids=current_app.uids, selected_uids=new_shared_uids)

        else: #create
            pf = Portfolio(new_name, new_market, uid)
            pf.users = new_shared_uids
            current_app.portfolio_manager.add(pf)
    # todo save portfolios
    flash('Saved portfolio %s' % (new_name, ), Alerts.SUCCESS)
    return redirect(url_for(portfolio.name + '.view', name=new_name, uid=uid))
            
    
@portfolio.route('/update/<name>')
@login_required
def update(name):    
    uid=current_user.get_id()
    pf = current_app.portfolio_manager.get(uid, name)
    if pf:
        return render_template('portfolio/pages/form.html', 
                           uid=uid,  selected_market=pf.market, 
                           uids=current_app.uids, selected_uids=pf.users)
    else:
        flash('Cannot modify the portfolio %s, the owner is %s. You can only modify your own portfolios.' % (name, uid), Alerts.ERROR)
        return redirect(url_for('index'))
    
    
@portfolio.route('/create')
@login_required
def create():
    return render_template('portfolio/pages/form.html', uid=current_user.get_id(), uids=current_app.uids)

@portfolio.route('/view/<name>/<uid>')
@login_required
def view(name, uid=None):
    if not uid:
        uid=current_user.get_id()
    pf = current_app.portfolio_manager.get(uid, name)
    if pf:
        return render_template('portfolio/pages/view.html', portfolio=pf, uid=current_user.get_id(), name=name)
    else:
        flash('Cannot get the portfolio of "%s" named "%s"' % (uid, name),Alerts.ERROR)
        return redirect(url_for('index'))


@portfolio.route('/select/filter/<name>', methods=['POST'])
@login_required
def select_filter(name):
    filter_type = request.form['filter_type']
    if filter_type:
        filter = Filter.factory(filter_type)
        if filter:
            logging.debug("filter -> '%s' fields %u" % (filter.id, len(filter.fields)))
            return render_template('portfolio/pages/add_filter.html', fields=filter.fields.values() ,filter_type=filter_type, p_name=name, uid=current_user.get_id(), name=name)
        else:
            flash('Cannot generate a filter of type ' + filter_type, Alerts.ERROR)
    else:
        flash('Filter type was not selected', Alerts.ERROR)
    return redirect(url_for(portfolio.name + '.view', name=name, uid=current_user.get_id()))

@portfolio.route('/<name>/add/filter/<filter_type>', methods=['POST'])
@login_required
def add_filter(name, filter_type):
    uid=current_user.get_id()
    if filter_type:
        filter = Filter.factory(filter_type)
        if filter:
            try:
                for field in filter.fields.values():
                    field.value = request.form[field.name]
                
                pf = current_app.portfolio_manager.get(uid, name)
                if pf:
                    pf.add_filter(filter)
                    save_portfolio_manager()
                else:
                    flash('Cannot get the portfolio %s for user %s'% (name, uid), Alerts.WARN)
            except BaseException as e:
                logging.exception(e)
                flash('Cannot create the filter because: %s' % (e,), Alerts.ERROR)
        else:
            flash('Cannot generate a filter of type "' + filter_type + '"', Alerts.ERROR)
    else:
        flash('Filter type was not selected', Alerts.ERROR)
    return redirect(url_for(portfolio.name + '.view', name=name, uid=uid))

@portfolio.route('/<name>/del/filter/<filter_id>', methods=['GET'])
@login_required
def del_filter(name, filter_id):
    uid=current_user.get_id()
    pf = current_app.portfolio_manager.get(uid, name)
    if pf:
        try:
            pf.del_filter(filter_id)
            save_portfolio_manager()
            flash('Deleted filter "%s" from portfolio "%s" of user "%s"' % (filter_id, name, uid), Alerts.SUCCESS)
        except KeyError as e:
            flash('Error deleting filter "%s" from portfolio "%s" of user "%s"'%(filter_id, name, uid), Alerts.ERROR)
    else:
        flash('Portfolio %s of user %s, not found'%(filter_id, name, uid), Alerts.ERROR)

    return redirect(url_for(portfolio.name + '.view', name=name, uid=uid))

@portfolio.route('/delete/<name>', methods=['GET'])
@login_required
def delete(name):
    uid=current_user.get_id()
    if current_app.portfolio_manager.delete(uid, name):
        flash('Deleted portfolio "%s" of user "%s"' % (name, uid), Alerts.SUCCESS)
        save_portfolio_manager()
    else:
        flash('Cannnot delete portfolio "%s" of user "%s"' % (name, uid), Alerts.ERROR)
    return redirect(url_for('index'))


        