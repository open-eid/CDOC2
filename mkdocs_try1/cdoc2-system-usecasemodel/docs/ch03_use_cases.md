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

TO-TRANSLATE "CDOC2.0 kasutusmallimudel", Section 3.2.1 "UC.CLIENT.01 Krüpteeri sõnum"

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

5a. Technical requirements are not met: { align=right }
    1. Client displays error message to Sender
    2. Use case ends.



### UC.Client.02 — Decrypt CDOC2 Container with Recipient's security token

TO-TRANSLATE "CDOC2.0 kasutusmallimudel", Section 3.2.2 "UC.CLIENT.02 Dekrüpteeri sõnum"


## Use cases for Recipients to be authenticated by CKCTS

These use cases can be used, when Sender cannot use Recipient's specific public key certificate (because they don't know it or because Recipient's authentication means doesn't support suitable CDOC2 encryption scheme). In this case, Sender uploads the CKC to one or multiple CKCTS servers. Recipients authenticate to CKCTS servers and download the CKC.

Additional use cases allow Sender to distribute KEK among multiple CKCs according to some kind of secret-sharing scheme (<https://en.wikipedia.org/wiki/Secret_sharing>). Sender uploads each CKC to different CKCTS server. Recipient would need to authenticate to CKCTS servers and download CKCs and reconstruct KEK from them. With $(t,n)$-threshold secret-sharing schemes, Recipient doesn't need to download all $n$ CKCs, in order to reconstruct KEK, but only $t$ CKCs.

### UC.Client.03 — Encrypt CDOC2 container for authenticated Recipients

### UC.Client.04 — Decrypt CDOC2 container by authenticating Recipient

### UC.Client.05 — Encrypt CDOC2 container with secret-shared KEK with Recipient authentication

### UC.Client.06 — Decrypt CDOC2 container with secret-shared KEK by by authenticating Recipient

## Use cases for password-based encryption

These use cases are useful when End-user wishes to protect confidential files by encrypting them with CEK generated from regular password. End-user may then store CDOC2 Container for longer period, without worrying that hardware security token may not be usable, or public key certificate might be revoked or expired. CDOC2 Container may be later decrypted by Sender itself or Recipient, who knows the shared password.

## UC.Client.07 — Encrypt CDOC2 container with password

## UC.Client.08 — Decrypt CDOC2 container with password

## Supporting use cases

### UC.Client.09 — Create application configuration

# Old UCs

## UC.CLIENT.01 Encrypt Message

TO-TRANSLATE "CDOC2.0 kasutusmallimudel", Section 3.2.1 "UC.CLIENT.01 Krüpteeri sõnum"

## UC.CLIENT.02 Decrypt Message

TO-TRANSLATE "CDOC2.0 kasutusmallimudel", Section 3.2.2 "UC.CLIENT.02 Dekrüpteeri sõnum"

## UC.CLIENT.03 Encrypt For Storage (with password)

TO-TRANSLATE "CDOC2.0 kasutusmallimudel", Section 3.2.3 "UC.CLIENT.03 Krüpteeri parooliga säilitamiseks"

MERGE WITH <https://gitlab.cyber.ee/cdoc-2.0/cdoc20_java/-/tree/rm55854#cdoc-20-with-symmetric-key-from-password>

# CDOC2 Key Transmission Server use cases

## Actors

## UC.KTS.01 Upload Key Capsule

TO-TRANSLATE "CDOC2.0 kasutusmallimudel", Section 4.2.1 "UC.KS.01 Edasta võtmekapsel"

## UC.KTS.02 Download Key Capsule

TO-TRANSLATE "CDOC2.0 kasutusmallimudel", Section 4.2.2 "UC.KS.02 Päri võtmekapsel"

## UC.KTS.03 Delete Key Capsule

TO-TRANSLATE "CDOC2.0 kasutusmallimudel", Section 4.2.3 "UC.KS.03 Kustuta võtmekapsel"

## UC.KTS.04 Authenticate Recipient

TO-TRANSLATE "CDOC2.0 kasutusmallimudel", Section 4.2.4 "UC.KS.04 Autendi Vastuvõtja"

