import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import warnings
warnings.filterwarnings("ignore")



def sentiment_df(df,col):
    analyzer = SentimentIntensityAnalyzer()
    df['compound'] = [analyzer.polarity_scores(x)['compound'] for x in df[col]]
    df['neg'] = [analyzer.polarity_scores(x)['neg'] for x in df[col]]
    df['neu'] = [analyzer.polarity_scores(x)['neu'] for x in df[col]]
    df['pos'] = [analyzer.polarity_scores(x)['pos'] for x in df[col]]

    return df.drop(columns = col)


if __name__ == "__main__":

    tweets = pd.read_csv('data_cleaning\\clean_tweets.csv')
    tweets = tweets.dropna()

    wsb_titles = pd.read_csv('data_cleaning\\clean_wsb_titles.csv')
    wsb_titles = wsb_titles.dropna()



    tweet_sentiments = sentiment_df(tweets,'Tweet')
    wsb_title_sentiments = sentiment_df(wsb_titles, 'Title')

    tweet_sentiments.to_csv('tweet_sentiments.csv', index=False)
    wsb_title_sentiments.to_csv('wsb_titles_sentiments.csv', index=False)

