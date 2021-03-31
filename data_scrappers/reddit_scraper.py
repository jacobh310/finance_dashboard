import datetime as dt
from datetime import datetime, timedelta
import re
import pandas as pd
import json
from psaw import PushshiftAPI

tickers = pd.read_csv('D:\\Github\\financial_dashboard\data_scrappers\\tickers.csv', header=None,names=['Tickers'])
tickers['Tickers'] = tickers['Tickers'].str[:-2]
tickers = tickers['Tickers'].values

api = PushshiftAPI()
start_epoch=dt.date.today() - timedelta(days=7)

subs= api.search_submissions(after=start_epoch,
                            subreddit='wallstreetbets',
                            filter=['url','author', 'title', 'subreddit'],
                            limit=20000)


cash_tags = {}

for sub in subs:
    for word in sub.title.split(' '):
        if (word.isupper() or '$' in word) and word in tickers:
            word =  re.sub("[^a-zA-Z]+", "", word)
            if word.upper() not in cash_tags:
                cash_tags[word.upper()] = 1
            else:
                cash_tags[word.upper()] += 1


cash_tags = pd.Series(cash_tags, name='tickers')
cash_tags.to_csv('wsb_tickers.csv')
