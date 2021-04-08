import sys

from datetime import datetime
from pymongo import MongoClient

import config

def connect():
    try:
        # !!!WORKAROUND!!! connect=False needed because of pymongo/MongoDB bug
        # https://jira.mongodb.org/browse/PYTHON-961
        mc = MongoClient(config.MONGO_URL, connect=False)

        return mc
    except Exception as e:
        log.error("unable to connect to MongoDB", e)
        sys.exit(-1)

cn = connect()[config.MONGO_DB_NAME]
