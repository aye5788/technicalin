import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

# Alpha Vantage API key
API_KEY = 'CLP9IN76G4S8OUXN'

# Function to fetch data from Alpha Vantage
def fetch_data(symbol, interval='1min'):
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize='full')
    return data

# Function to calculate and plot technical indicators (e.g., SMA, RSI)
def plot_technical_analysis(data, symbol):
    fig, ax = plt.subplots(figsize=(10,6))
    
    # Plotting the price data
    ax.plot(data['close'], label='Close Price', color='blue')
    
    # Simple Moving Average (SMA)
    ax.plot(data['close'].rolling(window=14).mean(), label='SMA 14', color='red')
    
    # Relative Strength Index (RSI)
    ax2 = ax.twinx()
    rsi = 100 - (100 / (1 + (data['close'].diff().clip(lower=0).rolling(window=14).mean() /
                             data['close'].diff().clip(upper=0).abs().rolling(window=14).mean())))
    ax2.plot(rsi, label='RSI', color='green')
    ax2.axhline(70, linestyle='--', color='red')
    ax2.axhline(30, linestyle='--', color='green')
    
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.set_title(f"Technical Analysis for {symbol}")
    st.pyplot(fig)

# Streamlit UI for user input
st.title("Stock Technical Analysis Dashboard")
ticker = st.text_input("Enter the Stock Ticker Symbol", "AAPL")
timeframe = st.selectbox("Select Timeframe", ['1min', '2min', '5min', '1hour', '4hour'])

# Fetch data and display analysis
if ticker:
    st.write(f"Fetching data for {ticker} with {timeframe} interval...")
    data = fetch_data(ticker, interval=timeframe)
    st.write(f"Data for {ticker}:")
    st.write(data.tail())
    plot_technical_analysis(data, ticker)
