import streamlit as st
import util
st.set_page_config(layout="wide")
from data_scrappers import financial_scraper as fs
import yfinance as yf
import pandas as pd

st.markdown("<h1 style='text-align: center; color:#295E61 ;'>Financial Dashboard</h1>",
            unsafe_allow_html=True)

options = ('Fundamentals','Twitter and Reddit Sentiment Analysis','Stock Sentiment Analysis')
dashboard = st.sidebar.selectbox('Which Dashboard',options,index=2)

if dashboard == options[0]:

    tickers = pd.read_csv('D:\\Github\\financial_dashboard\data_scrappers\\tickers.csv', header=None, names=['Tickers'])
    tickers['Tickers'] = tickers['Tickers'].str[:-2]
    tickers = tickers['Tickers'].tolist()

    ticker = st.selectbox('Which stock?', tickers , index=tickers.index('AAPL'))

    price_data = yf.Ticker(ticker).history(period='3y', interval='1d').drop(columns=['Volume','Dividends','Stock Splits'])

    st.plotly_chart(util.plot_candle_sticks(ticker,price_data))

    st.markdown("<h2 style='text-align: center; color:#295E61 ;'>Fundamentals and Metrics</h2>",
                unsafe_allow_html=True)

    ticker2 = st.selectbox('Stock to compare to', tickers , index=tickers.index('AAPL'))

    col1, col2 = st.beta_columns(2)

    yearly, quarter = fs.get_metrics(ticker)
    yearly2, quarter2 = fs.get_metrics((ticker2))

    col1.markdown(f"<h2 style='text-align: left; color:#295E61 ;'>{ticker} Yearly Metrics</h2>",  unsafe_allow_html=True)
    yearly = yearly.astype(float).round(3)
    col1.dataframe(yearly.T)

    col1.markdown(f"<body style='text-align: left; color:#0000FF ;'>{ticker}</body>", unsafe_allow_html=True)
    col1.markdown(f"<body style='text-align: left; color:#FF0000 ;'>{ticker2}</body>", unsafe_allow_html=True)

    col1.plotly_chart(util.plot_metrics(yearly,yearly2, 1500))
    col1.header(f'Yahoo Analyst Recommendations for {ticker}')
    col1.plotly_chart(util.recommendations(fs.get_reccomendations(ticker)))

    col2.markdown(f"<h2 style='text-align: left; color:#295E61 ;'>{ticker} Quarterly Metrics</h2>",  unsafe_allow_html=True)
    quarter = quarter.astype(float).round(3)
    col2.dataframe(quarter.T, height = 350)

    col2.markdown(f"<body style='text-align: left; color:#0000FF ;'>{ticker}</body>",  unsafe_allow_html=True)
    col2.markdown(f"<body style='text-align: left; color:#FF0000 ;'>{ticker2}</body>",  unsafe_allow_html=True)

    col2.plotly_chart(util.plot_metrics(quarter,quarter2,3500))

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

    st.markdown("<h2 style='text-align: center; color:#295E61 ;'>Twitter Sentiment over the Past  7 days</h2>",  unsafe_allow_html=True)
    avg_sent_day = twitter_sentiments.groupby(['ticker','tweet_date']).mean()['compound']
    st.plotly_chart(util.daily_sent(avg_sent_day,twitter_avg_sent.index))


if dashboard == options[2]:
    tickers = pd.read_csv('D:\\Github\\financial_dashboard\data_scrappers\\tickers.csv', header=None, names=['Tickers'])
    tickers['Tickers'] = tickers['Tickers'].str[:-2]
    tickers = tickers['Tickers'].tolist()

    ticker = st.selectbox('Which stock?', tickers, index=tickers.index('AAPL'))
    num_tweets = st.slider(min_value=500,
                           max_value=5000,
                           label="Number of tweets",
                           step = 100,
                           value=1000)
    df = util.tweet_sent_for_stock(ticker,num_tweets)
    avg_daily_sentiment = df.groupby('Date').mean()['compound']
    st.dataframe(avg_daily_sentiment)
    st.plotly_chart(util.plot_daily_sent(avg_daily_sentiment))