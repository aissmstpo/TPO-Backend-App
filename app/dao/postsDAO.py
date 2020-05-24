from werkzeug.local import LocalProxy

from bson import ObjectId

from app.db import get_db

from operator import itemgetter

db = LocalProxy(get_db)

def get_all_posts():
    try:
        posts = list(db["posts"].find())
        posts.sort(key=itemgetter('posted_date'),reverse=True)
        return posts
    except Exception as e:
        return e
    
