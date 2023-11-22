from uuid import uuid4
from common.mongo_calls import MongoConnect
from common.redis_calls import RedisClient
import common.extras as extras

mongo_client = MongoConnect("clients")
redis_client = RedisClient()


def generate_auth_token(client_id, client_secret):
    """
    Generates an auth token for the client, returns it, and stores it in Redis.  Token will be good for 15 minutes.
    :param client_id: Client ID
    :param client_secret: Client Secret
    :return: auth Token
    """
    client = mongo_client.find({'client_id': extras.encrypt_string(client_id)})
    if client:
        if client[0]['client_secret'] == extras.encrypt_string(client_secret):
            auth_token = f'auth_token_{str(uuid4())}'
            result = redis_client.set(client_id, auth_token)  # Client ID is the key, auth token is the value
            if result:
                redis_client.expire(client_id, 900)
                return {'auth_token': auth_token}
        else:
            return "Invalid Client Secret"
    else:
        return "Invalid Client ID"


def validate_auth_token(client_id, auth_token):
    """
    Validates the auth token for the client.  auth token is stored in Redis.
    :param client_id: Client ID
    :param auth_token: auth Token
    :return: True if valid, False if not
    """
    if redis_client.get(client_id) == auth_token:
        return True
    else:
        return False
