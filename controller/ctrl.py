"""
master controller
"""

from flask import Blueprint


from libs.helper import log_api_call, METRICS, response_success, expects, response_error
from libs.solana_helper import *
from config.errors import ErrorMessages

api = Blueprint("MAIN API", __name__, url_prefix="/api")


@api.route("/metrics", methods=["GET"])
def metrics():
    """ get metrics of server
        @return: Response
    """
    log_api_call(metrics.__name__)

    return response_success(METRICS)


@api.route("/auth/handshake", methods=["POST"])
@expects({"public_key"})
def handshake(public_key: str):
    """ user handshaking
        @param public_key: str
        @return: str
    """
    log_api_call(handshake.__name__)
    if not is_valid_public_key(public_key):
        return ErrorMessages.InvalidParams, 400
    nonce = handshake_initializer()
    # UserHelper.instance().save_handshake(public_key, nonce)
    return response_success(data=nonce)


@api.route("/auth/login", methods=["POST"])
@expects({"public_key", "signature"})
def login(public_key: str, signature: str):
    """ authentication
        @param signature: str
        @param public_key: str
    """
    log_api_call(login.__name__)
    app.logger.info(f"attempting to auth WALLET({public_key}), SIGNED({signature})")
    if not is_valid_public_key(public_key):
        return ErrorMessages.InvalidParams, 400
    # session = UserHelper.instance().get_user_session(public_key)
    # if session is None or session['expired_at'] < dt.utcnow() or \
    #         not check_signed_message(public_key, session["nonce"], signature):
    #     app.logger.info(f"invalid identity: WALLET({public_key}), SIGNED({signature})")
    #     return result_error_response(msg="Invalid identity")
    # token = UserHelper.instance().save_auth(public_key, signature, invited_by)
    app.logger.info(f"user created auth session: WALLET({public_key}), SIGNED({signature})")
    return response_success(data='A')
