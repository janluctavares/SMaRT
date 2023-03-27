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
from matplotlib.dates import MonthLocator, DateFormatter
import requests
import json
from streamlit_marquee import streamlit_marquee

location = "/home/eletronica/GIT/wallet-data-visualization/DownloadedStockPrices.csv"
data = pd.read_csv(location) #reads file where the downloaded stocks are stored
data = data.set_index('Date')


cov_matrix = np.cov(data.T)
corr_matrix = np.corrcoef(data.T) # This matrix contains the correlation coefficients of the stocks. They vary from -1 to 1.
	#dist_matrix = np.sqrt(2*(1-corr_matrix)) # The distance matrix contains the correlation "transposed" to an idea of distance, where 0 means total direct correlation and 2 means inverse correlation. "no" correlation is valued at 1.41 = sqrt(2))
corr_df = pd.DataFrame(corr_matrix, columns=data.columns, index=data.columns)
	#dist_df = pd.DataFrame(dist_matrix, columns=data.columns, index=data.columns)

fig, ax = plt.subplots()
sns.heatmap(corr_df, cmap="vlag_r")
plt.title("Heatmap da Matriz de Correlaçoes")
plt.show(fig)
	
n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(corr_matrix)
labels = kmeans.labels_
cluster_order = np.argsort(kmeans.labels_)
sorted_corr_df = corr_df.iloc[cluster_order, cluster_order]

fig, ax = plt.subplots()
sns.heatmap(sorted_corr_df, cmap="vlag_r")
plt.title("Ordered Distance Matrix Heatmap")
plt.show(fig)

corr_df['label'] = labels

# Use the pandas groupby function to count the number of stocks in each cluster
cluster_counts = corr_df.groupby('label').size()

# Create a dictionary where the keys are the cluster labels and the values are the names of the stocks in each cluster
cluster_dict = {}
for label in np.unique(labels):
    cluster_dict[label] = list(corr_df[corr_df['label'] == label].index)

# Print the count of each cluster and the names of the stocks in each cluster
for label, count in cluster_counts.items():
    print(f"Cluster {label} contem {count} açoes: {cluster_dict[label]}")


sectors = {"VALE3.SA" : "Materiais",
"PETR4.SA" : "Energia",
"ITUB4.SA" : "Financeiro",
"BBDC4.SA" : "Financeiro",
"BBAS3.SA" : "Financeiro",
"BOVA11.SA" : "Diversos",
"B3SA3.SA" : "Financeiro",
"PRIO3.SA" : "Energia",
"MGLU3.SA" : "Consumo Cíclico",
"ABEV3.SA" : "Consumo Não-Cíclico",
"PETR3.SA" : "Energia",
"ELET3.SA" : "Utilidade Pública",
"HAPV3.SA" : "Saúde",
"RENT3.SA" : "Financeiro",
"BPAC11.SA" : "Financeiro",
"GGBR4.SA" : "Materiais",
"LREN3.SA" : "Consumo Não-Cíclico",
"WEGE3.SA" : "Industriais",
"SUZB3.SA" : "Materiais",
"BBSE3.SA" : "Financeiro",
"JBSS3.SA" : "Consumo Não-Cíclico",
"BRFS3.SA" : "Consumo Não-Cíclico",
"EQTL3.SA" : "Utilidade Pública",
"ITSA4.SA" : "Financeiro",
"HYPE3.SA" : "Saúde",
"RAIL3.SA" : "Industriais",
"AZUL4.SA" : "Consumo Cíclico",
"IVVB11.SA" : "Diversos",
"SBSP3.SA" : "Utilidade Pública",
"ENEV3.SA" : "Materiais",
"VBBR3.SA" : "Materiais",
"MULT3.SA" : "Consumo Cíclico",
"VIIA3.SA" : "Consumo Não-Cíclico",
"CSAN3.SA" : "Consumo Não-Cíclico",
"AMER3.SA" : "Consumo Cíclico",
"KLBN11.SA" : "Materiais",
"TOTS3.SA" : "Tecnologia da Informação",
"ENBR3.SA" : "Utilidade Pública",
"BEEF3.SA" : "Consumo Não-Cíclico",
"RADL3.SA" : "Consumo Não-Cíclico",
"EMBR3.SA" : "Industriais",
"CSNA3.SA" : "Materiais",
"CYRE3.SA" : "Consumo Cíclico",
"UGPA3.SA" : "Consumo Não-Cíclico",
"MRFG3.SA" : "Consumo Não-Cíclico",
"CIEL3.SA" : "Financeiro",
"TIMS3.SA" : "Comunicações",
"CMIG4.SA" : "Utilidade Pública",
"USIM5.SA" : "Materiais",
"GOLL4.SA" : "Consumo Cíclico",
"VIVT3.SA" : "Comunicações",
"CCRO3.SA" : "Industriais",
"BBDC3.SA" : "Financeiro",
"ELET6.SA" : "Utilidade Pública",
"CPLE6.SA" : "Energia",
"ARZZ3.SA" : "Consumo Não-Cíclico",
"CRFB3.SA" : "Materiais",
"ENGI11.SA" : "Utilidade Pública",
"BRKM5.SA" : "Materiais",
"GOAU4.SA" : "Materiais",
"PCAR3.SA" : "Consumo Não-Cíclico",
"SMTO3.SA" : "Consumo Não-Cíclico",
"SMAL11.SA" : "Diversos",
"MRVE3.SA" : "Consumo Cíclico",
"TSLA34.SA" : "Diversos",
"EGIE3.SA" : "Utilidade Pública",
"OIBR3.SA" : "Comunicações",
"SLCE3.SA" : "Consumo Não-Cíclico",
"SANB11.SA" : "Financeiro",
"BRAP4.SA" : "Materiais",
"ALPA4.SA" : "Consumo Cíclico",
"TAEE11.SA" : "Utilidade Pública",
"CVCB3.SA" : "Consumo Cíclico",
"PSSA3.SA" : "Financeiro",
"CPFE3.SA" : "Utilidade Pública",
"ALSO3.SA" : "Financeiro",
"MDIA3.SA" : "Consumo Não-Cíclico",
"COGN3.SA" : "Consumo Cíclico",
"IRBR3.SA" : "Financeiro",
"YDUQ3.SA" : "Consumo Cíclico",
"STBP3.SA" : "Industriais",
"TRPL4.SA" : "Utilidade Pública"}

