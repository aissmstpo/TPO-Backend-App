from werkzeug.local import LocalProxy

from bson import ObjectId

from app.db import get_db


db = LocalProxy(get_db)

def get_all_users():
    try:
        return list(db["users"].find({},{"password":0}))
    except Exception as e:
        return e

def get_user_by_id(id):
    try:
        return db["users"].find_one({"_id":ObjectId(id)},{"password":0})
    except Exception as e:
        return e

def get_all_students():
    try:
        return list(db["users"].find({"role":"student"},{"password":0}))
    except Exception as e:
        return e

def get_all_companies():
    try:
        return list(db["users"].find({"role":"company"},{"password":0}))
    except Exception as e:
        return e

def get_approved_companies():
    try: 
        return list(db["users"].find({"role":"company", "approved":True},{"company_name":1, "concerned_person":1, "contact":1, "email":1}))
    except Exception as e:
        return e


