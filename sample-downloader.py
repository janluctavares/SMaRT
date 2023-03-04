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
STOCKS = [

"ABEV3.SA",
"SBSP3.SA",
"VALE3.SA",
"PETR4.SA",
"OIBR4.SA",
"BBDC4.SA",
"MRVE3.SA",
"ITUB4.SA",
"EMBR3.SA",
"CYRE3.SA",
"BRKM5.SA",
"USIM3.SA",
"BBDC3.SA",
"MRFG3.SA",
"JBSS3.SA",
"CPLE6.SA",
"CPFE3.SA",
"CGAS5.SA",
"USIM5.SA"
]
PERIOD = '1y'
INTERVAL = '1d'

# Retrieve data for all stocks
print('Retrieving data...')
data = yf.download(STOCKS, period=PERIOD, interval=INTERVAL)['Adj Close']
print('Data retrieved successfully.')

data.to_csv('DownloadedStockPrices.csv')
