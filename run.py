import os
from flask import jsonify
from app import create_app
from pymongo import MongoClient

# set the environment variable 'FLASK_CONFIG' to 'development' or 'production'
# for Linux
# export FLASK_CONFIG=development
# for windows
# set FLASK_CONFIG=development
config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
