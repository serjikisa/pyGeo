"""
Application configurations and settings
"""
import os

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', None)
if GOOGLE_API_KEY is None:
    raise ValueError('Please provide GOOGLE_API_KEY as env var before run')

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_DB_NO = os.environ.get('REDIS_DB_NO', 0)

CONFIG = {
    "REQUEST_INTRVAL": 10,   # 10 seconds between consequnce requests from same IPAddress
}
