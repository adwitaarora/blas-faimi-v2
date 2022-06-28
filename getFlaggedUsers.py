import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime as dt
from googletrans import Translator
from clean import clean_text
from nltk.sentiment.vader import SentimentIntensityAnalyzer


sid = SentimentIntensityAnalyzer()
translator = Translator()


def sentiment(tweet_text):
    score = sid.polarity_scores(str(tweet_text))
    if score['compound'] < 0:
        return True
    return False

        
def isFlagged(username):
    td=dt.datetime.today().strftime('%Y-%m-%d')
    query="(from:"+username+") until:"+td+ "since:2018-01-01"
    tweets=[]
    limit=25

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets)==limit:
            break
        else:
            tweets.append(tweet.content)

    count = 0
    negativeTweets = []
    for tweet in tweets:
        cleantweet = str(clean_text(tweet))
        if sentiment(cleantweet) == True:
            negativeTweets.append(tweet)
            count += 1
    if count >= 2:
        return negativeTweets
    return []

def users():
    df = pd.read_csv('sentiment_1.csv')
    users = df['username'].tolist()
    flaggedUsers = dict()
    for user in users:
        res = isFlagged(user)
        if len(res) > 0:
            flaggedUsers[user] = res
    return flaggedUsers

