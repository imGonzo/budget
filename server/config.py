import os

MONGO_URL = os.getenv('MONGO_URL') or 'mongodb://127.0.0.1:27017'
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME') or 'Budget'
