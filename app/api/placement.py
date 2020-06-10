"""
This module contains all API for the placements.
"""
from flask import Blueprint, jsonify, request

from app.dao.placementsDAO import (
    get_unapproved_phases,
    approve_phase,
    suggest_date_phase,
    upcoming_phases,
)

placement_api_v1 = Blueprint(
    "placement_api_v1", "placement_api_v1", url_prefix="/api/v1/placement"
)


@placement_api_v1.route("/phase/unapproved")
def api_get_unapproved_phases():
    try:
        limit = request.args.get("limit", None)
        if limit:
            return jsonify(get_unapproved_phases()[: int(limit)]), 200
        return jsonify(get_unapproved_phases()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@placement_api_v1.route("/phase/approve", methods=["PUT"])
def api_approve_phase():
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


@placement_api_v1.route("/phase/upcoming", methods=["GET"])
def api_upcoming_phases():
    try:
        limit = request.args.get("limit", None)
        if limit:
            return jsonify(upcoming_phases()[: int(limit)]), 200
        return jsonify(upcoming_phases()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

