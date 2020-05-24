from werkzeug.local import LocalProxy

from bson import ObjectId

from app.db import get_db

from app import login_manager

from flask import session

db = LocalProxy(get_db)

@login_manager.user_loader
def load_user(user_id):
    return db["users"].find_one({"_id":ObjectId(id)},{"password":0})

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
        return list(db["users"].find({"role":"company", "approved":True},
                    {"company_name":1, "concerned_person":1, "contact":1, "email":1}))
    except Exception as e:
        return e

def get_approved_students():
    try:
        return list(db["users"].find({"role" : "student", "approved" : True},
                    {"full_name" : 1, "class" : 1, "roll_number" : 1, "department" : 1}))
    except Exception as e:
        return e

def get_user_by_email(email):
    try:
        return db["users"].find_one({'email': email},{"password":0})       
    except Exception as e:
        return e
    
def get_user_password_by_email(email):
    try:
        return db["users"].find_one({'email': email})       
    except Exception as e:
        return e

def register_user(user):
    try:
        return db['users'].insert_one(user)
    except Exception as e:
        return e
