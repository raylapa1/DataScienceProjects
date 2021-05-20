import yfinance as yf
import streamlit as st
#import pandas as pd

st.write("""
# Simple Stock Price App

Shown are the stock **closing price** and **volume** of Google!
""")

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
tickerSymbol = 'GME'#'GOOGL'


#get data on this ticker

tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2021-4-21', end='2022-6-21')
# Open	High	Low	Close	Volume	Dividends	Stock Splits
st.write("""
## Closing price of Google
""")
st.line_chart(tickerDf.Close)
st.write("""
## Volume of Google shares
""")
st.line_chart(tickerDf.Volume)