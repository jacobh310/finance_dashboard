import pandas as pd
import re
import emoji




def cleaner(tweet):
    tweet = re.sub(r"RT @[\w]*:","",tweet)
    tweet = re.sub("@[A-Za-z0-9]+","",tweet) #Remove @ sign
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
    tweet = re.sub(r"[^a-zA-Z\s]","",tweet)
    tweet = " ".join(tweet.split())
    tweet = ''.join(c for c in tweet if c not in emoji.UNICODE_EMOJI) #Remove Emojis
    tweet = tweet.replace("#", "").replace("_", " ").replace('*','').replace('$','') #Remove hashtag sign but keep the text

    return tweet

if __name__ == "__main__":

    tweets = pd.read_csv('data_scrappers\\tweets.csv', index_col=0)
    wsb_titles = pd.read_csv('data_scrappers\\wsb_title.csv')

    tweets.columns = ['Date','Ticker','Tweet']
    tweets['Tweet'] = tweets['Tweet'].map(lambda x: cleaner(x))
    tweets['Date'] =  pd.to_datetime(tweets['Date']).dt.date
    tweets.to_csv('clean_tweets.csv', index=False)



    wsb_titles.columns = ['Ticker','Title','Date']
    wsb_titles['Title'] = wsb_titles['Title'].map(lambda  x: cleaner(x))
    wsb_titles['Date'] = pd.to_datetime(wsb_titles['Date'],utc=True, unit='s').dt.date
    wsb_titles.to_csv('clean_wsb_titles.csv', index=False)

