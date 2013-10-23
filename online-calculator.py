from calculator import InputData
from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True

@app.route("/")
@app.route('/calculate')
def index():
	input_values = None
	input_money =  request.args.get('input_money', '')
	buy_price = request.args.get('buy_price','')
	if (input_money!='' and buy_price!=''):
		input_values = InputData()
		input_values.input_money = float(input_money)
		input_values.buy_price = float(buy_price)
		print input_values.sell_price_0_profit
	return render_template('data_input.html', input_values=input_values)

if __name__ == "__main__":
    app.run()
