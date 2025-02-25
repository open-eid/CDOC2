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

## LDAP and OCSP servers

* LDAP: (<https://www.skidsolutions.eu/resources/ldap/>)
* OCSP: SK validity confirmation service is described [here](https://github.com/SK-EID/ocsp/wiki) and [here](http://open-eid.github.io/#_comp_central_conf_server_interfaces).

## Smart-ID app

Enables to authenticate and sign using Smart-ID. Installed on user smartphone.

(<https://www.smart-id.com/et/laadi-alla/>)

## Mobile-ID SIM application

* Needs SIM that supports Mobile-ID <https://www.mobiil-id.ee/mobiil-id-tellimine/>
