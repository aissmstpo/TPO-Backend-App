from werkzeug.local import LocalProxy

from bson import ObjectId

from app.db import get_db

from operator import itemgetter

db = LocalProxy(get_db)

# done
def get_all_questions():
    try:
        return list(db["QnaSection"].find({"Ans": None}, {"Ans": 0}))
    except Exception as e:
        return e


# done
def add_question(qna_details):
    try:
        qna_details["user_id"] = ObjectId(qna_details["user_id"])
        return db["QnaSection"].insert_one(qna_details)
    except Exception as e:
        return e


# done
def update_solution(qna_details):
    try:
        query = {"_id": ObjectId(qna_details["_id"])}
        new_values = {"$set": {"Ans": qna_details["Ans"]}}
        return db["QnaSection"].update_one(query, new_values)

    except Exception as e:
        return e


# done
def get_all_qna_by_user_id(user_id):
    try:
        user_id = ObjectId(user_id)
        return list(db["QnaSection"].find({"user_id": user_id}))
    except Exception as e:
        return e


def delete_question(que_id):
    try:
        return db["QnaSection"].remove({"_id": ObjectId(que_id)}, True)
    except Exception as e:
        return e
