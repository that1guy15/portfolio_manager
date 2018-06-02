import sys
import json
from pathlib import Path

class PortfolioMgmt():

    def __init__(self, portfolio):
        """
        Parameters
        ----------
        portfolio- file holding portfolio data - str
        """
        self.portfolio = portfolio

    def portfolio_read(self):
        """
        Read in portfolio data
        Returns - list
        """
        try:
            f = open(Path(self.portfolio), 'rb')
        except IOError:
            print("Could not read file:", self.portfolio)
            sys.exit()

        with f:
            data = json.load(f)

        return data

    def portfolio_add(self, symbol, amount, price, date):
        """
        Creates portfolio if dosent exist, Adds transaction to portfolio.
        Parameters
        ----------
        symbol - str

        Returns
        -------
        Returns success or failure message
        """
        data = {
            "symbol": symbol,
            "amount": amount,
            "price": price,
            "date": str(date),
            "value": amount * price
        }

        # Create portfolio file if not exist
        if Path(self.portfolio).is_file() == False:
            with open(Path(self.portfolio), mode='w', encoding='utf-8') as f:
                json.dump([], f)

        # Add transaction to portfolio file
        try:
            with open(Path(self.portfolio)) as f:
                load_data = json.load(f)

                load_data.append(data)
                json.dump(load_data, sys.stdout, indent=2)

                with open(Path(self.portfolio), mode='w', encoding='utf-8') as f:
                    json.dump(load_data, f, sort_keys=True, indent=2, ensure_ascii=False)


                return symbol + ' added to your portfolio'
        except Exception as e:
            return str(e)

    def portfolio_remove(self, symbol):
        """
        Removes symbol and transactions from portfolio.
        Parameters
        ----------
        symbol - str

        Returns
        -------
        Returns success or failure message
        """
        data = symbol

        # remove symbol from portfolio file
        try:
            with open(Path(self.portfolio)) as f:
                load_data = json.load(f)

                load_data.remove(data)
                json.dump(load_data, sys.stdout, indent=2)

                with open(Path(self.portfolio), mode='w', encoding='utf-8') as f:
                    json.dump(load_data, f, sort_keys=True, indent=2, ensure_ascii=False)

                return symbol + ' added to your portfolio'
        except Exception as e:
            return str(e)