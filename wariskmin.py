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

# Calculate covariance and distance
st.write('Calculating covariance, correlation and distance...')
cov_matrix = np.cov(data.T)
corr_matrix = np.corrcoef(data.T)
dist_matrix = np.sqrt(2*(1-corr_matrix))
corr_df = pd.DataFrame(corr_matrix, columns=data.columns, index=data.columns)
dist_df = pd.DataFrame(dist_matrix, columns=data.columns, index=data.columns)
st.write('Covariance and distance calculated successfully.')


# Cluster stocks
st.write('Clustering stocks...')
kmeans = KMeans(n_clusters=5, random_state=0).fit(cov_matrix)
labels = kmeans.labels_
st.write('Stocks clustered successfully.')


# Output results
#st.write(f'Covariance matrix:\n{cov_matrix}')
st.write("Correlation MATRIX (dataframe)")
st.write(corr_df)

st.write('Distance matrix (dataframe)')
st.write(dist_df)

st.write(f'Cluster labels:\n{labels}')


