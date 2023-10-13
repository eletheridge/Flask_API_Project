from functools import wraps
from flask import request
import hashlib
import os
from datetime import datetime
import base64


# Decorators
def authenticate(f):
    """
    Simple Authentication Example using headers
    ---
    Auth key is stored encrypted in ENV.  X-Auth-Key is encrypted and compared.  Header should be plain text.
    ---
    :return: Results of API call if authorized, error response if not
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get("X-Identity", False):
            if request.headers.get("X-Auth-Key"):
                if encrypt_string(request.headers.get("X-Auth-Key")) != os.environ.get("AUTH_HEADER_KEY"):
                    return {"Status": 401, "Response": "NOT AUTHORIZED"}, 401
            else:
                return {"Status": 401, "Response": "Missing Authentication Data"}, 401
        else:
            return {"Status": 401, "Response": "Missing X-Identity Data"}
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


def convert_base64_to_file(base64_string, filename):
    """
    Converts base64 string to file
    :param base64_string: Base64 string to be converted
    :param filename: Name of file to be created
    :return: True if successful, error if not
    """
    try:
        with open(filename, "wb") as fh:
            fh.write(base64.b64decode(base64_string))
        return True
    except Exception as e:
        return e


def convert_file_to_base64(filename):
    """
    Converts file to base64 string
    :param filename:
    :return: Base64 string
    """
    try:
        with open(filename, "rb") as fh:
            result = base64.b64encode(fh.read())
        return result.decode('utf-8')
    except Exception as e:
        raise Exception(e)
