---
title: 3. CDOC2 system components
---

# CDOC2 system components

## CDOC2 reference Java library

Implements client side functionality for CDOC2 system.

## CDOC2 Capsule Server (CCS)

Stores encryption/decryption key material. Provides endpoints for auth-ticket creation and
key material upload/download. 

## CDOC2 Shares Server (CSS) 

Returns share identifiers to CDOC2 Client Application. Stores Key Shares. Recipient has to authenticate with the CSSs in order to download the shares contained in a Shares Capsule.
Shares Capsules are distributed between multiple CDOC2 Shares Server instances, so that compromising one server doesn't expose key material.
Instances run on independent premises.

## Authentication proxy

A server that relays the Mobile-ID and Smart-ID authentication requests to actual Mobile-ID/Smart-ID RP API services and acts as relying party (RP). Generates and stores secrets that cannot be revealed to CDOC2 Client Applications.

## CDOC2 CLI user application

Command line utility to create/process CDOC2 files. Provides CLI interface to CDOC2 reference Java library.

# Interfaces between system components

## CDOC2 Capsule Server (CCS) interface

CSS interface provides the following endpoints:

* `/key-capsules/{transactionId}` Get Server Capsule based on the transaction identifier. Used by recipient to request a Server Capsule.
* `/key-capsules` Upload a Server Capsule to a CCS. Used by sender to upload Server Capsule to a CCS.

For full CCS OpenAPI specification, see Appendix C in [protocol and cryptography spec](../02_protocol_and_cryptography_spec/appendix_c_cdoc2-capsules.md).

## CDOC2 Shares Server (CSS) interface

* `/key-shares/{shareId}` Get key share for share identifier. Used by recipient to request a key share.
* `/key-shares` Upload a key share and receive a share identifier. Used by sender to upload key share.
* `/key-shares/{shareId}/nonce` Create nonce for creating an authentication ticket. Used by recipient to request a nonce.


For full CSS OpenAPI specification, see Appendix E in [protocol and cryptography spec](../02_protocol_and_cryptography_spec/appendix_e_cdoc2-shares.md).