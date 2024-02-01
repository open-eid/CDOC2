---
title: 3. CDOC2 system components
---

# CDOC2 system components

## CDOC2 reference Java library

Implements client side functionality for CDOC2 system.

## CDOC2 key transmission server (CKCTS)

Stores encryption/decryption key material. Provides endpoints for auth-ticket creation and
key material upload/download. For SID/MID use cases key material is distributed
between multiple CDOC2 servers instances, so that compromising one server doesn't expose key material.
Instances run on independent premises.

## CDOC2 authentication server

Web service to generate CKCTS and SID/MID proxy long-term authentication tokens.
Long-term authentication tokens are one-time, created once after installing CDOC2 client software.
Long-term tickets are used to access API only (Bearer-Auth HTTP header), not used for key-material
retrieval. Uses TARA OpenID Connect to authenticate. Token format is not yet decided.

## CDOC2 CLI user application

Command line utility to create/process CDOC 2.0 files. Provides CLI interface to CDOC2 reference Java library.

# Interfaces between system components

## CDOC2 key transmission server (CKCTS)

TODO: Add existing endpoints

New endpoints for shared secrets supporting SID/MID:
* [/shared-secrets](https://gitlab.cyber.ee/cdoc-2.0/cdoc20_java/-/blob/9206134e6936e7bdf5d62293c3f6f6ed5aeb0e98/cdoc20-openapi/cdoc20-key-capsules.yaml#L111) Upload Shamir Secret Share and get transactionId
* [/shared-secrets/{transactionId}/nonce](https://gitlab.cyber.ee/cdoc-2.0/cdoc20_java/-/blob/9206134e6936e7bdf5d62293c3f6f6ed5aeb0e98/cdoc20-openapi/cdoc20-key-capsules.yaml#L136) 
  Create nonce for transactionId (for authentication). [Authentication ticket creation schema](https://gitlab.cyber.ee/id/ee-ria/ria_tender_test_assignment_2023/-/blob/master/exercise-2.3-authentication-multi-server/multi-server-auth-protocol.md?ref_type=heads#nonsside-v%C3%A4ljastamise-p%C3%A4ringud)
* [/shared-secrets/{transactionId}](https://gitlab.cyber.ee/cdoc-2.0/cdoc20_java/-/blob/9206134e6936e7bdf5d62293c3f6f6ed5aeb0e98/cdoc20-openapi/cdoc20-key-capsules.yaml#L71) GET Shamir Shared Secret for transactionId

## CDOC2 authentication server

* [/gen-token] TBD: Starts authentication process through TARA. If authentication is successful, 
  `get-token` endpoint returns long-term token 
* [/get-token] TBD: Enables to poll for long-term token started by `gen-token` endpoint

