from flask import request, Blueprint
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Conflict
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import time
import datetime

blueprint = Blueprint("user_blueprint", __name__)

from sequencer import utils
from sequencer.user import models


@blueprint.route("/", methods=["GET"])
@utils.log_request
@utils.error_handler
def get_all_users():
    users = models.User.query.all()
    return (
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
        },
        200,
    )


@blueprint.route("/signup", methods=["POST"])
@utils.log_request
@utils.error_handler
def signup():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    if not username:
        raise BadRequest("Username missing")
    if not password:
        raise BadRequest("Password missing")
    if not email:
        raise BadRequest("Email missing")
    user = models.User.query.filter_by(username=username).first()
    if user is not None:
        raise Conflict("User already exists!")
    user = models.create_user(username=username, password=password, email=email)
    return (
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
        201,
    )


@blueprint.route("/refresh", methods=["POST"])
@utils.log_request
@utils.error_handler
@jwt_required
def refresh():
    current_user = get_jwt_identity()
    user = models.User.query.filter_by(username=current_user["username"]).first()
    fresh_token = create_access_token(
        identity=user.serialize(), expires_delta=datetime.timedelta(minutes=5)
    )
    return (
        {
            "links": {
                "self": request.url,
            },
            "data": {
                "type": user.__name__,
                "id": user.id,
                "attributes": user.serialize(),
                "token": fresh_token,
            },
            "meta": {
                "timestamp": int(time.time()),
            },
        },
        201,
    )


@blueprint.route("/protected", methods=["GET"])
@utils.log_request
@utils.error_handler
@jwt_required
def protected_resource():
    current_user = get_jwt_identity()
    user = models.User.query.filter_by(username=current_user["username"]).first()
    return (
        {
            "links": {
                "self": request.url,
            },
            "data": [{"Protected": "resource!", "Logged in as": user.username}],
            "meta": {
                "timestamp": int(time.time()),
            },
        },
        200,
    )


@blueprint.route("/delete", methods=["DELETE"])
@utils.log_request
@utils.error_handler
@jwt_required
def delete_user():
    current_user = get_jwt_identity()
    print(current_user)
    models.delete_user(username=current_user["username"])
    return ("", 204)
