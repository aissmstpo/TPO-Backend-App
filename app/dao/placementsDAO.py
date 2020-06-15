from datetime import datetime, timezone

from werkzeug.local import LocalProxy

from bson import ObjectId

from pymongo.errors import PyMongoError

from app.db import get_db

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def start_placement(placement_data):
    try:
        result = db["placements"].insert_one(
            {
                "year": datetime.now().year,
                "company_id": placement_data["company_id"],
                "domain": placement_data["domain"],
                "requirement": placement_data["requirement"],
                "eligibility": {
                    "sgpa": placement_data["spga"],
                    "live_backlog": placement_data["live_backlog"],
                    "gender": placement_data["gender"],
                },
                "positions": placement_data["positions"],
            }
        )
        return {"success": True, "_id": result.inserted_id}
    except PyMongoError as e:
        return e


def create_phase(phase_data):
    try:
        result = db["placements"].update_one(
            {"_id": ObjectId(phase_data["_id"])},
            {
                "$push": {
                    "phases": {
                        "title": phase_data["title"],
                        "description": phase_data["description"],
                        "requested_date": datetime.strptime(
                            phase_data["date"], "%Y-%m-%d"
                        ),
                    }
                }
            },
        )
        if result.matched_count == 0:
            raise ValueError("No such placement with that id")
        if result.modified_count == 0:
            raise ValueError("No document updated")
        return {"success": True}
    except PyMongoError as e:
        return e


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


def get_pending_phases():
    try:
        return list(
            db["placements"].aggregate(
                [
                    {"$unwind": {"path": "$phases"}},
                    {
                        "$match": {
                            "$and": [
                                {"phases.scheduled_date": {"$exists": False}},
                                {"phases.suggested_date": {"$exists": True}},
                            ]
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
                            "requested_date": "$phases.requested_date",
                            "suggested_date": "$phases.suggested_date",
                            "phase": "$phases.title",
                        }
                    },
                ]
            )
        )
    except PyMongoError as e:
        return e


def get_upcoming_phases():
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


# not used
def get_registered_students(company_id):
    try:
        return list(
            db["placements"].aggregate(
                [
                    {"$unwind": {"path": "$registered_students"}},
                    {"$match": {"company_id": ObjectId(company_id)}},
                    {"$project": {"id": "$registered_students", "_id": 0}},
                    {
                        "$lookup": {
                            "from": "users",
                            "let": {"id": "$id"},
                            "pipeline": [
                                {"$match": {"$expr": {"$eq": ["$$id", "$_id"]}}},
                                {"$project": {"full_name": 1, "email": 1, "_id": 0}},
                            ],
                            "as": "profile",
                        }
                    },
                    {"$unwind": {"path": "$profile"}},
                ]
            )
        )
    except PyMongoError as e:
        return e


def get_all_registered_students():
    try:
        return list(
            db["placements"].aggregate(
                [
                    {
                        "$lookup": {
                            "from": "users",
                            "localField": "registered_students",
                            "foreignField": "_id",
                            "as": "registered_students",
                        }
                    },
                    {"$project": {"registered_students": 1, "company_id": 1, "_id": 0}},
                    {
                        "$project": {
                            "registered_students.password": 0,
                            "registered_students.sem_marks": 0,
                            "registered_students.other_qualifications": 0,
                            "registered_students.projects": 0,
                            "registered_students.role": 0,
                            "registered_students.extra_activities": 0,
                        }
                    },
                ]
            )
        )
    except PyMongoError as e:
        return e


def get_phase_result(company_id, phase_title):
    print(company_id, phase_title)
    try:
        return list(
            db["placements"].aggregate(
                [
                    {
                        "$match": {
                            # "year": str(datetime.now().year),
                            "year": "2021",
                            "company_id": ObjectId(company_id),
                        }
                    },
                    {
                        "$project": {
                            "phase": {
                                "$arrayElemAt": [
                                    {
                                        "$filter": {
                                            "input": "$phases",
                                            "as": "phase",
                                            "cond": {
                                                "$eq": ["$$phase.title", phase_title]
                                            },
                                        }
                                    },
                                    0,
                                ]
                            }
                        }
                    },
                    {"$project": {"results": "$phase.results"}},
                    {"$unwind": {"path": "$results"}},
                    {
                        "$project": {
                            "student_id": "$results.student_id",
                            "status": "$results.status",
                        }
                    },
                    {
                        "$lookup": {
                            "from": "users",
                            "localField": "student_id",
                            "foreignField": "_id",
                            "as": "profile",
                        }
                    },
                    {
                        "$project": {
                            "profile": {"$arrayElemAt": ["$profile", 0]},
                            "status": 1,
                        }
                    },
                    {
                        "$project": {
                            "name": "$profile.full_name",
                            "class": "$profile.class",
                            "department": "$profile.department",
                            "rollno": "$profile.roll_number",
                            "status": "$status",
                        }
                    },
                ]
            )
        )
    except PyMongoError as e:
        return e
