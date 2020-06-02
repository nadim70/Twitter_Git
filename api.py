from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys
import numpy as np
from numpy import savetxt
import pandas as pd

API_key  =
API_secret_key= 
Access_token= 
Access_token_secret=


auth = OAuthHandler(API_key, API_secret_key)
auth.set_access_token(Access_token, Access_token_secret)
auth_api = API(auth)

account_list = []
if (len(sys.argv) > 1):
	account_list = sys.argv[1:]
else:

	print("Please provide a list of usernames at the command line.")
	sys.exit(0)

if len(account_list) > 0:

	for target in account_list:
		
		print("Getting data for " + target)
		item = auth_api.get_user(target)
		print("name: " + item.name)
		print("screen_name: " + item.screen_name)
		print("description: " + item.description)
		print("statuses_count: " + str(item.statuses_count))
		print("friends_count: " + str(item.friends_count))
		print("Location: "+str(item.location))
		print("followers_count: " + str(item.followers_count))
		print("Created_at: "+str(item.created_at))
		tweets = item.statuses_count
		account_created_date = item.created_at
		delta = datetime.utcnow() - account_created_date
		account_age_days = delta.days
		print("Account age (in days): " + str(account_age_days))
		if account_age_days > 0:
			print("Average tweets per day: " + "%.2f"%(float(tweets)/float(account_age_days)))
		hashtags = list()
		mentions = list()
		tweet = list()
		tweet_count = 0
		end_date = datetime.utcnow() - timedelta(days=30)
		for status in Cursor(auth_api.user_timeline, id=target).items():
			tweet_count += 1
			if hasattr(status, "entities"):
				entities = status.entities
				if "hashtags" in entities:
					for ent in entities["hashtags"]:
						if ent is not None:
							if "text" in ent:
								hashtag = ent["text"]
								if hashtag is not None:
									hashtags.append(hashtag)
									df2 = pd.DataFrame(hashtags,columns=['All_Hashtags'])
									#df2.to_html('hash.html')							
									#np.savetxt('/root/httpd/struct.html',result, delimiter=' , ', fmt='%s',header='Available Hashtags---------------------------------------------------------------------------------------------', comments='-----------------------------------------------------------------------------')
				if "user_mentions" in entities:
					for ent in entities["user_mentions"]:
						if ent is not None:
							if "screen_name" in ent:
								name = ent["screen_name"]
								if name is not None:
									mentions.append(name)
									df3 = pd.DataFrame(mentions)

			
			if hasattr(status, "retweeted_status"):
				try:
					a = status.retweeted_status.extended_tweet["full_text"]
					tweet.append(a)
				except AttributeError:
					b = status.retweeted_status.text
					tweet.append(b)
			else:
		
				try:
					c = status.extended_tweet["full_text"]
					tweet.append(c)
				except AttributeError:
					d = status.text
					tweet.append(d)

			if status.created_at < end_date:
				break

df1 = pd.DataFrame(tweet,columns=['tweets'])
df2 = pd.DataFrame(hashtags,columns=['All_Hashtags'])
df3 = pd.DataFrame(mentions)
df2['All_Screen_Name']=df3
df2['All_tweets']=df1
df2.to_html('/var/www/html/tweets.html')

import pandas as pd
tags= list()	
user= list()
for item,count in Counter(mentions).most_common(10):
	b = (item + "  " + str(count))
	user.append(b)
df = pd.DataFrame(user,columns=['Most_Users'])

for item,count in Counter(hashtags).most_common(10):
	a = (item + "  " + str(count))
	tags.append(a)
df1 = pd.DataFrame(tags)
df['Popular_hashtags']= df1
df.to_html('/var/www/html/hashtags.html')
print ("All done. Processed " + str(tweet_count) + " tweets.")
