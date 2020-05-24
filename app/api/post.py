"""
This module contains all API for the posts.
"""
from flask import Blueprint, jsonify

from app.dao.postsDAO import get_all_posts

post_api_v1 = Blueprint("post_api_v1","post_api_v1",url_prefix="/api/v1/post")


@post_api_v1.route("/")
def api_get_all_posts():
    """
    Get details of posts.

    :returns: list of posts with details
    :rtype: list
    """
    return jsonify(get_all_posts())

