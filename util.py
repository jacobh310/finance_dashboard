import  plotly.graph_objs as go
from plotly.subplots import make_subplots
import yfinance as yf
import pandas as pd
from data_base import TwitterSentiment, WsbSentiment
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker



def plot_candle_sticks(ticker, price_data):
    days = 200
    fig = go.Figure()
    fig.add_trace(
         go.Candlestick(x=price_data.reset_index()['Date'][days:],
                        open=price_data['Open'][days:],
                        high=price_data['High'][days:],
                        low=price_data['Low'][days:],
                        close=price_data['Close'][days:],
                        name='Candle stick'))

    fig.add_trace(go.Scatter(x=price_data.reset_index()['Date'][days:],
                             y=price_data['Close'].rolling(window=15).mean()[days:],
                             line=dict(color='purple', width=1),
                            name='15 Day Moving Average'))

    fig.add_trace(go.Scatter(x=price_data.reset_index()['Date'][days:],
                             y=price_data['Close'].rolling(window=50).mean()[days:],
                             line=dict(color='orange', width=1),
                            name='50 Day Moving Average'))

    fig.add_trace(go.Scatter(x=price_data.reset_index()['Date'][days:],
                             y=price_data['Close'].rolling(window=200).mean()[days:],
                             line=dict(color='blue', width=1),
                            name='200 Day Moving Average'))


    fig.layout.update(title=f'{ticker} Stock Price Chart for the past 2 years', yaxis_title="Stock Price ($)",
                      margin=dict(b=20),
                      font=dict(size=20),
                      width=1700,
                      height=700)
    return fig

def plot_metrics(df,df2,height):

    fig = make_subplots(
        rows=len(df.columns) + 1 , cols=1,
        subplot_titles=(df.columns))
    i = 1
    for col in df.columns:

        fig.add_trace(
            go.Scatter(x=df.index, y=df[col],
                       line=dict(color='blue', width=1)),
            row=i, col=1)
        fig.add_trace\
            (go.Scatter(x=df2.index, y=df2[col],
                line=dict(color='red', width=1)),
        row=i, col=1)
        i += 1


    fig.update_layout(height=height, width=850, showlegend= False)

    return fig

def get_twitter_sentiment():

    engine = create_engine('postgresql://postgres:chivas101@localhost:5432/Sentiment')

    df = pd.read_sql("""SELECT 
        tweet_date, 
        ticker, 
        compound
    FROM twitter_sentiment
    where tweet_date > current_date - interval '9 days'""", engine)

    return df

def get_wsb_sentiment():
    engine = create_engine('postgresql://postgres:chivas101@localhost:5432/Sentiment')

    df = pd.read_sql("""SELECT 
        date_added,
        ticker, 
        compound
    FROM wsb_sentiment
    where date_added > current_date - interval '9 days'""", engine)

    return df

def weekly_sent_bar(df):
    fig=go.Figure()
    fig.add_trace(go.Bar(x=df.index,y=df, textposition='auto'))
    fig.update_layout(title= 'Average Weekly Sentiment',
                       margin=go.layout.Margin(b=0),
                       width=800,
                       height=600)

    return fig

def daily_sent(df,tickers):
    fig=go.Figure()

    for ticker in tickers:
        fig.add_trace(go.Scatter(x=df.loc[ticker].index,
                                 y= df.loc[ticker],
                                name=ticker))

    fig.update_layout(title = 'Average Daily Sentiment',
                    height=800,
                    width=1500,
                    margin=dict(b=10,t=26))
    return fig

def recommendations(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df.index, y=df, textposition='auto'))
    fig.update_layout( margin=go.layout.Margin(b=0,t=15),
                       width=800,
                       height=600)
    return fig