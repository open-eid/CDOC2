---
title: 4. CDOC2 system components - SID/MID
---

# System Components - Smart-ID / Mobile-ID

This page describes the system components relevant to the Smart-ID/Mobile-ID context. For the Hardware Token/Capsule Server context, see [Hardware Token/Capsule Server](ch03_system_components.md).

## Shared Components

### CDOC2 reference Java library

Implements client side functionality for CDOC2 system. Used by both the Hardware Token/Capsule Server and SID/MID contexts.

## SID/MID Components

### CDOC2 Shares Server (CSS)

Returns share identifiers to CDOC2 Client Application. Stores Key Shares. Recipient has to authenticate with the CSSs in order to download the shares contained in a Shares Capsule.
Shares Capsules are distributed between multiple CDOC2 Shares Server instances, so that compromising one server doesn't expose key material.
Instances run on independent premises.

### CDOC2 Authentication server (auth-server)

The Session Token is an SD-JWT structure that is included, along with its signing certificate, as a header in requests
to other components in the CDOC2 infrastructure.

### CDOC2 Relying party server (rp-server)

Used to mediate and validate client requests to SID/MID relying party
services. Validation includes verifying the session token provided by the client.

### CDOC2 CLI user application

Command line utility to create/process CDOC2 files. Provides CLI interface to CDOC2 reference Java library.

## Interfaces between system components

### CDOC2 Shares Server (CSS) interface

* `/key-shares/{shareId}` Get key share for share identifier. Used by recipient to request a key share.
* `/key-shares` Upload a key share and receive a share identifier. Used by sender to upload key share.
* `/key-shares/{shareId}/nonce` Create nonce for creating an authentication token. Used by
  recipient to request a nonce.
* `/session_nonce` Generate a session nonce for embedding in the session token. Accessed only by
  CDOC2 Auth Server.

For full CSS OpenAPI specification, see [API References](../05_api_references/shares_server_api.md).

### CDOC2 Auth Server interface

* `/auth/start` Start a SID/MID authentication process. Returns a UUID for polling.
* `/auth/status/{authProcessUuid}` Poll authentication status. Returns session token and signing certificate when complete.
* `/.well-known/jwks.jws` Returns the Auth Server's public signing keys (JWK format).

For full Auth Server OpenAPI specification, see [API References](../05_api_references/auth_server_api.md).

### CDOC2 RP Server interface

* `/session-nonce` Generate a session nonce for embedding in the session token. Accessed only by
  CDOC2 Auth Server.
* `/sid/authenticate` Initiate a Smart-ID signing session using the registered RP credentials.
* `/sid/session/{sessionID}` Poll Smart-ID session status and retrieve signature.
* `/mid/authenticate` Initiate a Mobile-ID signing session using the registered RP credentials.
* `/mid/session/{sessionID}` Poll Mobile-ID session status. Returns signature and RFC 9421 countersignature headers.
* `/.well-known/jwks.jws` Returns the RP Server's public signing keys.

For full RP Server OpenAPI specification, see [API References](../05_api_references/rp_server_api.md).
