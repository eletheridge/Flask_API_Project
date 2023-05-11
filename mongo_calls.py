import pymongo
from bson import ObjectId
from json import JSONEncoder
import json


class MongoEncoder(JSONEncoder):
    """
    Class for ensuring mongo objects are able to be JSON serialized
    """
    def default(self, obj, **kwargs):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return JSONEncoder.default(obj, **kwargs)


class MongoConnect(object):
    """
    Class for interfacing with mongo server
    """
    def __init__(self, collection="test"):
        self.client = pymongo.MongoClient('mongodb://root:rootpassword@mongodb:27017/admin?authSource=admin&authMechanism=SCRAM-SHA-1')
        self.db = self.client.testing
        self.collection_obj = self.db[collection]

    def one(self, query=None):
        try:
            result = json.loads(MongoEncoder().encode(self.collection_obj.find_one(ObjectId(query))))
        except Exception as e:
            raise Exception(e)
        return result

    def post(self, payload=None):
        try:
            result = self.collection_obj.insert_one(payload)
        except Exception as e:
            raise Exception(e)
        return result