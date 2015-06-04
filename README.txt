This is README file for COMP90055 COMPUTING PROJECT
Author : Jierui Liu 678819
Supervisor : Richard Sinnott
School of Engineering, University of Melbourne
June 2015

*************** System requirement ***************
Python 3.4 with following packages
    - NLTK
    - Textblob
    - couchdb
    - tweepy
    - jsonpickle
Java 1.8 with following packages
    - Apache spark
    - Log4j
    - Apache hadoop
JavaScript
CouchDB 1.5.1

*************** Table of Content ***************
I. System installation
II. Twitter harvester
III. Data processing
IV. WebSystem


I. System installation
    // This file contains system contains the system setup for a new instance
    installUbuntu.py


II. Twitter harvester
    // This program will perform a twitter API search for a desinated keyword
    // The search result will be store to couchdb
    keywordSearch.py

    // This program will read a file that containing the screen_names and 
    // search the user timeline. Searched timeline Tweets will validate 
    // before store to couchDB
    searchScreenname.py

    // This program harvests Tweets using Twitter Streaming API and store 
    // Tweets to couchDB
    stream.py

    // This program will fetch followers of official Twitter account 
    // 'VictoriaPolice' and perform timeline search on the followers
    targetSearch.py


III. Data processing
    // This method takes will crawl census data from government website
    // Regex is used for match each of the attribute
    // result information will then be stored to a csv file
    ABSCensusFetcher.py

    // This file uses google reverse geocoding function to convert a given 
    // coordinates to postcode. The coordinate is an attribute from Tweet 
    // which is fetched from couchDB. After a post code is returned from 
    // google service, a new attribute "postcode" will be added to Tweet. The 
    // Tweet will then be updated in couchDB. Unfound result will be marked as 
    // "0000". Due to google service limitation, the function will 
    // automatically stop after 2500 requests attemps.
    addPostcodeAttr.py

    // This function will take a csv file as input and store corresponding 
    // information to couchDB
    csvToCouchDB.py

    // this function will transfer mapreduced result to another database
    // It will read information from a couchDB. It will then store results to 
    // corresponding documents in another database
    resultTransfer.py

    // This function will mark Tweets text with a sentiment score
    // The score is between -1 to 1
    // -1 indicates negative sentiment
    // 0 indicates neutral sentiment
    // 1 indicates positive sentiment
    // The corresponding Tweet will be added a new attribute "sentiment_score" 
    // and update in couchDB.
    sentimentTweets.py

    // This method reads from a file that contains geolocation boundary 
    // information (shape). It then store the location information to couchDB 
    // according to postcode.
    shapefileToDB.py

    // this function will create a design document which contain number of 
    // view for mapreduce function. The mapreduce function is base on the 
    // given set of keywords.
    viewCreator.py

    // This file contains a set of area postcode which is the target research areas
    // in this project
    activePostcode.txt
    
    // This file contains a set of tokenized keywords
    crimeCore.txt

IV. WebSystem
    // This folder contains the front end webpages
    // The navigation bar at the top will direct to anyother pages