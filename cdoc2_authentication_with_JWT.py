#!/Users/aivo/tmp/repos/CDOC2/sd-jwt/sd-jwt-python/venv/bin/python3.12
# -*- coding: utf-8 -*-

import re
import sys
import json
from jwcrypto.common import json_decode, json_encode
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT

def receive_nonce_from_server1(capsule_id):
    return "42"

def receive_nonce_from_server2(capsule_id):
    return "41"

def create_authentication_data(first_server_data, second_server_data):
    return True

def create_authentication_ticket_for_server1(signing_key, auth_signature):
    return True

def create_authentication_ticket_for_server2(signing_key, auth_signature):
    return True

user_EC_key_pair = {
    "kty": "EC",
    "crv": "P-256",
    "d": "Ur2bNKuBPOrAaxsRnbSH6hIhmNTxSGXshDSUD1a1y7g",
    "x": "b28d4MwZMjw8-00CG4xfnn9SLMVMM19SlqZpVb_uNtQ",
    "y": "Xv5zWwuoaTgdS6hV43yI6gBwTnjukmFQQnJ_kCxzqk8"
}

capsule_ID1 = "1"
capsule_ID2 = "2"

n1 = receive_nonce_from_server1(capsule_id=capsule_ID1)
n2 = receive_nonce_from_server2(capsule_id=capsule_ID2)

auth_data = create_authentication_data(first_server_data={'capsule_id': capsule_ID1, 'server_nonce': n1}, second_server_data={'capsule_id': capsule_ID2, 'server_nonce': n2})
signature = create_authentication_signature(signing_key=user_EC_key_pair, auth_data=auth_data)

ticket1 = create_authentication_ticket_for_server1(auth_data=auth_data, auth_signature=signature)
ticket2 = create_authentication_ticket_for_server2(auth_data=auth_data, auth_signature=signature)

verify_authentication_ticket_at_server1(ticket1)
verify_authentication_ticket_at_server2(ticket2)





