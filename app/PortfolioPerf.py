import json

class PortfolioPerf:

    def portfolio_read(self, portfolio):

        with open(portfolio) as f:
            load_data = json.load(f)

        return load_data

    def stock_quantity(self, stocks, portfolio):
        """
        Build list with current amount of each stock owened
        :param stocks: list
        :param portfolio: dict
        :return:
        Number of stocks owned: int or float
        """

        portload = self.portfolio_read(portfolio)

        holdings = {name: 0 for name in stocks}
        for s in portload:
            holdings[s['symbol']] += s['amount']

        return holdings

    def stock_purch_value(self, stocks, portfolio):
        """
        Build list with inital purchase value of each stock in stocks
        :param stocks: list
        :param portfolio: dict
        :return:
        Amount paid at purchase of stock: int or float
        """

        portload = self.portfolio_read(portfolio)

        purchase = {name: 0 for name in stocks}
        for s in portload:
            purchase[s['symbol']] += s['price'] * s['amount']

        return purchase
