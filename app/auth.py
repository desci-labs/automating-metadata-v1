# auth.py
from flask import request, abort
from functools import wraps
import os

VALID_API_KEY = os.environ.get('AM_API_KEY')  

def validate_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        print(api_key)
        print(VALID_API_KEY)
        if api_key != VALID_API_KEY:
            abort(401, 'Invalid API key')
        return func(*args, **kwargs)
    return wrapper