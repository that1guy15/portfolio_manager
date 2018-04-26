import sys
import requests
from flask import Flask, render_template, request, flash, jsonify
from flask_bootstrap import Bootstrap
import json
from app.forms import NewStock
from app.PortfolioPerf import PortfolioAddPerf

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'password'
portfolio = './portfolio.json'
crypto_url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=EOS,ETH,XRP,BTC,BCH&tsyms=USD"
crypto_watch = ['EOS', 'ETH', 'XRP', 'BTC', 'BCH']
currentcy = ['USD']

@app.route('/', methods=['POST', 'GET'])
def home():

    padd = PortfolioAddPerf(portfolio, crypto_watch, crypto_url)

    crypto_data = padd.portfolio_add_perf()

    return render_template('home.html', crypto_data=crypto_data)

@app.route('/crypto', methods=['GET', 'POST'])
def crypto():

    form = NewStock()
    symbol = form.symbol.data
    amount = form.amount.data
    price = form.price.data
    date = form.date.data
    message = None

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'error')
            return render_template('crypto.html', form=form)
        else:
            try:
                portfolio_add(symbol, amount, price, date)
                flash('Successfully added ' + symbol)
            except Exception as e:
                flash("Unexpected error:" + str(e), 'error')
        return render_template('crypto.html', form=form, error=message)

    elif request.method == 'GET':
        return render_template('crypto.html', form=form)

@app.route('/test')
def test():

    return render_template('test.html')

@app.route('/api', methods=['GET'])
def api():

    padd = PortfolioAddPerf(portfolio, crypto_watch, crypto_url)
    crypto_data = padd.portfolio_add_perf()

    return jsonify(crypto_data)

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
