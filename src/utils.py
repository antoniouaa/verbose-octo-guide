from flask import request, jsonify

import functools
import logging

from werkzeug.exceptions import HTTPException

# logging.basicConfig(
#     handlers=[logging.FileHandler(filename="./dev.log", encoding="utf-8", mode="w")],
#     level=logging.DEBUG,
# )

logger = logging.getLogger("genome-sequencer")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("dev.log")
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
