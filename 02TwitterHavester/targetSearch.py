# Author :  Jierui Liu
# Student Number : 678819
# Supervisor : Prof. Richard Sinnott
# COMP90055 COMPUTING PROJECT
# Project Title : Twitter-related Analysis of Crime data for Melbourne

# This program will fetch followers of official Twitter account 
# 'VictoriaPolice' and perform timeline search on the followers
import sys
import re
import tweepy
import couchdb
import json
import jsonpickle
import string
import pickle
from nltk.corpus import wordnet as wn
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords

#twitter access setup set 9 ################################### change output
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
DB = 'victoriaPoliceFollower' ################################### change output
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)
screenNames = []

regexAt = re.compile(r"@(\w+)")
targetScreenName = 'VictoriaPolice'

def expendKeywords(keywords):
    newKeywords = list(keywords)
    '''
    for keyword in keywords:
        try:
            syn = wn.synsets(keyword)[0]
            lemmas = syn.lemmas()
            for l in lemmas:
                newKeywords.append(l.name())
        except IndexError as e:
                continue
    '''
    st = LancasterStemmer()
    stemmed = [st.stem(word) for word in newKeywords]
    repeatRemoved = []
    for word in stemmed:
        if word not in repeatRemoved:
            repeatRemoved.append(word)
    return repeatRemoved

def getWords(docPath):
    raw = open(docPath,'r', encoding='utf-8')
    stemmed = []
    try:
        data = raw.read().replace('\n',' ').replace('_',' ')
        letters_only = re.sub("[^a-zA-Z0-9]", " ", data)
        lower_case = letters_only.lower()
        words = lower_case.split()
        words = [word for word in words if not word in stopwords.words("english")]
    except UnicodeDecodeError:
        print ("UnicodeDecodeError")
        pass
    #
    wordList = expendKeywords(words)
    return wordList

def containKeywords(text, keywords):
    letters_only = re.sub("[^a-zA-Z0-9]", " ", text)
    lower_case = letters_only.lower()
    words = lower_case.split()
    words = [word for word in words if not word in stopwords.words("english")]
    st = LancasterStemmer()
    stemmed = [st.stem(word) for word in words]
    return (any(i in stemmed for i in keywords))

def save_tweet(tweet, keywords):
    try:
        if tweet.id_str in db:
            pass
        else :
            pickled = jsonpickle.encode(tweet)
            results = json.loads(pickled)
            doc = results['py/state']['_json']
            if (containKeywords(doc['text'], keywords)) & (doc['coordinates'] != None):
                coordinates0 = doc['coordinates']['coordinates'][0]
                coordinates1 = doc['coordinates']['coordinates'][1]
                if (coordinates0 > 140.95) & (coordinates0 < 148.63) & (coordinates1 > -39.18) & (coordinates1 < -34):
                    db[tweet.id_str] = (doc)
                    #print (doc['user']['screen_name'])
                    return regexAt.findall(doc['text'])
    except Exception as e:
        print (("---Encountered Exception:", e),file=sys.stderr)
        pass
    return None

def userAllTweet(screenName):
    alltweets = []
    try:
        new_tweets = api.user_timeline(screen_name=screenName, count=200)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        
        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(screen_name=screenName, count=200, max_id=oldest)
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1
    except Exception as e:
        print ("userAllTweet", e)
        pass

    return alltweets

crimeKeywords = getWords('/home/ubuntu/twStream/crime.txt')

if __name__ == '__main__':
    try:
        db = couch.create(DB)
    except couchdb.http.PreconditionFailed as e:
        db = couch[DB]

    for user in tweepy.Cursor(api.followers, screen_name="targetScreenName").items():
        screenNames.append(user.screen_name)

    pickle.dump(screenNames, open("/home/ubuntu/twStream/targetNames.p","wb"))
    print ('target pickle saved')

    while (True):
        screenNames = pickle.load(open("/home/ubuntu/twStream/targetNames.p", "rb"))
        if len(screenNames) != 0:
            alltweets = userAllTweet(screenNames[0])
            for tweet in alltweets:
                save_tweet(tweet)
            pickle.dump(screenNames, open("/home/ubuntu/twStream/targetNames.p","wb"))
        else:
            break
        time.sleep(300)