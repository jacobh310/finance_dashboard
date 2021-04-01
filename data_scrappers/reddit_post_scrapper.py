from psaw import PushshiftAPI
import datetime as dt
from datetime import datetime, timedelta
import pandas as pd

wsb_tickers = pd.read_csv('D:\\Github\\financial_dashboard\data_scrappers\\wsb_tickers.csv',names=['Tickers'],header =0)
wsb_tickers = wsb_tickers.sort_values(by = 'Tickers', ascending=False)
top_15_tickers = wsb_tickers.head(15).index


def scrape_posts(tickers):
    api = PushshiftAPI()
    start_epoch=dt.date.today() - timedelta(days=7)


    titles = {}
    posts = {}

    subs = list(api.search_submissions(after=start_epoch, subreddit='wallstreetbets', filter=['title', 'selftext'], limit=10000))

    for ticker in tickers:
        titles[ticker] = []
        posts[ticker] = []

        for sub in subs:
            if ticker in sub.title:
                titles[ticker].append(sub.title)
                try:
                    if len(sub.selftext) > 2 and sub.selftext != '[removed]':
                        body = sub.selftext.replace('\n','')
                        posts[ticker].append(body)
                except:
                    posts[ticker].append(None)

    titles = pd.DataFrame.from_dict(titles,orient='index').T
    posts = pd.DataFrame.from_dict(posts, orient='index').T

    return titles, posts

# titles, posts = scrape_posts(top_15_tickers)
# titles.to_csv('wsb_title.csv', index=False)
# posts.to_csv('wsb_posts.csv', index=False)

def scrape_commets(tickers):

    api = PushshiftAPI()
    start_epoch = dt.date.today() - timedelta(days=7)
    subs = list(api.search_comments(after=start_epoch, subreddit='wallstreetbets', limit=50000))
    comments = {}
    for ticker in tickers:
        comments[ticker] = []
        for sub in subs:
            if ticker in sub.body:
                comments[ticker] = sub.body

    comments = pd.DataFrame.from_dict(comments,orient='index').T
    return  comments

# comments = scrape_commets(top_15_tickers)
# comments.to_csv('wsb_comments.csv',index=False)
