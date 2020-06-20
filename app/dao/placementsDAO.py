from datetime import datetime, timezone

from werkzeug.local import LocalProxy

from bson import ObjectId

from pymongo.errors import PyMongoError

from app.db import get_db

# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def start_placement(placement_data):
    """
    Inserts a document containing details of the placement.
    Returns a dictionary with success = True & the _id of the inserted document.

    In case of a PyMongoError it returns the exception

    :param placement_data: dictionary containing details of the placement
    :type placement_data: dict
    :returns: dictionary containing success = True & _id of the inserted document.
    :rtype: dict
    """
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
    """
    Inserts a phase in the array of phases in a particular placement.
    This phase contains a title, description & requested_date.
    Returns a dictionary with success = True.

    In case of a ValueError an exception is returned.

    :param phase_data: dictionary containing details of the phase to create.
    :type phase_data: dict
    :returns: dictionary containing success = True
    :rtype: dict
    """
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
    """
    Approves the requested date for the phase of a placement.
    Adds a field ``scheduled_date`` = ``requested_date`` in the phase.
    Returns a dictionary with success = True.

    In case of a ValueError an exception is returned.

    :param placement_id: id of the placement of which phase is to be approved.
    :type placement_id: str
    :param phase_title: title of the phase to be approved.
    :type phase_title: str
    :returns: Dictionary containing success = True
    :rtype: dict
    """
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
    """
    Suggest a date for a phase of the placement.
    Sets the suggested_date field of given phase.
    Returns a dictionary with success = True.

    In case of a ValueError an exception is returned.

    :param placement_id: id of the placement.
    :type placement_id: str
    :param phase_title: title of the phase for which a date is to be suggested.
    :type phase_title: str
    :param suggested_date: date suggested for the phase ("YYYY-mm-dd")
    :type suggested_date: str
    :returns: Dictionary containing success = True
    :rtype: dict
    """
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
    """
    This function returns the list of unapproved phases of all placements
    These phases are dictionary containining _id, email, requested_date,
    phase and phase_description.

    In case of a PyMongoError it returns the exception.

    :returns: list of unapproved phases of all placements.
    :rtype: list
    """
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
    """
    This function returns the list of pending phases of all placements
    These phases are dictionary containining company_name, email, requested_date,
    suggested_date and phase.

    In case of a PyMongoError it returns the exception.

    :returns: list of pending phases of all placements.
    :rtype: list
    """
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
    """
    This function returns the list of upcoming phases of all placements
    These phases are dictionary containing company_name, email, date,
    phase_title, phase_description and requirement.

    In case of a PyMongoError it returns the exception.

    :returns: list of upcoming phases of all placements.
    :rtype: list
    """
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
    """
    Returns a list of registered students of a particular company.
    This list contains dictionaries of students id of student and profile
    of student containing email & full_name.

    In case of a PyMongoError it returns the exception.

    :returns: list of registered students of a particular company.
    :rtype: list
    """
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
    """
    Returns a list of all registered students for every company(placement).
    This list contains dictionaries of students having various details.

    In case of a PyMongoError it returns the exception.

    :returns: list of all registered students for every company(placement).
    :rtype: list
    """
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
    """
    Returns list of results of a particular company_id having a particular phase_title
    containing _id, class, department, name, rollno & status of students.

    In case of an PyMongoError it returns the exception

    :returns: list of results
    :rtype: list
    """
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
