# Author :  Jierui Liu
# Student Number : 678819
# Supervisor : Prof. Richard Sinnott
# COMP90055 COMPUTING PROJECT
# Project Title : Twitter-related Analysis of Crime data for Melbourne

# this function will transfer mapreduced result to another database
# It will read information from a couchDB
# It will then store results to corresponding documents in another database

import json
import couchdb

USERNAME = ''
PASSWORD = ''

SERVER_URL = 'http://localhost:5984'
DBcombined = 'combined' ################################### change output
DBsuburb = 'suburb_boundaries'
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)
dbCombined = couch[DBcombined]
dbSuburb = couch[DBsuburb]

for doc in dbSuburb.view('_all_docs'):
    viewString = 'postcode/postcode_' + doc['id']
    myView = dbCombined.view(viewString, group_level=1).rows
    positive = 0
    neutral = 0
    negative = 0
    for myV in myView:
        if myV.key == 1:
            positive = myV['value']
        elif myV.key == -1:
            negative = myV['value']
        else:
            neutral = myV['value']
    totalCount = positive + neutral + negative
    print (doc['id'], ',',positive,',',neutral,',',negative,',', totalCount)
    # tweetPOACount = str(myView.total_rows)
    # print (doc['id'] + "," + tweetPOACount)
    # data = dbSuburb[doc['id']]
    # data['properties']['tweet_count'] = tweetPOACount
    # dbSuburb.save(data)