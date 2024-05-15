#!/Users/aivo/tmp/repos/CDOC2/RM-2776-authentication-protocol/sd-jwt/sd-jwt-python/venv/bin/python3.12
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

def create_and_sign_authentication_data(signing_key, server1_access_data, server2_access_data):     

      server_1_structure = {
            "serverURL": server1_access_data['serverURL'],
            "capsuleID": server1_access_data['capsuleID'],
            "serverNonce": server1_access_data['serverNonce'],
            }

      server_2_structure = {
            "serverURL": server2_access_data['serverURL'],
            "capsuleID": server2_access_data['capsuleID'],
            "serverNonce": server2_access_data['serverNonce'],
            }
      
      server_auth_data_array = json.loads('[]')
      #print("server_auth_data_array: " + json.dumps(server_auth_data_array,sort_keys=True, indent=4))
      server_auth_data_array.append(SDObj(server_1_structure))
      server_auth_data_array.append(SDObj(server_2_structure))
      #print("server_auth_data_array with two elements: " + json.dumps(server_auth_data_array,sort_keys=True, indent=4))
      disclosable_array = {
           SDObj("capsule_access_data"): server_auth_data_array
      }

      #print("SD array: " + json.dumps(disclosable_array,sort_keys=True, indent=4))

      SDJWT_disclosable_claims = {}
      SDJWT_disclosable_claims.update(disclosable_array)

#      SDJWT_disclosable_claims = {
#            SDObj([])
#            SDObj("FirstCapsuleID"): first_server_data['id'],
#            SDObj("FirstCapsuleNonce"): first_server_data['nonce'],
#
#            SDObj("SecondCapsuleID"): second_server_data['id'],
#            SDObj("SecondCapsuleNonce"): second_server_data['nonce']
#            }
      
      SDJWT_claims = {}
      SDJWT_regular_claims = {
            "CDOC2_token_type": "CTS authentication token v0.1",
            "iss": "etsi/PNOEE-48010010101",
            "iat": "1715694253"
            }
      SDJWT_claims.update(SDJWT_regular_claims)
      SDJWT_claims.update(SDJWT_disclosable_claims)

      issuer_jwk = JWK.from_json(json_encode(signing_key))
      holder_jwk = JWK.from_json(json_encode(signing_key))

      SDJWT_at_issuer = SDJWTIssuer(
            user_claims=SDJWT_claims,
            issuer_key=issuer_jwk,
            serialization_format="json"
      )

      SDJWT_at_holder = SDJWTHolder(
            sd_jwt_issuance=SDJWT_at_issuer.sd_jwt_issuance,
            serialization_format="json"
      )

      return SDJWT_at_holder

def create_authentication_ticket_for_server1(auth_signature):
    
      auth_signature.create_presentation(
            claims_to_disclose={
                 'capsule_access_data': [True, False]
                 }
            )

      auth_ticket = auth_signature.sd_jwt_presentation

      return auth_ticket

def create_authentication_ticket_for_server2(auth_signature):
    
      auth_signature.create_presentation(
            claims_to_disclose={
                 'capsule_access_data': [False, True]
                 }
            )

      auth_ticket = auth_signature.sd_jwt_presentation

      return auth_ticket

