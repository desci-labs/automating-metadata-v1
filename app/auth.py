# auth.py
from flask import request, abort
from functools import wraps
import os
import logging
from logging_config import setup_logging

VALID_API_KEY = os.environ.get('AM_API_KEY')  

setup_logging()
logger = logging.getLogger(__name__)

def validate_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        logger.info(f"Received API Key: {api_key}")
        logger.info(f"Expected API Key: {VALID_API_KEY}")
        if api_key != VALID_API_KEY:
            logger.warning('Invalid API key provided')
            abort(401, 'Invalid API key')
        return func(*args, **kwargs)
    return wrapper