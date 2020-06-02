from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import twitter_credentials
import numpy as np
import pandas as pd
import re
import sys
import matplotlib.pyplot as plt

API_key  = 
API_secret_key= 
Access_token= 
Access_token_secret= 

account_list = []
if (len(sys.argv) > 1):
	account_list = sys.argv[1:]
else:

	print("Please provide a list of usernames at the command line.")
	sys.exit(0)

class TwitterClient():
	def __init__(self,twitter_user=None):
		self.auth = TwitterAuthenticator().authenticate_twitter_app()
		self.twitter_client = API(self.auth)
		self.twitter_user = twitter_user

	def get_twitter_client_api(self):
		return self.twitter_client
	def get_user_timeline_tweets(self, num_tweets):
		tweets = []
		for tweet in Cursor(self.twitter_client.user_timeline,id=self.twitter_user).items(num_tweets):
			tweets.append(tweet)
		return tweets

	def get_friend_list(self,num_tweets):
		friend_list = []
		for friend in Cursor(self.twitter_client.friends,id=self.twitter_user).items(num_tweets):
			friend_list.append(friend)
		return friend_list

	def get_home_timeline_tweets(self,num_tweets):
		home_timeline_tweets = []
		for tweet in Cursor(self.twitter_client.home_timeline,id=self.twitter_user).items(num_tweets):
                        home_timeline_tweets.append(tweet)
		return home_timeline_tweets

class TwitterAuthenticator():

	def authenticate_twitter_app(self):
		auth = OAuthHandler(twitter_credentials.API_key, twitter_credentials.API_secret_key)
		auth.set_access_token(twitter_credentials.Access_token,twitter_credentials.Access_token_secret)
		return auth
class TwitterStreamer():
	def __init__(self):
		self.twitter_authenticator = TwitterAuthenticator()
	def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
		listener = TwitterListener(fetched_tweets_filename)
		auth = self.twitter_authenticator.authenticate_twitter_app()
		stream = Stream(auth, listener)
		stream.filter(track= hash_tag_list)

class TwitterListener(StreamListener):
	def __init__(self,fetched_tweets_filename):
		self.fetched_tweets_filename = fetched_tweets_filename
	def on_data(self, data):
		try:
			print(data)
			with open(self.fetched_tweets_filename,'a')as tf:
				tf.write(data)
	
			return True
		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True

	def on_error(self, status):
		if status == 420:
			return False
		print(status)

class TweetAnalyzer():

	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def analyze_sentiment(self, tweet):
		analyze = TextBlob(self.clean_tweet(tweet))

		if analyze.sentiment.polarity > 0:
			return 1
		elif analyze.sentiment.polarity == 0:
			return 0
		else:
			return -1



	def tweets_to_data_frame(self,tweets):
		df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
		df['id'] = np.array([tweet.id for tweet in tweets])
		df['len'] = np.array([len(tweet.text) for tweet in tweets])
		df['Date'] = np.array([tweet.created_at for tweet in tweets])
		df['Favorite'] = np.array([tweet.favorite_count for tweet in tweets])
		df['Retweet'] = np.array([tweet.retweet_count for tweet in tweets])
		df['geo'] = np.array([tweet.geo for tweet in tweets])
		return df
	

if __name__ == "__main__":
	twitter_client = TwitterClient()
	tweet_analyzer = TweetAnalyzer()
	api = twitter_client.get_twitter_client_api()
	tweets = api.user_timeline(screen_name=account_list[0],count=40)
	df = tweet_analyzer.tweets_to_data_frame(tweets)
	df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['Tweets']])
	df.to_html('/var/www/html/index.html')


