"""
master controller
"""

from flask import Blueprint


from libs.helper import *

api = Blueprint("MAIN API", __name__, url_prefix="/api")


@api.route("/metrics", methods=["GET"])
def metrics():
    """ get metrics of server
        @return: Response
    """
    log_api_call(metrics.__name__)

    return response_success(METRICS)


@api.route("/login", methods=["POST"])
@expects({"username", "password"})
def login(username: str, password: str):
    """ login
        @param username: str
        @param password: str
    """
    log_api_call(login.__name__)
    if not check_password(password, username):
        return error_401()
    data = get_config()
    data, error = call_rpc([data['username'], data['password']], "auth")
    if error:
        return error, 400
    save_token({"token": data})
    return response_success(data=data)


@api.route("/auth/handshake", methods=["POST"])
@expects({"public_key"})
def setup_handshake(public_key: str):
    """ user handshaking
        @param public_key: str
        @return: str
    """
    log_api_call(setup_handshake.__name__)
    data, error = call_rpc([public_key], "registerHandshake")
    if error:
        return error, 400
    return response_success(data=data)


@api.route("/auth/login", methods=["POST"])
@expects({"public_key", "signature"})
def setup_auth(public_key: str, signature: str):
    """ authentication
        @param signature: str
        @param public_key: str
    """
    log_api_call(setup_auth.__name__)
    data, error = call_rpc([public_key, signature], "register")
    if error:
        return error, 400
    save_config(data)
    data, error = call_rpc([data['username'], data['password']], "auth")
    if error:
        return error, 400
    save_token({"token": data})
    return response_success(data=data)


@api.route("/stake/create-payment", methods=["POST"])
@expects({"token"})
def create_stake(token: str, amount: float = 20000):
    """ create staking payment
        @param token: str
        @param amount: float
        @return: dict
    """
    log_api_call(create_stake.__name__)
    data, error = call_rpc([token, amount], "createPayment")
    if error:
        return error, 400
    return response_success(data=data)


@api.route("/stake/confirm-payment", methods=["POST"])
@expects({"token", "tracking_code"})
def confirm_stake(token: str, tracking_code: str):
    """ confirming staking payment
        @param token: str
        @param tracking_code: str
        @return: dict
    """
    log_api_call(confirm_stake.__name__)
    data, error = call_rpc([token, tracking_code], "confirmPayment")
    if error:
        return error, 400
    return response_success(data=data)


@api.route("/stake/destake", methods=["POST"])
@expects({"token"})
def destake(token: str):
    """ destake
        @param token: str
        @return: dict
    """
    log_api_call(destake.__name__)
    data, error = call_rpc([token], "deStake")
    if error:
        return error, 400
    return response_success(data=data)


@api.route("/reward/get", methods=["POST"])
@expects({"token"})
def get_rewards(token: str):
    """ get rewards
        @param token: str
        @return: dict
    """
    log_api_call(get_rewards.__name__)
    data, error = call_rpc([token], "getRewards")
    if error:
        return error, 400
    return response_success(data=data)


@api.route("/reward/claim", methods=["POST"])
@expects({"token"})
def claim_rewards(token: str):
    """ claim rewards
        @param token: str
        @return: dict
    """
    log_api_call(claim_rewards.__name__)
    data, error = call_rpc([token], "claimReward")
    if error:
        return error, 400
    return response_success(data=data)


@api.route("/info/set-password", methods=["POST"])
@expects({"token", "password", "username"})
def set_password(token: str, username: str, password: str):
    """ set password
        @param token: str
        @param username: str
        @param password: str
        @return: dict
    """
    log_api_call(set_password.__name__)
    if not check_token(token):
        return error_401()
    err, msg = username_strong(username)
    if not err:
        return {"message": msg, "status": -1, "data": msg}, 400
    err, msg = password_strong(password)
    if not err:
        return {"message": msg, "status": -1, "data": msg}, 400
    save_password({"password": password, "username": username})
    return response_success(data="Success")


@api.route("/is-setup", methods=["GET"])
def is_setup():
    """ check node is set up
        @return: dict
    """
    log_api_call(is_setup.__name__)
    return response_success(data=check_setup())
