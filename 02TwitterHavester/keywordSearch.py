# Author :  Jierui Liu
# Student Number : 678819
# Supervisor : Prof. Richard Sinnott
# COMP90055 COMPUTING PROJECT
# Project Title : Twitter-related Analysis of Crime data for Melbourne

# This program will perform a twitter API search for a desinated keyword
# The search result will be store to couchdb

import sys
import tweepy
import couchdb
import json
import jsonpickle
import string
import pickle
import time

#twitter access setup set 12 ################################### change output
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
USERNAME = ''
PASSWORD = ''
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#couchdb access setup
SERVER_URL = 'http://localhost:5984'
DB = 'keyword_homicide' ################################### change output
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)
# location is limited at greater melbourne area
location = [140.95, -36.59, 145.06, -34]

def save_tweet(tweet):
    try:
        if tweet.id_str in db:
            pass
        else :
            pickled = jsonpickle.encode(tweet)
            results = json.loads(pickled)
            doc = results['py/state']['_json']
            if (doc['coordinates'] != None):
                coordinates0 = doc['coordinates']['coordinates'][0]
                coordinates1 = doc['coordinates']['coordinates'][1]
            else:
                coordinates0 = 0
                coordinates1 = 0
            if (coordinates0 > 140.95) & (coordinates0 < 148.63) & (coordinates1 > -39.18) & (coordinates1 < -34) | (doc['place']['full_name'] == 'Melbourne, Victoria'):
                db[tweet.id_str] = (doc)
                return None
    except Exception as e:
        print (("---Encountered Exception:", e),file=sys.stderr)
        pass
    return None

if __name__ == '__main__':
    try:
        db = couch.create(DB)
    except couchdb.http.PreconditionFailed as e:
        db = couch[DB]

    api = tweepy.API(auth)
    allTweets = tweepy.Cursor(api.search,
                       q="#Homicide",
                       locations=location).items()
    while True:
        try:
            t = allTweets.next()
            save_tweet(t)
        except tweepy.TweepError:
            print ('We got a timeout ...')
            time.sleep(15*60)
            continue
        except StopIteration:
            break
    print ('keyword search ends')
