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
	#dist_matrix = np.sqrt(2*(1-corr_matrix)) # The distance matrix contains the correlation "transposed" to an idea of distance, where 0 means total direct correlation and 2 means inverse correlation. "no" correlation is valued at 1.41 = sqrt(2))
	corr_df = pd.DataFrame(corr_matrix, columns=data.columns, index=data.columns)
	#dist_df = pd.DataFrame(dist_matrix, columns=data.columns, index=data.columns)
	st.write('Calculado com sucesso.')
	st.write("### Confira a matriz de correlaçoes!")
	st.write("Quanto mais cor, mais correlacionada a açao esta! Azul representa correlaçao direta e vermelho representa correlaçao inversa.")
	fig, ax = plt.subplots()
	sns.heatmap(corr_df, cmap="vlag_r")
	plt.title("Heatmap da Matriz de Correlaçoes")
	st.pyplot(fig)
	
	# Cluster stocks
	st.write('# Agrupando ações (clustering)')
	st.write("Vamos agrupar as ações de acordo com suas tendências de variação. Assim, teremos 'famílias' de ações que tendem a ter comportamentos semelhantes e podemos investigar como estes grupos são compostos.")
	n_clusters = st.slider("Numero de Grupos", min_value=1, max_value=14, value=1, step=1, label_visibility="visible")
	kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(corr_matrix)
	labels = kmeans.labels_
	st.write('Clustering realizado com sucesso.')
		


	st.write("## Agrupando as ações baseado nas suas distâncias")
	cluster_order = np.argsort(kmeans.labels_)
	sorted_corr_df = corr_df.iloc[cluster_order, cluster_order]


	fig, ax = plt.subplots()
	sns.heatmap(sorted_corr_df, cmap="vlag_r")
	plt.title("Matriz de correlaçoes rearranjada")
	st.pyplot(fig)
    
	corr_df['label'] = labels

    # Use the pandas groupby function to count the number of stocks in each cluster
	cluster_counts = corr_df.groupby('label').size()
    
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
    
    
    # Cria um DataFrame com as ações e suas classificações setoriais
	Setores_df = pd.DataFrame(list(sectors.items()), columns=['Açao', 'Setor'])
	Setores_df.set_index("Açao")
    
    # Create a dictionary where the keys are the cluster labels and the values are the names of the stocks in each cluster
	cluster_dict = {}
	for label in np.unique(labels):
		cluster_dict[label] = list(corr_df[corr_df['label'] == label].index)

    # Print the count of each cluster and the names of the stocks in each cluster
	col1, col2 = st.columns(2)
	i = 0
	for label, count in cluster_counts.items():
		if i%2 ==0:
			col1.write(f"### Cluster {label + 1}\n Numero de açoes: {count}.\n\n")
			col1.write(Setores_df.loc[Setores_df.Açao.isin(cluster_dict[label])])
		elif i%2 == 1:
			col2.write(f"### Cluster {label + 1}\n Numero de açoes: {count}.\n\n")
			col2.write(Setores_df.loc[Setores_df.Açao.isin(cluster_dict[label])])      
		i+=1
    


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
    total_investido = sum(wallet_percentages.values())
    for stock in wallet_percentages:
        wallet_percentages[stock] = wallet_percentages[stock] * factor * 100
        
    # Calculate wallet variance
    selected_data = data[selected_stocks] # Filter the data so the dataframe is made only by the selected stocks.
    selected_data_normalized = selected_data / selected_data.iloc[0] 
    wallet_weights = pd.Series(wallet_percentages).div(100)
    stocks_var = selected_data_normalized.var()
    wallet_var = selected_data_normalized.mul(wallet_weights, axis=1).sum(axis=1).var() # TODO: Evaluate this line in detail. done
    #st.write(wallet_var)
    
    # Calculate last year returns
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
    st.write(f"#### Sua carteira renderia: R$ {wallet_returns[-1]*total_investido/100 :.2f}")
    st.write(f"#### Enquanto na poupança, renderia aproximadamente: R$ {.079*total_investido :.2f}")
    versus_poupanca =pd.DataFrame( {"Carteira": [(0 + wallet_returns[-1]*total_investido/100)], "Poupança": [(0 + .079*total_investido )] })
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(data=versus_poupanca)
    plt.xlabel('Investimento')
    plt.ylabel('Retorno (R$)')
    st.pyplot(fig)
    st.write(versus_poupanca)
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

    st.header('Simule sua carteira')	

    col1, col2 = st.columns(2)
    with col1:

        selected_stocks = st.multiselect('Selecione as ações', data.columns, default=data.columns[0])
    with col2:
        wallet_percentages = {}
        for stock in selected_stocks:
            wallet_percentages[stock] = st.slider(f'Valor investido na {stock} (R$)', 0, 1000, 10)
    st.write("Valor total investido na carteira: " + str(sum(wallet_percentages.values())))
    #st.write("As porcentagens de cada ação serao normalizadas para somar 100%")
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
