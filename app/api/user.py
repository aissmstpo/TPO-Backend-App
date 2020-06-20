"""
This module contains all API for the users.
"""

import qrcode

from flask import Blueprint, jsonify, url_for, request, current_app, g, make_response

from bson.json_util import dumps, loads

from flask_jwt_extended import jwt_required, create_access_token, get_jwt_claims

from werkzeug.local import LocalProxy

from app.dao.usersDAO import (
    get_all_users,
    get_user_by_id,
    get_all_students,
    get_all_companies,
    approve_user,
    reject_user,
    create_profile,
    update_profile,
    create_user,
    get_user_by_email,
    get_approved_companies,
    get_unapproved_companies,
    get_approved_students,
    get_unapproved_students,
    get_eligible_companies,
    get_not_eligible_companies,
    current_placement_details,
)

from ..helpers import expect


def get_bcrypt():
    bcrypt = getattr(g, "_bcrypt", None)
    if bcrypt is None:
        bcrypt = g._bcrypt = current_app.config["BCRYPT"]
    return bcrypt


def get_jwt():
    jwt = getattr(g, "_jwt", None)
    if jwt is None:
        jwt = g._jwt = current_app.config["JWT"]
    return jwt


jwt = LocalProxy(get_jwt)
bcrypt = LocalProxy(get_bcrypt)

user_api_v1 = Blueprint("user_api_v1", "user_api_v1", url_prefix="/api/v1/user")


