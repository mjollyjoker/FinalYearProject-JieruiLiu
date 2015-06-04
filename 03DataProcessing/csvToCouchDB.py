# This function will take a csv file as input and store corresponding information to couchDB

import re
import json
import couchdb
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords

# couchDB initialization
USERNAME = ''
PASSWORD = ''

SERVER_URL = 'http://localhost:5984'
DB = 'boundary_backup' ################################### change output
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)
db = couch[DB]

# read file that contains the attribute information
raw = open('finalData.csv','r', encoding='utf-8')
raw.readline()
# for each line in the file, attributes will be extracted
# and these attributes will then be added to corresponding document and update in couchDB
for line in raw:
    properties = line.split(',')
    name = properties[0]
    policeRecord = properties[1]
    postcode = properties[3]
    population = properties[4]
    averageAge = properties[5]
    unemployment = properties[6]
    averageIncome = properties[7]
    eduPrimary = properties[8]
    eduSecondary = properties[9]
    eduTertiery = properties[10][:-1]
    dbData = db[postcode]
    dbData['properties']['name'] = name
    dbData['properties']['population'] = population
    dbData['properties']['averageAge'] = averageAge
    dbData['properties']['unemployment'] = unemployment
    dbData['properties']['averageIncome'] = averageIncome
    dbData['properties']['eduPrimary'] = eduPrimary
    dbData['properties']['eduSecondary'] = eduSecondary
    dbData['properties']['eduTertiery'] = eduTertiery
    db.save(dbData)