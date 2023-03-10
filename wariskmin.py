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


data = pd.read_csv("DownloadedStockPrices.csv") #reads file where the downloaded stocks are stored
data = data.set_index('Date')



def home_page():
    st.write(" # Bem-vindo ao Wariskmin")
    st.write("### Entendendo ações e exposição a risco")
    st.write("Investir no mercado de ações pode ser intimidador, mas com as estratégias certas, você pode construir uma carteira diversificada que minimiza o risco.")
    st.write("A diversificação é a principal dessas estratégias: Ao investir em uma variedade de ações em diferentes setores e indústrias, você pode espalhar seu risco e se proteger contra as flutuações do mercado.")
    st.write(" # Vamos entender mais sobre isso!") 
def market_page():
	st.write("# Conhecendo o mercado")
	st.write("Vamos trabalhar com dados das ações mais negociadas da bolsa de valores brasileira! Dos 100 'papeis' mais negociados na bolsa, estas 82 são as que temos acesso a 4 anos de dados.")
	st.write("Por uma ou outra razão (como mudança de nome ou entrada recente no capital aberto), alguns 'papeis' não têm dados disponíveis para tanto tempo e precisamos de informação para fazer as análises que queremos.")

	st.write("# Correlação")
	st.write("### Algumas companhias valorizam ou desvalorizam juntas, enquanto outras se beneficiam com a devalorização de certos setores. Vamos entender melhor isso!")
	st.write('Vamos calcular a *covariância* das ações, para então estabelecer as correlações e uma ideia de *distância* entre as ações. Aguarde uns instantes...')
	cov_matrix = np.cov(data.T)
	corr_matrix = np.corrcoef(data.T) # This matrix contains the correlation coefficients of the stocks. They vary from -1 to 1.
	dist_matrix = np.sqrt(2*(1-corr_matrix)) # The distance matrix contains the correlation "transposed" to an idea of distance, where 0 means total direct correlation and 2 means inverse correlation. "no" correlation is valued at 1.41 = sqrt(2))
	corr_df = pd.DataFrame(corr_matrix, columns=data.columns, index=data.columns)
	dist_df = pd.DataFrame(dist_matrix, columns=data.columns, index=data.columns)
	st.write('Calculado com sucesso.')

	fig, ax = plt.subplots()
	sns.heatmap(dist_df, cmap="coolwarm")
	plt.title("Heatmap da Matriz de Distâncias")
	st.pyplot(fig)
	
	# Cluster stocks
	st.write('# Agrupando ações (clustering)')
	st.write("Vamos agrupar as ações de acordo com suas tendências de variação. Assim, teremos 'famílias' de ações que tendem a ter comportamentos semelhantes e podemos investigar como estes grupos são compostos.")
	n_clusters = st.slider("Numero de Grupos", min_value=1, max_value=10, value=1, step=1, label_visibility="visible")
	kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(dist_matrix)
	labels = kmeans.labels_
	st.write('Clustering realizado com sucesso.')
		


	st.write("## Agrupando as ações baseado nas suas distâncias")
	cluster_order = np.argsort(kmeans.labels_)
	sorted_dist_df = dist_df.iloc[cluster_order, cluster_order]


	fig, ax = plt.subplots()
	sns.heatmap(sorted_dist_df, cmap="coolwarm")
	plt.title("Ordered Distance Matrix Heatmap")
	st.pyplot(fig)
	st.write("# TODO: Inserir, nos dados, a classificação setorial da B3. Dessa forma, quando realizarmos o clustering, podemos mostrar tabelas com a contagem de setores de cada cluster.")

    # Add more content about diversification here
def risk_page():
    st.header("Estratégias de Investimento")
    
    st.subheader("Alocação de recursos")
    st.write("Placeholder para textos e dados interativos para mostrar a importância da diversificação")
    labels = ["US Stocks", "International Stocks", "Bonds", "Real Estate", "Commodities", "Cash"]
    sizes = [30, 20, 20, 10, 10, 10]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
    
    st.subheader("Retornos históricos")
    st.write("Diferentes estratégias têm diferentes RISCOS e RETORNOS. A construção da sua carteira deve estar atrelada a seu perfil. Quanto você aceita perder para obter retornos.")
    strategies = ["Index Funds", "Dividend Stocks", "Growth Stocks", "Value Stocks"]
    returns = [8.2, 10.6, 12.3, 9.1]
    fig, ax = plt.subplots()
    ax.bar(strategies, returns)
    ax.set_ylabel("Annual Return (%)")
    st.pyplot(fig)
    
def portfolio_page():
	st.write("Esta página contem o grosso do projeto. Seleção de ações e visualização dos retornos passados das ações e da carteira.")


# Define pages
PAGES = {
    "Home": home_page,
    "Conheça o Mercado": market_page,
    "Entenda a diversificação": risk_page,
    "Construção de Carteira": portfolio_page }


# Create sidebar
st.sidebar.title("Navegação")
selection = st.sidebar.radio("Ir para", list(PAGES.keys()))

# Display selected page
page = PAGES[selection]
page()
