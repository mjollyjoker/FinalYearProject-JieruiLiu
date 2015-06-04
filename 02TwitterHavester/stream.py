# This program harvests Tweets and store Tweets to couchDB

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

#twitter access setup set 1 ################################### change output
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
DB = 'melb_tweets' ################################### change output
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)
screenNames = []
#pickle.dump(screenNames, open( "screenNames1.p", "wb" ))################################### change output

# This function takes in a raw formated Tweet and print Tweet content
# Tweet user screen_name, name, posting date and text will be printed
def print_tweet(tweet):
    pickled = jsonpickle.encode(tweet)
    results = json.loads(pickled)
    doc = results['py/state']['_json']
    print ("@%s - %s (%s)" % (doc['user']['screen_name'], doc['user']['name'], doc['created_at']))
    print (doc['text'])

# The function takes in a raw tweet and a set of keywords
# tweet will be examied if containing any keyword, if so, it will be stored to couchDB
# User screen_name will be returned for valid Tweet
def save_tweet(tweet, keywords):
    print (keywords)
    try:
        if tweet.id_str in db:
            pass
        else :
            pickled = jsonpickle.encode(tweet)
            results = json.loads(pickled)
            doc = results['py/state']['_json']
            if (containKeywords(doc['text'], keywords)):
                db[tweet.id_str] = (doc)
                #print (doc['user']['screen_name'])
                return doc['user']['screen_name']
            
    except Exception as e:
        print (("---Exception in save_tweet:", e))
        pass
    return None

# This function takes in a set of keywords and expends with synonums
# The words will be stemmed and repeated words will be removed
# The expended ste of keywords will be returned
def expendKeywords(keywords):
    newKeywords = list(keywords)
    for keyword in keywords:
        try:
            syn = wn.synsets(keyword)[0]
            lemmas = syn.lemmas()
            for l in lemmas:
                newKeywords.append(l.name())
        except IndexError as e:
                continue
    st = LancasterStemmer()
    stemmed = [st.stem(word) for word in newKeywords]
    repeatRemoved = []
    for word in stemmed:
        if word not in repeatRemoved:
            repeatRemoved.append(word)
    return repeatRemoved

# This function reads from a file and return a set of keywords
# The input keywords will go through tokenization before further comparison is made
def getWords(docPath):
    raw = open(docPath,'r', encoding='utf-8')
    stemmed = []
    try:
        data = raw.read().replace('\n',' ')
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

# This function takes in a string text and a list of keywords and check if it contain any keyword
# A boolean value will be returend
# The text will go through tokenization before comparison is made
def containKeywords(text, keywords):
    letters_only = re.sub("[^a-zA-Z0-9]", " ", text)
    lower_case = letters_only.lower()
    words = lower_case.split()
    words = [word for word in words if not word in stopwords.words("english")]
    st = LancasterStemmer()
    stemmed = [st.stem(word) for word in words]
    return (any(i in stemmed for i in keywords))

# This function takes in a Twitter user screen_name as input search for user's timeline
# A list of will be returned that containing timeline tweets
def userAllTweet(screenName):
    alltweets = []  
    new_tweets = api.user_timeline(screen_name=screenName, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=screenName, count=200, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
    return alltweets

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    # read input keywords
    crimeKeywords = getWords('/home/ubuntu/twStream/crime.txt')
    
    def on_status(self, data):
        # returned screen_names will be store to a exteral file and read by another program
        screenNames = pickle.load(open("/home/ubuntu/twStream/screenNames1.p","rb")) ################################### change output
        screenName = save_tweet(data, crimeKeywords)
        if screenName not in screenNames:
            if screenName != None:
                screenNames.append(screenName)
        pickle.dump(screenNames, open("/home/ubuntu/twStream/screenNames1.p","wb")) ################################### change output
        return True

    def on_error(self, status):
        print ("error%s" % status)
        return True

    def on_timeout(self):
        return True

if __name__ == '__main__':
    try:
        db = couch.create(DB)
    except couchdb.http.PreconditionFailed as e:
        db = couch[DB]

    l = StdOutListener()

    print ("Steaming starts!")

    stream = tweepy.Stream(auth, l)
    # stream is limited for Melbourne area only
    stream.filter(locations=[144.4701516,-37.8394484,144.9411904,-37.6398952]) ################################### change output