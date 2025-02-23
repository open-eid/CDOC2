---
title: 3. CDOC2 system components
---

# CDOC2 system components

## CDOC2 reference Java library

Implements client side functionality for CDOC2 system.

## CDOC2 Capsule Server (CCS)

Stores encryption/decryption key material. Provides endpoints for auth-ticket creation and
key material upload/download. For SID/MID use cases key material is distributed
between multiple CDOC2 servers instances, so that compromising one server doesn't expose key material.
Instances run on independent premises.

## Authentication proxy
A server that relays the Mobile-ID and Smart-ID authentication requests to actual Mobile-ID/Smart-ID RP API services and acts as relying party (RP). Generates and stores secrets that cannot be revealed to CDOC2 Client Applications.

## CDOC2 CLI user application

Command line utility to create/process CDOC2 files. Provides CLI interface to CDOC2 reference Java library.

# Interfaces between system components

## CDOC2 Capsule Server (CCS) interface

TODO: Add existing endpoints

New endpoints for shared secrets supporting SID/MID:

* [/shared-secrets](https://gitlab.ext.cyber.ee/cdoc2/cdoc20_java/-/blob/RM-55885/cdoc2-openapi/cdoc2-key-capsules.yaml#L111) Upload Shamir Secret Share and get transactionId
* [/shared-secrets/{transactionId}/nonce](https://gitlab.ext.cyber.ee/cdoc2/cdoc20_java/-/blob/RM-55885/cdoc2-openapi/cdoc2-key-capsules.yaml#L136)
  Create nonce for transactionId (for authentication). [Authentication ticket creation schema](https://gitlab.cyber.ee/id/ee-ria/ria_tender_test_assignment_2023/-/blob/master/exercise-2.3-authentication-multi-server/multi-server-auth-protocol.md?ref_type=heads#nonsside-v%C3%A4ljastamise-p%C3%A4ringud)
* [/shared-secrets/{transactionId}](https://gitlab.ext.cyber.ee/cdoc2/cdoc20_java/-/blob/RM-55885/cdoc2-openapi/cdoc2-key-capsules.yaml#L71) GET Shamir Shared Secret for transactionId
