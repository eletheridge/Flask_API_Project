from flask import Flask, request
import auth
import common.extras as extras
app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to Auth Service"


@app.route('/auth_token', methods=["POST", "GET"])
@extras.responder
def auth_token():
    if request.method == "POST":
        body = request.form
        if "client_id" in body.keys() and "client_secret" in body.keys():
            client_id = body['client_id']
            client_secret = body['client_secret']
            response = auth.generate_auth_token(client_id, client_secret)
            return response, 200
        else:
            response = "Missing expected argument(s): 'client_id', 'client_secret'"
            return response, 400
    if request.method == "GET":
        cid = request.args.get("cid")
        token = request.args.get("auth_token")
        response = auth.validate_auth_token(cid, token)
        if not response:
            return "NOT AUTHORIZED", 401
        else:
            return "AUTHORIZED", 200


if __name__ == '__main__':
    app.run()
