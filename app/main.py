import sys
import json
import app
import pandas as pd
import requests
from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from app.forms import NewStock
from pathlib import Path

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'password'
portfolio = Path("portfolio.json")
watching = ['btc', 'bch', 'eth']

def api_get(query):
    """
    Runs given API query
    :param query:
    :return:
    """
    resp = requests.get(query)
    if resp.status_code != 200:
        raise ApiError('GET API {}'.format(resp.status_code))
    data = resp.json()

    return data

def stock_perf(open, last):
    """
    Calculate the performance of the given stock
    :param open:
    :param last:
    :return:
    """

    data = [float(open), float(last)]
    price_df = pd.Series(data).pct_change()
    perf = price_df.round(decimals=4)

    return perf[1] * 100

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
        symbol: {
            "symbol": symbol,
            "amount": amount,
            "price": price,
            "date": date
            }
        }

    #Create portfolio file if not exist and add entry
    if portfolio.is_file() == False:
        with open(portfolio, mode='w', encoding='utf-8') as f:
            json.dump([], f)

    #Add entry to existing portfolio file
    try:
        with open(portfolio) as f:
            load_data = json.load(f)
            print(load_data)

            load_data.append(data)
            json.dump(load_data, sys.stdout, indent=2)
            print(load_data)

            with open(portfolio, mode='w', encoding='utf-8') as f:
                json.dump(load_data, f, sort_keys=True, indent= 2, ensure_ascii= False)

            return symbol + ' added to your portfolio'
    except Exception as e:
        return str(e)

@app.route('/')
def home():

    btc = api_get('https://www.bitstamp.net/api/v2/ticker/btcusd')
    bch = api_get('https://www.bitstamp.net/api/v2/ticker/bchusd')
    eth = api_get('https://www.bitstamp.net/api/v2/ticker/ethusd')
    btc_perf = stock_perf(btc['open'], btc['last'])
    bch_perf = stock_perf(bch['open'], bch['last'])
    eth_perf = stock_perf(eth['open'], eth['last'])
    return render_template('home.html', btc=btc, bch=bch, eth=eth, btc_perf=btc_perf, bch_perf=bch_perf,
                           eth_perf=eth_perf)

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


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
