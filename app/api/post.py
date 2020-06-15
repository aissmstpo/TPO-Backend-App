"""
This module contains all API for the posts.
"""
from flask import Blueprint, jsonify, request
import datetime

from app.dao.usersDAO import get_comapany_id_by_name
from app.dao.postsDAO import (
    add_post,
    get_all_posts,
    get_post_by_id,
    update_post,
    delete_post,
    delete_all_posts,
    delete_post_by_company_id,
    add_notice,
    get_all_notices,
    delete_notice,
    delete_all_notices,
    update_notice,
)

post_api_v1 = Blueprint("post_api_v1", "post_api_v1", url_prefix="/api/v1/post")
notice_api_v1 = Blueprint("notice_api_v1", "notice_api_v1", url_prefix="/api/v1/notice")


@post_api_v1.route("/")
def api_get_all_posts():
    """
    Get details of posts.

    :returns: list of posts with details
    :rtype: list
    """
    return jsonify(get_all_posts())


@post_api_v1.route("/company")
def api_get_all_posts_by_company_name():
    """
    Get posts of particular company by company_name

    :input: company_name
    :returns: list of posts of particular company with post details
    :rtype: list
    """
    post_details = request.json
    company_name = post_details["company_name"]
    company_id = get_comapany_id_by_name(
        company_name
    )  # it returns {"company_id":"5ea...."}
    return jsonify(get_post_by_id(company_id["_id"]))


@post_api_v1.route("/company/id")
def api_get_all_posts_by_company_id():
    """
    Get posts of particular company by company_id

    :input: company_id
    :returns: list of posts of particular company with post details
    :rtype: list
    """
    post_details = request.json
    company_id = post_details["company_id"]
    return jsonify(get_post_by_id(company_id))


@post_api_v1.route("/add", methods=["GET", "POST"])
def api_add_post():
    """
    add post of particular company

    :input: company_id,title,description
    :returns: successfully added or Error in adding
    """
    post_details = request.json
    post_details["updated_at"] = datetime.datetime.now()
    post_details["posted_date"] = datetime.datetime.now()
    if request.method == "POST":
        if add_post(post_details):
            return "successfully added"
        else:
            return "Error in adding"
    return jsonify()


@post_api_v1.route("/delete", methods=["DELETE"])
def api_delete_post():
    """
    delete post by id

    :input: post_id
    :returns: Deleted successfully or Error in deleting
    """
    post_details = request.json
    if request.method == "DELETE":
        if delete_post(post_details["post_id"]):
            return "Deleted successfully"
        else:
            return "Error in deleting"
    return jsonify()


@post_api_v1.route("/delete/all", methods=["DELETE"])
def api_delete_all_posts():
    """
    delete all posts

    :returns: Deleted successfully or Error in deleting
    """
    if request.method == "DELETE":
        if delete_all_posts():
            return "Deleted successfully"
        else:
            return "Error in deleting"
    return jsonify()


@post_api_v1.route("/delete/company", methods=["DELETE"])
def api_delete_post_company():
    """
    delete post by company_name

    :input: comapny_name
    :returns: Deleted successfully or Error in deleting
    """
    post_details = request.json
    company_name = post_details["company_name"]
    company_id = get_comapany_id_by_name(company_name)  # it returns {"_id":"5ea...."}
    print(company_id)
    if request.method == "DELETE":
        if delete_post_by_company_id(company_id["_id"]):
            return "Deleted successfully"
        else:
            return "Error in deleting"
    return jsonify()


@post_api_v1.route("/update", methods=["PUT"])
def api_update_post():
    """
    update post by id

    :input: post_id,title,description
    :returns: updated successfully or Error in updating
    """
    post_details = request.json
    post_details["updated_at"] = datetime.datetime.now()
    if request.method == "PUT":
        if update_post(post_details):
            return "updated successfully"
        else:
            return "Error in updating"
    return jsonify()


"________________________________________________________________________________________________________________________________________________"


@notice_api_v1.route("/")
def api_get_all_notices():
    """
    Get details of notices.

    :returns: list of notices with details
    :rtype: list
    """
    return jsonify(get_all_notices())


@notice_api_v1.route("/add", methods=["GET", "POST"])
def api_add_notice():
    """
    add notice
    
    :input: title,description
    :returns: successfully added or Error in adding
    """
    notice_details = request.json
    notice_details["updated_at"] = datetime.datetime.now()
    notice_details["posted_date"] = datetime.datetime.now()
    if request.method == "POST":
        if add_notice(notice_details):
            return "added successfully"
        else:
            return "Error in adding"
    return jsonify()


@notice_api_v1.route("/delete", methods=["DELETE"])
def api_delete_notice():
    """
    delete notice by id

    :input: notice_id
    :returns: Deleted successfully or Error in deleting
    """
    notice_details = request.json
    if request.method == "DELETE":
        if delete_notice(notice_details["notice_id"]):
            return "Deleted successfully"
        else:
            return "Error in deleting"
    return jsonify()


@notice_api_v1.route("/delete/all", methods=["DELETE"])
def api_delete_all_notices():
    """
    delete all notices

    :returns: Deleted successfully or Error in deleting
    """
    if request.method == "DELETE":
        if delete_all_notices():
            return "Deleted successfully"
        else:
            return "Error in deleting"
    return jsonify()


@notice_api_v1.route("/update", methods=["PUT"])
def api_update_notice():
    """
    update notice by id

    :input: notice_id,title,description
    :returns: updated successfully or Error in updating
    """
    notice_details = request.json
    notice_details["updated_at"] = datetime.datetime.now()
    if request.method == "PUT":
        if update_notice(notice_details):
            return "updated successfully"
        else:
            return "Error in updating"
    return jsonify()
