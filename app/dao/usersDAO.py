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

def get_user_name_by_id(id):
    try:
        user = db["users"].find_one({"_id":ObjectId(id)},{"password":0})
        print("1")
        if user["role"] == "student":
            return {"role":"student","user_name":user["full_name"]}
        elif user["role"] == "company":
            return {"role":"company","user_name":user["company_name"]}
    except Exception as e:
        return e

def get_comapany_id_by_name(company_name):
    try:
        return db["users"].find_one({"role":"company","company_name":company_name},{"_id":1})
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

