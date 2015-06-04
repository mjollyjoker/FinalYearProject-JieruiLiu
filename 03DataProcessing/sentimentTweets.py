# This function will mark Tweets text with a sentiment score
# The score is between -1 to 1
# -1 indicates negative sentiment
# 0 indicates neutral sentiment
# 1 indicates positive sentiment
# The corresponding Tweet will be added a new attribute "sentiment_score" and update in couchDB

import couchdb
from textblob import TextBlob

# couchDB initialization
USERNAME = ''
PASSWORD = ''

SERVER_URL = 'http://localhost:5984'
DB = 'unfiltered_tweets' ################################### change output
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)
db = couch[DB]

# for each document in the view, a sentiment score will be added and updated in database
for doc in db.view('senti/noSenti_even'):
    print (doc['key'])
    blob = TextBlob(doc['value']['text'])
    doc['value']['sentiment_score'] = blob.sentiment.polarity
    db.save(doc['value'])
