# This app is for educational purpose only. Insights gained is not financial advice. Use at your own risk!
import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import math
# ---------------------------------#
# New feature (make sure to upgrade your streamlit library)
# pip install --upgrade streamlit
# psycopg2.connect()
# connect to database
# con = psycopg2.connect(database="crytocoins", user="", password="1234", host="localhost", port=5432)
# print("Not Database opened successfully")
# ---------------------------------#
# Page layout
# # Page expands to full width
st.set_page_config(layout="wide")
# ---------------------------------#
# Title

image = Image.open('logo.jpg')

st.image(image, width=500)

st.title('Crypto Price App')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **CoinMarketCap**!
""")
# ---------------------------------#
# About
# This is an expander bar to add additional information about the app/page
expander_bar = st.beta_expander("About Crypto Price App")
# Expander bar markdown are the information in the expander bar when clicked
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
* **Data source:** [CoinMarketCap](http://coinmarketcap.com).
* **Credit:** Web scraper adapted from the Medium article *[Web Scraping Crypto Prices With Python]
(https://towardsdatascience.com/web-scraping-crypto-prices-with-python-41072ea5b5bf)* written by [Bryan Feng]
(https://medium.com/@bryanf).
""")


# ---------------------------------#
# Page layout (continued)
#  Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.beta_columns((2, 1))

# ---------------------------------#
# Sidebar + Main panel
col1.header('Input Options')

# Sidebar - Currency price unit
currency_per_unit = col1.selectbox('Select currency for price', ('GBP', 'USD', 'BTC', 'ETH', 'INR', 'EUR', 'AUD', 'CAD',
                                                                 'SGD', 'CHF', 'MYR', 'JPY', 'CNY', 'NZD', 'THB', 'HUF',
                                                                 'AED', 'HKD', 'MXN', 'ZAR'))
# Select the number of coins to be displayed. N on this slider represent the number of pages of coins to be web scraped
# on https://coinmarketcap.com/coins.com when each page contains up 10 100 coins
# number_of_coins = col1.slider('Display N hundreds of Coins', 1, 11, 11)

# Web scraping of CoinMarketCap data
# Sidebar - Number of coins to display
num_coin = col1.slider('Select the top N Number of Coins for Display', 1, 1100, 1100)
# Check the number of pages of coins to be web scraped on https://coinmarketcap.com/coins.com when each page
# contains up 10 100 coins
number_of_pages = math.ceil(num_coin/100)


@st.cache
def load_data():
    currency_price_unit = currency_per_unit
    currency_converter = 1.0
    if currency_per_unit not in ['USD', 'BTC', 'ETH']:
        # Load exchange url with the selected currency at the end
        url = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=" + currency_price_unit
        # use pandas for web scraping the data for that currency
        html = pd.read_html(url, header=0)
        # Use the second table in the dataframe indexed 1
        df_currency = html[1]
        # The data will be in the table with two columns, the first been USD and the second the selected currency.
        # Since we don't know which currency has been
        # selected we use iloc to select the first row and second column which will be the price of 1 USD in the
        # selected currency which all then converted to float
        currency_converter = float(df_currency.iloc[0][1][:-4])
        currency_price_unit = 'USD'
    coin_data = {}

    df_all = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h',
                                   'percent_change_7d', 'price', 'volume_24h'])
    # Use a for loop to iterate through every page with coins data to web scrap the data
    for number in range(1, number_of_pages + 1):
        url_page = 'https://coinmarketcap.com/coins/?page=' + str(number)
        cmc = requests.get(url_page)
        soup = BeautifulSoup(cmc.content, 'html.parser')

        data = soup.find('script', id='__NEXT_DATA__', type='application/json')
        coins = {}
        coin_data.update(json.loads(data.contents[0]))

        listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
        # Check exchange price if not using USD, BTC or ETH and use https://www.xe.com/currencyconverter to get
        # the current exchange rate for that currency

        for i in listings:
            coins[str(i['id'])] = i['slug']

        coin_name = []
        coin_symbol = []
        market_cap = []
        percent_change_1h = []
        percent_change_24h = []
        percent_change_7d = []
        price = []
        volume_24h = []

        for i in listings:
            coin_name.append(i['slug'])
            coin_symbol.append(i['symbol'])
            price.append(i['quote'][currency_price_unit]['price'] * currency_converter)
            percent_change_1h.append(i['quote'][currency_price_unit]['percentChange1h'] * currency_converter)
            percent_change_24h.append(i['quote'][currency_price_unit]['percentChange24h'] * currency_converter)
            percent_change_7d.append(i['quote'][currency_price_unit]['percentChange7d'] * currency_converter)
            market_cap.append(i['quote'][currency_price_unit]['marketCap'] * currency_converter)
            volume_24h.append(i['quote'][currency_price_unit]['volume24h'] * currency_converter)

        df1 = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h',
                                    'percent_change_7d', 'price', 'volume_24h'])
        df1['coin_name'] = coin_name
        df1['coin_symbol'] = coin_symbol
        df1['price'] = price
        df1['percent_change_1h'] = percent_change_1h
        df1['percent_change_24h'] = percent_change_24h
        df1['percent_change_7d'] = percent_change_7d
        df1['market_cap'] = market_cap
        df1['volume_24h'] = volume_24h

        frames = [df_all, df1]
        df_all = pd.concat(frames)
        df_all.reset_index(drop=True, inplace=True)
    return df_all


df = load_data()

# Sidebar - Cryptocurrency selections
sorted_coin = sorted(df['coin_symbol'])
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)
# Filtering data
df_selected_coin = df[(df['coin_symbol'].isin(selected_coin))]


df_coins = df_selected_coin[:num_coin]

# Sidebar - Percent change timeframe
percent_timeframe = col1.selectbox('Percent change time frame', ['7d', '24h', '1h'])
percent_dict = {"7d": 'percent_change_7d', "24h": 'percent_change_24h', "1h": 'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

# Sidebar - Sorting values
sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

col2.subheader('Price Data of Selected Cryptocurrency')
col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1])
           + 'columns.')

col2.dataframe(df_coins)

# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806


def filedownload(df_data):
    csv = df_data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href


col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

# ---------------------------------#
# Preparing data for Bar plot of % Price change
col2.subheader('Table of % Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h,
                       df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
col2.dataframe(df_change)

# Conditional creation of Bar plot (time frame)
col3.subheader('Bar plot of % Price Change')

if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_7d'])
    col3.write('*7 days period*')
    plt.figure(figsize=(5, 25))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g',
                                                                                                     False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_24h'])
    col3.write('*24 hour period*')
    plt.figure(figsize=(5, 25))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g',
                                                                                                       False: 'r'}))
    col3.pyplot(plt)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_1h'])
    col3.write('*1 hour period*')
    plt.figure(figsize=(5, 25))
    plt.subplots_adjust(top=1, bottom=0)
    df_change['percent_change_1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g',
                                                                                                     False: 'r'}))
    col3.pyplot(plt)
# End of code
