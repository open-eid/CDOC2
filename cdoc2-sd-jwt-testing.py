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

standard_claims = {
    "iss": "some_issuer",
    "iat": "some_timestamp"
}

disclosable_claims = {
    SDObj("TX1"): "nonce1",
    SDObj("TX2"): "nonce2"
}

issuer_EC = {
    "kty": "EC",
    "crv": "P-256",
    "d": "Ur2bNKuBPOrAaxsRnbSH6hIhmNTxSGXshDSUD1a1y7g",
    "x": "b28d4MwZMjw8-00CG4xfnn9SLMVMM19SlqZpVb_uNtQ",
    "y": "Xv5zWwuoaTgdS6hV43yI6gBwTnjukmFQQnJ_kCxzqk8"
}

holder_EC = {
    "kty": "EC",
    "crv": "P-256",
    "d": "Ur2bNKuBPOrAaxsRnbSH6hIhmNTxSGXshDSUD1a1y7g",
    "x": "b28d4MwZMjw8-00CG4xfnn9SLMVMM19SlqZpVb_uNtQ",
    "y": "Xv5zWwuoaTgdS6hV43yI6gBwTnjukmFQQnJ_kCxzqk8"
}

issuer_jwk = JWK.from_json(json_encode(issuer_EC))
holder_jwk = JWK.from_json(json_encode(holder_EC))

user_claims = {}
user_claims.update(standard_claims)
user_claims.update(disclosable_claims)

sdjwt_at_issuer = SDJWTIssuer(
    user_claims=user_claims,
    issuer_key=issuer_jwk,
    holder_key=holder_jwk,
    serialization_format="json"
)

print("issuer serialized_sd_jwt:\n", 
      json.dumps(json.loads(sdjwt_at_issuer.serialized_sd_jwt), indent=4))
print("issuer sd_jwt_payload:\n", 
      json.dumps(sdjwt_at_issuer.sd_jwt_payload, indent=4))
print("issuer sd_jwt_protected:\n",
      json.dumps(sdjwt_at_issuer.sd_jwt.jose_header, indent=4))

sdjwt_at_holder = SDJWTHolder(
    sd_jwt_issuance=sdjwt_at_issuer.sd_jwt_issuance,
    serialization_format="json"
)

sdjwt_at_holder.create_presentation(
    claims_to_disclose={"TX1": True},
    nonce="1234",
    aud="Server1",
    holder_key=holder_jwk,
    sign_alg="ES256"
)

print("holder serialized_sd_jwt:\n", 
      json.dumps(json.loads(sdjwt_at_holder.serialized_sd_jwt), indent=4)
      )

print("holder sd_jwt_payload:\n", 
      json.dumps(sdjwt_at_holder.sd_jwt_payload, indent=4)
      )

print("holder sd_jwt_presentation:\n", 
      json.dumps(json.loads(sdjwt_at_holder.sd_jwt_presentation), indent=4)
      )

# Define a function to check the issuer and retrieve the
# matching public key
def cb_get_issuer_key(issuer, header_parameters):
    issuer_JWK = JWK.from_json(json_encode(issuer_EC))
    return JWK.from_json(issuer_JWK.export_public())
        
sdjwt_at_verifier = SDJWTVerifier(
    sd_jwt_presentation=sdjwt_at_holder.sd_jwt_presentation,
    cb_get_issuer_key=cb_get_issuer_key,
    expected_aud="Server1",
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


