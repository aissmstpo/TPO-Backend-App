from datetime import datetime, timezone

from werkzeug.local import LocalProxy
from bson import ObjectId
from app.db import get_db
from pymongo.errors import PyMongoError

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def approve_phase(placement_id, phase_title):
    try:
        # type of requested_date is datetime.datetime
        requested_date = list(
            db["placements"].find(
                {"_id": ObjectId(placement_id), "phases.title": phase_title},
                {"phases.$": 1},
            )
        )[0]["phases"][0]["requested_date"]

        result = db["placements"].update_one(
            {"_id": ObjectId(placement_id), "phases.title": phase_title},
            {"$set": {"phases.$.scheduled_date": requested_date}},
        )
        if result.matched_count == 0:
            raise ValueError("No such phase")
        if result.modified_count == 0:
            raise ValueError("No document updated(Phase is already approved)")
        return {"success": True}
    except PyMongoError as e:
        return e


def suggest_date_phase(placement_id, phase_title, suggested_date):
    try:
        result = db["placements"].update_one(
            {"_id": ObjectId(placement_id), "phases.title": phase_title},
            {
                "$set": {
                    "phases.$.suggested_date": datetime.strptime(
                        suggested_date, "%Y-%m-%d"
                    )
                }
            },
        )
        if result.matched_count == 0:
            raise ValueError("No such phase")
        if result.modified_count == 0:
            raise ValueError("No document updated")
        return {"success": True}
    except PyMongoError as e:
        return e


def get_unapproved_phases():
    try:
        return list(
            db["placements"].aggregate(
                [
                    {"$unwind": {"path": "$phases"}},
                    {
                        "$match": {
                            "phases.scheduled_date": {"$exists": False},
                            "phases.requested_date": {"$exists": True},
                            "phases.suggested_date": {"$exists": False},
                        }
                    },
                    {
                        "$lookup": {
                            "from": "users",
                            "localField": "company_id",
                            "foreignField": "_id",
                            "as": "company_details",
                        }
                    },
                    {"$unwind": {"path": "$company_details"}},
                    {
                        "$project": {
                            "_id": 1,
                            "company_name": "$company_details.company_name",
                            "email": "$company_details.concerned_person.email",
                            "requested_date": "$phases.requested_date",
                            "phase": "$phases.title",
                            "phase_description": "$phases.phase_description",
                        }
                    },
                ]
            )
        )
    except PyMongoError as e:
        return e


def upcoming_phases():
    try:
        return list(
            db["placements"].aggregate(
                [
                    {"$unwind": {"path": "$phases"}},
                    {
                        "$match": {
                            "phases.scheduled_date": {
                                "$gt": datetime(
                                    2020, 5, 8, 0, 0, 0, tzinfo=timezone.utc
                                )
                            }
                        }
                    },
                    {
                        "$lookup": {
                            "from": "users",
                            "localField": "company_id",
                            "foreignField": "_id",
                            "as": "company_details",
                        }
                    },
                    {"$unwind": {"path": "$company_details"}},
                    {
                        "$project": {
                            "company_name": "$company_details.company_name",
                            "email": "$company_details.concerned_person.email",
                            "date": "$phases.scheduled_date",
                            "phase_title": "$phases.title",
                            "phase_description": "$phases.phase_description",
                            "requirement": 1,
                        }
                    },
                ]
            )
        )
    except PyMongoError as e:
        return e

