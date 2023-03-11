"""
Wariskmin - Wallet Data Visualization for Risk Minimization
----------------------------------------

This script retrieves historical market data for a set of stocks from Yahoo Finance,
calculates the covariance and distance of their time series, and clusters them to visualize groups of related time series.

Author: Jan Luc Tavares
CMP596 - Visual Analytics for Data Science
PPGC - INF/UFRGS
"""

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
    st.sidebar.header('Configure sua carteira')
    selected_stocks = st.sidebar.multiselect('Selecione as ações', data.columns, default=data.columns[0])
    wallet_percentages = {}
    for stock in selected_stocks:
        wallet_percentages[stock] = st.sidebar.slider(f'{stock} (%)', 0, 100, 10)
    st.sidebar.write("As porcentagens de cada açao serao normalizadas para somar 100%")
    
    
    factor = 1.0/sum(wallet_percentages.values())
    for stock in wallet_percentages:
        wallet_percentages[stock] = wallet_percentages[stock] * factor * 100

    
    # Calculate wallet variance
    # TODO: Calculate variance CORRECTLY - not only by averaging, but by using the covariance, etc.
    selected_data = data[selected_stocks]
    selected_data_normalized = selected_data / selected_data.iloc[0]
    wallet_weights = pd.Series(wallet_percentages).div(100)
    wallet_var = selected_data_normalized.mul(wallet_weights, axis=1).sum(axis=1).pct_change().var()
    
    # Calculate last year returns
    # TODO: PLOT the returns of the selected stocks with alpha 0.3 and the wallet with larger alpha
    last_date = pd.to_datetime(data.index[-1])
    one_year_ago = pd.Timestamp(last_date.year - 1, last_date.month, last_date.day)
    one_year_data = data.loc[str(one_year_ago):str(last_date)][selected_stocks]
    one_year_returns = ((one_year_data.iloc[-1] - one_year_data.iloc[0]) *100 / one_year_data.iloc[0]).to_frame('Retorno % em 1 ano do ativo')
    
    # Display results
    st.write('### Carteira configurada')
    wallet_df = pd.DataFrame(wallet_percentages, index=['%']).T
    st.write(wallet_df)
    st.write(f'Variância da carteira: {wallet_var:.4f}')
    st.write(one_year_returns)

    cumulative_returns = (selected_data / selected_data.iloc[0] - 1).fillna(0)
	# TODO: Colocar o retorno da carteira criada para comparar com o retorno cumulativo das ações individualmente. 
    st.write('## Preços das ações')
    fig, ax = plt.subplots(figsize=(12, 8))


    date_labels = pd.date_range(start=selected_data.index.min(), end=selected_data.index.max(), freq='MS')
    date_ticks = [date_labels[i].strftime('%Y-%m-%d') for i in range(0, len(date_labels), 3)]
    #st.write(date_ticks)
    #st.write(date_labels)
    #ax.set_xticks(date_labels)
    #ax.set_xticklabels(date_ticks, rotation=45, ha='right')

    sns.lineplot(data=selected_data)
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Price')
    st.pyplot(fig)
    
    # Line plot of cumulative returns
    st.write('## Retorno em um ano')
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.lineplot(data=cumulative_returns)
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')

    st.pyplot(fig)
    
    fig, ax = plt.subplots()
    for stock in selected_stocks:
        sns.lineplot(x='Date', y=stock, data=selected_data)
    st.pyplot(fig)

    fig, ax = plt.subplots()
    N = 10
    returns = np.zeros((N, 100))
    assets = np.zeros((N, 100))
    for i in range(1,N):
        R_i = np.random.normal(1.01, 0.03, 100)
        returns[i] = R_i 
        assets[i] = np.cumprod(R_i)
        plt.plot(assets[i], alpha=0.3)
    R_P = np.mean(returns, axis=0)
    P = np.mean(assets, axis=0)
    ax.set_xlabel("Tempo")
    ax.set_ylabel("Preço")
    st.pyplot(fig)


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
