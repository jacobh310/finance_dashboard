# Finance and Market Dashboard
---
This web app is comprised of three different dashboards.
1) In the Stock Financials and Funementals
2) Wall street bets and twitter sentiment analaysis 
3) Twitter Sentiment Analaysis 


## Stock Financial Page
- This page show price, financials, and other metrics for user selected stocks though tables and plots. Users can also select another stock to compar metrics and financials for a more educated investment decision 

## Wall street bets and twitter sentiment analaysis 
### Data Collection
- the wall street bets subreddit was scrapped to find the most popular tickers. 
- Reddit post from wall streat bets and tweets containing the most popular tickers from wall street bets were scrapped 
### Data Evalutation 
- tweets and wallstreet bets post are evulated for sentiment using the VADER sentiment model and plotted for weekly average and daily average over a week   
- The vader models a complete positive sentiment as a 1.0 and a compleete negative sentiment as a -1.0

![Alt text](https://github.com/jacobh310/finance_dash_csv/blob/master/images/twitter_daily.JPG?raw=true "Sentiment")

## Twitter Sentiment Analaysis 
- Collects tweets containing the ticker that the user inputed.
- Outputs a bar plot of the twitter daily sentiment 

### Resources 
- https://github.com/grsahagian/data-works/blob/main/twitter-sentiment-analysis/twitter-sentiment-analysis.ipynb
- https://towardsdatascience.com/how-to-scrape-tweets-from-twitter-59287e20f0f1
- https://github.com/awrd2019/Reddit-Sentiment-NLP-for-Trading/blob/master/reddit_nlp_for_trading.ipynb