# Classifica cada ação da lista STOCKS
sectors = {}
for stock in STOCKS:
    sector = classifier.classify(stock)
    sectors[stock] = sector

# Cria um DataFrame com as ações e suas classificações setoriais
df = pd.DataFrame(list(sectors.items()), columns=['Stock', 'Sector'])

# Imprime o DataFrame
print(df)


## THE TESTING IS ONLY UP UNTIL HERE

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
    
    
def DisplayResults(selected_stocks, wallet_percentages):
    '''
    Function created to display the results of the built wallet on the Portfolio Page.
    '''
    factor = 1.0/sum(wallet_percentages.values())
    for stock in wallet_percentages:
        wallet_percentages[stock] = wallet_percentages[stock] * factor * 100
        
    # Calculate wallet variance
    # TODO: Check if this variance is being calculated CORRECTLY (maybe not only by averaging, but by using the covariance, etc.)
    selected_data = data[selected_stocks] # Filter the data so the dataframe is made only by the selected stocks.
    selected_data_normalized = selected_data / selected_data.iloc[0] 
    wallet_weights = pd.Series(wallet_percentages).div(100)
    stocks_var = selected_data_normalized.var()
    wallet_var = selected_data_normalized.mul(wallet_weights, axis=1).sum(axis=1).var() # TODO: Evaluate this line in detail
    #st.write(wallet_var)
    
    # Calculate last year returns
    # TODO: PLOT the returns of the selected stocks with alpha 0.3 and the wallet with larger alpha
    last_date = pd.to_datetime(data.index[-1])
    one_year_ago = pd.Timestamp(last_date.year - 1, last_date.month, last_date.day)
    one_year_data = selected_data.loc[str(one_year_ago):str(last_date)]
    one_year_returns = ((one_year_data - one_year_data.iloc[0]) *100 / one_year_data.iloc[0])
    
    wallet_returns = one_year_returns.mul(wallet_weights, axis=1).sum(axis=1)
    
    # Display results

    
    st.write('### Sua carteira:')
    wallet_df = pd.DataFrame(wallet_percentages, index=['Porção da carteira (%)']).T
    #wallet_df["Porção da carteira (%)"]["Carteira"] = 100
    wallet_df = pd.concat([wallet_df, one_year_returns.iloc[-1], stocks_var], axis = "columns")
    wallet_df.rename(columns = {list(wallet_df)[1]:'Retorno em 1 ano', 0:"Variância normalizada (risco)"}, inplace = True)
    st.write(wallet_df)
    st.write(f'Variância da carteira: {wallet_var:.6f}')
    st.write(f'Retorno da carteira: {wallet_returns[-1]:.2f}%')
    #st.write(one_year_returns)

    cumulative_returns = (selected_data/selected_data.iloc[0] - 1).fillna(0)
	# TODO: Colocar o retorno da carteira criada para comparar com o retorno cumulativo das ações individualmente. 

    
    #cumulative_returns["Carteira"] = cumulative_returns.mul(wallet_weights, axis=1).sum(axis=1)
    # Line plot of the cumulative returns
    st.write('## Retorno em um ano')
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.lineplot(data=one_year_returns, alpha=0.3, markers=False)
    sns.lineplot(data=wallet_returns, markers=False)
    ax.xaxis.set_major_formatter(DateFormatter(' '))

    plt.xticks(rotation=45)
    plt.xlabel('Data')
    plt.ylabel('Retorno acumulado (%)')

    st.pyplot(fig)
        
    
def portfolio_page():

    st.header('Configure sua carteira')	

    col1, col2 = st.columns(2)
    with col1:

        selected_stocks = st.multiselect('Selecione as ações', data.columns, default=data.columns[0])
    with col2:
        wallet_percentages = {}
        for stock in selected_stocks:
            wallet_percentages[stock] = st.slider(f'{stock} (%)', 0, 100, 10)

    st.write("As porcentagens de cada ação serao normalizadas para somar 100%")
    if(st.button("Carteira Configurada")):
        DisplayResults(selected_stocks, wallet_percentages)

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

## Adicionando newsflash


from chaves import key

# Chave de API da NewsAPI
api_key = key
url = f"https://newsapi.org/v2/top-headlines?country=br&category=business&apiKey={api_key}"

# Faz a requisição para a API e obtém as notícias
response = requests.get(url)
noticias = json.loads(response.text)
headlines= "ULTIMAS NOTICIAS: "

for i in range(len(noticias['articles'])):
    headlines += "  " + str(i+1) + ". " + noticias['articles'][i]['title'] + "  ||"

# Exibe as notícias em uma barra horizontal
st.write("### Headlines de noticias de finanças:")

streamlit_marquee(**{
    # the marquee container background color
    'background': "#e5e5e5",
    # the marquee text size
    'font-size': '12px',
    # the marquee text color
    "color": "#1a1a1a",
    # the marquee text content
    'content': headlines,
    # the marquee container width
    'width': '1200px',
    # the marquee container line height
    'lineHeight': "35px",
    # the marquee duration
    'animationDuration': '180s',
})
