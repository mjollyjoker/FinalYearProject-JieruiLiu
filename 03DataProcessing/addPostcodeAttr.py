# This file uses google reverse geocoding function to convert a given coordinates to postcode
# The coordinate is an attribute from Tweet which is fetched from couchDB
# After a post code is returned from google service, a new attribute "postcode" will be added to Tweet
# The Tweet will then be updated in couchDB
# Unfound result will be marked as "0000"
# Due to google service limitation, the function will automatically stop after 2500 requests attemps

import couchdb
import urllib.request
import json

# connect to couchDB
USERNAME = ''
PASSWORD = ''

SERVER_URL = 'http://localhost:5984'
DB = 'combined' ################################### change output
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)
db = couch[DB]
counter = 0

# the function will take a latitude and a longtitude as input
# a cooresponding postcode will be returned, otherwise, None will be returned
def getPostcode(latString, lonString):
    geoGoogle = "http://maps.googleapis.com/maps/api/geocode/json?address="
    page = urllib.request.urlopen(geoGoogle+latString+','+lonString)
    pageString = page.read().decode("utf-8")
    json_data = json.loads(pageString)['results']
    for result in json_data:
        if result['types'] == ["postal_code"]:
            for addr in result["address_components"]:
                if addr['types'] == ["postal_code"]:
                    return addr['long_name']

for doc in db.view('postcode_filter/with_postcode_0000'):
    if (counter >= 2500):
        break
    data = db[str(doc['key'])]
    postcode = getPostcode(str(data['coordinates']['coordinates'][1]),str(data['coordinates']['coordinates'][0]))
    if (postcode == None):
        postcode = "0000"
    # new attribute will be added to Tweet and updated to couchDB
    data['postcode'] = postcode
    print (postcode)
    db.save(data)
    counter += 1