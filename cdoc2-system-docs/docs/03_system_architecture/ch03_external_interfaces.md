---
title: 4. External components and services
---
# External components and services

This section will describe, how CDOC2 system is using external components and services.

## LDAP servers

LDAP servers are used by CDOC2 client applications (for example, reference CLI application and DigiDoc4) to search for Recipient' certificate. Following servers are used:

* SK public LDAP servers - <https://www.skidsolutions.eu/resources/ldap/>
* Zetes public LDAP servers - <ldaps://ldap.eidpki.ee>

## OCSP servers

OCSP servers are used by CDOC2 client applications and CDOC2 Capsule Server to verify that Recipient's certificate is valid and if the Recipient's key pair is still valid.

* SK OCSP servers - SK validity confirmation service is described at <https://github.com/SK-EID/ocsp/wiki> and <http://open-eid.github.io/#_comp_central_conf_server_interfaces>.
* Zetes OCSP servers - <http://ocsp.eidpki.ee/>