def verify_authentication_ticket_at_server1(user_public_key, auth_ticket):

      expected_serverNonce = "42"
      expected_capsuleID = "9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3"

      # Define a function to check the issuer and retrieve the
      # matching public key
      def cb_get_issuer_key(issuer, header_parameters):
            issuer_JWK = JWK.from_json(json_encode(user_public_key))
            return JWK.from_json(issuer_JWK.export_public())
            
      sdjwt_at_verifier = SDJWTVerifier(
            sd_jwt_presentation=auth_ticket,
            cb_get_issuer_key=cb_get_issuer_key,
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
      
      if (verified_payload['capsule_access_data'][0]['capsuleID'] == expected_capsuleID) and (verified_payload['capsule_access_data'][0]['serverNonce'] == expected_serverNonce):
           return True
      else:
           return False
    
def verify_authentication_ticket_at_server2(user_public_key, auth_ticket):

      expected_serverNonce = "41"
      expected_capsuleID = "5BAE4603-C33C-4425-B301-125F2ACF9B1E"

      # Define a function to check the issuer and retrieve the
      # matching public key
      def cb_get_issuer_key(issuer, header_parameters):
            issuer_JWK = JWK.from_json(json_encode(user_public_key))
            return JWK.from_json(issuer_JWK.export_public())
            
      sdjwt_at_verifier = SDJWTVerifier(
            sd_jwt_presentation=auth_ticket,
            cb_get_issuer_key=cb_get_issuer_key,
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

      if (verified_payload['capsule_access_data'][0]['capsuleID'] == expected_capsuleID) and (verified_payload['capsule_access_data'][0]['serverNonce'] == expected_serverNonce):
           return True
      else:
           return False

## Main flow

user_EC_key_pair = {
    "kty": "EC",
    "crv": "P-256",
    "d": "Ur2bNKuBPOrAaxsRnbSH6hIhmNTxSGXshDSUD1a1y7g",
    "x": "b28d4MwZMjw8-00CG4xfnn9SLMVMM19SlqZpVb_uNtQ",
    "y": "Xv5zWwuoaTgdS6hV43yI6gBwTnjukmFQQnJ_kCxzqk8"
}

user_RSA_keypair = {
  "kty" : "RSA",
  "use" : "sig",
  "n"   : "pjdss8ZaDfEH6K6U7GeW2nxDqR4IP049fk1fK0lndimbMMVBdPv_hSpm8T8EtBDxrUdi1OHZfMhUixGaut-3nQ4GG9nM249oxhCtxqqNvEXrmQRGqczyLxuh-fKn9Fg--hS9UpazHpfVAFnB5aCfXoNhPuI8oByyFKMKaOVgHNqP5NBEqabiLftZD3W_lsFCPGuzr4Vp0YS7zS2hDYScC2oOMu4rGU1LcMZf39p3153Cq7bS2Xh6Y-vw5pwzFYZdjQxDn8x8BG3fJ6j8TGLXQsbKH1218_HcUJRvMwdpbUQG5nvA2GXVqLqdwp054Lzk9_B_f1lVrmOKuHjTNHq48w",
  "e"   : "AQAB",
  "d"   : "ksDmucdMJXkFGZxiomNHnroOZxe8AmDLDGO1vhs-POa5PZM7mtUPonxwjVmthmpbZzla-kg55OFfO7YcXhg-Hm2OWTKwm73_rLh3JavaHjvBqsVKuorX3V3RYkSro6HyYIzFJ1Ek7sLxbjDRcDOj4ievSX0oN9l-JZhaDYlPlci5uJsoqro_YrE0PRRWVhtGynd-_aWgQv1YzkfZuMD-hJtDi1Im2humOWxA4eZrFs9eG-whXcOvaSwO4sSGbS99ecQZHM2TcdXeAs1PvjVgQ_dKnZlGN3lTWoWfQP55Z7Tgt8Nf1q4ZAKd-NlMe-7iqCFfsnFwXjSiaOa2CRGZn-Q",
  "p"   : "4A5nU4ahEww7B65yuzmGeCUUi8ikWzv1C81pSyUKvKzu8CX41hp9J6oRaLGesKImYiuVQK47FhZ--wwfpRwHvSxtNU9qXb8ewo-BvadyO1eVrIk4tNV543QlSe7pQAoJGkxCia5rfznAE3InKF4JvIlchyqs0RQ8wx7lULqwnn0",
  "q"   : "ven83GM6SfrmO-TBHbjTk6JhP_3CMsIvmSdo4KrbQNvp4vHO3w1_0zJ3URkmkYGhz2tgPlfd7v1l2I6QkIh4Bumdj6FyFZEBpxjE4MpfdNVcNINvVj87cLyTRmIcaGxmfylY7QErP8GFA-k4UoH_eQmGKGK44TRzYj5hZYGWIC8",
  "dp"  : "lmmU_AG5SGxBhJqb8wxfNXDPJjf__i92BgJT2Vp4pskBbr5PGoyV0HbfUQVMnw977RONEurkR6O6gxZUeCclGt4kQlGZ-m0_XSWx13v9t9DIbheAtgVJ2mQyVDvK4m7aRYlEceFh0PsX8vYDS5o1txgPwb3oXkPTtrmbAGMUBpE",
  "dq"  : "mxRTU3QDyR2EnCv0Nl0TCF90oliJGAHR9HJmBe__EjuCBbwHfcT8OG3hWOv8vpzokQPRl5cQt3NckzX3fs6xlJN4Ai2Hh2zduKFVQ2p-AF2p6Yfahscjtq-GY9cB85NxLy2IXCC0PF--Sq9LOrTE9QV988SJy_yUrAjcZ5MmECk",
  "qi"  : "ldHXIrEmMZVaNwGzDF9WG8sHj2mOZmQpw9yrjLK9hAsmsNr5LTyqWAqJIYZSwPTYWhY4nu2O0EY9G9uYiqewXfCKw_UngrJt8Xwfq1Zruz0YY869zPN4GiE9-9rzdZB33RBw8kIOquY3MK74FMwCihYx_LiU2YTHkaoJ3ncvtvg"
}

capsule_ID1 = "9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3"
capsule_ID2 = "5BAE4603-C33C-4425-B301-125F2ACF9B1E"

nonce1 = receive_nonce_from_server1(capsule_id=capsule_ID1)
nonce2 = receive_nonce_from_server2(capsule_id=capsule_ID2)

server1_access_data = {
     'serverURL': "https://cdoc.ria.ee:443/capsules",
     'capsuleID': capsule_ID1,
     'serverNonce': nonce1
}

server2_access_data = {
      'serverURL': "https://cdoc.smit.ee:443/capsules",
     'capsuleID': capsule_ID2,
     'serverNonce': nonce2
}

signed_auth_data = create_and_sign_authentication_data(
      signing_key=user_EC_key_pair, 
      server1_access_data = server1_access_data,
      server2_access_data = server2_access_data
      )

print("signed auth_data serialized_sd_jwt:\n", 
      json.dumps(json.loads(signed_auth_data.serialized_sd_jwt), indent=4))
print("signed auth_data sd_jwt_payload:\n", 
      json.dumps(signed_auth_data.sd_jwt_payload, indent=4))
#print("signed auth_data sd_jwt_protected:\n",
#      json.dumps(signed_auth_data.sd_jwt.jose_header, indent=4))

ticket1 = create_authentication_ticket_for_server1(auth_signature=signed_auth_data)

print("auth_ticket1 serialized_sd_jwt:\n", 
      json.dumps(json.loads(ticket1), indent=4)
      )

print("auth_ticket1 sd_jwt_payload:\n", 
      json.dumps(json.loads(ticket1)['payload'], indent=4)
      )

ticket2 = create_authentication_ticket_for_server2(auth_signature=signed_auth_data)

print("auth_ticket1 serialized_sd_jwt:\n", 
      json.dumps(json.loads(ticket2), indent=4)
      )

print("auth_ticket1 sd_jwt_payload:\n", 
      json.dumps(json.loads(ticket2)['payload'], indent=4)
      )

ok1 = verify_authentication_ticket_at_server1(user_public_key=user_EC_key_pair, auth_ticket=ticket1)
ok2 = verify_authentication_ticket_at_server2(user_public_key=user_EC_key_pair, auth_ticket=ticket2)

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

