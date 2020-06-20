"""
This module contains all API for the placements.
"""
from flask import Blueprint, jsonify, request

from ..helpers import expect
from app.dao.placementsDAO import (
    start_placement,
    create_phase,
    approve_phase,
    suggest_date_phase,
    get_unapproved_phases,
    get_upcoming_phases,
    get_pending_phases,
    get_phase_result,
)

placement_api_v1 = Blueprint(
    "placement_api_v1", "placement_api_v1", url_prefix="/api/v1/placement"
)


@placement_api_v1.route("/start")
def api_start_placement():
    """
    Starts the placement by adding the details of the placement in the database.
    This function will send a JSON response to the browser containing
    success = True & the _id of the inserted document &
    a 200 OK status code.

    In case of an Exception it sends a JSON response containing the errors &
    a 400 Bad Request status code.

    :returns: tuple of dictionary and status code
    :rtype: tuple
    """
    try:
        try:
            post_data = request.get_json()
            expect(post_data["company_id"], str, "company id")
            expect(post_data["domain"], str, "domain")
            expect(post_data["requirement"], str, "requirement"),
            expect(post_data["sgpa"], str, "sgpa"),
            expect(post_data["live_backlog"], str, "live_backlog"),
            expect(post_data["gender"], str, "gender"),
            expect(post_data["positions"], str, "positions"),
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        return jsonify(start_placement(post_data)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@placement_api_v1.route("/phase/create")
def api_create_phase():
    """
    Creates a new phase in placement by adding the details of the phase in the database.
    This function will send a JSON response to the browser containing
    success = True and a 200 OK status code.

    In case of an Exception it sends a JSON response containing the errors &
    a 400 Bad Request status code.

    :returns: tuple of dictionary and status code
    :rtype: tuple
    """
    try:
        try:
            post_data = request.get_json()
            expect(post_data["_id"], str, "placement id(_id)")
            expect(post_data["title"], str, "title")
            expect(post_data["description"], str, "description"),
            expect(post_data["date"], str, "date"),
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        return jsonify(create_phase(post_data)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@placement_api_v1.route("/phase/approve", methods=["PUT"])
def api_approve_phase():
    """
    Approves the requested date for the phase of a placement.
    This function will send a JSON response to the browser containing
    success = True and a 200 OK status code.

    In case of an Exception it sends a JSON response containing the errors &
    a 400 Bad Request status code.

    :returns: tuple of dictionary and status code
    :rtype: tuple
    """
    try:
        try:
            post_data = request.get_json()
            placement_id = expect(post_data["placement_id"], str, "placement id")
            phase_title = expect(post_data["phase_title"], str, "Phase title")
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        return jsonify(approve_phase(placement_id, phase_title)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@placement_api_v1.route("/phase/suggest_date", methods=["PUT"])
def api_suggest_date_phase():
    """
    Suggests a date for a phase of the placement.
    This function will send a JSON response to the browser containing
    success = True and a 200 OK status code.

    In case of an Exception it sends a JSON response containing the errors &
    a 400 Bad Request status code.

    :returns: tuple of dictionary and status code
    :rtype: tuple
    """
    try:
        try:
            post_data = request.get_json()
            placement_id = expect(post_data["placement_id"], str, "placement id")
            phase_title = expect(post_data["phase_title"], str, "Phase title")
            suggested_date = expect(post_data["suggested_date"], str, "Suggested date")
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        return (
            jsonify(suggest_date_phase(placement_id, phase_title, suggested_date)),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@placement_api_v1.route("/phase/unapproved")
def api_get_unapproved_phases():
    """
    Returns a list of unapproved phases of all placements and a 200 OK status code.
    If a limit is passed in the request then list contains no more than ``limit``
    number of unapproved phases.

    This function will send a JSON response to the browser containing
    list of unapproved phases and a 200 OK status code.

    In case of an Exception it sends a JSON response containing the errors &
    a 400 Bad Request status code.

    :returns: tuple of dictionary and status code
    :rtype: tuple
    """
    try:
        limit = request.args.get("limit", None)
        if limit:
            return jsonify(get_unapproved_phases()[: int(limit)]), 200
        return jsonify(get_unapproved_phases()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@placement_api_v1.route("/phase/upcoming", methods=["GET"])
def api_upcoming_phases():
    """
    Returns a list of upcoming phases of all placements and a 200 OK status code.
    If a limit is passed in the request then list contains no more than ``limit``
    number of upcoming phases.

    This function will send a JSON response to the browser containing
    list of upcoming phases and a 200 OK status code.

    In case of an Exception it sends a JSON response containing the errors &
    a 400 Bad Request status code.

    :returns: tuple of dictionary and status code
    :rtype: tuple
    """
    try:
        limit = request.args.get("limit", None)
        if limit:
            return jsonify(get_upcoming_phases()[: int(limit)]), 200
        return jsonify(get_upcoming_phases()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@placement_api_v1.route("/phase/pending", methods=["GET"])
def api_get_upcoming_phases():
    """
    Returns a list of pending phases of all placements and a 200 OK status code.
    If a limit is passed in the request then list contains no more than ``limit``
    number of pending phases.

    This function will send a JSON response to the browser containing
    list of pending phases and a 200 OK status code.

    In case of an Exception it sends a JSON response containing the errors &
    a 400 Bad Request status code.

    :returns: tuple of dictionary and status code
    :rtype: tuple
    """
    try:
        limit = request.args.get("limit", None)
        if limit:
            return jsonify(get_pending_phases()[: int(limit)]), 200
        return jsonify(get_pending_phases()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@placement_api_v1.route("/phase/result", methods=["GET"])
def api_get_phase_result():
    """
    This function will send a JSON response to the browser containing
    results of a particular company & phase &
    a 200 OK status code.

    In case of an Exception it sends a JSON response containing the errors &
    a 400 Bad Request status code.
    """
    try:
        company_id = expect(request.args["company_id"], str, "Company id")
        phase_title = expect(request.args["phase_title"], str, "Phase title")
        return jsonify(get_phase_result(company_id, phase_title)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
