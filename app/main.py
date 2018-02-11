import sys
import requests
from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from urllib.parse import urlencode, quote_plus
from pathlib import Path
from app.forms import NewStock
from app.PortfolioPerf import PortfolioPerf

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'password'
portfolio = Path("portfolio.json")
crypto = 'ETH,XRP,BTC,BCH'
currentcy = ['USD']


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
            "date": date
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

    # URL and encode payload request by cryptocompare.com api
    crypto_url = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms=ETH,XRP,BTC,BCH&tsyms=USD"
    crypto_data = api_get(crypto_url)

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


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
