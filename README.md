# Wariskmin - **Wa**llet Data Visualization for **Risk** **Min**imization

This project is a Python-based visualization tool that aims to help investors minimize risks while building a diversified portfolio. It calculates the covariance and distance of stock prices time series and uses clustering algorithms to group stocks based on their correlation, allowing users to visualize and gain insights about risk on their wallets.

The software is built using the following libraries:

* Streamlit: A web framework for building interactive data-driven applications.
* NumPy: A fundamental package for scientific computing with Python.
* yfinance:  provides an easy-to-use interface for retrieving historical market data, such as stock prices, dividends, and splits, from Yahoo Finance. Not affiliated, endorsed, or vetted by Yahoo, Inc. It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for **research and educational purposes**. 

This project is being developed in the context of the *CMP596 - Visual Analytics for Data Science* course in the [PPGC program at INF/UFRGS](https://www.inf.ufrgs.br/ppgc/), and is not intended for commercial use.

# Getting Started

To use this software, follow these steps:

1. Clone the repository to your local machine.
2. Create and activate a new virtual environment by running the following commands:

> cd wallet-data-visualization
> 
> pipenv install
> 
> pipenv shell
> 

3. Download the sample data by running "python3 ./sample-downloader.py"
4. Launch the application by running ''streamlit run wariskmin.py'' in your terminal.

# License

This project is licensed under the MIT License. For more information, see the LICENSE file.

# ROADMAP

* DONE: *Chat with finance professionals in order to gather requirements and interesting features to the project. Show presentation and develop details of the Roadmap. Divide roadmap by weeks.*
* DONE: *Save data for offline usage.*
* DONE: *Explore basic pairwise correlations.*
* DONE: *Check if Bokeh is compatible with Streamlit or if I'll need to work with Altair.* RESULT: It is not compatible, but I can you either Altair or Matplotlib and Seaborn.
* DONE: Make first data visualizations and implement side panel.
* DONE: Insert current news widget
* Make a wallet construction page including: dropdown menu of stocks selection showing calculated volatility, estimated returns and potential losses.
* Interesting useful data source and API: http://www.ipeadata.gov.br/Default.aspx. Implement usage of this (to obtain benchmark data)

The author is enthusiastic about ChatGPT and will be using it for bits and pieces throughout the project, like the creation of this readme file. The chat couldn't make a complete the readme file, but helped by building a sketch.

# Contact Information

For questions or comments about this project, please contact the author at jan.luc@ufrgs.br 
