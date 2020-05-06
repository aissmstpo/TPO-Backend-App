"""
This module contains all API for the placements.
"""
from flask import Blueprint

placement_api_v1 = Blueprint("placement_api_v1","placement_api_v1",url_prefix="/api/v1/placement")
