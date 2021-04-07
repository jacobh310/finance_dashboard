import pandas as pd
import numpy as np
import re
import emoji

tweets = pd.read_csv('D:\\Github\\financial_dashboard\data_scrappers\\tweets.csv', index_col=0)
wsb_titles = pd.read_csv('D:\\Github\\financial_dashboard\data_scrappers\\wsb_title.csv')
wsb_titles = pd.melt(wsb_titles, var_name='Ticker', value_name='Title').dropna()

def cleaner(tweet):
    tweet = re.sub(r"RT @[\w]*:","",tweet)
    tweet = re.sub("@[A-Za-z0-9]+","",tweet) #Remove @ sign
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
    tweet = re.sub(r"[^a-zA-Z\s]","",tweet)
    tweet = " ".join(tweet.split())
    tweet = ''.join(c for c in tweet if c not in emoji.UNICODE_EMOJI) #Remove Emojis
    tweet = tweet.replace("#", "").replace("_", " ").replace('*','').replace('$','') #Remove hashtag sign but keep the text

    return tweet

tweets.columns = ['Date','Ticker','Tweet']
tweets['Tweet'] = tweets['Tweet'].map(lambda x: cleaner(x))
tweets['Date'] =  pd.to_datetime(tweets['Date']).dt.date
tweets.to_csv('clean_tweets.csv', index=False)


for col in wsb_titles.columns:
    wsb_titles[col] = wsb_titles[col].map(lambda x: np.nan if pd.isna(x)  else cleaner(x))

wsb_titles.to_csv('clean_wsb_titles.csv', index=False)