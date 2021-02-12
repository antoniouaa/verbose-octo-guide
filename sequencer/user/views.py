from flask import jsonify, request, Blueprint
from werkzeug.exceptions import BadRequest, Unauthorized
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import time

blueprint = Blueprint("user_blueprint", __name__)

from sequencer import utils
from sequencer.user import models


@blueprint.route("/", methods=["GET"])
@utils.log_request
@utils.error_handler
def index():
    return (
        jsonify(
            {
                "links": {
                    "self": request.url,
                },
                "data": [{"This is the": "user landing page!"}],
            }
        ),
        200,
    )


@blueprint.route("/login", methods=["POST"])
@utils.log_request
@utils.error_handler
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username:
        raise BadRequest("Username missing")
    if not password:
        raise BadRequest("Password missing")
    if username != utils.get_root():
        raise Unauthorized("You are not allowed to request a token")
    access_token = create_access_token(identity=username, expires_delta=None)
    return (
        jsonify(
            {
                "links": {
                    "self": request.url,
                },
                "data": {
                    "username": username,
                    "password": password,
                    "token": access_token,
                },
            },
        ),
        200,
    )


@blueprint.route("/protected", methods=["GET"])
@jwt_required
@utils.log_request
@utils.error_handler
def protected_resource():
    current_user = get_jwt_identity()
    return (
        jsonify(
            {
                "links": {
                    "self": request.url,
                },
                "data": [{"Protected": "resource!", "Logged in as": current_user}],
            }
        ),
        200,
    )
