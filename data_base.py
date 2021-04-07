from sqlalchemy import  create_engine, Column, Float, DateTime, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import  pandas as pd


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
    date_added = Column('date_added',DateTime, default=datetime.date.today() )
    ticker = Column('ticker', String)
    compound=Column('compound',Float)
    neg=Column('neg', Float)
    neu=Column('neu',Float)
    pos=Column('pos',Float)


twitter_sentiments = pd.read_csv('D:\\Github\\financial_dashboard\Sentiment_analysis\\tweet_sentiments.csv')
twitter_sentiments['Date'] = pd.to_datetime(twitter_sentiments['Date']).dt.date
wsb_sentiments = pd.read_csv('D:\\Github\\financial_dashboard\Sentiment_analysis\\wsb_titles_sentiments.csv')

# engine = create_engine('sqlite:///sentiment_db.sqlite3')
engine = create_engine('postgresql://postgres:chivas101@localhost:5432/Sentiment')
Base.metadata.create_all(bind=engine)

def add_to_wsb():

    Session = sessionmaker(bind=engine)
    session = Session()

    for i, row in wsb_sentiments.iterrows():
        entry = WsbSentiment(ticker = row['Ticker'],
                            compound= row['compound'],
                             neg = row['neg'],
                             neu = row['neu'],
                             pos=row['pos'])

        session.add(entry)
        session.commit()

    session.close()

# add_to_wsb()



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

# add_to_twitter()