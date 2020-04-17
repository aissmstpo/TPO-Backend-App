import os
from flask import jsonify
from app import create_app
from pymongo import MongoClient

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)


@app.route("/")
def index():
    client = MongoClient(app.config["DB_URI"])
    dbs = client.list_database_names()
    return jsonify(dbs)

if __name__ == '__main__':
    app.run()