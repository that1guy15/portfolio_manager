from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap
import requests
import pandas as pd


app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'password'


def api_get(query):
    resp = requests.get(query)
    if resp.status_code != 200:
        raise ApiError('GET API {}'.format(resp.status_code))
    data = resp.json()

    return data

def stock_perf(open, last):

    data = [float(open), float(last)]
    price_df = pd.Series(data).pct_change()
    perf = price_df.round(decimals=4)

    return perf[1] * 100


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/crypto', methods=['GET'])
def crypto():

    btc = api_get('https://www.bitstamp.net/api/v2/ticker/btcusd')
    bch = api_get('https://www.bitstamp.net/api/v2/ticker/bchusd')
    eth = api_get('https://www.bitstamp.net/api/v2/ticker/ethusd')
    btc_perf = stock_perf(btc['open'], btc['last'])
    bch_perf = stock_perf(bch['open'], bch['last'])
    eth_perf = stock_perf(eth['open'], eth['last'])
    return render_template('crypto.html', btc=btc, bch=bch, eth=eth, btc_perf=btc_perf, bch_perf=bch_perf, eth_perf=eth_perf)

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
