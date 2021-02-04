from flask import request

import functools


def log_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Route {request.url} called from {request.remote_addr}")
        return func(*args, **kwargs)

    return wrapper


def handle_error(request, err, status):
    print(f"Error of type {type(err)} occured: {str(err)}")
    code, title = status.split(maxsplit=1)
    return {
        "links": {
            "self": request.url,
        },
        "errors": {
            "method": request.method,
            "title": title,
            "status": code,
            "details": str(err),
        },
    }
