# this function will create a design document which contain number of view for mapreduce function
# the mapreduce function is base on the given set of keywords

import couchdb
import re
import json
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords

USERNAME = ''
PASSWORD = ''

SERVER_URL = 'http://localhost:5984'
DB = 'combined' ################################### change output
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)
db = couch[DB]

def getWords(docPath):
    raw = open(docPath,'r', encoding='utf-8')
    words = []
    try:
        # tokenization
        data = raw.read().replace('\n',' ').replace('_',' ')
        letters_only = re.sub("[^a-zA-Z0-9]", " ", data)
        lower_case = letters_only.lower()
        words = lower_case.split()
        words = [word for word in words if not word in stopwords.words("english")]
        #st = LancasterStemmer()
        #stemmed = [st.stem(word) for word in words]
    except UnicodeDecodeError:
        print ("UnicodeDecodeError")
        pass
    #
    repeatRemoved = []
    for word in words:
        if word not in repeatRemoved:
            repeatRemoved.append(word)
    return repeatRemoved

keywords = getWords("mydoc.txt")

views = {}
allwords = ""
# generate map and reduce function according to given keywords
# for each view, it will be store to an view array
for word in keywords:
    allwords += "\\\s"+word+"|^" + word + "|\\\#"+word +"|"
    viewName = "postcode_" + word
    mapReduce = {}
    mapReduce['map'] = "function(doc) {if(doc.postcode == "+word+"){var rank = 0;if(doc.sentiment_score>0){rank = 1;}else if(doc.sentiment_score<0){rank = -1;}emit(rank, 1);}}"
    mapReduce['reduce'] = "_count"
    views[viewName] = mapReduce

# create a desigen for list of view and convert to json format
# fomated design document will then upload to couchDB
design = {}
design['views'] = views
design['language'] = "javascript"
json_design = json.dumps(design)
db["_design/postcode"] = json_design