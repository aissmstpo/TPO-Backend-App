"""
This module contains all API for the users.
"""
from flask import Blueprint, jsonify, request

from app.dao.usersDAO import (get_all_users, get_all_students, get_user_by_id, get_all_companies,
                            get_approved_companies, get_approved_students,get_user_by_email,get_user_password_by_email,register_user)
user_api_v1 = Blueprint("user_api_v1","user_api_v1",url_prefix="/api/v1/user")
import qrcode


@user_api_v1.route("/")
def api_get_all_users():
    """
    Get all users details.

    :returns: list of users with details
    :rtype: list
    """
    return jsonify(get_all_users())

@user_api_v1.route("/student")
def api_get_all_students():
    """
    Get all student details.

    :returns: list of students with details
    :rtype: list
    """
    return jsonify(get_all_students())

@user_api_v1.route("/<id>")
def api_get_user_by_id(id):
    """
    Get a particular user details by his id.

    :param id: Id of the user
    :type id: str
    :return: a dict containing user details
    :rtype: dict
    """
    return jsonify(get_user_by_id(id))

@user_api_v1.route("/company")
def api_get_all_companies():
    """
    Get all student details.
    :returns: a list of companies with details.
    :rtype: list
    """
    return jsonify(get_all_companies())

    
@user_api_v1.route("<id>/create_profile")
def create_profile():
    """
    """
    pass

@user_api_v1.route("/company/approved")
def api_get_approved_companies():
    """
    Get list of all approved copmanies
    :returns: a list of approved companies with details.
    :rtype: list
    """
    return jsonify(get_approved_companies())

@user_api_v1.route("/info")
def all_available_endpoints():
    """
    Get all availale api endpoint details.
    :return: dict containing all api endpoint details.
    :rtype: dict
    """
    info = {
        'info' : {
            "url" : "GET " +  url_for('user_api_v1.all_available_endpoints'),
            "description" : all_available_endpoints.__doc__.strip()
        },
        'login' : {
            "url" : "GET " +  url_for('user_api_v1.login'),
            "description" : login.__doc__.strip()
        },
        'register' : {
            "url" : "GET " +  url_for('user_api_v1.register'),
            "description" : register.__doc__.strip()
        },
        'create profile' : {
            "url" : "GET " + user_api_v1.url_prefix + "/<id>/create_profile",
            "description" : create_profile.__doc__.strip()
        },
        'all users' : {
            "url" : "GET " +  url_for('user_api_v1.api_get_all_users'),
            "description" : api_get_all_users.__doc__.strip()
        },
        'all students' : {
            "url" : "GET " +  url_for('user_api_v1.api_get_all_students'),
            "description" : api_get_all_students.__doc__.strip()
        },
        'all companies' : {
            "url" : "GET " +  url_for('user_api_v1.api_get_all_companies'),
            "description" : api_get_all_companies.__doc__.strip()
        },
        'particular user' : {
            "url" : "GET " + user_api_v1.url_prefix + "/<id>",
            "description" : api_get_user_by_id.__doc__.strip()
        }
    }
    return jsonify(info)

@user_api_v1.route("/student/approved")
def api_get_approved_students():
    """
    Get details of all students 'approved by college'.
    :returns: a list of 'approved' students details
    :rtype: list
    """
    return jsonify(get_approved_students())

@user_api_v1.route("/student/qrcode",methods = ["POST","GET"])
def api_generate_qrcode():
    user_details = request.json
    id = user_details["_id"]
    user = get_user_by_id(id)
    if user:
            qr = qrcode.QRCode(
            version = 1,
            box_size =15,
            border = 5
            )
            data = {
                "roll_number":user['roll_number'],
                "department":user['department'],
                "class":user['class']
                }
            qr.add_data(data)
            qr.make(fit = True)
            img = qr.make_image(fill='black',back_color='white')
            img.save('static/'+user['roll_number']+'.png')
            return "QRCode Generated"
    else:
        return "ERROR QRCode is not Generated"
    return jsonify()
