from domain.calculator import InputData
from flask import Flask, render_template, request, Blueprint


calculator = Blueprint('calculator', __name__, template_folder='templates/calculator/')

@calculator.route('/')
def calculate():
	input_values = None
	input_money =  request.args.get('input_money', '')
	buy_price = request.args.get('buy_price','')
	if (input_money!='' and buy_price!=''):
		input_values = InputData()
		input_values.input_money = float(input_money)
		input_values.buy_price = float(buy_price)
	return render_template('calculator/calculate.html', input_values=input_values)
