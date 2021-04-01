import pandas as pd
import numpy as np
import yfinance as yf
from twitter_scraper import get_tweets
from datetime import datetime, timedelta
import datetime as dt
import time



# print(tweets_df)
# wsb_tickers = pd.read_csv('D:\\Github\\financial_dashboard\data_scrappers\\wsb_tickers.csv',names=['Tickers'],header =0)
# wsb_tickers = wsb_tickers.sort_values(by = 'Tickers', ascending=False)
# top_15_tickers = wsb_tickers.head(15).index
# top_15_comp_name = [yf.Ticker(ticker).info['shortName'].split()[0] for ticker in top_15_tickers]