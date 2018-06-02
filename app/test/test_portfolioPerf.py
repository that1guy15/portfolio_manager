import sys
import json
import requests
from unittest import TestCase
from nose.tools import *
from ..PortfolioPerf import api_get, PortfolioAddPerf

class test_portfolio_perf(TestCase):

    # Tests for PortfolioPerf.py

    def test_api_get(self):
        response = api_get('http://jsonplaceholder.typicode.com/users')

        self.assertIsNotNone(response, msg=None)

    def test_stock_quantity_own_all(self):
        """
        All stocks listed in stock are listed in portfolio
        """
        self.portfolio = './app/test/payloads/port_own_all.json'
        self.stock = ['ETH', 'BTC']
        self.stock_url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=ETH&tsyms=USD'

        expected_data = {'ETH': 1.01, 'BTC': 0.098}

        #Run stock_quantity on test data
        self.add_perf = PortfolioAddPerf(self.portfolio, self.stock, self.stock_url)
        return_data = self.add_perf.stock_quantity()

        self.assertEqual(expected_data, return_data)

    def test_stock_quantity_own_part(self):
        """
        Some stocks listed in stock are listed in portfolio. Others are missing.
        Multiple transactions per single stock
        """
        self.portfolio = './app/test/payloads/port_own_part.json'
        self.stock = ['ETH', 'BTC']
        self.stock_url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=ETH&tsyms=USD'

        expected_data = {'ETH': 1.108, 'BTC': 0}

        #Run stock_quantity on test data
        self.add_perf = PortfolioAddPerf(self.portfolio, self.stock, self.stock_url)
        return_data = self.add_perf.stock_quantity()

        self.assertEqual(expected_data, return_data)

    def test_purchase_value_own_all(self):
        """
        All stocks listed in stock are listed in portfolio
        """
        self.portfolio = './app/test/payloads/port_own_all.json'
        self.stock = ['ETH', 'BTC']
        self.stock_url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=ETH&tsyms=USD'

        expected_data = {'ETH': 988.66, 'BTC': 9.8}

        #Run purchase value on test data
        self.add_perf = PortfolioAddPerf(self.portfolio, self.stock, self.stock_url)
        return_data = self.add_perf.purchase_value()

        self.assertEqual(expected_data, return_data)

    def test_purchase_value_own_part(self):
        """
        Some stocks listed in stock are listed in portfolio. Others are missing.
        Multiple transactions per single stock
        """
        self.portfolio = './app/test/payloads/port_own_part.json'
        self.stock = ['ETH', 'BTC']
        self.stock_url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=ETH&tsyms=USD'

        expected_data = {'ETH': 998.4599999999999, 'BTC': 0}

        #Run purchase value on test data
        self.add_perf = PortfolioAddPerf(self.portfolio, self.stock, self.stock_url)
        return_data = self.add_perf.purchase_value()

        self.assertEqual(expected_data, return_data)


if __name__ == '__main__':
    unittest.main()