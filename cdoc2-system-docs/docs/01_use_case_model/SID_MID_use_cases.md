---
title: 3. Use Case Model - Smart-ID and Mobile-ID
---

## Use cases for Recipients to be authenticated by CCS

These use cases can be used, when Sender cannot use Recipient's specific public key certificate (because they don't know it or because Recipient's authentication means don't support a suitable CDOC2 encryption scheme). In this case, Sender uploads the KC to one or KC shares to multiple CCS-s. Recipient authenticates to multiple CCS-s at once and downloads the KC shares.

Additional use cases allow Sender to distribute KEK among multiple KC-s according to a [secret-sharing scheme](<https://en.wikipedia.org/wiki/Secret_sharing>). Sender uploads each KC to a different CCS server. Recipient would need to authenticate to CCS servers and download KC-s and reconstruct KEK from them. With $(t,n)$-threshold secret-sharing schemes, Recipient doesn't need to download all $n$ KC-s, in order to reconstruct KEK, but only $t$ KC-s.

### UC.Client.03 — Encrypt CDOC2 container using key shares

**Use Case Context**
TODO!

**Scope**
: CDOC2 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: Sender

**Preconditions**

* Client has a long-term token to use the required CDOC2 API service.
* Client has configuration for N CDOC2 servers used to upload KEK shares.

**Success Guarantees**

*  

**Main Success Scenario**

Prerequisites:

Scheme:

1. Sender checks that SID/MID certificate exists for recipient in SK LDAP server.

    !!! info "TODO"
        SID certificates are not available through SK LDAP server. Need to find a way to check existence of SID account.

2. Sender generates `secret` (symmetric key) and `salt` using secure random.
   key_label value will be: etsi/${etsi_identifier}

    !!! info "TODO"
        _JK: MID uses additionally mobile phone, but this can be asked from user, when decrypting.
        Later private identifiers could also be supported_

3. Sender [derives key encryption key (KEK)](https://github.com/open-eid/cdoc2-java-ref-impl/blob/main/cdoc2-lib/src/main/java/ee/cyber/cdoc2/crypto/Crypto.java#L121)
   from `secret`, `key_label` and `salt` using HKDF algorithm
4. Sender [generates file master key (FMK)](https://github.com/open-eid/cdoc2-java-ref-impl/blob/main/cdoc2-lib/src/main/java/ee/cyber/cdoc2/crypto/Crypto.java#L94)
    using HKDF extract algorithm
5. Sender derives content encryption key (CEK) and HMAC key (HHK) from FMK using HKDF expand algorithm
6. Sender encrypts FMK with KEK (xor) and gets encrypted_FMK
7. Sender splits `secret` into `N` shares using Shamir Shared Secret Scheme. N is configuration option in CDOC2 client configuration.

    !!! info "TODO"
        SSSS needs analysis [#RM-55926](https://rm-int.cyber.ee/ito/issues/55926)

8. Sender uploads each `secret share` and recipient `etsi_identifier` to each CDOC2 server
    (each CDOC2 server will receive a different share).
    CDOC2 servers are configured in client configuration.
    Sender gets `transactionID` for each share. [^1] FBS and OAS

9. Sender adds `encrypted FMK`, `salt`, `key_label` and `server:transactionId` pairs into CDOC2 header. [FBS](https://gitlab.ext.cyber.ee/cdoc2/cdoc20_java/-/blob/RM-55885/cdoc2-schema/src/main/fbs/recipients.fbs#L70)

    !!! info "TODO"
        _JK:In current FBS and OAS spec, instead of server:transactionId pair,
        `secret shares` are identified by full urls. That way there is no need to keep synced list of server_name, server_url in client configuration._

10. Sender calculates header hmac using hmac key (HHK) and adds calculated hmac to CDoc
11. Sender encrypts content with CEK (ChaCha20-Poly1305 with AAD)
12. Sender sends CDOC2 document to Recipient.

### UC.Client.04 — Decrypt CDOC2 container using multiserver authentication

TODO!

### UC.Client.06 — Decrypt CDOC2 container with secret-shared KEK by authenticating Recipient

TODO!

1. Recipient enters ID-code and chooses Smart-ID decryption method.
1. Recipient searches CDOC header for Smart-ID record with entered id-code.
1. Recipient downloads Smart-ID certificate from SK LDAP using his id (isikukood).
1. {--Recipient verifies that certificate serial from LDAP matches with certificate serial from CDOC SID recipient record.--}
1. Recipient loops over secret shares and for each `server:transactionId` asks `nonce` from server.
    Uses '/secret-shares/{transactionId}/nonce' endpoint in each server.

1. Recipient creates [signed part of authentication_ticket](https://gitlab.cyber.ee/id/ee-ria/ria_tender_test_assignment_2023/-/blob/master/exercise-2.3-authentication-multi-server/multi-server-auth-protocol.md?ref_type=heads#allkirjastatavate-andmete-koostamine)
    that includes transaction_id and SHA256(nonce) pairs from all servers
    and signs it with Smart-ID RP API v2 [/authentication](https://github.com/SK-EID/smart-id-documentation/blob/v2/README.md#239-authentication-session)
    endpoint. `hash` parameter is `SHA256(authentication_ticket)`.
1. Recipient will create [authentication ticket](https://gitlab.cyber.ee/id/ee-ria/ria_tender_test_assignment_2023/-/blob/master/exercise-2.3-authentication-multi-server/multi-server-auth-protocol.md?ref_type=heads#autentimispiletite-koostamine)
    for each CDOC2 server and download matching secret share. CDOC2 server `GET /secret-share/${transactionId}` endpoint
1. Recipient combines 'secret' shares into full secret (symmetric key) using Shamir Shared Secret Scheme.

    !!! info "TODO"
        TODO: SSSS needs analysis [#RM-55926](https://rm-int.cyber.ee/ito/issues/55926)

1. Recipient [derives key encryption key (KEK)](https://github.com/open-eid/cdoc2-java-ref-impl/blob/main/cdoc2-lib/src/main/java/ee/cyber/cdoc2/crypto/Crypto.java#L121)
    from secret, key_label and salt using HKDF algorithm
1. Recipient decrypts FMK using KEK.
1. Recipient derives CEK and HHK from FMK using HKDF algorithm
1. Recipient calculates hmac and checks it against hmac in CDOC2 header
1. Recipient decrypts content using CEK

## Supporting use cases

### UC.Client.09 — Acquire a long-term access token

**Use Case Context**
: CDOC2 Client Application asks User to authenticate in order to establish a long-term access token which is required to gain API access to any CDOC2 Capsule Servers.

**Scope**
: CDOC2 Client Application (Client)

**Use Case Level**
: Subfunction

**Primary Actor**
: User

**Preconditions**

* CDOC2 Client Application is installed on User system.

**Success Guarantees**

* Client has a long-term access token to CDOC2 Capsule Server API-s.
* Client allows User to encrypt CDOC2 containers for other Recipients besides the User.

**Main Success Scenario**

1. Client asks User to authenticate in order to gain access to CDOC2 Capsule Servers.
2. User agrees to authenticate.
3. Client opens a web view and directs user to an authentication service (e.g. TARA) that follows the OpenID Connect protocol. The authentication request is inside the redirect URL and the request is mediated by a CDOC2 Authentication Server. User is shown a choice of authentication methods.
4. User chooses an authentication method.
5. User completes the authentication by using an external authentication device.
6. User is redirected back to the Client, mediated by a CDOC2 Authentication Server.
7. CDOC2 Authentication Server requests the authentication service an identity token providing a client secret inside the request.
8. CDOC2 Authentication Server receives the identity token and validates its signature, address and expiration time.
9. Client receives a long-term access token from the CDOC2 Authentication Server.
10. Client notifies User that the authentication is successfully completed.

**Extensions**

5a. Authentication results in an error:

1. Authentication service displays the error and offers User to try again or try another authentication method.
2. Use case continues from step 4.

5b. User cancels the authentication flow:

1. Client redirects User back to the Client and notifies about the error.
2. Use case ends.

7a. Identity token is invalid:

1. Client notifies the User.
2. Use case ends.

8a. Identity token request expires:

1. Client notifies the User that the authentication process has to be restarted.
2. Use case continues from step 1.

8b. Identity token is not valid:

1. Client notifies the User.
2. Use case ends.