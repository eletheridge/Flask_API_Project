from functools import wraps
from flask import request
import hashlib
import requests


# Decorators
def authenticate(f):
    """
    Crude implementation of an oauth type flow.  auth token must first be obtained with /get_auth_token endpoint.
    That auth token is then used in headers for all other requests.  auth token is valid for 15 minutes.
    Once expired, a new auth token must be obtained.  auth token is stored in redis for quick lookup.
    :return: Results of API call if authorized, error response if not
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get("X-Client-ID", False):
            if request.headers.get("X-Auth-Token"):
                cid = request.headers.get("X-Client-ID")
                auth_token = request.headers.get("X-Auth-Token")
                response = requests.get("http://auth:5433/auth_token",
                                        params={'cid': cid, 'auth_token': auth_token})
                if response.json()["Response"] == "NOT AUTHORIZED":
                    return response.json(), 401
            else:
                return {"Status": 401, "Response": "Missing auth Token"}, 401
        else:
            return {"Status": 401, "Response": "Missing Client ID"}
        return f(*args, **kwargs)

    return decorated


def responder(f):
    """
    Wrapper to ensure uniform response object for all calls for simple handling
    :return: A dictionary containing the response returned by the function and a sta†us
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        response, status_code = f(*args, **kwargs)
        return {"Status": status_code, "Response": response}
    return decorated


# Misc Functionality
def encrypt_string(h_string):
    """
    Rudimentary encryption function for demonstration purposes
    :param h_string: Auth Key from header
    :return: Encrypted Auth Key
    """
    signature = hashlib.sha256(h_string.encode()).hexdigest()
    return signature
