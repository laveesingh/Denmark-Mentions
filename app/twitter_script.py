import tweepy
import os
import json

from app.models import Tweet

from tw_users_list import dump_to_file

consumer_key = 'P6jSQmeVPeA7YJK3oI14oz46h'
consumer_secret = 'Uvaa3T5xuy6qsAJ3YLON5qOM42ACXxhjB9Xyo0COfiVeC3cXwZ'
token = '732728148-mneIJp9gAxHpzln28mpPcgIQpB2iVFVoB7vp6wsx'
token_secret = 'iomDBUPBrlDkMHflhMVNivbyygobhx7OdeGFPkkg4Sqd3'


def fetch_tweets_list(api, userid):
    for pageno in xrange(1, 1000):
        response = api.user_timeline(userid, page=pageno)
        if len(response) == 0: return
        for tweet in response:
            user = tweet.author.name
            message = tweet.text
            timestamp = tweet.created_at
            tweet_id = tweet.id
            Tweet.objects.create(
                tweet_id=tweet_id,
                message=message,
                username=user,
                timestamp=timestamp
            )

def scrape_twitter():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)
    if os.path.isfile('tw_users_list.json'):
        pass
    else:
        dump_to_file()
    json_data = open('tw_users_list.json', 'r').read()
    users_list = json.loads(json_data)['tw_users_list']
    print "%d long list of twitter users found" % len(users_list)
    for userid in users_list:
        fetch_tweets_list(api, userid)
    
