from flask import Flask
from flask.json import JSONEncoder

from bson import json_util, ObjectId

from config import app_config
from app.api.user import user_api_v1
from app.api.placement import placement_api_v1
from flask_bcrypt import Bcrypt


class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    bcrypt = Bcrypt(app)
    bcrypt.init_app(app)
    app.secret_key = '123456789'
    app.json_encoder = MongoJsonEncoder
    
    app.register_blueprint(user_api_v1)
    app.register_blueprint(placement_api_v1)

    return app
