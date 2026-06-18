---
title: 2. System Context — Smart-ID / Mobile-ID
---
# System Context -  SID/MID

The CDOC2 system operates in two distinct deployment contexts. This page describes the SID/MID context; for the Hardware Token/Capsule Server context, see [Hardware Token/Capsule Server](ch01_system_context.md). Both contexts share the CDOC2 reference library and CDOC2 CLI client as common components.

> **Note:** DigiDoc4 is the primary end-user client application through which
> most users interact with CDOC2. However, DigiDoc4 is not part of the CDOC2
> system scope defined here, as its architecture and documentation are
> maintained separately.

## Overview

![SID/MID](../img/CDOC2_SID_MID_system_context.png)

In the SID/MID context, encryption and decryption flows rely on the Recipient authenticating with Smart-ID or Mobile-ID. Rather than storing a single key capsule, the key material is split into Key Shares that are distributed across multiple CDOC2 Shares Servers, potentially operated by different service providers. Successful decryption requires the Recipient to authenticate and retrieve a threshold of Key Shares from these servers.

Authentication involves the user's smartphone: the Smart-ID app or Mobile-ID SIM app receives the authentication challenge and the user confirms it with PIN1. This out-of-band confirmation step is a core part of the security model.

The system is designed to support multiple independent service provider deployments. Each service provider operates its own set of CDOC2 infrastructure components (RP Server, Shares Server, Auth Server), and Key Shares are distributed across providers so that no single provider can reconstruct the key unilaterally.

## Primary Components

Each service provider deployment contains the following server components, each backed by a local database:

1. CDOC2 Shares Server (CSS): Stores and mediates Key Shares between Sender and Recipient, used by CDOC2 clients such as the CLI Client and DigiDoc4. Multiple instances are deployed across service providers so that key material is distributed and no single server holds a complete key. Exposes endpoints for Key Share retrieval and submission. Every CDOC2 Shares Server uses a local database component as well.
2. CDOC2 Authentication Server (cdoc2-auth-server): Handles the SID/MID authentication session on behalf of CDOC2 clients. Upon successful authentication, composes and issues a signed Session Token that are included as headers in subsequent requests. Also performs OCSP certificate validity checking independently of the RP Server. Has a local database component.
3. CDOC2 Relying Party Server (cdoc2-rp-server): The entry point for SID/MID authentication requests from the CDOC2 Client. Mediates requests to the SK ID Solutions SID/MID APIs, verifies Session Tokens issued by the Auth Server, and performs OCSP certificate validity checking. Has a local database component.

## Shared Libraries

1. CDOC2 Reference Library: used by CDOC2 servers and the CLI client.
2. CDOC2 CLI Client: a command-line Java application that implements all CDOC2 end-user use cases, but without graphical user interface.

## External Systems

The CDOC2 system depends on the following external components and services.
See [External Interfaces](ch05_external_interfaces.md) for API details and endpoints.

1. Smart-ID RP API (SK ID Solutions): Used by the CDOC2 RP Server to initiate and verify Smart-ID authentication sessions using the ACSP_V2 protocol.
2. Mobile-ID REST API (SK ID Solutions): Used by the CDOC2 RP Server to initiate and verify Mobile-ID authentication sessions.
3. OCSP servers (SK ID Solutions, Zetes): Both the RP Server and the Auth Server perform OCSP certificate validity checks for SID/MID certificates.
4. LDAP servers (SK ID Solutions, Zetes): Used by CDOC2 client applications to look up Recipient certificates by identifier (e.g., personal code) prior to encryption. (Not shown in the SID/MID context diagram but applicable to client-side certificate lookup.)
