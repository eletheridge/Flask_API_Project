from flask import Flask, request
from mongo_calls import MongoConnect
from datetime import datetime
import extras
from redis_calls import RedisClient

app = Flask(__name__)

mongo_client = MongoConnect("test")


@app.route('/')
def index():
    return "Welcome to the Jungle"


@app.route('/mongotest', methods=["POST", "GET"])
@extras.authenticate
@extras.responder
def mongo_test():
    if request.method == "POST":
        body = request.json
        if "post_message" in body.keys():
            dt = datetime.now()
            payload = {"post_message": body['post_message'], "timestamp": dt.strftime("%m/%d/%Y, %H:%M:%S")}
            response = mongo_client.post(payload)
            _id = str(response.inserted_id)
            response = mongo_client.one(_id)
            return response, 200
        else:
            response = "FAIL"
            return response, 400
    if request.method == "GET":
        if request.args.get("id"):
            query = str(request.args.get("id"))
            response = mongo_client.one(query)
            return response, 200
        else:
            response = "Missing expected argument: 'id'"
            return response, 400


@app.route('/redistest', methods=["GET", "POST"])
@extras.authenticate
@extras.responder
def redis_test():
    client = RedisClient()
    if request.method == "GET":
        if request.args.get("key"):
            response = client.get(request.args.get("key"))
            return response, 200
        else:
            return "Missing expected argument: 'key'", 400
    if request.method == "POST":
        body = request.json
        if len(body.keys()) > 1 or len(body.keys()) < 1:
            return "Malformed Payload", 400
        else:
            for key in body:
                response = client.set(key, body[key])
                if response:
                    return {key: client.get(key)}, 200


if __name__ == '__main__':
    app.run()
