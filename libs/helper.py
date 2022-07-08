import datetime
import time
from typing import Tuple

import flask
import psutil
from flask import current_app
from config.errors import ErrorMessages
from functools import wraps
from flask import request

METRICS = []


def log_api_call(name: str):
    """ log rpc calls
        @param name: str
    """
    current_app.logger.info("API-CALL{%s}" % name)


def get_ip_and_agent() -> Tuple[str, str]:
    """ extract request ip and agent
        @return: Tuple[str, str]
    """
    agent = flask.request.user_agent if flask.has_request_context() else ""
    ip = flask.request.headers.getlist("X-Forwarded-For")[0] if flask.request.headers.getlist(
        "X-Forwarded-For") else flask.request.remote_addr
    ip = str(ip).split(',')[1].replace(' ', '') if "," in ip else ip
    return str(ip), str(agent)


def response_error(error_obj: dict) -> dict:
    """ error response to client
        @return: str
    """
    return error_obj


def response_success(data: int | list | str | tuple | dict, message: str = "Success!") -> dict:
    """ error response to client
        @param message: str
        @param data: int | list | str | tuple | dict
        @return: dict
    """
    return {
        "status": 0,
        "message": message,
        "data": data
    }


def error_401():
    """ public method
        @return: [dict, int]
    """
    return ErrorMessages.AuthenticationError, 401


def expects(fields: set):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return ErrorMessages.InvalidRequest

            if not fields.issubset(request.json):
                return ErrorMessages.InvalidRequest

            return f(*args, **request.json, **kwargs)

        return decorated_function

    return decorator


def metric_jobs():
    while True:
        METRICS.append({
            "time": str(datetime.datetime.utcnow()),
            "cpu_usage_pct": psutil.cpu_percent(interval=0.5),
            "cpu_frequency_mh": int(psutil.cpu_freq().current),
            "ram_usage_mb": int((int(psutil.virtual_memory().total - psutil.virtual_memory().available)) / 1024 / 1024),
            "ram_total_mb": int(int(psutil.virtual_memory().total) / 1024 / 1024),
            "ram_usage_pct": psutil.virtual_memory().percent
        })
        if len(METRICS) > 1000:
            METRICS.pop(0)
        time.sleep(2)
