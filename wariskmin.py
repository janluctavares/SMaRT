"""
Wariskmin - Wallet Data Visualization for Risk Minimization
----------------------------------------

This script retrieves historical market data for a set of stocks from Yahoo Finance,
calculates the covariance and distance of their time series, and clusters them to visualize groups of related time series.

Author: Jan Luc Tavares
CMP596 - Visual Analytics for Data Science
PPGC - INF/UFRGS
"""

import yfinance as yf
import numpy as np
from sklearn.cluster import KMeans
import streamlit as st
import pandas as pd

data = pd.read_csv("DownloadedStockPrices.csv")
data = data.set_index('Date')
st.write(data.head())

# Calculate covariance and distance
st.write('Calculating covariance and distance...')
cov_matrix = np.cov(data.T)
dist_matrix = np.sqrt(np.sum((np.diff(data, axis=0) / data[:-1]) ** 2, axis=1))
st.write('Covariance and distance calculated successfully.')


# Cluster stocks
st.write('Clustering stocks...')
kmeans = KMeans(n_clusters=5, random_state=0).fit(cov_matrix)
labels = kmeans.labels_
st.write('Stocks clustered successfully.')


# Output results
st.write(f'Covariance matrix:\n{cov_matrix}')
st.write(f'Distance matrix:\n{dist_matrix}')
st.write(f'Cluster labels:\n{labels}')


