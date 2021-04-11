import yfinance as yf
import pandas as pd
import datetime as dt

# ticker = 'AAPL'

def get_metrics(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'

    valuation = pd.read_html(url)[0]
    valuation.columns = ['Metrics','Current']  + [i for i in valuation.columns[2:]]
    valuation['Metrics'] = valuation['Metrics'].apply(lambda x: x[:-1] if x[-1].isnumeric() else x)
    valuation.set_index('Metrics', inplace=True)

    valuation.columns =[dt.date.today()] + [dt.datetime.strptime(i, '%m/%d/%Y').date() for i in valuation.columns[1:]]
    valuation = valuation.T

    return  valuation

def clean_val(df):
    df[df.columns[0]] = df[df.columns[0]].apply(lambda x:float(x[:-1])*1000000000000 if x[-1]=='T' else float(x[:-1]) *1000000000 )
    df[df.columns[1]] = df[df.columns[1]].apply(lambda x:float(x[:-1])*1000000000000 if x[-1]=='T' else float(x[:-1]) *1000000000 )
    df = df.apply(pd.to_numeric, errors='coerce')

    return  df


def get_summary(ticker):
    stock = yf.Ticker(ticker)
    overview = pd.Series(stock.info, name='Overview')

    summary = pd.Series({
            'Previous Close': overview['previousClose'],
            'Market Cap' : overview['marketCap'],
            'Enterprise Value': overview['enterpriseValue'],
            'EV/Revenue': overview['enterpriseToRevenue'],
            'EV/EBIDTA': overview['enterpriseToEbitda'],
            '52 week high': overview['fiftyTwoWeekHigh'],
            '52 week low': overview['fiftyTwoWeekLow']},
        name='Overview')

    return summary

# summary = get_summary(ticker)

def get_reccomendations(ticker):
    stock = yf.Ticker(ticker)
    recomends = stock.recommendations
    recomends =recomends['To Grade'].value_counts()

    return recomends

# rec = get_reccomendations(ticker)

