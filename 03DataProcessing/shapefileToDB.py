# This method reads from a file that contains geolocation boundary information (shape)
# It then store the location information to couchDB according to postcode

import json
import couchdb
import string

# couchDB initialization
SERVER_URL = 'http://localhost:5984'
DB = 'suburb_boundaries' ################################### change output
USERNAME = ''
PASSWORD = ''
couch = couchdb.Server(SERVER_URL)
couch.resource.credentials = (USERNAME, PASSWORD)

try:
    db = couch.create(DB)
except couchdb.http.PreconditionFailed as e:
    db = couch[DB]

with open("greaterMelbourne.json") as json_file:
    json_data = json.load(json_file)['features']
    for data in json_data:
        # only documents will postcode attribute will be stored
        if('postcode' in data['properties']):
            data['_id'] = data['properties']['postcode']
            newCoor = []
            # parsing data to correct format
            for l in data['geometry']['coordinates']:
                l[0] = l[0] - 180
                l[1] = -1*l[1] + 180
                newCoor.append(l)
            data['geometry']['coordinates'] = newCoor
            if ('name' in data['properties']):
                suburbName = data['properties']['name'].replace("?", " ")
                suburbName = suburbName.replace("-", " ")
                data['properties']['name'] = suburbName
            try:
                db.save(data)
            except Exception as e:
                print (data["_id"], e)
