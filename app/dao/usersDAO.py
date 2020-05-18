from werkzeug.local import LocalProxy

from bson import ObjectId

from app.db import get_db

from flask import session,request

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

def login():
    user_details = request.json
    if request.method == "POST":
        try:
            user = db["users"].find_one({'username': user_details['username']})
            if user:
                if bcrypt.check_password_hash(user['password'],user_details["password"]):
#                    session['username'] = user['username']
                    return "logged in"
                else:
                    return "Wrong Password"
            else:
                return "User Not Found"
        except Exception as e:
            return e
    return

def register():
    user_details = request.json
    if request.method == "POST":
        try:
            user = db["users"].find_one({'username': user_details['username']},{"password":0})
            if user is None:
                user_details["password"] = bcrypt.generate_password_hash(user_details["password"]).decode('utf-8')
                doc_id = mongo_collection.insert_one(user_details)
                if doc_id != None: 
                    return "Registered"
                else:
                    return "Network Error"
            else:
                return "user already exist"
        except Exception as e:
            return e
    return  ""
