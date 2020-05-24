from flask import Flask
from flask.json import JSONEncoder

from bson import json_util, ObjectId

from config import app_config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
bcrypt = Bcrypt()
login_manager = LoginManager()
from app.api.user import user_api_v1
from app.api.placement import placement_api_v1
from app.api.post import post_api_v1

class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    bcrypt.init_app(app)
    app.secret_key = '123456789'
    app.json_encoder = MongoJsonEncoder
    login_manager.init_app(app)
    app.register_blueprint(user_api_v1)
    app.register_blueprint(placement_api_v1)
    app.register_blueprint(post_api_v1)
    return app
