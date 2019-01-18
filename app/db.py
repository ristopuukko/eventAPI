from pymongo import MongoClient
import bson.objectid as oid
from bson.json_util import dumps

import datetime
import json

class Db():
    uri = 'mongodb://root:example@mongodb'
    # uri = 'mongodb://root:example@127.0.0.1' # DEBUG
    def __init__(self):
        '''init the db connection
        '''
        cli = MongoClient(self.uri)     
        self.db = cli['eventsDb']
        self.coll = self.db['events']


    def status(self):
        serverstatus=self.db.command("serverStatus")
        
        return serverstatus

    def set(self, ipaddress=None, hostname=None, location=None, jsonpayload=[]):
        '''set the JSON payload & other data to the db
        '''
        data = { 
                    "timestamp": datetime.datetime.utcnow(),
                    "ipaddress": ipaddress,
                    "hostname" : hostname,
                    "geolocation" : location.upper(),
                    "payload" : jsonpayload
                }

        result = self.coll.insert_one(data)

        return result.acknowledged

    def get(self, location=None, timestart=None, timeend=None):
        ''' we use the default _objectId to get the date & time for the timerange query
        '''

        try:
            st=datetime.datetime.strptime(timestart, "%Y-%m-%d:%H.%M.%S")
        except ValueError:
            return 'ValueError:timestart'
        try:        
            et=datetime.datetime.strptime(timeend, "%Y-%m-%d:%H.%M.%S")
        except ValueError:
            return 'ValueError:timeend'

        location=location.upper()
        query_string = {"timestamp":{"$gte":st, "$lte":et},"geolocation":location}

        count = self.coll.count_documents(query_string)
        result=str('')
        if count>0:
            rescursor = self.coll.find(query_string)
            result = dumps(rescursor)

        else:
            result = 'queryError'

        return result
