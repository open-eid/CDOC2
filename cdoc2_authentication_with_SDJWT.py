#!/Users/aivo/tmp/repos/CDOC2/sd-jwt/sd-jwt-python/venv/bin/python3.12
# -*- coding: utf-8 -*-

import re
import sys
import json
from jwcrypto.common import json_decode, json_encode
from jwcrypto.jwk import JWK
from sd_jwt.common import SDObj
from sd_jwt.issuer import SDJWTIssuer
from sd_jwt.holder import SDJWTHolder
from sd_jwt.verifier import SDJWTVerifier

SDJWTIssuer.unsafe_randomness = True

def receive_nonce_from_server1(capsule_id):
    return "42"

def receive_nonce_from_server2(capsule_id):
    return "41"

def create_and_sign_authentication_data(signing_key, first_server_data, second_server_data):     
      SDJWT_regular_claims = {
            "typ": "CDOC2 authentication token v0.1",
            "iss": "some_issuer",
            "iat": "some_timestamp"
            }

      SDJWT_disclosable_claims = {
            SDObj("FirstCapsuleID"): first_server_data['id'],
            SDObj("FirstCapsuleNonce"): first_server_data['nonce'],

            SDObj("SecondCapsuleID"): second_server_data['id'],
            SDObj("SecondCapsuleNonce"): second_server_data['nonce']
            }
      
      SDJWT_claims = {}
      SDJWT_claims.update(SDJWT_regular_claims)
      SDJWT_claims.update(SDJWT_disclosable_claims)

      issuer_jwk = JWK.from_json(json_encode(signing_key))
      holder_jwk = JWK.from_json(json_encode(signing_key))

      SDJWT_at_issuer = SDJWTIssuer(
            user_claims=SDJWT_claims,
            issuer_key=issuer_jwk,
            holder_key=holder_jwk,
            serialization_format="json"
      )

      SDJWT_at_holder = SDJWTHolder(
            sd_jwt_issuance=SDJWT_at_issuer.sd_jwt_issuance,
            serialization_format="json"
      )

      return SDJWT_at_holder

def create_authentication_ticket_for_server1(signing_key, auth_signature):
    
      holder_jwk = JWK.from_json(json_encode(signing_key))

      auth_signature.create_presentation(
            claims_to_disclose={'FirstCapsuleID': True, 'FirstCapsuleNonce': True},
            nonce="1234",
            aud="ServerID1",
            holder_key=holder_jwk,
            sign_alg="ES256"
            )

      auth_ticket = auth_signature.sd_jwt_presentation

      return auth_ticket

def create_authentication_ticket_for_server2(signing_key, auth_signature):
    
      holder_jwk = JWK.from_json(json_encode(signing_key))

      auth_signature.create_presentation(
            claims_to_disclose={'SecondCapsuleID': True, 'SecondCapsuleNonce': True},
            nonce="1234",
            aud="ServerID2",
            holder_key=holder_jwk,
            sign_alg="ES256"
            )

      auth_ticket = auth_signature.sd_jwt_presentation

      return auth_ticket

def verify_authentication_ticket_at_server1(user_key, auth_ticket):

      expected_CDOC_authentication_nonce=42

      # Define a function to check the issuer and retrieve the
      # matching public key
      def cb_get_issuer_key(issuer, header_parameters):
            issuer_JWK = JWK.from_json(json_encode(user_key))
            return JWK.from_json(issuer_JWK.export_public())
            
      sdjwt_at_verifier = SDJWTVerifier(
            sd_jwt_presentation=auth_ticket,
            cb_get_issuer_key=cb_get_issuer_key,
            expected_aud="ServerID1",
            expected_nonce="1234",
            serialization_format="json"
            )

      verified_payload = sdjwt_at_verifier.get_verified_payload()

      print("verifier unverified input sd:\n", 
            json.dumps(json.loads(sdjwt_at_verifier._unverified_input_sd_jwt), indent=4)
            )

      print("verifier unverified input sd payload:\n", 
            json.dumps(sdjwt_at_verifier._unverified_input_sd_jwt_payload, indent=4)
            )

      print("verifier parsed sd_jwt_payload:\n", 
            json.dumps(sdjwt_at_verifier._sd_jwt_payload, indent=4)
            )

      print("Verifier verified payload: \n", 
            json.dumps(verified_payload, indent=4)
            )
      
      if (verified_payload['FirstCapsuleID'] == "1") and (verified_payload['FirstCapsuleNonce'] == "42"): 
           return True
      else:
           return False
    
