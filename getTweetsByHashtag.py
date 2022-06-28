from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tweepy import OAuthHandler
import tweepy
import pandas as pd
from clean import clean_text
sid = SentimentIntensityAnalyzer()


def get_n_tweets(api, hashtag, n, lang=None):
    tweets = tweepy.Cursor(
        api.search_tweets,
        q=hashtag,
        lang=lang,
        tweet_mode = 'extended'
    ).items(n)
    return tweets

def saveTweets(api, hashtag, lang=None):
    db_tweets = pd.DataFrame(columns = ['username', 'text', 'sentiment'])
    tweet_list = get_n_tweets(api, hashtag, 10)
    tweet_list = [tweet for tweet in tweet_list]
    users = []
    for tweet in tweet_list:
        username = tweet.user.screen_name
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError: 
            text = tweet.full_text
        cleaned_text = clean_text(text)
        sentiment = sid.polarity_scores(str(cleaned_text))
        if(sentiment['compound'] < 0):
            ith_tweet = [username, text, sentiment]
            db_tweets.loc[len(db_tweets)] = ith_tweet
            users.append(ith_tweet)
    db_tweets.to_csv('sentiment_1.csv', index = False)
    return users
    
