import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import warnings
warnings.filterwarnings("ignore")


tweets = pd.read_csv('D:\\Github\\financial_dashboard\data_cleaning\\clean_tweets.csv')
tweets = tweets.dropna()

wsb_titles = pd.read_csv('D:\\Github\\financial_dashboard\data_cleaning\\clean_wsb_titles.csv')
wsb_titles = wsb_titles.dropna()
# wsb_titles = pd.melt(wsb_titles, var_name='Ticker', value_name='Title').dropna()
analyzer = SentimentIntensityAnalyzer()


def sentiment_df(df,col):

    df['compound'] = [analyzer.polarity_scores(x)['compound'] for x in df[col]]
    df['neg'] = [analyzer.polarity_scores(x)['neg'] for x in df[col]]
    df['neu'] = [analyzer.polarity_scores(x)['neu'] for x in df[col]]
    df['pos'] = [analyzer.polarity_scores(x)['pos'] for x in df[col]]

    return df.drop(columns = col)

tweet_sentiments = sentiment_df(tweets,'Tweet')
wsb_title_sentiments = sentiment_df(wsb_titles, 'Title')

tweet_sentiments.to_csv('tweet_sentiments.csv', index=False)
wsb_title_sentiments.to_csv('wsb_titles_sentiments.csv', index=False)