def verify_authentication_ticket_at_server2(user_key, auth_ticket):

      # Define a function to check the issuer and retrieve the
      # matching public key
      def cb_get_issuer_key(issuer, header_parameters):
            issuer_JWK = JWK.from_json(json_encode(user_key))
            return JWK.from_json(issuer_JWK.export_public())
            
      sdjwt_at_verifier = SDJWTVerifier(
            sd_jwt_presentation=auth_ticket,
            cb_get_issuer_key=cb_get_issuer_key,
            expected_aud="ServerID2",
            expected_nonce="1234",
            serialization_format="json"
            )

      verified_payload = sdjwt_at_verifier.get_verified_payload()

      print("verifier unverified input sd:\n", 
            json.dumps(json.loads(sdjwt_at_verifier._unverified_input_sd_jwt), indent=4)
            )

      print("verifier unverified input sd payload:\n", 
            json.dumps(sdjwt_at_verifier._unverified_input_sd_jwt_payload, indent=4)
            )

      print("verifier parsed sd_jwt_payload:\n", 
            json.dumps(sdjwt_at_verifier._sd_jwt_payload, indent=4)
            )

      print("Verifier verified payload: \n", 
            json.dumps(verified_payload, indent=4)
            )

      if (verified_payload['SecondCapsuleID'] == "2") and (verified_payload['SecondCapsuleNonce'] == "41"): 
           return True
      else:
           return False

## Main flow

user_key_pair = {
    "kty": "EC",
    "crv": "P-256",
    "d": "Ur2bNKuBPOrAaxsRnbSH6hIhmNTxSGXshDSUD1a1y7g",
    "x": "b28d4MwZMjw8-00CG4xfnn9SLMVMM19SlqZpVb_uNtQ",
    "y": "Xv5zWwuoaTgdS6hV43yI6gBwTnjukmFQQnJ_kCxzqk8"
}

capsule_ID1 = "1"
capsule_ID2 = "2"

nonce1 = receive_nonce_from_server1(capsule_id=capsule_ID1)
nonce2 = receive_nonce_from_server2(capsule_id=capsule_ID2)

signed_auth_data = create_and_sign_authentication_data(signing_key=user_key_pair, first_server_data={'id': capsule_ID1, 'nonce': nonce1}, second_server_data={'id': capsule_ID2, 'nonce':nonce2})

print("signed auth_data serialized_sd_jwt:\n", 
      json.dumps(json.loads(signed_auth_data.serialized_sd_jwt), indent=4))
print("signed auth_data sd_jwt_payload:\n", 
      json.dumps(signed_auth_data.sd_jwt_payload, indent=4))
#print("signed auth_data sd_jwt_protected:\n",
#      json.dumps(signed_auth_data.sd_jwt.jose_header, indent=4))

ticket1 = create_authentication_ticket_for_server1(signing_key=user_key_pair, auth_signature=signed_auth_data)

print("auth_ticket1 serialized_sd_jwt:\n", 
      json.dumps(json.loads(ticket1), indent=4)
      )

print("auth_ticket1 sd_jwt_payload:\n", 
      json.dumps(json.loads(ticket1)['payload'], indent=4)
      )

ticket2 = create_authentication_ticket_for_server2(signing_key=user_key_pair, auth_signature=signed_auth_data)

print("auth_ticket1 serialized_sd_jwt:\n", 
      json.dumps(json.loads(ticket2), indent=4)
      )

print("auth_ticket1 sd_jwt_payload:\n", 
      json.dumps(json.loads(ticket2)['payload'], indent=4)
      )

ok1 = verify_authentication_ticket_at_server1(user_key=user_key_pair, auth_ticket=ticket1)
ok2 = verify_authentication_ticket_at_server2(user_key=user_key_pair, auth_ticket=ticket2)

if ok1 and ok2:
    print("both tickets verified ok")
else:
    print("tickets not valid")

#if verify_authentication_ticket_at_server2(user_key=user_key_pair, auth_ticket=ticket1): 
#     print("Something wrong, ticket1 verified at server2")
#else:
#     print("Good, server2 rejected ticket1")
#
# TODO: Should create better test

