import datetime
import json
import string
import threading
import time
from functools import wraps
from typing import Tuple

import jsonrpcclient.requests as jsr
import jsonrpcclient.responses as jsp
import psutil
import requests
import schedule
from flask import current_app
from flask import request

from config.app import TELEMETRY_ENDPOINT, DATA_DIR
from config.errors import ErrorMessages

METRICS = []


def log_api_call(name: str):
    """ log rpc calls
        @param name: str
    """
    current_app.logger.info("API-CALL{%s}" % name)


def call_rpc(params: list, method: str) -> Tuple:
    """ calling KMS API
        :param params: list
        :param method: str
        :return:
    """
    try:
        res = requests.post(TELEMETRY_ENDPOINT, json=jsr.request(method, params))
        if res.status_code >= 500:
            raise Exception(f"{TELEMETRY_ENDPOINT} is DOWN!")
        if res.status_code >= 400:
            raise Exception("Bad request!")
        if res.status_code == 200:
            rpc_response = jsp.parse(res.json())
            res = [None, None]
            if isinstance(rpc_response, jsp.Ok):
                res[0] = rpc_response.result
            else:
                res[1] = {
                    "message": rpc_response.message,
                    "status": -1,
                    "data": rpc_response.data
                }
            return res[0], res[1]
        raise Exception("Unknown Error!")
    except Exception as e:
        return None, str(e)


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


def save_config(data: dict):
    file = open(f"{DATA_DIR}/_cfg.json", "w")
    file.write(json.dumps(data))
    file.close()


def get_config():
    try:
        file = open(f"{DATA_DIR}/_cfg.json", "r")
        data = json.loads(file.read())
        file.close()
        if "password" not in data or "username" not in data:
            return None
        return data
    except:
        return None


def save_token(data: dict):
    file = open(f"{DATA_DIR}/_token.json", "w")
    file.write(json.dumps(data))
    file.close()


def save_password(data: dict):
    file = open(f"{DATA_DIR}/_pass.json", "w")
    file.write(json.dumps(data))
    file.close()


def get_token():
    try:
        file = open(f"{DATA_DIR}/_token.json", "r")
        data = json.loads(file.read())
        file.close()
        return data['token']
    except:
        return None


def check_token(token: str):
    return get_token() == token


def get_password():
    try:
        file = open(f"{DATA_DIR}/_pass.json", "r")
        data = json.loads(file.read())
        file.close()
        if 'username' not in data or 'password' not  in data:
            return None
        return data
    except:
        return None


def check_password(password: str, username: str):
    cred = get_password()
    if cred is None:
        return False
    return cred['username'] == username, password == cred['password']


def password_strong(password: str):
    if len(password) < 10:
        return False, "Password length must bigger than 10!"
    lwasci = len([i for i in password if i in string.ascii_lowercase]) != 0
    upasci = len([i for i in password if i in string.ascii_uppercase]) != 0
    num = len([i for i in password if i in string.digits]) != 0
    if not lwasci:
        return False, "Password must contain lower case ascii!"
    if not upasci:
        return False, "Password must contain upper case ascii!"
    if not lwasci:
        return False, "Password must contain digits!"
    return True, None


def username_strong(username: str):
    if len(username) < 4:
        return False, "Username length must bigger than 3!"
    valids = [i for i in string.ascii_letters]
    for i in username:
        if i == ' ' or i =='' or i not in valids:
            return False, "Invalid character in username!"
    return True, None


def error_401():
    """ public method
        @return: [dict, int]
    """
    return ErrorMessages.AuthenticationError, 401


def get_metrics():
    global METRICS
    METRICS = []
    try:
        file = open(f"{DATA_DIR}/_metrics.json", "r")
        METRICS = json.loads(file.read())
        file.close()
    except:
        file = open(f"{DATA_DIR}/_metrics.json", "w")
        file.write(json.dumps(METRICS))
        file.close()


def check_setup():
    res = {
        "registered": False,
        "password": False,
        "staked": False,
        "info": None
    }
    if (token := get_token()) is None:
        return res
    data, error = call_rpc([token], "getInfo")
    if error:
        return res
    res['info'] = data
    res['staked'] = data['staking'] != 0
    res['registered'] = get_config() is not None
    if (password := get_password()) is not None:
        res['password'] = True
    return res


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
    METRICS.append({
        "time": str(datetime.datetime.utcnow()),
        "cpu_usage_pct": psutil.cpu_percent(interval=0.5),
        "ram_usage_mb": int((int(psutil.virtual_memory().total - psutil.virtual_memory().available)) / 1024 / 1024),
        "ram_total_mb": int(int(psutil.virtual_memory().total) / 1024 / 1024),
        "ram_usage_pct": psutil.virtual_memory().percent
    })
    if len(METRICS) > 8640:
        METRICS.pop(0)
    file = open(f"{DATA_DIR}/_metrics.json", "w")
    file.write(json.dumps(METRICS))
    file.close()


def _gather_metrics_thread():
    metric_jobs()
    schedule.every(5).minutes.do(metric_jobs)
    while True:
        schedule.run_pending()
        time.sleep(60)


threading.Thread(target=_gather_metrics_thread, daemon=True).start()
