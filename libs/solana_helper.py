from urllib.parse import quote

import base58
from flask import current_app as app
from solana.keypair import Keypair
from solana.publickey import PublicKey

from nacl.signing import VerifyKey
import string
from random import choice


def is_valid_public_key(public_key: str):
    """ check a public key is a valid account on solana
        @param public_key: str
        @return: bool
    """
    try:
        PublicKey(public_key)
        return True
    except:
        app.logger.info(f"invalid public key: {public_key}")
        return False


def get_keypair():
    """ creating new keypair
        @return: tuple
    """
    account = Keypair()
    return str(account.public_key), base58.b58encode(account.seed).decode("ascii")


def get_random_string(length: int):
    """ create a random string
        @param length: int
        @return: str
    """
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(length))


def handshake_initializer():
    """ initialization of handshake
        @return str
    """
    try:
        unique = get_random_string(32)
        sign_message = f"Sign this message for authenticating with your wallet. Nonce: \n{unique}"
        # sign_message = "Hello, world!"
        return sign_message
    except Exception as e:
        app.logger.critical(f'Handshake initiation failed! {str(e)}')
        raise e


def check_signed_message(public_key: str, nonce: str, signature: str):
    """ checking signed message validity
        @param public_key: str
        @param nonce: str
        @param signature: str
        @return: bool
    """
    try:
        VerifyKey(
            bytes(PublicKey(public_key))
        ).verify(
            smessage=bytes(nonce, 'utf8'),
            signature=base58.b58decode(bytes(signature, 'utf8'))
        )
        return True
    except:
        return False
