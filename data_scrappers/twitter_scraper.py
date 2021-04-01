import pandas as pd
import numpy as np
import yfinance as yf
import snscrape.modules.twitter as sntwitter
import csv
from twitterscraper import query_tweets
from datetime import datetime, timedelta
import datetime as dt

start_date=dt.date.today() - timedelta(days=7)
end_date= dt.date.today() + timedelta(days=1)

# wsb_tickers = pd.read_csv('D:\\Github\\financial_dashboard\data_scrappers\\wsb_tickers.csv',names=['Tickers'],header =0)
# wsb_tickers = wsb_tickers.sort_values(by = 'Tickers', ascending=False)
# top_15_tickers = wsb_tickers.head(15).index
# top_15_comp_name = [yf.Ticker(ticker).info['shortName'].split()[0] for ticker in top_15_tickers]


limit = 100 




# # Set maximum tweets to pull
# maxTweets = 1000
# # Set what keywords you want your twitter scraper to pull
# keyword = top_15_comp_name[2]
# #Open/create a file to append data to
# csvFile = open('gme_tweets_result.csv', 'a', newline='', encoding='utf8')
# #Use csv writer
# csvWriter = csv.writer(csvFile)
# csvWriter.writerow(['id','date','tweet',])
#
# # Write tweets into the csv file
# for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' lang:en since:2020-03-24 until:2020-03-31 -filter:links -filter:replies').get_items()):
#         if i > maxTweets :
#             break
#         csvWriter.writerow([tweet.id, tweet.date, tweet.content])
# csvFile.close()