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
import seaborn as sns
import matplotlib.pyplot as plt

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
n_clusters = 8
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(dist_matrix)
labels = kmeans.labels_
st.write('Stocks clustered successfully.')


# Output results
#st.write(f'Covariance matrix:\n{cov_matrix}')
st.write("Correlation MATRIX (dataframe)")
st.write(corr_df)

st.write('Distance matrix (dataframe)')
st.write(dist_df)

st.write("# Testes")

st.write(f'Cluster labels:\n{labels}')


fig, ax = plt.subplots()
sns.heatmap(dist_df, cmap="coolwarm")
plt.title("Distance Matrix Heatmap")
st.pyplot(fig)

st.write("# Rearranjando as ações baseado nas suas distâncias")
cluster_order = np.argsort(kmeans.labels_)
sorted_dist_df = dist_df.iloc[cluster_order, cluster_order]

#corr_df["clusters"] = labels

# Sort the DataFrame by cluster label and then by correlation value
#sorted_corr_df = corr_df.sort_values(by=['clusters'])
#sorted_corr_df = sorted_corr_df.drop(columns='clusters')

fig, ax = plt.subplots()
sns.heatmap(sorted_dist_df, cmap="coolwarm")
plt.title("Ordered Correlation Matrix Heatmap")
st.pyplot(fig)




