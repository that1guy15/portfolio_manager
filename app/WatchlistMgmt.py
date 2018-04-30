import sys
import json
from pathlib import Path

class WatchlistMgmt():

    def __init__(self, watchlist):
        """
        Parameters
        ----------
        watchlist- file holding watchlist data - str
        """
        self.watchlist = watchlist

    def watchlist_read(self):
        """
        Read in watchlist data
        Returns - list
        """
        try:
            f = open(self.watchlist, 'rb')
        except IOError:
            print("Could not read file:", self.watchlist)
            sys.exit()

        with f:
            data = json.load(f)

        return data

    def watchlist_add(self, symbol):
        """
        Creates watchlist if dosent exist, Adds symbol to watchlist.
        Parameters
        ----------
        symbol - str

        Returns
        -------
        Returns success or failure message
        """
        data = symbol

        # Create watchlist file if not exist
        if Path(self.watchlist).is_file() == False:
            with open(self.watchlist, mode='w', encoding='utf-8') as f:
                json.dump([], f)

        # Add symbol to portfolio file
        try:
            with open(self.watchlist) as f:
                load_data = json.load(f)

                load_data['watchlist'].append(data)
                json.dump(load_data, sys.stdout, indent=2)

                with open(self.watchlist, mode='w', encoding='utf-8') as f:
                    json.dump(load_data, f, sort_keys=True, indent=2, ensure_ascii=False)

                return symbol + ' added to your watchlist'
        except Exception as e:
            return str(e)

    def watchlist_remove(self, symbol):
        """
        Creates watchlist if dosent exist, Adds symbol to watchlist.
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
            with open(self.watchlist) as f:
                load_data = json.load(f)

                load_data['watchlist'].remove(data)
                json.dump(load_data, sys.stdout, indent=2)

                with open(self.watchlist, mode='w', encoding='utf-8') as f:
                    json.dump(load_data, f, sort_keys=True, indent=2, ensure_ascii=False)

                return symbol + ' added to your watchlist'
        except Exception as e:
            return str(e)