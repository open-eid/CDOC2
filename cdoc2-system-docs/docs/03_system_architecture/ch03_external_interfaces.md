---
title: 4. External components and services
---
# External components and services

This section describes how the CDOC2 system is using external components and services.

## Shared Components

The following external components are used by both the [Hardware Token/Capsule Server](ch01_system_context.md) and [SID/MID](ch001_system_context_sid_mid.md) contexts.

### LDAP servers

LDAP servers are used by CDOC2 client applications (for example, reference CLI application and DigiDoc4) to search for Recipient' certificate. Following servers are used:

* SK public LDAP servers ([Documentation](https://www.skidsolutions.eu/resources/ldap/)) - [ldaps://esteid.ldap.sk.ee](ldaps://esteid.ldap.sk.ee)
* Zetes public LDAP servers - [ldaps://ldap.eidpki.ee](ldaps://ldap.eidpki.ee)

### OCSP servers

OCSP servers are used by CDOC2 client applications and CDOC2 Capsule Server to verify that Recipient's certificate is valid and if the Recipient's key pair is still valid.

* SK OCSP servers (SK validity confirmation service is described at <https://github.com/SK-EID/ocsp/wiki> and <http://open-eid.github.io/#_comp_central_conf_server_interfaces>) - [http://ocsp.sk.ee/](http://ocsp.sk.ee/)
* Zetes OCSP servers - [http://ocsp.eidpki.ee/](http://ocsp.eidpki.ee/)

## SID/MID Components

### Smart-ID RP API

Relying Party API used by the CDOC2 RP Server to start and poll Smart-ID authentication sessions. The CDOC2 system uses Smart-ID RP API v3 with the ACSP_V2 signature protocol.

* [Smart-ID RP API documentation](https://github.com/SK-EID/smart-id-documentation)
  Starts authentication sessions and polls session status

### Mobile-ID REST API

Relying Party API used by the CDOC2 RP Server to start and poll Mobile-ID authentication sessions.

* <https://github.com/SK-EID/MID>


### Smart-ID app

Enables to authenticate and sign using Smart-ID. Installed on user smartphone.

(<https://www.smart-id.com/et/laadi-alla/>)

### Mobile-ID SIM application

* Needs SIM that supports Mobile-ID <https://www.mobiil-id.ee/mobiil-id-tellimine/>
