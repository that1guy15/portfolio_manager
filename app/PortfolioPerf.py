import sys
import json
import requests
from app.PortfolioMgmt import *

def api_get(query):
    """
    Runs API GET query on given url
    query - str

    :return:
    Returns JSON payload
    """
    resp = requests.get(query)
    if resp.status_code != 200:
        raise ApiError('GET API {}'.format(resp.status_code))
    api_data = resp.json()

    return api_data

class PortfolioAddPerf():

    def __init__(self, portfolio, stock, stock_url):
        """

        Parameters
        ----------
        portfolio - file holding portfolio data - str
        stock - list of stocks watching - list
        stock_url - url of stock tracker API - str
        """
        self.portfolio = portfolio
        self.stock = stock
        self.stock_url = stock_url
        self.my_data = api_get(stock_url)

        # Read in portfolio data
        pfadd = PortfolioMgmt(self.portfolio)
        self.portfolio_data = pfadd.portfolio_read()


    def stock_quantity(self):
        """

        Returns
        -------
        Returns the quantity of each stock from portfolio owned
        """

        # Total of each crypto owned
        holdings = {name: 0 for name in self.stock}
        for s in self.portfolio_data:
            holdings[s['symbol']] += s['amount']

        return holdings

    def purchase_value(self):
        """

        Returns
        -------
        Returns the purchase value of each stock owned from portfolio
        """

        # Total value of each crypto owned
        hold_value = {name: 0 for name in self.stock}
        for s in self.portfolio_data:
            hold_value[s['symbol']] += s['value']

        return hold_value

    def portfolio_add_perf(self):
        """

        Returns
        -------
        Combines stock_quantity and purchase_value into performance data (my_data)
        and returns combined portfolio data.
        """

        # Add total amount owned to my_data
        total_stock = self.stock_quantity()
        for k, v in total_stock.items():
            self.my_data['RAW'][k]['USD']['AmountOwned'] = v
            self.my_data['DISPLAY'][k]['USD']['AmountOwned'] = v

        # Add purchase value of each stock to my_data
        stock_value = self.purchase_value()
        for k, v in stock_value.items():
            self.my_data['RAW'][k]['USD']['StartValue'] = v
            self.my_data['DISPLAY'][k]['USD']['StartValue'] = '${:,.2f}'.format(v)

        # Calculate performance gains on each crypto and add to my_data
        for k, v in self.my_data['RAW'].items():

            if float(v['USD']['AmountOwned']) == 0:
                self.my_data['DISPLAY'][k]['USD']['CurrentValue'] = 0
                self.my_data['DISPLAY'][k]['USD']['TotalReturn'] = 0
                self.my_data['DISPLAY'][k]['USD']['TotalReturnPCT'] = 0
                self.my_data['RAW'][k]['USD']['CurrentValue'] = 0
                self.my_data['RAW'][k]['USD']['TotalReturn'] = 0
                self.my_data['RAW'][k]['USD']['TotalReturnPCT'] = 0
            else:
                amount_owned = float(v['USD']['AmountOwned'])
                start_val = float(v['USD']['StartValue'])
                current_price = float(v['USD']['PRICE'])
                current_value = (amount_owned * current_price)
                total_return = (current_value - start_val)
                current_value_pct = (total_return / start_val) * 100

                self.my_data['DISPLAY'][k]['USD']['CurrentValue'] = '${:,.2f}'.format(current_value)
                self.my_data['DISPLAY'][k]['USD']['TotalReturn'] = '${:,.2f}'.format(total_return) if total_return>0 else '(${:,.2f})'.format(abs(total_return))
                self.my_data['DISPLAY'][k]['USD']['TotalReturnPCT'] = '{:.2%}'.format((total_return/ start_val))
                self.my_data['RAW'][k]['USD']['CurrentValue'] = current_value
                self.my_data['RAW'][k]['USD']['TotalReturn'] = total_return
                self.my_data['RAW'][k]['USD']['TotalReturnPCT'] = current_value_pct

        return self.my_data
