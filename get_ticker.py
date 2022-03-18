import os
from stocksymbol import StockSymbol
# import pandas as pd
# from yahoo_fin import stock_info as si

class Get_Tickers:   
    def __init__(self):
      pass
      
    def penny_stocks(self):
      api_key = os.environ['STOCK_API']
      ss = StockSymbol(api_key)
      market_list = ss.market_list
      return market_list
      
    def index_stock(self):
      api_key = os.environ['STOCK_API']
      ss = StockSymbol(api_key)
      index_list = ss.index_list
      return index_list

    def symbols_us_stocks(self):
      api_key = os.environ['STOCK_API']
      ss = StockSymbol(api_key)
      symbol_list_us = ss.get_symbol_list(market="US")
      return symbol_list_us
    def symbols_stocks(self, arg):
      api_key = os.environ['STOCK_API']
      ss = StockSymbol(api_key)
      symbol_list = ss.get_symbol_list(market=str(arg))
      return symbol_list
    def symbol_list_nas(self):
      api_key = os.environ['STOCK_API']
      ss = StockSymbol(api_key)
      symbol_list_nas = ss.get_symbol_list(index="NASDAQ")
      return symbol_list_nas