"""
Sample Data Downloader
----------------------------------------

This script retrieves historical market data for a set of stocks from Yahoo Finance, it saves as a local file in order to avoid making multiple downloads for experimentation.

Author: Jan Luc Tavares
CMP596 - Visual Analytics for Data Science
PPGC - INF/UFRGS
"""

import yfinance as yf
import pandas as pd

# Define constants.
STOCKS = ['AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT', 'NVDA', 'JPM', 'JNJ', 'V']
PERIOD = '10y'
INTERVAL = '1d'

# Retrieve data for all stocks
print('Retrieving data...')
data = yf.download(STOCKS, period=PERIOD, interval=INTERVAL)['Adj Close']
print('Data retrieved successfully.')

data.to_csv('DownloadedStockPrices.csv')
