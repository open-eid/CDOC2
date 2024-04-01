---
title: 3. Use Case Model
---

# CDOC2 Client Application use cases

CDOC2 Client Application is an abstract component in the CDOC2 System. CDOC2 Client Applications help End-user to encrypt files to CDOC2 Container, decrypt received CDOC2 Containers. Specific examples of CDOC2 Client Applications include:

* DigiDoc4 desktop application for Windows, MacOS and Linux operating systems (<https://open-eid.github.io/#desktop-applications>, <https://www.id.ee/en/rubriik/digidoc4-client/>, <https://github.com/open-eid/DigiDoc4-Client>)
* DigiDoc4 mobile application for Android and IOS operating systems (<https://open-eid.github.io/#mobile-applications>)
* CDOC2 Client CLI Application

Use cases specified here are written in generic form, so that they are applicable to all client applications. Client applications will implement specified use cases and their documentation may include additional information (use case models, UX wireframes, ...) about the implemented functions.

## Actors

### Human actors

**End-user**
: Person, who is using CDOC2 Client Applications for sending encrypted files to somebody else, or decrypting received CDOC2 Containers. In some use cases, the End-user may encrypt files with symmetric encryption key or password, store the CDOC2 Container for themselves and later decrypt the CDOC2 Container by themself.

**Sender**
: End-user, who wishes to send encrypted files, which are packaged into a CDOC2 Container, to one or multiple Receivers

**Recipient**
: End-user, who wishes to decrypt the received CDOC2 Container and has control over necessary cryptographic key material

**Administrator**
: Person, who is managing CDOC2 Client Application for End-users and is creating the configuration data for them 

### System components as actors

**CDOC2 Client Application (Client)**
: Desktop or mobile application, which encrypts or decrypts CDOC2 Containers and is used by End-users

**CDOC2 Key Capsule Transmission Server (CKCTS)**
: CKCTS mediates CDOC2 Key Capsules (CKC) between Sender and Recipient. Sender's Client can upload CKC to one or multiple CKCTS servers. Recipient's Client can download CKC from CKCTS server after authentication.

## Use cases for Recipients with hardware security tokens

These use cases are useful, when Sender knows that Recipient has specific hardware security token, and knows the public key certificate which correspond to the asymmetric cryptographic key pair on that security token. CKC, which can be decrypted only with Recipient's security token, may be transmitted alongside with the CDOC2 Container itself with the encrypted payload, or with the help of CKCTS server.

### UC.Client.01 — Encrypt CDOC2 Container for sending to Recipient with security token

TO-TRANSLATE "CDOC2 kasutusmallimudel", Section 3.2.1 "UC.CLIENT.01 Krüpteeri sõnum"

**Use Case Context**
: CDOC2 Client Application (Client) adds Sender's chosen files into the CDOC2 Container and encrypts the container with CEK. CEK is encrypted with KEK, which is generated with key-agreement protocol between Sender and Recipient.

**Use Case Level**
: User goal

**Primary Actor**
: Sender

**Main Success Scenario**

1. Sender chooses files to be included in CDOC2 Container and specifies the target filename for CDOC2 Container
2. Sender enters identifiers for each Recipient
3. Client searches for Recipient information in LDAP directory and displays possible public key certificates
4. Sender chooses public key certificates for each Recipient
3. Client executes [CDOC2 encryption scheme SC01](cdoc2-proto-crypto-spec/ch02_encryption_schemes/#sc01_direct_encryption_scheme_for_recipient_with_ec_keys) and generates cryptographic material (FMK, CEK)
4. Client creates CKC for each Recipient and adds CEK
5. Client verifies technical requirements (size of CDOC2 Container header, file correctness, ...)
5. Client encrypts files with CEK, adds them to CDOC2 Container, adds CKC for each Recipient and saves CDOC2 Container

**Extensions**

5a. Technical requirements are not met:

   1. Client displays error message to Sender
   2. Use case ends.

### UC.Client.02 — Decrypt CDOC2 Container with Recipient's security token

TO-TRANSLATE "CDOC2 kasutusmallimudel", Section 3.2.2 "UC.CLIENT.02 Dekrüpteeri sõnum"

## Use cases for Recipients to be authenticated by CKCTS

These use cases can be used, when Sender cannot use Recipient's specific public key certificate (because they don't know it or because Recipient's authentication means doesn't support suitable CDOC2 encryption scheme). In this case, Sender uploads the CKC to one or multiple CKCTS servers. Recipients authenticate to CKCTS servers and download the CKC.

Additional use cases allow Sender to distribute KEK among multiple CKCs according to some kind of secret-sharing scheme (<https://en.wikipedia.org/wiki/Secret_sharing>). Sender uploads each CKC to different CKCTS server. Recipient would need to authenticate to CKCTS servers and download CKCs and reconstruct KEK from them. With $(t,n)$-threshold secret-sharing schemes, Recipient doesn't need to download all $n$ CKCs, in order to reconstruct KEK, but only $t$ CKCs.

### UC.Client.03 — Encrypt CDOC2 container for authenticated Recipients

### UC.Client.04 — Decrypt CDOC2 container by authenticating Recipient

### UC.Client.05 — Encrypt CDOC2 container with secret-shared KEK with Recipient authentication

Prerequisites:

* Client has long-term token to use CDOC2 API.
* Client has configuration for N CDOC2 servers used to upload KEK shares.
* Client has configuration for $t$-number of shares out of $N$ required to combine full secret.

Scheme:



1. Sender checks that SID/MID certificate exists for recipient in SK LDAP server.

    !!! info "TODO"
        SID certificates are not available through SK LDAP server. Need to find a way to check existence of SID account.

2. Sender generates `secret` (symmetric key) and `salt` using secure random.
   key_label value will be: etsi/${etsi_identifier}

    !!! info "TODO"
        _JK: MID uses additionally mobile phone, but this can be asked from user, when decrypting. 
        Later private identifiers could also be supported_

3. Sender [derives key encryption key (KEK)](https://github.com/open-eid/cdoc2-java-ref-impl/blob/main/cdoc20-lib/src/main/java/ee/cyber/cdoc20/crypto/Crypto.java#L121)
   from `secret`, `key_label` and `salt` using HKDF algorithm
4. Sender [generates file master key (FMK)](https://github.com/open-eid/cdoc2-java-ref-impl/blob/main/cdoc20-lib/src/main/java/ee/cyber/cdoc20/crypto/Crypto.java#L94)
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
12. Sender sends CDOC2 document to Recipient

### UC.Client.06 — Decrypt CDOC2 container with secret-shared KEK by by authenticating Recipient

1. Recipient  will enter her _isikukood_ (id-code) and choose Smart-ID decryption method.
1. Recipient searches CDOC header for Smart-ID record with entered id-code.
1. Recipient downloads Smart-ID certificate from SK LDAP using his id (isikukood).
1. {--Recipient verifies that certificate serial from LDAP matches with certificate serial from CDOC SID recipient record.--}
1. Recipient loops over secret shares and for each `server:transactionId` asks `nonce` from server.
    Uses '/secret-shares/{transactionId}/nonce' endpoint in each server.

1. Recipient creates [signed part of authentication_ticket](https://gitlab.cyber.ee/id/ee-ria/ria_tender_test_assignment_2023/-/blob/master/exercise-2.3-authentication-multi-server/multi-server-auth-protocol.md?ref_type=heads#allkirjastatavate-andmete-koostamine)
    that includes transaction_id and SHA256(nonce) pairs from all servers
    and signs it with Smart-ID RP-API v2 [/authentication](https://github.com/SK-EID/smart-id-documentation/blob/v2/README.md#239-authentication-session)
    endpoint. `hash` parameter is `SHA256(authentication_ticket)`.
1. Recipient will create [authentication ticket](https://gitlab.cyber.ee/id/ee-ria/ria_tender_test_assignment_2023/-/blob/master/exercise-2.3-authentication-multi-server/multi-server-auth-protocol.md?ref_type=heads#autentimispiletite-koostamine)
    for each CDOC2 server and download matching secret share. CDOC2 server `GET /secret-share/${transactionId}` endpoint
1. Recipient combines 'secret' shares into full secret (symmetric key) using Shamir Shared Secret Scheme. 
   
    !!! info "TODO"
        TODO: SSSS needs analysis [#RM-55926](https://rm-int.cyber.ee/ito/issues/55926)

1. Recipient [derives key encryption key (KEK)](https://github.com/open-eid/cdoc2-java-ref-impl/blob/main/cdoc20-lib/src/main/java/ee/cyber/cdoc20/crypto/Crypto.java#L121)
    from secret, key_label and salt using HKDF algorithm
1. Recipient decrypts FMK using KEK.
1. Recipient derives CEK and HHK from FMK using HKDF algorithm
1. Recipient calculates hmac and checks it against hmac in CDOC2 header
1. Recipient decrypts content using CEK

## Use cases for password-based encryption

These use cases are useful when End-user wishes to protect confidential files by encrypting them with CEK generated from regular password. End-user may then store CDOC2 Container for longer period, without worrying that hardware security token may not be usable, or public key certificate might be revoked or expired. CDOC2 Container may be later decrypted by Sender itself or Recipient, who knows the shared password.

## UC.Client.07 — Encrypt CDOC2 container with password

## UC.Client.08 — Decrypt CDOC2 container with password

## Supporting use cases

### UC.Client.09 — Create application configuration

# Old UCs

## UC.CLIENT.01 Encrypt Message

TO-TRANSLATE "CDOC2 kasutusmallimudel", Section 3.2.1 "UC.CLIENT.01 Krüpteeri sõnum"

## UC.CLIENT.02 Decrypt Message

TO-TRANSLATE "CDOC2 kasutusmallimudel", Section 3.2.2 "UC.CLIENT.02 Dekrüpteeri sõnum"

## UC.CLIENT.03 Encrypt For Storage (with password)

TO-TRANSLATE "CDOC2 kasutusmallimudel", Section 3.2.3 "UC.CLIENT.03 Krüpteeri parooliga säilitamiseks"

MERGE WITH <https://gitlab.ext.cyber.ee/cdoc2/cdoc20_java#cdoc2-with-symmetric-key-from-password>

# CDOC2 Key Transmission Server use cases

## Actors

## UC.KTS.01 Upload Key Capsule

TO-TRANSLATE "CDOC2 kasutusmallimudel", Section 4.2.1 "UC.KS.01 Edasta võtmekapsel"

## UC.KTS.02 Download Key Capsule

TO-TRANSLATE "CDOC2 kasutusmallimudel", Section 4.2.2 "UC.KS.02 Päri võtmekapsel"

## UC.KTS.03 Delete Key Capsule

TO-TRANSLATE "CDOC2 kasutusmallimudel", Section 4.2.3 "UC.KS.03 Kustuta võtmekapsel"

## UC.KTS.04 Authenticate Recipient

TO-TRANSLATE "CDOC2 kasutusmallimudel", Section 4.2.4 "UC.KS.04 Autendi Vastuvõtja"

