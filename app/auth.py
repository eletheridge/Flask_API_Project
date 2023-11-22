from uuid import uuid4
from common.mongo_calls import MongoConnect
from common.redis_calls import RedisClient
import common.extras as extras
import requests

mongo_client = MongoConnect("clients")
redis_client = RedisClient()


def generate_auth_token(client_id, client_secret):
    """
    Reaches out to the Auth Service to generate an auth token for the client, returns it, and stores it in Redis.
    :param client_id: Client ID
    :param client_secret: Client Secret
    :return: auth Token
    """
    try:
        response = requests.post("http://auth:5433/auth_token",
                                 data={'client_id': client_id, 'client_secret': client_secret})
        return response.json()["Response"]
    except Exception as e:
        return e


def generate_client_keys(client_name):
    """
    Generates a client ID and client secret, returns it once, and stores it encrypted in the database.
    :return: Client ID, Client Secret
    """
    client_id = f'client_id_{str(uuid4())}'
    client_secret = f'client_secret_{str(uuid4())}'
    db_object = {
        "client_name": client_name,
        "client_id": extras.encrypt_string(client_id),
        "client_secret": extras.encrypt_string(client_secret)
    }
    try:
        res = mongo_client.post(db_object)
        return {'_id': str(res.inserted_id), 'client_id': client_id, 'client_secret': client_secret}
    except Exception as e:
        return e
