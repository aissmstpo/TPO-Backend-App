from werkzeug.local import LocalProxy

from bson import ObjectId

from app.db import get_db


db = LocalProxy(get_db)

def get_all_posts():
    try:
        return list(db["posts"].find())
    except Exception as e:
        return e
