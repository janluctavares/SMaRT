"""
SMaRT - Stock MArket Risk Tolerance
----------------------------------------

This script is about informing people and sharing knowledge about risk and diversification of investments.

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
#from streamlit_marquee import streamlit_marquee
from datetime import datetime, timedelta


data = pd.read_csv("DownloadedStockPrices.csv") #reads file where the downloaded stocks are stored
data = data.set_index('Date')



def home_page():
    st.write(" # Bem-vindo ao SMaRT")
    st.write("### Entendendo ações e exposição a risco")
    st.write("Investir no mercado de ações pode ser intimidador, mas com as estratégias certas, você pode construir uma carteira diversificada que minimiza o risco.")
    st.write("A diversificação é a principal dessas estratégias: Ao investir em uma variedade de ações em diferentes setores e indústrias, você pode espalhar seu risco e se proteger contra as flutuações do mercado.")
    st.write(" # Vamos entender mais sobre isso!")
    st.write("Utilize a barra de navegação à esquerda para navegar entre as páginas do app.")
     
    st.subheader("Sobre o dataset")
    st.write("Nesta ferramenta, trabalhamos com os dados de 78 companhias negociadas na bolsa de valores brasileira e com dois indices, o IBOV (Brasil) e o S&P500 (EUA) representados por 'BOVA11.SA' e 'IVVB11.SA' respectivamente.")
    st.write("Os dados obtidos compreendem os dias uteis de 11/03/2019 a 10/03/2023 e um programa auxiliar foi desenvolvido para fazer o download para outras datas, ativos e indices.")
    st.write(" ### Abaixo, ainda pretendo detalhar melhor o dataset")
    
def market_page():
	st.write("# Conhecendo o mercado")
	st.write("Vamos trabalhar com dados das ações mais negociadas da bolsa de valores brasileira! Dos 100 'papeis' mais negociados na bolsa, estas 80 são as que temos acesso a 4 anos de dados.")
	st.write("Por uma ou outra razão (como mudança de nome ou entrada recente no capital aberto), alguns 'papeis' não têm dados disponíveis para tanto tempo e precisamos de informação para fazer as análises que queremos.")

	st.write("# Correlação")
	st.write("Algumas companhias valorizam ou desvalorizam juntas, enquanto outras se beneficiam com a devalorização de certos setores. Vamos entender melhor isso!")
	st.write('Vamos calcular as *correlações* entre cada ação com todas as demais, assim teremos noção de quanto elas variam juntas.')
	with st.spinner("Calculando..."):
		cov_matrix = np.cov(data.T)
		corr_matrix = np.corrcoef(data.T) # This matrix contains the correlation coefficients of the stocks. They vary from -1 to 1.
		#dist_matrix = np.sqrt(2*(1-corr_matrix)) # The distance matrix contains the correlation "transposed" to an idea of distance, where 0 means total direct correlation and 2 means inverse correlation. "no" correlation is valued at 1.41 = sqrt(2))
		corr_df = pd.DataFrame(corr_matrix, columns=data.columns, index=data.columns)
		#dist_df = pd.DataFrame(dist_matrix, columns=data.columns, index=data.columns)
		
	st.write("### Confira a matriz de correlaçoes!")
	st.write("Quanto mais cor, mais correlacionada a ação está! Azul representa correlação direta e vermelho representa correlação inversa.")
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
		


	st.write("## Agrupando as ações baseado nas suas correlações")
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
    "BOVA11.SA" : "Índice",
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
    "IVVB11.SA" : "Índice",
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
    "MRVE3.SA" : "Consumo Cíclico",
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
	st.write("Note que as tabelas abaixo acabam agrupando ações do mesmo setor quando o número de clusters aumenta. Isso quer dizer que as companhias que mais variam juntas são dos mesmos setores. Para diminuir o risco, prefira construir uma carteira com ações que estejam menos correlacionadas.")
	
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
    

def risk_page():
    st.header("Estratégias de Investimento")
    st.subheader("Por que diversificar é importante?")
    
    st.write("Vamos supor que você foi a um cassino e aprendeu alguma técnica que lhe dê uma vantagem de 1% sobre as chances do cassino ganhar.\n\nVocê vai a um cassino com 1000 para apostar e seria imprudente apostar tudo no mesmo jogo. Teríamos 51% de chance de ganhar e a casa ainda teria 49% de chance de ganhar (nossa vantagem seria de apenas 1%). A expectativa é de você ganhar o jogo, mas as chances dos possíveis resultados são muito altas (você também tem grande chance de perder).\n\nMas você pode analisar o problema e apostar em 100 mesas diferentes. Isso significa que você fez apostas independentes, porque assim o resultado de uma mesa não terá influência sobre o resultado da outra. Nesse caso, na medida em que mais apostas em mais mesas forem feitas, os resultados que você obtém se aproximam de uma média. Você espera ganhar em 51% das mesas e a chance de perder recursos é menor.")
    st.subheader("Estas ideias se aplicam à noção de *risco* na Teoria das Carteiras")
    st.write("Simplificando um pouco as coisas, podemos ver com essa analogia que seria melhor fazer investimentos tão independentes quanto fosse possível, investindo em vários ativos não-correlacionados.\n\nEm finanças, o risco é estimado pelo *desvio padrão* de uma série temporal, e o risco futuro de uma carteira será estimado pela volatilidade (desvio padrão) passada da carteira. Ou seja, usamos as informações do que já aconteceu para estimar o que **pode** acontecer, mas não temos como garantir que o futuro vai ser como esperamos.")
    st.subheader("Risco e expectativa de retorno")
    st.write("Imagine que você é uma pessoa em busca de um emprego em um parque, e há duas opções de trabalho disponíveis para você. A primeira opção é trabalhar no portão do parque, perto da saída. O trabalho é relativamente tranquilo, e suas principais tarefas envolvem receber e dar informações aos visitantes, conferir ingressos e controlar a entrada e saída de pessoas. A segunda opção é trabalhar em um galpão mais distante controlando o almoxarifado, também com tarefas administrativas simples mas aí, eventualmente, aparecem ursos. Neste segundo trabalho você precisará lidar com o risco de encontrar um urso em seu caminho. Em qual você esperaria receber mais dinheiro pelo trabalho? Se o salário fosse o mesmo, você escolheria o sem riscos, não é mesmo?\n\nEssa escolha pode parecer trivial, mas a verdade é que ela reflete uma importante questão de finanças: risco e retorno. Em finanças, o retorno se refere ao lucro ou rendimento que você pode obter com um investimento ou atividade financeira, enquanto o risco se refere à incerteza sobre esse retorno. Em outras palavras, quanto maior o risco, maior a incerteza sobre o retorno que você pode esperar.\n\nA escolha depende das preferências e objetivos pessoais de cada indivíduo. Cada pessoa deve avaliar sua própria tolerância ao risco e fazer escolhas financeiras que sejam coerentes com seus objetivos e circunstâncias pessoais. Por isso, com a teoria das carteiras tentamos estabelecer a carteira com maiores retornos para um determinado risco estimado.")
    st.subheader("Mas diversificação **elimina** o risco?")
    st.write("Diversificar não elimina completamente o risco de um investimento, mas pode ajudar a reduzir a exposição ao risco.\n\nA diversificação é uma estratégia de investimento que envolve a alocação de recursos em diferentes tipos de ativos financeiros, tais como ações, títulos, fundos imobiliários, commodities, entre outros. Essa estratégia busca reduzir o risco de perdas em um único ativo ou setor, distribuindo o risco em diferentes classes de ativos ou setores da economia.\n\nPor exemplo, se você investe todo o seu dinheiro em uma única ação, seu risco está concentrado naquele ativo e em sua performance. Se a empresa não tiver um bom desempenho ou enfrentar problemas, você pode perder todo o seu dinheiro investido. Por outro lado, se você diversifica seus investimentos em diferentes ações de empresas de setores variados, como tecnologia, saúde e varejo, você reduz o risco de perdas significativas em um único setor ou empresa. Nesta ferramenta, veremos como diversificar as **ações**.\n\nMesmo que a diversificação possa ajudar a reduzir o risco, ela não é capaz de eliminá-lo completamente. Afinal, não é possível prever ou controlar todos os fatores que afetam o desempenho dos ativos financeiros. Além disso, eventos imprevisíveis, como desastres naturais, crises políticas e pandemias, podem afetar todos os mercados simultaneamente, mesmo que você tenha diversificado seus investimentos.\n\nPortanto, embora a diversificação seja uma estratégia importante de gestão de risco, é sempre importante lembrar que todo investimento possui um nível de risco associado a ele, e que os retornos esperados devem ser avaliados em relação a esse risco.")
    st.subheader("Vamos entender o risco e o tempo de evolução")
    st.write("Ao longo do tempo, as variações dos valores dos ativos tendem a se equilibrar e as chances de obter retornos positivos aumentam. Quando o investimento é mantido por um período mais longo, permitimos que as flutuações de curto prazo sejam compensadas por um desempenho mais consistente a longo prazo. Por isso, é importante ter uma visão de longo prazo e ser paciente com seus investimentos. Além disso, é importante manter uma estratégia consistente de investimentos, diversificando sua carteira de acordo com seus objetivos e perfil de risco.")
    st.subheader("No exemplo a seguir, podemos alterar o risco e o tempo (número de dias) de um determinado ativo fictício")
    st.write("O gráfico mostra a contagem dos valores percentuais de retorno de algum ativo que tenha a variância escolhida e que tenha sido contabilizado pelo número de dias escolhidos. Serão gerados dados aleatórios.")
    
    variance = st.slider('Escolha a variância do seu ativo', 0.0, 3.0, step=0.05, value=0.35)
    dias = st.slider('Escolha o número de dias que vamos contar os retornos', 1, 500, value=150)
    mean = 0
    
    # Gera a curva normal aleatória
    normal = np.random.normal(mean, variance, dias)
    fig, ax = plt.subplots()
    plt.xlabel('Retorno (%)')
    plt.ylabel('Quantidade de dias que este retorno acontece')
    # Plota o histograma da curva normal
    sns.histplot(normal, kde=True)
    st.pyplot(fig)
    st.write("Observe que podemos brincar com os valores dos seletores e escolher vários dias de observação. Quando os dias são valores muito baixos, temos retornos diversos e não percebemos uma tendência geral, mas quando temos muitos dias, os retornos tem um formato que se aproximam de uma curva que chamamos de *normal*.\n\nNote também que quando a variância é em torno de 0,35 os retornos ficam entre -1% e 1%, mas e aumentam junto com a variância, mas não aumentam com o número de dias. Ou seja, com uma variância maior, pode-se perder mais (ou ganhar mais).\n\nOBS: ativos reais não tem a curva tão bem comportada como esta, mas assim conseguimos ter ideia da importância da variância.")
    st.write(f'Em uma curva normal, esperamos que 95% dos valores estejam entre 2*(raiz da variância), ou seja, para a curva que você fez, 95% dos valores devem estar entre {np.sqrt(variance)*(-2):.2f}% e {np.sqrt(variance)*(2):.2f}%')
    st.write("Vamos ver isso na prática na página 'Construção da Carteira'")
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
    selected_data_returns = selected_data.pct_change()[1:]
    wallet_weights = pd.Series(wallet_percentages).div(100)
    stocks_var = selected_data_normalized.var()
    returns_var = selected_data_returns.var()
    
    wallet_var = selected_data_returns.mul(wallet_weights, axis=1).sum(axis=1).var()
    wallet_sd = np.sqrt(wallet_var)
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
    wallet_df = pd.concat([wallet_df, one_year_returns.iloc[-1], returns_var], axis = "columns")
    wallet_df.rename(columns = {list(wallet_df)[1]:'Retorno em 1 ano', 0:"Variância dos retornos (risco)"}, inplace = True)
    st.write(wallet_df)
    st.write(f'Variância dos retornos da carteira: {wallet_var:.3e}')
    st.write(f'Isso quer dizer que esperamos 95% dos retornos da carteira entre {np.sqrt(wallet_var)*(-200):.2f}% e {np.sqrt(wallet_var)*200:.2f}%' )
    st.write(f'Retorno da carteira: {wallet_returns[-1]:.2f}%')
    st.write(f"#### Sua carteira renderia: R$ {wallet_returns[-1]*total_investido/100 :.2f}")
    st.write(f"#### Enquanto na poupança, renderia aproximadamente: R$ {.079*total_investido :.2f}")
    versus_poupanca =pd.DataFrame( {"Carteira": [(0 + wallet_returns[-1]*total_investido/100)], "Poupança": [(0 + .079*total_investido )] })
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(data=versus_poupanca)
    plt.xlabel('Investimento')
    plt.ylabel('Retorno (R$)')
    st.pyplot(fig)
    #st.write(versus_poupanca)
    #st.write(one_year_returns)

    

    
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
        
    walletReturns = selected_data_returns.mul(wallet_weights, axis=1).sum(axis=1)[-255:]*100
    fig, ax = plt.subplots()
    plt.xlabel('Retorno (%)')
    plt.ylabel('Quantidade de dias que este retorno acontece')
    # Plota o histograma da curva normal
    sns.histplot(walletReturns, kde=True, bins=30)
    st.pyplot(fig)

    
def portfolio_page():

    st.header('Simule sua carteira')	
	st.write("Vamos simular uma carteira! Para isso, use as informações da tabela para escolher suas ações, escolha as ações e clique no botão no fim da página para conferir os resultados."
	st.write("Utilize a barra abaixo para selecionar o período para construção das estatísticas. Na tabela, você observa informações importantes como média de retornos (uma média mais alta quer dizer que o ativo costuma crescer mais), uma ideia de quanto o valor da ação oscila (dada pela informação da nossa expectativa sobre a maioria dos retornos diários) e o retorno acumulado em todo o período selecionado. Depois de escolher suas ações ")

    tempo = st.slider('Escolha o tempo para fazer a análise das ações (ANOS)', 1, 4, step=1, value=2)
    st.write(f'### Use a tabela abaixo para escolher as ações baseando-se nos dados dos últimos {tempo} anos:')

    dados = data.loc[str(int(data.index[-1][:4]) - tempo)+data.index[-1][4:]:]
    st.write("A ideia aqui é escolher as maiores médias de retornos com os menores riscos. Queremos que 95% dos retornos diários estejam entre valores baixos, pois dessa forma a volatilidade é baixa (é apenas outra forma de representar a volatilidade).")
    data_returns = dados.pct_change()[1:]
    cumulative_returns = (data_returns+1).cumprod(axis=0)
    cumulative_returns = ((cumulative_returns-1)*100).iloc[-1]
    returns_var = data_returns.var()
    returns_deltas = (2*np.sqrt(returns_var))*100
    returns_means = data_returns.mean()*100
    #st.write(cumulative_returns)
    summary = pd.concat([returns_means, returns_deltas, cumulative_returns], axis = "columns")
    
    summary.rename(columns = {list(summary)[0]:'Média dos retornos (%)', 1:"~95% dos retornos diários entre +- (%)", "2023-03-10":"Retorno acumulado no periodo (%)"}, inplace = True)
    st.write(summary)


    col1, col2 = st.columns(2)
    with col1:

        selected_stocks = st.multiselect('Selecione as ações', data.columns, default=data.columns[0])
    with col2:
        wallet_percentages = {}
        for stock in selected_stocks:
            wallet_percentages[stock] = st.slider(f'Valor investido na {stock} (R$)', 0, 1000, 10)
    
    st.write("Valor total investido na carteira: " + str(sum(wallet_percentages.values())))
    #st.write("As porcentagens de cada ação serao normalizadas para somar 100%")
    if(st.button("Mostrar resultados da carteira:")):
        DisplayResults(selected_stocks, wallet_percentages)
    # Alguns cálculos para adiantar para o usuário
    



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

