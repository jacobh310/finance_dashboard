from sqlalchemy import  create_engine, Column, Float, DateTime, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import  pandas as pd
from data_scrappers import reddit_scraper, reddit_post_scrapper, twitter_scraper_
from data_cleaning import data_cleaning
from Sentiment_analysis import vader_model
import config

Base = declarative_base()

class TwitterSentiment(Base):
    __tablename__ = 'twitter_sentiment'

    id = Column('id',Integer, primary_key=True)
    tweet_date = Column('tweet_date',DateTime)
    date_added = Column('date_added',DateTime, default=datetime.date.today() )
    ticker = Column('ticker', String)
    compound=Column('compound',Float)
    neg=Column('neg', Float)
    neu=Column('neu',Float)
    pos=Column('pos',Float)

class WsbSentiment(Base):
    __tablename__ = 'wsb_sentiment'

    id = Column('id',Integer, primary_key=True)
    date_posted = Column('date_posted',DateTime)
    date_added = Column('date_added',DateTime, default=datetime.date.today() )
    ticker = Column('ticker', String)
    compound=Column('compound',Float)
    neg=Column('neg', Float)
    neu=Column('neu',Float)
    pos=Column('pos',Float)



def add_to_wsb():
    Session = sessionmaker(bind=engine)
    session = Session()

    for i, row in wsb_sentiments.iterrows():
        entry = WsbSentiment(ticker = row['Ticker'],
                            compound= row['compound'],
                             date_posted = row['Date'],
                             neg = row['neg'],
                             neu = row['neu'],
                             pos=row['pos'])

        session.add(entry)
        session.commit()

    session.close()



def add_to_twitter():
    Session = sessionmaker(bind=engine)
    session = Session()

    for i, row in twitter_sentiments.iterrows():
        entry = TwitterSentiment(tweet_date = row['Date'],
                            ticker = row['Ticker'],
                            compound= row['compound'],
                             neg = row['neg'],
                             neu = row['neu'],
                             pos=row['pos'])

        session.add(entry)
        session.commit()

    session.close()


if __name__ == "__main__":

    # scrapes the most popular tickers from wsb
    wsb_tickers = reddit_scraper.get_tickers()
    wsb_tickers = wsb_tickers.sort_values(ascending=False)
    top_15_tickers = wsb_tickers.head(15).index
    print('Finished Scrapping Most Popular Tickers on WSB. Now Scrapping the the WSB titles')
    # scrapes titles from popular tickers on wbs
    wsb_titles = reddit_post_scrapper.scrape_posts(top_15_tickers)

    # scrapes tweets that contain popular tickers from wsb
    print("Finished Scrapping wsb titles. Now scrapping twitter")
    tweets = twitter_scraper_.get_tweets()

    print('Cleaning tweets')
    #cleans tweets
    tweets.columns = ['Date','Ticker','Tweet']
    tweets['Tweet'] = tweets['Tweet'].map(lambda x: data_cleaning.cleaner(x))
    tweets['Date'] =  pd.to_datetime(tweets['Date']).dt.date

    print('Cleaning titles from WSB')
    # cleans titles from wsb
    wsb_titles.columns = ['Ticker', 'Title', 'Date']
    wsb_titles['Title'] = wsb_titles['Title'].map(lambda x: data_cleaning.cleaner(x))
    wsb_titles['Date'] = pd.to_datetime(wsb_titles['Date'], utc=True, unit='s').dt.date

    tweets = tweets.dropna()
    wsb_titles = wsb_titles.dropna()

    print("Running tweets and wsb titles through vader model")
    # runs the vader sentiment model on the tweets and the wsb titles
    twitter_sentiments = vader_model.sentiment_df(tweets,'Tweet')
    wsb_sentiments = vader_model.sentiment_df(wsb_titles, 'Title')

    # twitter_sentiments = pd.read_csv('D:\\Github\\financial_dashboard\Sentiment_analysis\\tweet_sentiments.csv')
    # twitter_sentiments['Date'] = pd.to_datetime(twitter_sentiments['Date']).dt.date
    # wsb_sentiments = pd.read_csv('D:\\Github\\financial_dashboard\Sentiment_analysis\\wsb_titles_sentiments.csv')
    # wsb_sentiments['Date'] = pd.to_datetime(wsb_sentiments['Date']).dt.date

    # creates connection with database

    # engine = create_engine(config.local_data_base_uri)
    engine = create_engine(config.heroku_database_uri)
    Base.metadata.create_all(bind=engine)

    print("Adding to database")
    # adds to the database
    add_to_wsb()
    add_to_twitter()