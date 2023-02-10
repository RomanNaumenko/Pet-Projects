import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from mongo_utils import MongoDBConnection
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

app = Flask(__name__)


@app.route("/alarms", methods=["GET", "POST", "PUT"])
def alarms():
    if request.method == "GET":
        with MongoDBConnection("admin", "admin", "127.0.0.1") as db:
            collection = db["alarm_status"]
            output = collection.find()
            return jsonify({'result': [[result["Point"], result["Status"]] for result in output]})

    if request.method == "POST":
        with MongoDBConnection("admin", "admin", "127.0.0.1") as db:
            collection = db["alarm_status"]
            object_id = collection.insert_one(
                {'Point': request.json["Point"], 'Status': request.json["Status"]}).inserted_id
        return jsonify({"id": f"{object_id}"})

    if request.method == "PUT":
        with MongoDBConnection("admin", "admin", "127.0.0.1") as db:
            collection = db["alarm_status"]
            collection.update_one({"_id": request.json["id"]},
                                  {"$set": {'Point': request.json["Point"], 'Status': request.json["Status"]}})
            return jsonify({"id": f'{request.json["id"]}'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
