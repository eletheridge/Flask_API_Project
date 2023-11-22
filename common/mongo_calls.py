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
            return str(obj)     # Return string representation of ObjectId since it is not JSON serializable
        else:
            return JSONEncoder.default(obj, **kwargs)


class MongoConnect(object):
    """
    Class for interfacing with mongo server
    """
    def __init__(self, collection="test"):
        # Username and Password would be abstracted away as env vars in a production environment
        self.client = pymongo.MongoClient('mongodb://root:rootpassword@mongodb:27017'
                                          '/admin?authSource=admin&authMechanism=SCRAM-SHA-1')
        self.db = self.client.testing
        self.collection_obj = self.db[collection]

    def one(self, query=None):
        """
        Locates object in the database by id
        :param query: Id of object to be located
        :return: Object from database
        """
        try:
            result = json.loads(MongoEncoder().encode(self.collection_obj.find_one(ObjectId(query))))
        except Exception as e:
            raise Exception(e)
        return result

    def find(self, query=None):
        """
        Locate multiple objects in the database by query
        :param query: Query to be executed
        :return: List of objects from database
        """
        try:
            result = self.collection_obj.find(query)
            response = []
            for r in result:
                response.append(json.loads(MongoEncoder().encode(r)))
        except Exception as e:
            raise Exception(e)
        return response

    def post(self, payload=None):
        """
        Inserts object into database
        :param payload: Data to be inserted
        :return: Result of insert
        """
        try:
            result = self.collection_obj.insert_one(payload)
        except Exception as e:
            raise Exception(e)
        return result
