"""
This module contains all API for the posts.
"""
from flask import Blueprint, jsonify, request

from app.dao.usersDAO import get_user_name_by_id
from app.dao.qnaDAO import (
    get_all_questions,
    add_question,
    update_solution,
    get_all_qna_by_user_id,
    delete_question,
)

qna_api_v1 = Blueprint("qna_api_v1", "qna_api_v1", url_prefix="/api/v1/qna")


@qna_api_v1.route("/")
def api_get_all_questions():
    """
    Get all questions.

    :returns: list of questions with details
    :rtype: list
    """
    questions = get_all_questions()
    for que in questions:
        user = get_user_name_by_id(que["user_id"])
        que["user_name"] = user["user_name"]
    return jsonify(questions)


@qna_api_v1.route("/role")
def api_get_all_questions_by_role():
    """
    Get all questions.
    
    :input: role
    :returns: list of questions with details
    :rtype: list
    """
    que_details = request.json
    role = que_details["role"]
    questions = get_all_questions()
    questions_by_role = list()
    for que in questions:
        user = get_user_name_by_id(que["user_id"])
        if user["role"] == role:
            que["user_name"] = user["user_name"]
            questions_by_role.append(que)
    return jsonify(questions_by_role)


@qna_api_v1.route("/question/user_id")
def api_get_all_qna_by_user_id():
    """
    Get details of qna by username.
    :input:"user_id"
    :returns: list of qna with details
    :rtype: list
    """
    que_details = request.json
    return jsonify(get_all_qna_by_user_id(que_details["user_id"]))


@qna_api_v1.route("/add", methods=["GET", "POST"])
def api_add_question():
    que_details = request.json
    que_details["Ans"] = None
    if request.method == "POST":
        if add_question(que_details):
            return "successfully added que"
        else:
            return "Error in posting"
    return jsonify()


@qna_api_v1.route("/update/answer", methods=["PUT"])
def api_update_answer():
    que_details = request.json
    if request.method == "PUT":
        print(update_solution(que_details))
        if update_solution(que_details):
            return "successfully added ans"
        else:
            return "Error in posting"
    return jsonify()


@qna_api_v1.route("/delete", methods=["DELETE"])
def api_DELETE_question():
    que_details = request.json
    if request.method == "DELETE":
        if delete_question(que_details["_id"]):
            return "successfully deleted question"
        else:
            return "Error in posting"
    return jsonify()
