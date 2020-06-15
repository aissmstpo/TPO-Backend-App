from datetime import timedelta

from flask import Flask
from flask.json import JSONEncoder
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from bson import json_util, ObjectId

from config import app_config
from app.api.user import user_api_v1
from app.api.placement import placement_api_v1
from app.api.post import post_api_v1
from app.api.post import notice_api_v1


class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")

    app.json_encoder = MongoJsonEncoder

    # bcrypt
    app.config["BCRYPT"] = Bcrypt(app)

    # jwt
    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_access_token(identity):
        return {"user": identity}

    app.config["JWT_SECRET_KEY"] = "asdat8d5#@b3m13iu"
    app.config["JWT"] = jwt
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)

    app.register_blueprint(user_api_v1)
    app.register_blueprint(placement_api_v1)
    app.register_blueprint(post_api_v1)
    app.register_blueprint(notice_api_v1)

    return app
