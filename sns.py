import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime as dt
from sentimentAnalysis import analyseEnglish, analyseHindi
from googletrans import Translator
from clean import clean_text
from nltk.sentiment.vader import SentimentIntensityAnalyzer


sid = SentimentIntensityAnalyzer()
translator = Translator()

def sentiment(tweet_text):
    if tweet_text == "" or len(tweet_text) <= 0:
        return False
    language = translator.detect(tweet_text).lang
    try:
        if language == 'en' :
            prediction, certainity = analyseEnglish([tweet_text])
        elif language == 'hi':
            prediction, certainity = analyseHindi([tweet_text])
        else:
            tweet_text =  translator.translate(tweet_text).text
            prediction, certainity = analyseEnglish([tweet_text])
    except:
        prediction = "Could Not Predict"
        certainity = "0"
        
    if prediction == 'Negative':
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
    for tweet in tweets:
        tweet = str(clean_text(tweet))
        if sentiment(tweet) == True:
            count += 1
    if count >= 5:
        return True
    return False

df = pd.read_csv('sentiment_1.csv')
df['text'] = df['text'].apply(lambda x : clean_text(x))
df['isFlagged'] = df['username'].apply(lambda x : isFlagged(x))
df.to_csv('sentiment_2.csv')

