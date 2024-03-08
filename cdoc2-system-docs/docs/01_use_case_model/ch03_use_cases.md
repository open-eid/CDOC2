---
title: 3. Use Case Model
---

# CDOC 2.0 Client Application use cases

CDOC 2.0 Client Application is an abstract component in the CDOC 2.0 System. CDOC 2.0 Client Applications help End-user to encrypt files to CDOC 2.0 Container, decrypt received CDOC 2.0 Containers. Specific examples of CDOC 2.0 Client Applications include:

* DigiDoc4 desktop application for Windows, MacOS and Linux operating systems (<https://open-eid.github.io/#desktop-applications>, <https://www.id.ee/en/rubriik/digidoc4-client/>, <https://github.com/open-eid/DigiDoc4-Client>)
* DigiDoc4 mobile application for Android and IOS operating systems (<https://open-eid.github.io/#mobile-applications>)
* CDOC 2.0 Client CLI Application

Use cases specified here are written in generic form, so that they are applicable to all client applications. Client applications will implement specified use cases and their documentation may include additional information (use case models, UX wireframes, ...) about the implemented functions.

## Actors

### Human actors

**User**
: Person, who is using CDOC 2.0 Client Applications for sending encrypted files to somebody else (then as a Sender), or decrypting received CDOC 2.0 Containers (then as a Recipient). In some use cases, the User may encrypt files with symmetric encryption key or password, store the CDOC 2.0 Container for themselves and later decrypt the CDOC 2.0 Container by themself.

**Sender**
: User, who wishes to send encrypted files, which are packaged into a CDOC 2.0 Container, to one or multiple Receivers

**Recipient**
: User, who wishes to decrypt the received CDOC 2.0 Container and has control over necessary cryptographic key material

**Administrator**
: Person, who is managing CDOC 2.0 Client Application for Users and is creating the configuration data for them 

### System components as actors

**CDOC 2.0 Client Application (Client)**
: Desktop or mobile application, which encrypts or decrypts CDOC 2.0 Containers and is used by Users

**Key Capsule Transmission Server (KCTS)**
: KCTS mediates CDOC 2.0 Key Capsules (KC) between Sender and Recipient. Sender's Client can upload KC to one or multiple KCTS servers. Recipient's Client can download KC from KCTS server after authentication.

**LDAP-server**
: An application used for storing private keys of persons.

# CDOC 2.0 Client Application Use Case Model

## Use cases for Recipients with hardware security tokens

These use cases are useful, when Sender knows that Recipient has specific hardware security token, and knows the public key certificate which correspond to the asymmetric cryptographic key pair on that security token. KC, which can be decrypted only with Recipient's security token, may be transmitted alongside with the CDOC 2.0 Container itself with the encrypted payload, or with the help of KCTS server.

### UC.Client.01 — Encrypt CDOC 2.0 container for sending to Recipient with a security token

**Use Case Context**
: CDOC 2.0 Client Application adds Sender's chosen files into the CDOC 2.0 container and encrypts the container with CEK. CEK is encrypted with KEK, which is generated with key-agreement protocol between Sender and Recipient.

**Scope**
: CDOC 2.0 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: Sender

**Success Guarantees**

* CDOC 2.0 container is saved into filesystem.
* A key capsule is sent for each Recepient to the CDOC 2.0 key capsule transmission server.
* Client has received a transaction code for each key capsule.

**Main Success Scenario**

1. Sender chooses files to be included in CDOC 2.0 container and specifies the target filename and path for CDOC 2.0 container.
2. Sender enters identifiers for each Recipient.
3. Client creates a content encryption key (CEK).
4. Client creates a key capsule for each Recipient, encrypt for each Recipient a content encryption key and adds it to the corresponding key capsule.
5. Client displays user from configuration all Key Capsule Transmission Servers.
6. Sender chooses a Key Capsule Transmission Server.
7. Client creates a TLS-connection with the chosen Key Capsule Transmission Server and receives the server's certificate.
8. Client verifies the server's certificate against the configuration. 
9. Client forwards each Receiver's key capsule to the chosen Key Capsule Transmission Server and receives a transaction code for each key capsule.
10. Client creates a container into filesystem in the chosen target path and adds a header.
11. Client verifies that the header does not exceed the size limit defined by the specification.
12. Client verifies technical file correctness, creates an archive, compresses it, encrypts the compressed archive with CEK and adds it to the container as payload.
13. Client saves the CDOC 2 container and displays Receiver a notification.

**Extensions**

2a. Client chooses to search for Recipient information in LDAP directory:

1. Sender inserts Receiver personal code (natural person) or name /business registry code (juridical person).
2. Client requests corresponding certificates and displays those.
3. Sender chooses certificate(s).
4. Use case continues from step 2.

2b. Certificate is not readable or is not in proper format:

1. Client displays Sender a notification.
2. Use case ends.

5a. Configuration has no CDOC 2.0 key capsule transmission servers:

1. Client creates a container in the target path and adds a header with key capsules.
2. Use case continues from step 11.

5b. Configuration has a default CDOC 2.0 key capsule transmission server:

1. Use case continues from step 7.

6a. Sender chooses to not use the CDOC 2.0 key capsule transmission server:

1. Client creates a container in the target path and adds a header with key capsules.
2. Use case continues from step 11.

7a. TLS connection cannot be established:

1. Client displays Sender a notification.
2. Use case continues from step 5.

8a. Certificate validation against the configuration fails:

1. Client displays Sender a notification.
2. Use case continues from step 5.

9a. Forwarding key capsules to a CDOC 2.0 key capsule transmission server fails:

1. Client displays Sender a notification.
2. Use case ends.

9b. CDOC 2.0 key capsule transmission server does not return a transaction identifier for each key capsule:

1. Client displays Sender a notification.
2. Use case ends.

11a. Header size is larger than allowed by the specification:

1. Client displays Sender a notification.
2. Use case ends.

12a. Files are not correct:

1. Client displays Sender a notification.
2. Use case ends.

### UC.Client.02 — Decrypt CDOC 2.0 Container with a security token

**Use Case Context**
: CDOC 2.0 Client Application (Client) decrypts the archive in the CDOC 2 container provided by Receiver, using a key capsule from either Key Capsule Transmission Server or from inside the container.

**Scope**
CDOC 2.0 Client Application

**Use Case Level**
: User goal

**Primary Actor**
: Receiver

**Preconditions**
: Receiver's key device is connected.

**Success Guarantees**

* Files from the CDOC 2.0 container are decrypted and saved into filesystem.

**Main Success Scenario**

1. Sender chooses the CDOC 2.0 Container to be decrypted and specifies the target filename and path for the files.
2. Client verifies that the header does not exceed the size limit defined by the specification.
3. Client reads Receiver certificate from the key device.
4. Client verifies that the container has a record of the Receiver.
5. Client verifies that the Receiver record has a Key Capsule Transmission Server reference.
6. Client redirect Receiver to the Key Capsule Transmission Server for authentication.
7. Client sends the Key Capsule Transmission Server the transaction code from the container.
8. Client receives a key capsule from the Key Capsule Transmission Server.
9. Client decrypts the content encryption key from the key capsule using the connected key device.
10. Client decrypts the encrypted archive in the CDOC 2.0 container using the content encryption key.
11. Client saves the files into the target path in filesystem and notifies the Receiver.

**Extensions**
2a. Header size is larger than allowed by the specification:

1. Client displays Receiver a notification.
2. Use case ends.

3a. Reading certificate from the key device fails.

1. Client displays Receiver a notification.
2. Use case ends.

4a. Receiver record not found in the container.

1. Client displays user a notification.
2. Use case ends.

5a. Receiver record does not contain a reference to a Key Capsule Transmission Server.

1. Client finds a key capsule from the Receiver record.
2. Use case continues from step 9.

6a. Authentication fails:

1. Client displays user a notification.
2. Use case ends.

8a. No key capsule returned from Key Capsule Transmission Server:

1. Client displays user a notification.
2. Use case ends.

9a. Decryption of the content encryption key fails:

1. Client displays user a notification.
2. Use case ends.

## Use cases for Recipients to be authenticated by KCTS

These use cases can be used, when Sender cannot use Recipient's specific public key certificate (because they don't know it or because Recipient's authentication means doesn't support suitable CDOC 2.0 encryption scheme). In this case, Sender uploads the KC to one or multiple KCTS-s. Recipient authenticates to multiple KCTS-s at once and downloads the KC.

Additional use cases allow Sender to distribute KEK among multiple KCs according to some kind of secret-sharing scheme (<https://en.wikipedia.org/wiki/Secret_sharing>). Sender uploads each KC to different KCTS server. Recipient would need to authenticate to KCTS servers and download KCs and reconstruct KEK from them. With $(t,n)$-threshold secret-sharing schemes, Recipient doesn't need to download all $n$ KCs, in order to reconstruct KEK, but only $t$ KCs.

### UC.Client.03 — Encrypt CDOC 2.0 container using key shares

**Use Case Context**
TODO!

**Scope**
: CDOC 2.0 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: Sender

**Preconditions**

* Client has long-term token to use the required CDOC 2.0 API service.
* Client has configuration for N CDOC 2.0 servers used to upload KEK shares.

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

3. Sender [derives key encryption key (KEK)](https://github.com/open-eid/cdoc2-java-ref-impl/blob/main/cdoc20-lib/src/main/java/ee/cyber/cdoc20/crypto/Crypto.java#L121)
   from `secret`, `key_label` and `salt` using HKDF algorithm
4. Sender [generates file master key (FMK)](https://github.com/open-eid/cdoc2-java-ref-impl/blob/main/cdoc20-lib/src/main/java/ee/cyber/cdoc20/crypto/Crypto.java#L94)
    using HKDF extract algorithm
5. Sender derives content encryption key (CEK) and HMAC key (HHK) from FMK using HKDF expand algorithm
6. Sender encrypts FMK with KEK (xor) and gets encrypted_FMK
7. Sender splits `secret` into `N` shares using Shamir Shared Secret Scheme. N is configuration option in CDOC 2.0 client configuration.
   
    !!! info "TODO"
        SSSS needs analysis [#RM-55926](https://rm-int.cyber.ee/ito/issues/55926)

8. Sender uploads each `secret share` and recipient `etsi_identifier` to each CDOC 2.0 server
    (each CDOC 2.0 server will receive a different share).
    CDOC 2.0 servers are configured in client configuration.
    Sender gets `transactionID` for each share. [^1] FBS and OAS

9. Sender adds `encrypted FMK`, `salt`, `key_label` and `server:transactionId` pairs into CDOC 2.0 header. [FBS](https://gitlab.cyber.ee/cdoc-2.0/cdoc20_java/-/blob/RM-55885/cdoc20-schema/src/main/fbs/recipients.fbs#L70)

    !!! info "TODO"
        _JK:In current FBS and OAS spec, instead of server:transactionId pair,
        `secret shares` are identified by full urls. That way there is no need to keep synced list of server_name, server_url in client configuration._

10. Sender calculates header hmac using hmac key (HHK) and adds calculated hmac to CDoc
11. Sender encrypts content with CEK (ChaCha20-Poly1305 with AAD)
12. Sender sends CDOC 2.0 document to Recipient

### UC.Client.04 — Decrypt CDOC 2.0 container using multi-server authentication

TODO!

### UC.Client.06 — Decrypt CDOC 2.0 container with secret-shared KEK by authenticating Recipient

TODO!

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
    for each CDOC 2.0 server and download matching secret share. CDOC 2.0 server `GET /secret-share/${transactionId}` endpoint
1. Recipient combines 'secret' shares into full secret (symmetric key) using Shamir Shared Secret Scheme.
   
    !!! info "TODO"
        TODO: SSSS needs analysis [#RM-55926](https://rm-int.cyber.ee/ito/issues/55926)

1. Recipient [derives key encryption key (KEK)](https://github.com/open-eid/cdoc2-java-ref-impl/blob/main/cdoc20-lib/src/main/java/ee/cyber/cdoc20/crypto/Crypto.java#L121)
    from secret, key_label and salt using HKDF algorithm
1. Recipient decrypts FMK using KEK.
1. Recipient derives CEK and HHK from FMK using HKDF algorithm
1. Recipient calculates hmac and checks it against hmac in CDOC 2.0 header
1. Recipient decrypts content using CEK

## Use cases for password-based encryption

These use cases are useful when End-user wishes to protect confidential files by encrypting them with CEK generated from regular password. End-user may then store CDOC 2.0 Container for longer period, without worrying that hardware security token may not be usable, or public key certificate might be revoked or expired. CDOC 2.0 Container may be later decrypted by Sender itself or Recipient, who knows the shared password.

This group of UCs also include a special use case, when Recipient re-encrypts the content from received Container with a password.

## UC.Client.P.01 — Encrypt CDOC 2.0 container with password for long-term storage

**Use Case Context**
: Encrypt local files for long-term storage using CDOC 2.0 Client Application and password-based cryptography by creating a new CDOC 2.0 Container. This use case is useful for occasions where decryption does not depend on availability of hardware tokens.

**Scope**
: CDOC 2.0 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: User

**Success Guarantees**

* A new CDOC 2.0 container is created and it is encrypted with a password.

**Main Success Scenario**

1. User chooses the files that are to be encrypted.
2. Client asks User to specify the target name and path.
3. User specifies a target name and path in local filesystem.
4. User enters a password to be used for password-based cryptography.
5. Client verifies that the password satisfies minimal requirements.
6. Client adds the files to an archive and creates a new CDOC 2.0 container, which it saves to the target location.

**Extensions**
4a. Password does not meet minimum requirements.

1. Client notifies the User with instructions to insert a new password.
2. Use case continues from step 3.

5a. Container creation or saving fails.

1. System notifies the User.
2. Use case ends.

## UC.Client.P.02 - Encrypt and send CDOC 2.0 container with a pre-shared password

**Use Case Context**
: Encrypt local files for transmitting to another user using CDOC 2.0 Client Application (Client) and password-based cryptography by creating a new CDOC 2.0 Container. This use case is useful for sending encrypted messages to Receivers who do not have eID authentication means and for cases where decryption should not depend on availability of hardware tokens.

**Scope**
: CDOC 2.0 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: Sender

**Preconditions**

* Sender and recipient have a pre-shared secret identified by ``key_label``

**Success Guarantees**

* A new CDOC 2.0 container is created for each Receiver and it is encrypted with a password.

**Main Success Scenario**

1. Sender chooses the files that are to be encrypted. 
2. Sender defines one or more Recipients by providing a ``key_label`` valiue for each (eg. person's ID code).
3. Sender enters a password to be used for password-based cryptography.
4. Client verifies that the password satisfies minimal requirements.
5. Client asks user to specify a target location and name for the container(s).
6. Client generates file master key (FMK) using HKDF extract algorithm. Client derives content encryption key (CEK) and hmac key (HHK) from FMK using HKDF expand algorithm. Client encrypts FMK with KEK (xor). Client adds the files to an archive and creates new CDOC 2.0 containers for each Recipient. Client adds encrypted FMK with ``key_label`` to container header. Client calculates header hmac using hmac key (HHK) and adds calculated hmac to each container. Client encrypts the archive with CEK.
7. Client saves the containers to the target location, generating unique names in case there are multiple recipients and containers.

**Extensions**
4a. Password does not meet minimum requirements.

1. Client notifies the User with instructions to insert a new password.
2. Use case continues from step 3.

7a. Container saving fails.

1. System notifies the User.
2. Use case ends.

## UC.Client.P.03 — Decrypt CDOC 2.0 container with password

**Use Case Context**
: CDOC 2.0 Client Application decrypts CDOC 2.0 Container with password-based cryptography.

**Scope**
: CDOC 2.0 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: User, Recipient

**Main Success Scenario**

1. User specifies which CDOC 2.0 container they wish to open.
2. Client opens the container and retrieves the header information. Client verifies that the header does not exceed the limit defined in the specification.
3. Client asks User for the password to decrypt the container.
4. User enters the password.
5. Client reads password salt and key material salt from container header, uses the password and password salt to calculate password key material. Then uses it with the key material salt to derive the key encryption key. Finally Client derives file master key, uses that to derive the content encryption key and finally decodes the archive in the CDOC 2.0 container.
6. Client asks user for the target location where to save the files.
7. User defines the target location.
8. Client unpacks the archive contents and saves it to the target location.

**Extensions**

2a. Header exceed the length limit according to the specification:

1. Client notifies the user.
2. Use case ends.

5a. Reading password salt or key material salt fails:

1. Client notifies the user.
2. Use case ends.

8a. Saving archive contents to disk fails:

1. Client notifies the user.
2. Use case ends.

## UC.Client.P.04 — Re-encrypt existing CDOC 2.0 container for long-term storage

**Use Case Context**
: CDOC 2.0 Client Application offers Receiver to re-encrypt all files after CDOC 2.0 container decryption and before extracting and saving files locally.

**Scope**
: CDOC 2.0 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: User, in a Recipient role

**Preconditions**

* CDOC 2.0 container is decrypted.

**Success Guarantees**

* Files are re-encrypted.
* The re-encrypted container is saved locally.

**Main Success Scenario**

1. Client suggests Receiver to re-encrypt the decrypted container contents and displays multiple options for encryption.
2. Receiver chooses to re-encrypt and chooses to encrypt with a password.
3. Client asks User to specify the target name and path.
4. User specifies a target name and path in local filesystem.
5. User enters a password to be used for password-based cryptography.
6. Client verifies that the password satisfies minimal requirements.
7. Client adds the files to an archive and creates a new CDOC 2.0 container, which it saves to the target location.

**Extensions**

2a. Receiver chooses to re-encrypt using a key device:

1. Client verifies that the key device is connected.
2. User specifies a target name and path in local filesystem and enters the key device password.
3. Client verifies the password. If password is not correct, the use case continues from the previous step.
4. Use case continues from step 7.

2a. Receiver chooses to re-encrypt using Smart-ID or Mobile-ID:

1. TODO!
2. Use case continues from step 7.

5a. Password does not meet minimum requirements.

1. Client notifies the User with instructions to insert a new password.
2. Use case continues from step 3.

7a. Container creation or saving fails.

1. System notifies the User.
2. Use case ends.

## Supporting use cases

### UC.Client.09 — Create application configuration

TODO!

# Old UCs

MERGE WITH <https://gitlab.cyber.ee/cdoc-2.0/cdoc20_java/-/tree/rm55854#cdoc-20-with-symmetric-key-from-password>

# CDOC 2.0 Key Transmission Server Use Case Model

## UC.KTS.01 Forward Key Capsule

**Context of Use**
: CDOC 2.0 Client Application forwards Key Transmission Server a Receiver key capsule, which contains a content encryption key encrypted for a particular Receiver, which is used for decrypting the archive in CDOC 2.0 container. Key Capsule is saved with an expiration time and a unique transaction code is created and returned to the CDOC 2.0 Client Application.

**Scope**
Key Transmission Server (KS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC 2.0 Client Application (Client)

**Success Guarantees**

* Key capsule is saved with an expiration time.
* Transaction code is forwarded to the CDOC 2.0 Client Application.

**Main Success Scenario**

1. Client sends a key capsule using the appropriate API service to a KS.
2. KS validates the key capsule against specification rules.
3. KS generates a universally unique transaction code (UUID).
4. KS saves the key capsule and an expiration time, which it calculates based on KS system configuration settings.
5. KS returns Client the transaction code.

**Extensions**
2a. Key capsule exceeds the allowed length limit:

1. KS returns Client a error message.
2. Use case ends.

## UC.KTS.02 Request Key Capsule

**Context of Use**
: CDOC 2.0 Client Application requests a Key Capsule from Key Transmission Server, which contains an encrypted content encryption key, used for decrypting the archive in CDOC 2.0 container. Key Capsule is identified by public key in Receiver certificate and the transaction code provided by CDOC 2.0 Client Application.

**Scope**
Key Transmission Server (KS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC 2.0 Client Application (Client)

**Preconditions**

* Receiver is authenticated.

**Success guarantees**

* Key Capsule is forwarded to CDOC 2.0 Client Application.

**Main Success Scenario**

1. Client requests a key capsule using the appropriate API service, providing a transaction code as input.
2. KS validates the transaction code against specification rules.
3. KS finds the correct Key Capsule useing the transaction code and validates that the Receiver public key matches with the one in the Key Capsule.
4. KS sends the Client the Key Capsule.

**Extensions**
2a. Transaction code is too long:

1. KS returns Client an error message.
2. Use case ends.

3a. Key Capsule was not found:

1. KS returns Client an error message.
2. Use case ends.

3b. Receiver public key does not match the one in the Key Capsule:

1. KS returns Client an error message.
2. Use case ends.

## UC.KTS.03 Delete Key Capsule

**Context of Use**
: System timer deletes expired Key Capsules.

**Scope**
Key Transmission Server (KS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC 2.0 Client Application (Client)

**Success guarantees**

* Expired Key Capsules are removed from the storing KS.

**Trigger**

* System timer schedules and initiates the deletion fo expired Key Capsules.

**Main Success Scenario**

1. KS identifies expired Key Capsules.
2. KS deletes expired Key Capsules.

**Extensions**

1a. No expired Key Capsules found.

1. Use case ends.

## UC.KTS.04 Authenticate Recipient

**Context of Use**
: CDOC 2.0 Client Application (Client) establishes a TLS-connection to Key Transmission Server and forwards Receiver certificate.

**Scope**
Key Transmission Server (KS)

**Use Case Level**
: Subfunction

**Primary Actor**
: CDOC 2.0 Client Application (Client)

**Success guarantees**

* TLS-connection is established.
* Receiver certificate exists and is received.

**Main Success Scenario**

1. Client initiates a TLS-connection and forwards Receiver certificate.
2. KS verifies certificate validity using an OCSP service.
3. KS establishes the TLS connection.

**Extensions**

2a. Receiver certificate is not valid:

1. KS replies to the Client with an error message.
2. Use case ends.
