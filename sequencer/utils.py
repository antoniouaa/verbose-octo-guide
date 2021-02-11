from flask import request, jsonify
from werkzeug.exceptions import HTTPException

import functools
import logging

from sequencer.extensions import jwt

logger = logging.getLogger("genome-sequencer")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("./dev.log", mode="w")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def log_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Route {request.url} called from {request.remote_addr}")
        return func(*args, **kwargs)

    return wrapper


def handle_error(request, err, status):
    logger.error(f"Error occured: {str(err)}\tType: {type(err)}")
    error = {
        "links": {
            "self": request.url,
        },
        "errors": {
            "method": request.method,
            "status": status,
            "details": str(err),
        },
    }
    if len(err.args) > 0:
        error["errors"]["title"] = err.args[0]
    return error


def error_handler(func):
    @functools.wraps(func)
    def error_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException as err:
            status = err.get_response().status
            return (
                jsonify(handle_error(request=request, err=err, status=status)),
                status,
            )
        except Exception as err:
            status = 400
            return (
                jsonify(handle_error(request=request, err=err, status=status)),
                status,
            )

    return error_handler


@jwt.expired_token_loader
def expired_token_callback(expired_token):
    token_type = expired_token["type"]
    code = 401
    return (
        jsonify(
            {
                "links": {
                    "self": request.url,
                },
                "errors": {
                    "method": request.method,
                    "status": code,
                    "details": f"Expired authorization {token_type} token",
                },
            }
        ),
        code,
    )
