# This program will read a file that containing the screen_names and search the user timeline
# Searched timeline Tweets will validate before store to couchDB

import sys
import re
import tweepy
import couchdb
import json
import jsonpickle
import string
import pickle
import time
from nltk.corpus import wordnet as wn
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords

#twitter access setup set 5 ################################### change output
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
USERNAME = ''
PASSWORD = ''
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#couchdb access setup
SERVER_URL = 'http://localhost:5984'
DB = 'keywords_filtered' ################################### change output
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)

regexAt = re.compile(r"@(\w+)")

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
    return words

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
            if (doc['coordinates'] != None):
                coordinates0 = doc['coordinates']['coordinates'][0]
                coordinates1 = doc['coordinates']['coordinates'][1]
            else:
                coordinates0 = 0
                coordinates1 = 0
            if doc['place'] != None:
                placeFullName = doc['place']['full_name']
            else:
                placeFullName = None
            if ((coordinates0 > 140.95) & (coordinates0 < 148.63) & (coordinates1 > -39.18) & (coordinates1 < -34)) | (placeFullName == 'Melbourne, Victoria'):
                if (containKeywords(doc['text'], keywords)):
                    db[tweet.id_str] = (doc)
                    #print (doc['user']['screen_name'])
                    return regexAt.findall(doc['text'])
    except Exception as e:
        print ("---Encountered Exception:", e)
        pass
    return None

# This function takes in a Twitter user screen_name as input search for user's timeline
# A list of will be returned that containing timeline tweets
# When it exceeds time limit, it will be paused for 15 mins and continue to work
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
    except tweepy.TweepError:
        print ('We got a timeout ...')
        time.sleep(15*60)
        pass
    except IndexError:
        return alltweets
    except Exception as e:
        print ("---Encountered Exception userAllTweet: ", e)

    return alltweets

#pickle.dump([], open("/home/ubuntu/twSearch/secondarySearch1.p","wb")) ################################### change output
crimeKeywords = getWords('/home/ubuntu/twSearch/crime.txt')

if __name__ == '__main__':
    try:
        db = couch.create(DB)
    except couchdb.http.PreconditionFailed as e:
        db = couch[DB]

    while (True):
        # searched screen_name will not be used again to optimize efficiency
        # it will combine with other programs' progress
        screenNames = pickle.load(open("/home/ubuntu/twSearch/screenNames9.p", "rb")) ################################### change output
        searched1 = pickle.load(open("/home/ubuntu/twSearch/searched1.p", "rb")) ################################### change output
        searched2 = pickle.load(open("/home/ubuntu/twSearch/searched2.p", "rb")) ################################### change output
        searched3 = pickle.load(open("/home/ubuntu/twSearch/searched3.p", "rb")) ################################### change output
        searched4 = pickle.load(open("/home/ubuntu/twSearch/searched4.p", "rb")) ################################### change output
        allSearched = list(set(searched1)|set(searched2)|set(searched3)|set(searched4))
        secondarySearch = []
        if len(screenNames) > 0:
            screenName = screenNames[0]
            screenNames.remove(screenName)
            pickle.dump(screenNames,open("/home/ubuntu/twSearch/screenNames9.p","wb"))
            if screenName not in allSearched:
                tweets = userAllTweet(screenName)
                for t in tweets:
                    beingAted = save_tweet(t, crimeKeywords)
                    if beingAted != None:
                        secondarySearch += beingAted
                searched1.append(screenName)

        # name after @ will also be searched
        for second in secondarySearch:
            if second not in allSearched:
                tweets = userAllTweet(second)
                for t in tweets:
                    save_tweet(t, crimeKeywords)
            searched1.append(second)

        pickle.dump(searched1,open("/home/ubuntu/twSearch/searched1.p","wb")) ################################### change output

