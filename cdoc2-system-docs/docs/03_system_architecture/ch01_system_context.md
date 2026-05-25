---
title: 2. System Context
---
# System Context

![SID/MID](../img/CDOC2_SID_MID_system_context.png)

## Overview

"CDOC2 system" - IT system, which contains following primary components:

1. CDOC2 Capsule Server (CCS) to be used by CDOC2 clients, such as reference CLI client and DigiDoc4 client application. Every CDOC2 Capsule Server uses local database component as well.
2. CDOC2 Shares Server (CSS) to be used by CDOC2 clients, such as reference CLI client and DigiDoc4 client application. Every CDOC2 Shares Server uses local database component as well.
3. CDOC2 Authentication Server (cdoc2-auth-server) is used in SID/MID autentication flows only. Composes and issues session tokens that are included as headers in subsequent requests to other CDOC2 infrastructure components. Has a local database component.
4. CDOC2 Relying Party Server (cdoc2-rp-server). Mediates and validates client requests to the SID/MID relying party API, including verifying the Session Token issued by the Authentication Server. Has a local database component.
5. CDOC2 reference library, to be used by CDOC2 servers, CLI client.
6. CDOC2 CLI client, which is a command-line Java application and which implements all CDOC2 end-user use cases, but without graphical user interface.

> **Note:** DigiDoc4 is the primary end-user client application through which most users interact with CDOC2. However, DigiDoc4 is not part of the CDOC2 system scope defined here, as its architecture and documentation are maintained separately.

## External Systems

The CDOC2 system depends on the following external components and services. 
See [External Interfaces](ch03_external_interfaces.md) for API details and endpoints. 

1. Smart-ID RP API (SK ID Solutions), which the CDOC2 RP Server connects to for Smart-ID authentication sessions using protocol ACSP_V2.
2. Mobile-ID REST API (SK ID Solutions), which the CDOC2 RP Server connects to for Mobile-ID authentication sessions.
3. OCSP servers (SK ID Solutions, Zetes), which provide certificate validity checking for ID-card/MID/SID certificates.
4. LDAP servers (SK ID Solutions, Zetes), which are used by CDOC2 client applications to search for Recipient certificates.
