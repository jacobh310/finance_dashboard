import  plotly.graph_objs as go
from plotly.subplots import make_subplots
import yfinance as yf
import pandas as pd



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

def plot_metrics(df,height):
    fig = make_subplots(
        rows=len(df)+1, cols=1,
        subplot_titles=(df.columns))
    i = 1
    for col in df.columns:

        fig.add_trace(
            go.Scatter(x=df.index, y=df[col]),
            row=i, col=1
        )
        i += 1


    fig.update_layout(height=height, width=850, showlegend=False)

    return fig
