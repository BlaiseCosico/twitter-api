""" The challenge
    Define a class called UserTweets that takes a Twitter handle / user in its constructor. it also receives an optional max_id parameter to start from a particular tweet id.
    Create a tweepy API object using the tokens imported from config.py (again, you can use another package if you prefer).
    Create an instance variable to hold the last 100 tweets of the user.
    Implement len() and getitem() magic (dunder) methods to make the UserTweets object iterable.
    Save the generated data as CSV in the data subdirectory: data/some_handle.csv, columns: id_str,created_at,text 
"""

import os
import tweepy
from collections import namedtuple

TWITTER_KEY = os.environ['TWITTER_KEY']
TWITTER_SECRET = os.environ['TWITTER_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']

Tweet = namedtuple('Tweet', 'id text created likes rts')

DEST_DIR = 'data'
EXT = 'csv'
NUM_TWEETS = 100

class UserTweets:

	def __init__(self, handle, max_id=None):
		self.handle = handle
		self.max_id = max_id
		self.auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET)
		self.authAccessToken = self.auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
		self.api = tweepy.API(self.auth)
		self.tweets = self.get_tweets()
		self.filename = f'{DEST_DIR}/{handle}.{EXT}'
		self.save(self.tweets)

	def get_tweets(self):
		return list((Tweet(tw.id, tw.text, tw.created_at, tw.favorite_count, tw.retweet_count) for tw in tweepy.Cursor(self.api.user_timeline, screen_name=self.handle,
								max_id=self.max_id, count=NUM_TWEETS, exclude_replies=False, include_rts=True).items()))
		return self.tweets

	def save(self, tweets):
		if not os.path.exists(DEST_DIR):
			os.mkdirs(DEST_DIR)
		with open(self.filename, w+) as f:
			writer = csv.writer(f)
			writer.writerow(Tweet._fields)
			writer.writerows([(x.id, x.text, x.created) for x in self.tweets])

	def __repr__ (self):
		return f"UserTweets({self.handle} {self.api})"

	def __len__(self):
		return len(self.tweets)

	def __getitem__(self, item):
		return self.tweets[item]


if __name__ == "__main__":
	user1 = UserTweets('CosicoBlaise')
	# print(len(user1))
	print(user1[2])