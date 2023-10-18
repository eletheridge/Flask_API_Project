from uuid import uuid4
from mongo_calls import MongoConnect
from redis_calls import RedisClient
import extras


mongo_client = MongoConnect("clients")
redis_client = RedisClient()


def generate_refresh_token(client_id, client_secret):
    """
    Generates a refresh token for the client, returns it, and stores it in Redis.  Token will be good for 15 minutes.
    :param client_id: Client ID
    :param client_secret: Client Secret
    :return: Refresh Token
    """
    client = mongo_client.find({'client_id': extras.encrypt_string(client_id)})
    if client:
        if client[0]['client_secret'] == extras.encrypt_string(client_secret):
            refresh_token = f'refresh_token_{str(uuid4())}'
            result = redis_client.set(client_id, refresh_token)  # Client ID is the key, refresh token is the value
            if result:
                redis_client.expire(client_id, 900)
                return {'refresh_token': refresh_token}
        else:
            return "Invalid Client Secret"
    else:
        return "Invalid Client ID"


def validate_refresh_token(client_id, refresh_token):
    """
    Validates the refresh token for the client.  Refresh token is stored in Redis.
    :param client_id: Client ID
    :param refresh_token: Refresh Token
    :return: True if valid, False if not
    """
    if redis_client.get(client_id) == refresh_token:
        return True
    else:
        return False


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
