---
title: 4. External components and services
---
# External components and services

This section will describe, how CDOC2 system is using external components and services

## MID/SID authentication proxy

Proxy provided by RIA to provide access to Smart-ID RP API and Mobile-ID REST API

## Smart-ID RP API

Relaying Party API is used to start authentication with Smart-ID accessed through MID/SID authentication proxy

* [/authentication](https://github.com/SK-EID/smart-id-documentation/blob/v2/README.md#239-authentication-session)
  Starts authentication with Smart-ID
* [/session](https://github.com/SK-EID/smart-id-documentation/blob/v2/README.md#2311-session-status)
  Poll authentication status

## Mobile-ID REST API

* <https://github.com/SK-EID/MID>

## LDAP servers

LDAP servers are used by CDOC2 client applications (for example, reference CLI application and DigiDoc4) to search for Recipient' certificate. Following servers are used:

* SK public LDAP servers ([Documentation](https://www.skidsolutions.eu/resources/ldap/)) - [ldaps://esteid.ldap.sk.ee](ldaps://esteid.ldap.sk.ee)
* Zetes public LDAP servers - [ldaps://ldap.eidpki.ee](ldaps://ldap.eidpki.ee)

## OCSP servers

OCSP servers are used by CDOC2 client applications and CDOC2 Capsule Server to verify that Recipient's certificate is valid and if the Recipient's key pair is still valid.

* SK OCSP servers (SK validity confirmation service is described at <https://github.com/SK-EID/ocsp/wiki> and <http://open-eid.github.io/#_comp_central_conf_server_interfaces>) - [http://ocsp.sk.ee/](http://ocsp.sk.ee/)
* Zetes OCSP servers - [http://ocsp.eidpki.ee/](http://ocsp.eidpki.ee/)

## Smart-ID app

Enables to authenticate and sign using Smart-ID. Installed on user smartphone.

(<https://www.smart-id.com/et/laadi-alla/>)

## Mobile-ID SIM application

* Needs SIM that supports Mobile-ID <https://www.mobiil-id.ee/mobiil-id-tellimine/>
