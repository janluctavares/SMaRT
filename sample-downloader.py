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

# Define constants. 82 of the 100 most traded stocks  of the Brazilian stock market. These 82 are the ones with 4 years of data available.
STOCKS = ["VALE3.SA","PETR4.SA","ITUB4.SA","BBDC4.SA","BBAS3.SA","BOVA11.SA","B3SA3.SA","PRIO3.SA","MGLU3.SA","ABEV3.SA","PETR3.SA","ELET3.SA","HAPV3.SA","RENT3.SA","BPAC11.SA","GGBR4.SA","LREN3.SA","WEGE3.SA","SUZB3.SA","BBSE3.SA","JBSS3.SA","BRFS3.SA","EQTL3.SA","ITSA4.SA","HYPE3.SA","RAIL3.SA","AZUL4.SA","IVVB11.SA","SBSP3.SA","ENEV3.SA","VBBR3.SA","MULT3.SA","VIIA3.SA","CSAN3.SA","AMER3.SA","KLBN11.SA","TOTS3.SA","ENBR3.SA","BEEF3.SA","RADL3.SA","EMBR3.SA","CSNA3.SA","CYRE3.SA","UGPA3.SA","MRFG3.SA","CIEL3.SA","TIMS3.SA","CMIG4.SA","USIM5.SA","GOLL4.SA","VIVT3.SA","CCRO3.SA","BBDC3.SA","ELET6.SA","CPLE6.SA","ARZZ3.SA","CRFB3.SA","ENGI11.SA","BRKM5.SA","GOAU4.SA","PCAR3.SA","SMTO3.SA","SMAL11.SA","MRVE3.SA","TSLA34.SA","EGIE3.SA","OIBR3.SA","SLCE3.SA","SANB11.SA","BRAP4.SA","ALPA4.SA","TAEE11.SA","CVCB3.SA","PSSA3.SA","CPFE3.SA","ALSO3.SA","MDIA3.SA","COGN3.SA","IRBR3.SA","YDUQ3.SA","STBP3.SA","TRPL4.SA"]
PERIOD = '4y'
INTERVAL = '1d'

# Retrieve data for all stocks
print('Retrieving data...')
data = yf.download(STOCKS, period=PERIOD, interval=INTERVAL)['Adj Close']
print('Data retrieved successfully.')

data.to_csv('DownloadedStockPrices.csv')
