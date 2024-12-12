import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from alpha_vantage.timeseries import TimeSeries
import talib

# Alpha Vantage API key
API_KEY = 'CLP9IN76G4S8OUXN'

# Function to fetch data from Alpha Vantage
def fetch_data(symbol, interval='1min'):
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize='full')
    return data

# Function to calculate and plot technical indicators (e.g., SMA, RSI, MACD)
def plot_technical_analysis(data, symbol):
    # Plot candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['1. open'],
        high=data['2. high'],
        low=data['3. low'],
        close=data['4. close'],
        name='Candlesticks'
    )])

    # Add Moving Average (SMA)
    sma = talib.SMA(data['4. close'], timeperiod=14)
    fig.add_trace(go.Scatter(x=data.index, y=sma, mode='lines', name='SMA 14'))

    # Add RSI
    rsi = talib.RSI(data['4. close'], timeperiod=14)
    fig.add_trace(go.Scatter(x=data.index, y=rsi, mode='lines', name='RSI'))

    # Display the chart
    st.plotly_chart(fig)

    # Display Textual Interpretation
    last_price = data['4. close'][-1]
    sma_last = sma[-1]
    rsi_last = rsi[-1]

    interpretation = f"**Latest Price:** {last_price:.2f}\n\n"
    
    if last_price > sma_last:
        interpretation += "Price is above the SMA 14, indicating a bullish trend.\n"
    else:
        interpretation += "Price is below the SMA 14, indicating a bearish trend.\n"
    
    if rsi_last > 70:
        interpretation += "RSI is above 70, indicating the stock may be overbought.\n"
    elif rsi_last < 30:
        interpretation += "RSI is below 30, indicating the stock may be oversold.\n"
    else:
        interpretation += "RSI is within a neutral range.\n"
    
    st.text_area("Technical Analysis Interpretation", interpretation, height=300)

# Streamlit UI for user input
st.title("Stock Technical Analysis Dashboard")
ticker = st.text_input("Enter the Stock Ticker Symbol", "AAPL")
timeframe = st.selectbox("Select Timeframe", ['1min', '2min', '5min', '1hour', '4hour'])

# Fetch data and display analysis
if ticker:
    st.write(f"Fetching data for {ticker} with {timeframe} interval...")
    data = fetch_data(ticker, interval=timeframe)
    plot_technical_analysis(data, ticker)
