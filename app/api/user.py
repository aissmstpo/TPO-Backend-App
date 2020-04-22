"""
This module contains all API for the users.
"""
from flask import Blueprint

user_api_v1 = Blueprint("user_api_v1","user_api_v1",url_prefix="/api/v1/user")

@user_api_v1.route("/")
def api_get_all_users():
    """
    Get all users details.
    """
    pass

@user_api_v1.route("/student")
def api_get_all_students():
    """
    Get all student details.
    :returns: list of students with details
    :rtype: list
    """
    pass

@user_api_v1.route("/student/<id>")
def api_get_student_by_id(id):
    """
    Get a particular student details by his id.
    
    :param id: Id of the student
    :type id: str
    :return: a dict containing student details
    :rtype: dict
    """
    pass

@user_api_v1.route("/company")
def api_get_all_companies():
    """
    Get all student details.
    """
    pass

@user_api_v1.route("/company/<id>")
def api_get_company_by_id(id):
    """
    Get a particular student details by his id.
    
    :param id: Id of the particular company
    :type id: str
    :return: a dict containing all the company details(company_name,concerned_person_name)
    :rtype: dict
    """
    pass

@user_api_v1.route("/register")
def register():
    pass

@user_api_v1.route("/login")
def login():
    pass

@user_api_v1.route("<id>/create_profile")
def create_profile():
    pass
