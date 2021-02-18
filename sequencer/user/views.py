from flask import jsonify, request, Blueprint
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Conflict
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import time


blueprint = Blueprint("user_blueprint", __name__)

from sequencer import utils
from sequencer.user import models


@blueprint.route("/", methods=["GET"])
@utils.log_request
@utils.error_handler
def get_all_users():
    users = models.User.query.all()
    return (
        jsonify(
            {
                "links": {
                    "self": request.url,
                },
                "data": [
                    {
                        "type": user.__name__,
                        "id": user.id,
                        "attributes": user.serialize(),
                    }
                    for user in users
                    if user is not None
                ],
                "meta": {
                    "length": len(users),
                    "timestamp": int(time.time()),
                },
            }
        ),
        200,
    )


@blueprint.route("/signup", methods=["POST"])
@utils.log_request
@utils.error_handler
def signup():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username:
        raise BadRequest("Username missing")
    if not password:
        raise BadRequest("Password missing")
    user = models.User.query.filter_by(username=username).first()
    if user is not None:
        raise Conflict("User already exists!")
    user = models.create_user(username=username, password=password)
    return (
        jsonify(
            {
                "links": {
                    "self": request.url,
                },
                "data": {
                    "type": user.__name__,
                    "id": user.id,
                    "attributes": user.serialize(),
                },
                "meta": {
                    "timestamp": int(time.time()),
                },
            },
        ),
        201,
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
    user = models.User.query.filter_by(username=username).first()
    if user is None:
        raise NotFound("User does not exist")
    if not user.validate_password(password):
        raise Unauthorized("Passwords don't match")
    access_token = create_access_token(identity=user.serialize(), expires_delta=None)
    return (
        jsonify(
            {
                "links": {
                    "self": request.url,
                },
                "data": {
                    "type": user.__name__,
                    "id": user.id,
                    "attributes": user.serialize(),
                    "token": access_token,
                },
                "meta": {
                    "timestamp": int(time.time()),
                },
            },
        ),
        201,
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
                "data": [
                    {"Protected": "resource!", "Logged in as": current_user["username"]}
                ],
                "meta": {
                    "timestamp": int(time.time()),
                },
            }
        ),
        200,
    )
