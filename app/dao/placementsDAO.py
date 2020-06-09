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
