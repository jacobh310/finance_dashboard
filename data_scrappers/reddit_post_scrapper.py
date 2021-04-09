from psaw import PushshiftAPI
import datetime as dt
from datetime import datetime, timedelta
import pandas as pd




def scrape_posts(tickers):
    api = PushshiftAPI()
    start_epoch=dt.date.today() - timedelta(days=7)

    subs = list(api.search_submissions(after=start_epoch, subreddit='wallstreetbets', filter=['title', 'created_utc'], limit=15000))

    df = pd.DataFrame()
    for ticker in tickers:
        # for sub in subs:
        #     if ticker in sub.title:
        #         titles.append([ticker,sub.title, sub.created_utc])
        titles = [[ticker,sub.title, sub.created_utc]  for sub in subs if ticker in sub.title]
        titles = pd.DataFrame(titles)
        df = df.append(titles, ignore_index=True)

    return df


def scrape_comments(tickers):

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

if __name__ == "__main__":
    wsb_tickers = pd.read_csv('data_scrappers\\wsb_tickers.csv', names=['Tickers'],header=0)
    wsb_tickers = wsb_tickers.sort_values(by='Tickers', ascending=False)
    top_15_tickers = wsb_tickers.head(15).index
    titles = scrape_posts(top_15_tickers)
    titles.to_csv('wsb_title.csv', index=False)
