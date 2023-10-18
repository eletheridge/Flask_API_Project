from flask import Flask, request
from mongo_calls import MongoConnect
from datetime import datetime
import extras
from redis_calls import RedisClient
from logger import Logger
import s3_calls
import auth

app = Flask(__name__)

mongo_client = MongoConnect("test")
s3 = s3_calls.S3()
logger = Logger(filename='logs/api.log', app_name='API')


@app.route('/')
def index():
    return "Welcome to the Jungle"


@app.route('/create_client', methods=["POST"])
@extras.responder
def create_client():
    logger.write(level="INFO",
                 message=f'INBOUND CREATE CLIENT REQUEST -- BODY: {request.json}')
    body = request.json
    if "client_name" in body.keys():
        client_name = body['client_name']
        response = auth.generate_client_keys(client_name)
        logger.write(level="INFO",
                     message=f'OUTBOUND CREATE CLIENT RESPONSE -- ID: {response["_id"]} -- BODY: {response}')
        return response, 200


@app.route('/get_refresh_token', methods=["POST"])
@extras.responder
def get_refresh_token():
    logger.write(level="INFO",
                 message=f'INBOUND GET REFRESH TOKEN REQUEST -- ID: {request.headers.get("X-Client-ID", "NONE")}')
    body = request.json
    if "client_id" in body.keys() and "client_secret" in body.keys():
        client_id = body['client_id']
        client_secret = body['client_secret']
        response = auth.generate_refresh_token(client_id, client_secret)
        logger.write(level="INFO",
                     message=f'OUTBOUND GET REFRESH TOKEN RESPONSE -- ID: {client_id} -- BODY: {response}')
        return response, 200
    else:
        response = "Missing expected argument(s): 'client_id', 'client_secret'"
        logger.write(level="INFO",
                     message=f'OUTBOUND GET REFRESH TOKEN RESPONSE -- ID: {request.args.get("id")} -- BODY: {response}')
        return response, 400


@app.route('/mongotest', methods=["POST", "GET"])
@extras.authenticate
@extras.responder
def mongo_test():
    if request.method == "POST":
        logger.write(level="INFO",
                     message=f'INBOUND POST REQUEST -- ID: {request.args.get("id")} -- BODY: {request.json}')
        body = request.json
        if "post_message" in body.keys():
            dt = datetime.now()
            payload = {"post_message": body['post_message'], "timestamp": dt.strftime("%m/%d/%Y, %H:%M:%S")}
            response = mongo_client.post(payload)
            _id = str(response.inserted_id)
            response = mongo_client.one(_id)
            logger.write(level="INFO",
                         message=f'OUTBOUND POST RESPONSE -- ID: {_id} -- BODY: {response}')
            return response, 200
        else:
            response = "FAIL"
            return response, 400
    if request.method == "GET":
        logger.write(level='INFO', message={"method": request.method, "id": request.args.get("id")})
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
        logger.write(level='INFO', message={"method": request.method, "id": request.args.get("id")})

        if request.args.get("key"):
            response = client.get(request.args.get("key"))
            return response, 200
        else:
            return "Missing expected argument: 'key'", 400
    if request.method == "POST":
        logger.write(level="INFO",
                     message=f'INBOUND POST REQUEST -- ID: {request.args.get("id")} -- BODY: {request.json}')
        body = request.json
        if len(body.keys()) > 1 or len(body.keys()) < 1:
            return "Malformed Payload", 400
        else:
            for key in body:
                response = client.set(key, body[key])
                if response:
                    logger.write(level="INFO",
                                 message=f'OUTBOUND POST RESPONSE -- ID: {key} -- BODY: {client.get(key)}')
                    return {key: client.get(key)}, 200


@app.route('/s3/upload/', methods=["POST"])
@extras.authenticate
@extras.responder
def s3_upload():
    logger.write(level="INFO",
                 message=f'INBOUND S3 UPLOAD REQUEST -- ID: {request.args.get("id")} -- BODY: {request.json}')
    body = request.json
    if "bucket" in body.keys() and "file" in body.keys() and 'filename' in body.keys():
        bucket = body['bucket']
        file = body['file']
        if len(file) % 4 != 0:
            logger.write(level="INFO",
                         message=f'OUTBOUND UPLOAD RESPONSE -- ID: {body["filename"]} -- BODY: Invalid Base64 String')
            return "Invalid Base64 String", 400
        filename = body['filename']
        result = s3.upload_file(file, bucket, filename)
        if result == "Success":
            logger.write(level="INFO",
                         message=f'OUTBOUND UPLOAD RESPONSE -- ID: {filename} -- BODY: {result}')
            return "File Uploaded", 200
        else:
            logger.write(level="INFO",
                         message=f'OUTBOUND UPLOAD RESPONSE -- ID: {filename} -- BODY: {result}')
            return result, 400


@app.route('/s3/download/', methods=["POST"])
@extras.authenticate
@extras.responder
def s3_download():
    logger.write(level="INFO",
                 message=f'INBOUND DOWNLOAD REQUEST -- ID: {request.args.get("id")} -- BODY: {request.json}')
    body = request.json
    if "bucket" in body.keys() and "file" in body.keys():
        bucket = body['bucket']
        file = body['file']
        result, data = s3.download_file(bucket, file)
        if result == "Success":
            logger.write(level="INFO",
                         message=f'OUTBOUND DOWNLOAD RESPONSE -- ID: {file} -- BODY: {data}')
            return data, 200
        else:
            logger.write(level="INFO",
                         message=f'OUTBOUND DOWNLOAD RESPONSE -- ID: {file} -- BODY: {result}')
            return result, 404


if __name__ == '__main__':
    app.run()
