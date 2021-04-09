import pandas as pd
import time
import tweepy
import config


def get_tweets():

    auth = tweepy.OAuthHandler(config.key, config.key_secret)
    auth.set_access_token(config.token, config.token_secret)

    api = tweepy.API(auth,wait_on_rate_limit=True)

    wsb_tickers = pd.read_csv('D:\\Github\\financial_dashboard\data_scrappers\\wsb_tickers.csv',names=['Tickers'],header =0)
    wsb_tickers = wsb_tickers.sort_values(by = 'Tickers', ascending=False)
    top_15_tickers = wsb_tickers.head(15).index
    # top_15_comp_name = [yf.Ticker(ticker).info['shortName'].split()[0] for ticker in top_15_tickers]

    count = 10000

    df = pd.DataFrame()
    for ticker in top_15_tickers:
        try:
            # Creation of query method using parameters
            tweets = tweepy.Cursor(api.search, q=ticker,count=450, lang='en',result_type='mixed').items(count)

            # Pulling information from tweets iterable object
            tweets_list = [[tweet.created_at, ticker, tweet.text] for tweet in tweets]

            # Creation of dataframe from tweets list
            # Add or remove columns as you remove tweet information
            tweets_df = pd.DataFrame(tweets_list)
            df = df.append(tweets_df,ignore_index=True)
        except BaseException as e:
            print('failed on_status,', str(e))
            time.sleep(3)

    return df
if __name__ == "__main__":

    df = get_tweets()
    df.to_csv('tweets.csv')
