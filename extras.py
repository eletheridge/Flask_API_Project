from functools import wraps
from flask import request
import hashlib
import os


# Decorators
def authenticate(f):
    """
    Simple Authentication Example using headers
    ---
    :parameter: Auth key is stored encrypted in ENV.  X-Derp-Key is encrypted and compared.  Header should be plain text.
    :return: Results of API call if authorized, error response if not
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get("X-Derp-Key"):
            if encrypt_string(request.headers.get("X-Derp-Key")) != os.environ.get("AUTH_HEADER_KEY"):
                return {"Status": 401, "Response": "NOT AUTHORIZED"}, 401
        else:
            return {"Status": 401, "Response": "Missing Authentication Data"}, 401
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
    signature = hashlib.sha256(h_string.encode()).hexdigest()
    return signature
