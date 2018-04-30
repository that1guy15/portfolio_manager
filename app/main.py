import sys
import requests
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
import json
from app.forms import NewStock, AddSymbol
from app.PortfolioPerf import PortfolioAddPerf
from app.WatchlistMgmt import *

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'password'
portfolio = './portfolio.json'
watchlist = './watchlist.json'

currentcy = ['USD']

def portfolio_add(symbol, amount, price, date):
    """
    Add the given stock purchase to the portfolio
    :param symbol:
    :param amount:
    :param price:
    :param date:
    :return:
    """

    data = {
            "symbol": symbol,
            "amount": amount,
            "price": price,
            "date": date,
            "value": amount * price
            }

    #Create portfolio file if not exist and add entry
    if Path(portfolio).is_file() == False:
        with open(portfolio, mode='w', encoding='utf-8') as f:
            json.dump([], f)

    #Add entry to existing portfolio file
    try:
        with open(portfolio) as f:
            load_data = json.load(f)

            load_data.append(data)
            json.dump(load_data, sys.stdout, indent=2)

            with open(portfolio, mode='w', encoding='utf-8') as f:
                json.dump(load_data, f, sort_keys=True, indent= 2, ensure_ascii= False)

            return symbol + ' added to your portfolio'
    except Exception as e:
        return str(e)

@app.route('/', methods=['POST', 'GET'])
def home():

    wl = WatchlistMgmt(watchlist)
    crypto_watch = wl.watchlist_read()
    crypto_url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + ",".join(crypto_watch['watchlist']) + "&tsyms=USD"

    padd = PortfolioAddPerf(portfolio, crypto_watch['watchlist'], crypto_url)
    crypto_data = padd.portfolio_add_perf()


    form = AddSymbol()
    symbol = form.symbol.data
    add_transaction = form.addtransaction.data
    message = None

    if request.method == 'POST':
        if form.validate() == False:
            flash('Symbol required.', 'error')
            return render_template('home.html', form=form, crypto_data=crypto_data)
        else:
            try:
                message = wl.watchlist_add(symbol.upper())
                flash(message)
            except Exception as e:
                flash("Unexpected error:" + str(e), 'error')

            if add_transaction is True:
                return redirect(url_for('crypto'))
            else:
                return redirect(url_for('home'), form=form, error=message, crypto_data=crypto_data)

    elif request.method == 'GET':
        return render_template('home.html', form=form, crypto_data=crypto_data)


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

    return render_template('test.html', crypto=crypto_watch)

@app.route('/api', methods=['GET'])
def api():

    padd = PortfolioAddPerf(portfolio, crypto_watch, crypto_url)
    crypto_data = padd.portfolio_add_perf()

    return jsonify(crypto_data)

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
