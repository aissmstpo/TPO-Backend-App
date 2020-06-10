from werkzeug.local import LocalProxy

from bson import ObjectId

from app.db import get_db

db = LocalProxy(get_db)

def get_all_posts():
    try:
        posts = list(db["posts"].find()).sort({"updated_at":-1})
        return posts
    except Exception as e:
        return e

def get_post_by_id(company_id):
    try:        
        posts = list(db["posts"].find({"company_id":ObjectId(company_id)})).sort({"updated_at":-1})
        return posts
    except Exception as e:
        return e
    
def add_post(post_details):
    try:
        post_details["company_id"] = ObjectId(post_details["company_id"])
        return db["posts"].insert_one(post_details)
    except Exception as e:
        return e

def delete_post(post_id):
    try:
        return db["posts"].remove({"_id":ObjectId(post_id)},True)
    except Exception as e:
        return e

def delete_post_by_company_id(company_id):
    try:
        return db["posts"].remove({"company_id":ObjectId(company_id)},True)
    except Exception as e:
        return e

def delete_all_posts():
    try:
        return db["posts"].remove({})
    except Exception as e:
        return e

def update_post(post_details):
    try:
        query = {"_id":ObjectId(post_details["post_id"])}
        para = {"$set":{"description":post_details["description"],"title":post_details["title"],"updated_at":post_details["updated_at"]}}
        return db["posts"].update_one(query,para)
    except Exception as e:
        return e

    
def get_all_notices():
    try:
        notices = list(db["notices"].find()).sort({"updated_at":-1})
        return notices
    except Exception as e:
        return e

def add_notice(notice_details):
    try:
        return db["notices"].insert_one(notice_details)
    except Exception as e:
        return e

def delete_notice(notice_id):
    try:
        return db["notices"].remove({"_id":ObjectId(notice_id)},True)
    except Exception as e:
        return e

def delete_all_notices():
    try:
        return db["notices"].remove({})
    except Exception as e:
        return e

def update_notice(notice_details):
    try:
        query = {"_id":ObjectId(notice_details["notice_id"])}
        para = {"$set":{"description":notice_details["description"],"title":notice_details["title"],"updated_at":notice_details["updated_at"]}}
        return db["notices"].update_one(query,para)
    except Exception as e:
        return e
