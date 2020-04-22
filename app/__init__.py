from flask import Flask

from config import app_config
from app.api.user import user_api_v1
from app.api.placement import placement_api_v1
def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.register_blueprint(user_api_v1)
    app.register_blueprint(placement_api_v1)

    return app