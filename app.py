import streamlit as st
import util
st.set_page_config(layout="wide")
from data_scrappers import financial_scraper as fs
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd

st.markdown("<h1 style='text-align: center; color:#295E61 ;'>Financial Dashboard</h1>",
            unsafe_allow_html=True)

options = ('Fundamentals','Sentiment Analysis','Price Forecaster')
dashboard = st.sidebar.selectbox('Which Dashboard',options,index=1)

if dashboard == options[0]:


    stocks = ("AAPL", "GOOG", "MSFT", "TSLA", "AMD")
    ticker = st.selectbox('Which stock?', stocks)

    price_data = yf.Ticker(ticker).history(period='3y', interval='1d').drop(columns=['Volume','Dividends','Stock Splits'])

    st.plotly_chart(util.plot_candle_sticks(ticker,price_data))

    st.markdown("<h2 style='text-align: center; color:#295E61 ;'>Fundamentals and Metrics</h2>",
                unsafe_allow_html=True)

    col1, col2 = st.beta_columns(2)

    yearly, quarter = fs.get_metrics(ticker)

    col1.markdown("<h2 style='text-align: left; color:#295E61 ;'>Yearly Metrics</h2>",  unsafe_allow_html=True)
    yearly = yearly.astype(float).round(3)
    col1.dataframe(yearly.T)

    col1.plotly_chart(util.plot_metrics(yearly,1000))

    col2.markdown("<h2 style='text-align: left; color:#295E61 ;'>Quarterly Metrics</h2>",  unsafe_allow_html=True)
    quarter = quarter.astype(float).round(3)
    col2.dataframe(quarter.T, height = 350)

    col2.plotly_chart(util.plot_metrics(quarter,3000))

if dashboard == options[1]:

    col1, col2 = st.beta_columns(2)
    twitter_sentiments = util.get_twitter_sentiment()
    wsb_sentiments = util.get_wsb_sentiment()

    twitter_avg_sent = twitter_sentiments.groupby('ticker').mean()['compound']
    wsb_avg_sent = wsb_sentiments.groupby('ticker').mean()['compound']

    col1.header('Twitter')
    col1.plotly_chart(util.weekly_sent_bar(twitter_avg_sent))

    col2.header('Wall Street Bets')
    col2.plotly_chart(util.weekly_sent_bar(wsb_avg_sent))

    st.markdown("<h2 style='text-align: center; color:#295E61 ;'>Twitter  Sentiment over the Past  7 days</h2>",  unsafe_allow_html=True)
    avg_sent_day = twitter_sentiments.groupby(['ticker','tweet_date']).mean()['compound']
    st.plotly_chart(util.daily_sent(avg_sent_day,twitter_avg_sent.index))
