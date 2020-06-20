from flask import current_app, g
from werkzeug.local import LocalProxy
from bson import ObjectId
from pymongo import MongoClient


def get_db():
    """
    Returns instance of database

    :returns: ``db`` instance of database
    :rtype: `pymongo.database.Database`_
    .. _pymongo.database.Database: https://pymongo.readthedocs.io/en/stable/api/pymongo/database.html?highlight=Database#pymongo.database.Database
    """
    db = getattr(g, "_database", None)
    DB_URI = current_app.config["DB_URI"]
    DB_NAME = current_app.config["DB_NAME"]
    if db is None:
        db = g._database = MongoClient(DB_URI,)[DB_NAME]
    return db
