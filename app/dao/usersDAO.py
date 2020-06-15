from datetime import datetime

from werkzeug.local import LocalProxy

from bson import ObjectId

from app.db import get_db

from pymongo.errors import PyMongoError, DuplicateKeyError

db = LocalProxy(get_db)


def get_all_users():
    try:
        return list(db["users"].find({}, {"password": 0}))
    except Exception as e:
        return e


def get_user_by_id(id):
    try:
        return db["users"].find_one({"_id": ObjectId(id)})
    except Exception as e:
        return e


def get_all_students():
    try:
        return list(db["users"].find({"role": "student"}, {"password": 0}))
    except Exception as e:
        return e


def get_all_companies():
    try:
        return list(db["users"].find({"role": "company"}, {"password": 0}))
    except Exception as e:
        return e


def approve_user(id):
    try:
        user = db["users"].find_one({"_id": ObjectId(id)})
        if user is None:
            raise ValueError("No such user found!")
        if "approved_date" in user:
            raise Exception("User is already approved")
        result = db["users"].update_one(
            {"_id": ObjectId(id)}, {"$set": {"approved_date": datetime.utcnow()}}
        )
        if result.matched_count == 0:
            raise ValueError("No such user found")
        if result.modified_count == 0:
            raise ValueError("No document updated")
        return result
    except PyMongoError as e:
        return e


def reject_user(id, reason):
    try:
        user = db["users"].find_one({"_id": ObjectId(id)})
        if user is None:
            raise ValueError("No such user found!")
        if "approved_date" in user:
            raise Exception("User is already approved")
        result = db["users"].update(
            {"_id": ObjectId(id)},
            {
                "$set": {"profile_completed": False},
                "$push": {
                    "rejected": {"rejected_date": datetime.utcnow(), "reason": reason}
                },
            },
        )
        print("result", result)
        return result
    except PyMongoError as e:
        return e


def create_profile(id, profile_data):
    try:
        print(profile_data)
        db["users"].find_one({"_id": ObjectId(id)})
        result = db["users"].update_one(
            {"_id": ObjectId(id)}, {"$set": {"profile_completed": True, **profile_data}}
        )
        if result.matched_count == 0:
            raise ValueError("No such user found")
        if result.modified_count == 0:
            raise ValueError("No document updated")
        return result
    except PyMongoError as e:
        return e


def update_profile(id, data):
    """
        actually only set profile_completed to true if no approve_date or user is
        not yet approved(due to rejection) else simply update the profile
        but for now let it be
    """
    try:
        result = db["users"].update_one(
            {"_id": ObjectId(id)}, {"$set": {"profile_completed": True, **data}}
        )
        if result.matched_count == 0:
            raise ValueError("No such user found")
        if result.modified_count == 0:
            raise ValueError("No document updated")
        return result
    except PyMongoError as e:
        return e


def create_user(userdata):
    try:
        result = db["users"].insert_one({**userdata})
        return {"success": True, "_id": result.inserted_id}
    except PyMongoError as e:
        return e


def get_user_by_email(email):
    try:
        return db["users"].find_one(
            {"$or": [{"email": email}, {"concerned_person.email": email}]}
        )
    except Exception as e:
        return e


def get_approved_companies():
    try:
        return list(
            db["users"].find(
                {"role": "company", "approved_date": {"$exists": True}},
                {
                    "company_name": 1,
                    "concerned_person": 1,
                    "contact": 1,
                    "email": 1,
                    "approved_date": 1,
                },
            )
        )
    except Exception as e:
        return e


def get_unapproved_companies():
    try:
        return list(
            db["users"].find(
                {
                    "role": "company",
                    "approved_date": {"$exists": False},
                    "profile_completed": True,
                },
                {"company_name": 1, "concerned_person": 1, "contact": 1, "email": 1},
            )
        )
    except Exception as e:
        return e


def get_approved_students():
    try:
        return list(
            db["users"].find(
                {"role": "student", "approved_date": {"$exists": True}},
                {"full_name": 1, "class": 1, "roll_number": 1, "department": 1},
            )
        )
    except Exception as e:
        return e


def get_unapproved_students():
    try:
        return list(
            db["users"].find(
                {
                    "role": "student",
                    "approved_date": {"$exists": False},
                    "profile_completed": True,
                },
                {"full_name": 1, "class": 1, "roll_number": 1, "department": 1},
            )
        )
    except Exception as e:
        return e


def get_user_name_by_id(id):
    try:
        user = db["users"].find_one({"_id": ObjectId(id)}, {"password": 0})
        print("1")
        if user["role"] == "student":
            return {"role": "student", "user_name": user["full_name"]}
        elif user["role"] == "company":
            return {"role": "company", "user_name": user["company_name"]}
    except Exception as e:
        return e


def get_comapany_id_by_name(company_name):
    try:
        return db["users"].find_one(
            {"role": "company", "company_name": company_name}, {"_id": 1}
        )
    except Exception as e:
        return e