class UserObject(object):
    def __init__(self, id, role, is_approved, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.is_approved = is_approved

    def to_json(self):
        return loads(dumps(self, default=lambda o: o.__dict__, sort_keys=True))


@user_api_v1.route("/")
def api_get_all_users():
    """
    Get all users details.

    :returns: list of users with details
    :rtype: list
    """
    return jsonify(get_all_users())


@user_api_v1.route("/<id>")
def api_get_user_by_id(id):
    """
    Get a particular user details by his id.

    :param id: Id of the user
    :type id: str
    :returns: a dict containing user details
    :rtype: dict
    """
    return jsonify(get_user_by_id(id))


@user_api_v1.route("/student")
def api_get_all_students():
    """
    Get all student details.

    :returns: list of students with details
    :rtype: list
    """
    return jsonify(get_all_students())


@user_api_v1.route("/company")
def api_get_all_companies():
    """
    Get all student details.

    :returns: a list of companies with details.
    :rtype: list
    """
    return jsonify(get_all_companies())


@user_api_v1.route("/<id>/approve", methods=["PUT"])
def api_approve_user(id):
    try:
        result = approve_user(id)
        update_user = get_user_by_id(id)
        return jsonify({"user": update_user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_api_v1.route("/<id>/reject", methods=["PUT"])
def api_reject_user(id):
    try:
        result = reject_user(id, request.form["reason"])
        update_user = get_user_by_id(id)
        return jsonify({"user": update_user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_api_v1.route("<id>/create_profile", methods=["PUT"])
def api_create_profile(id):
    """
    """
    try:
        result = create_profile(id, request.get_json())
        return jsonify({"user_id": id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_api_v1.route("<id>/update_profile", methods=["PUT"])
def api_update_profile(id):
    """
    """
    try:
        result = update_profile(id, request.get_json())
        return jsonify({"user_id": id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_api_v1.route("/company/register", methods=["POST"])
def company_register():
    try:
        post_data = request.get_json()
        email = expect(post_data["email"], str, "email")
        password = expect(post_data["password"], str, "password")
        company_name = expect(post_data["company_name"], str, "company name")
        address = expect(post_data["address"], str, "address")
        website = expect(post_data["website"], str, "website")
        address = expect(post_data["address"], str, "address")
        name = expect(post_data["name"], str, "name")
        position = expect(post_data["position"], str, "position")
        contact = expect(post_data["contact"], str, "contact")

    except Exception as e:
        return jsonify({"error": str(e)})

    errors = {}
    user = get_user_by_email(email)
    if user:
        errors["email"] = "A user with the given email already exists."

    # add validation
    if len(password) < 8:
        errors["password"] = "Your password must be at least 8 characters."

    if len(errors.keys()) != 0:
        response_object = {"status": "fail", "error": errors}
        return jsonify(response_object), 411

    userdata = {
        "company_name": company_name,
        "role": "company",
        "website": website,
        "address": address,
        "password": bcrypt.generate_password_hash(
            password=password.encode("utf8")
        ).decode("utf-8"),
        "concerned_person": {
            "name": name,
            "position": position,
            "email": email,
            "contact": contact,
        },
        "profile_completed": True,
    }

    result = create_user(userdata)
    if "error" in result:
        errors["email"] = result["error"]
        return jsonify(errors), 400

    userdata = get_user_by_id(result["_id"])

    if not userdata:
        errors["general"] = "Internal error, please try again later."

    if len(errors.keys()) != 0:
        response_object = {"error": errors}
        return make_response(jsonify(response_object)), 400
    else:
        userdata = {
            "id": str(userdata["_id"]),
            "email": userdata["concerned_person"]["email"],
            "name": userdata["company_name"],
            "role": userdata["role"],
            "is_approved": True if "approved_date" in userdata else False,
        }
        user = UserObject(**userdata)
        jwt = create_access_token(user.to_json())
        ret = {"access_token": jwt}
        return jsonify(ret), 200


@user_api_v1.route("/login", methods=["POST"])
def login():
    """
    """
    try:
        post_data = request.get_json()
        email = expect(post_data["email"], str, "email")
        password = expect(post_data["password"], str, "password")
    except Exception as e:
        return jsonify({"error": str(e)})
    errors = {}
    user = get_user_by_email(email)
    if not user:
        errors["email"] = "No user with the given email already exists."
    # add validation
    if not bcrypt.check_password_hash(user["password"], password):
        errors["password"] = "Invalid password!"
    if len(errors) != 0:
        return jsonify({"error": errors})
    print(user)
    if user["role"] == "company":
        userdata = {
            "id": str(user["_id"]),
            "email": user.get("concerned_person").get("email"),
            "name": user.get("company_name"),
            "role": user["role"],
            "is_approved": True if "approved_date" in user else False,
        }
    else:
        userdata = {
            "id": str(user["_id"]),
            "email": user.get("email"),
            "name": user.get("full_name",""),
            "role": user["role"],
            "is_approved": True if "approved_date" in user else False,
        }
    user = UserObject(**userdata)
    jwt = create_access_token(user.to_json())
    ret = {"access_token": jwt}
    return jsonify(ret), 200


@user_api_v1.route("/company/approved")
def api_get_approved_companies():
    return jsonify(get_approved_companies())


@user_api_v1.route("/company/unapproved")
def api_get_unapproved_companies():
    limit = request.args.get("limit", None)
    if limit:
        return jsonify(get_unapproved_companies()[: int(limit)])
    return jsonify(get_unapproved_companies())


@user_api_v1.route("/student/approved")
def api_get_approved_students():
    return jsonify(get_approved_students())


@user_api_v1.route("/student/unapproved")
def api_get_unapproved_students():
    limit = request.args.get("limit", None)
    if limit:
        return jsonify(get_unapproved_students()[: int(limit)])
    return jsonify(get_unapproved_students())


@user_api_v1.route("/student/<id>/eligible_companies")
def api_get_eligible_companies(id):
    try:
        return jsonify(get_eligible_companies(id)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_api_v1.route("/student/<id>/not_eligible_companies")
def api_get_not_eligible_companies(id):
    try:
        return jsonify(get_not_eligible_companies(id)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_api_v1.route("/company/<id>/current_placement_details")
def api_current_placement_details(id):
    try:
        return jsonify(current_placement_details(id)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@user_api_v1.route("/student/register", methods=["POST"])
def student_register():
    try:
        post_data = request.get_json()
        email = expect(post_data["email"], str, "email")
        password = expect(post_data["password"], str, "password")
    except Exception as e:
        return jsonify({"error": str(e)})

    errors = {}
    user = get_user_by_email(email)
    if user:
        errors["email"] = "A user with the given email already exists."

    # add validation
    if len(password) < 8:
        errors["password"] = "Your password must be at least 8 characters."

    if len(errors.keys()) != 0:
        response_object = {"status": "fail", "error": errors}
        return jsonify(response_object), 411

    userdata = {
        "role": "student",
        "password": bcrypt.generate_password_hash(
            password=password.encode("utf8")
        ).decode("utf-8"),
        "email": email,
        "profile_completed": False,
    }

    result = create_user(userdata)
    if "error" in result:
        errors["email"] = result["error"]
        return jsonify(errors), 400

    userdata = get_user_by_id(result["_id"])

    if not userdata:
        errors["general"] = "Internal error, please try again later."

    if len(errors.keys()) != 0:
        response_object = {"error": errors}
        return make_response(jsonify(response_object)), 400
    else:
        userdata = {
            "id": str(userdata["_id"]),
            "email": userdata["email"],
            "role": userdata["role"],
            "name": userdata.get("full_name", ""),
            "is_approved": True if "approved_date" in userdata else False,
        }
        user = UserObject(**userdata)
        jwt = create_access_token(user.to_json())
        ret = {"access_token": jwt}
        return jsonify(ret), 200


@user_api_v1.route("/student/qrcode", methods=["POST", "GET"])
def api_generate_qrcode():
    user_details = request.json
    id = user_details["_id"]
    user = get_user_by_id(id)
    if user:
        qr = qrcode.QRCode(version=1, box_size=15, border=5)
        data = {
            "roll_number": user["roll_number"],
            "department": user["department"],
            "class": user["class"],
        }
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        img.save("static/" + user["roll_number"] + ".png")
        return "QRCode Generated"
    else:
        return "ERROR QRCode is not Generated"
    return jsonify()


@user_api_v1.route("/info")
def all_available_endpoints():
    """
    Get all availale api endpoint details.

    :returns: dict containing all api endpoint details.
    :rtype: dict
    """
    info = {
        "info": {
            "url": "GET " + url_for("user_api_v1.all_available_endpoints"),
            "description": all_available_endpoints.__doc__.strip(),
        },
        "login": {
            "url": "GET " + url_for("user_api_v1.login"),
            "description": login.__doc__.strip(),
        },
        "register": {
            "url": "GET " + url_for("user_api_v1.register"),
            "description": register.__doc__.strip(),
        },
        "create profile": {
            "url": "GET " + user_api_v1.url_prefix + "/<id>/create_profile",
            "description": create_profile.__doc__.strip(),
        },
        "all users": {
            "url": "GET " + url_for("user_api_v1.api_get_all_users"),
            "description": api_get_all_users.__doc__.strip(),
        },
        "all students": {
            "url": "GET " + url_for("user_api_v1.api_get_all_students"),
            "description": api_get_all_students.__doc__.strip(),
        },
        "all companies": {
            "url": "GET " + url_for("user_api_v1.api_get_all_companies"),
            "description": api_get_all_companies.__doc__.strip(),
        },
        "particular user": {
            "url": "GET " + user_api_v1.url_prefix + "/<id>",
            "description": api_get_user_by_id.__doc__.strip(),
        },
    }
    return jsonify(info)
