import tweepy
from tweepy import OAuthHandler
from googletrans import Translator
from flask import Flask, render_template, url_for, request, redirect, send_file
from dotenv import load_dotenv
from getTweetsByHashtag import saveTweets
from getHashtags import get_trends
from getFlaggedUsers import users
import os

load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


translator = Translator()

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('landing.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        hashtags = get_trends(api, "India")
        return render_template('search.html', hashtags = hashtags)

@app.route('/results/', methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        hashtag = request.args.get('hashtag')
        negativeTweets = saveTweets(api, hashtag)
        return render_template('results.html', tweets = negativeTweets)
    else:
        hashtag = request.form['hashtag']
        negativeTweets = saveTweets(api, hashtag)
        return render_template('results.html', tweets = negativeTweets)

@app.route('/flagged/', methods=['GET', 'POST'])
def flagsers():
    if request.method == 'GET':
        flaggedUsers = users()
        return render_template('users.html', users = flaggedUsers)

@app.route('/download/', methods=['GET', 'POST'])
def download():
    if request.method == 'GET':
        return send_file('sentiment_1.csv', as_attachment = True)



if __name__ == "__main__":
    app.run(debug=True)
