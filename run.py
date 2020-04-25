import os
from flask import jsonify
from app import create_app
from pymongo import MongoClient

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()