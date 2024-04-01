---
title: 3. Use Case Model
---

# CDOC2 Client Application Use Case Model

CDOC2 Client Application is an abstract component in the CDOC2 System. CDOC2 Client Applications help users to encrypt files to CDOC2 Container, decrypt received CDOC2 Containers. Specific examples of CDOC2 Client Applications include:

* DigiDoc4 desktop application for Windows, MacOS and Linux operating systems (<https://open-eid.github.io/#desktop-applications>, <https://www.id.ee/en/rubriik/digidoc4-client/>, <https://github.com/open-eid/DigiDoc4-Client>)
* DigiDoc4 mobile application for Android and IOS operating systems (<https://open-eid.github.io/#mobile-applications>)
* CDOC2 Client CLI Application

Use cases specified here are written in generic form, so that they are applicable to all client applications. Client applications will implement specified use cases and their documentation may include additional information (use case models, UX wireframes, ...) about the implemented functions.

## Actors

### Human actors

**User**
: Person, who is using CDOC2 Client Applications for sending encrypted files to somebody else (then as a Sender), or decrypting received CDOC2 Containers (then as a Recipient). In some use cases, the User may encrypt files with symmetric encryption key or password, store the CDOC2 Container for themselves and later decrypt the CDOC2 Container by themself.

**Sender**
: User, who wishes to send encrypted files, which are packaged into a CDOC2 Container, to one or multiple Recipients

**Recipient**
: User, who wishes to decrypt the received CDOC2 Container and has control over necessary cryptographic key material

**Administrator**
: Person, who is managing CDOC2 Client Application for Users and is creating the configuration data for them

### System components as actors

**CDOC2 Client Application (Client)**
: Desktop or mobile application, which encrypts or decrypts CDOC2 Containers and is used by Users

**Key Capsule Transmission Server (KCTS)**
: KCTS mediates CDOC2 Key Capsules (KC) between Sender and Recipient. Sender's Client can upload KC to one or multiple KCTS servers. Recipient's Client can download KC from KCTS server after authentication.

**LDAP-server**
: An application used for publishing public keys.

## Use cases for Recipients with hardware security tokens

These use cases are useful, when Sender knows that Recipient has specific hardware security token, and knows the public key certificate which correspond to the asymmetric cryptographic key pair on that security token. KC, which can be decrypted only with Recipient's security token, may be transmitted alongside with the CDOC2 Container itself with the encrypted payload, or with the help of KCTS server.

### UC.Client.01 — Encrypt CDOC2 container for sending to Recipient with a security token

**Use Case Context**
: CDOC2 Client Application adds Sender's chosen files into the CDOC2 container and encrypts the container with CEK. CEK is encrypted with KEK, which is generated with key-agreement protocol between Sender and Recipient.

**Scope**
: CDOC2 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: Sender

**Success Guarantees**

* CDOC2 container is saved into filesystem.
* A key capsule is sent for each Recipient to the CDOC2 key capsule transmission server.
* Client has received a transaction code for each key capsule.

**Main Success Scenario**

1. Sender chooses files to be included in CDOC2 container and specifies the target filename and path for CDOC2 container.
2. Sender enters identifiers for each Recipient.
3. Client creates a key capsule for each Recipient.
4. Client displays a list of Key Capsule Transmission Servers to Sender.
5. Sender chooses a Key Capsule Transmission Server.
6. Client creates a TLS-connection with the chosen Key Capsule Transmission Server and receives the server's certificate.
7. Client verifies the server's certificate against the configuration.
8. Client forwards each Recipient's key capsule to the chosen Key Capsule Transmission Server and receives a transaction code for each key capsule.
9. Client creates a container into filesystem in the chosen target path and adds a header.
10. Client verifies that the header does not exceed the size limit defined by the specification.
11. Client verifies technical file correctness, creates an archive, compresses it, encrypts the compressed archive with CEK and adds it to the container as payload.
12. Client saves the CDOC2 container and displays Sender a notification.

**Extensions**

1a. Sender chose to encrypt from the Windows Explorer / MacOS Finder / Linux folder explorer context dialog: "Encrypt with eID" and "Encrypt with password":

1. Client asks Sender for the container target name and path.
2. Sender specifies the target name and path.
3. Use case continues from step 2.

2a. Client chooses to search for Recipient information in LDAP directory:

1. Sender inserts Recipient personal code (natural person) or name / business registry code (juridical person).
2. Client requests corresponding certificates and displays those.
3. Sender chooses certificate(s).
4. Use case continues from step 2.

2b. Certificate is not readable or is not in proper format:

1. Client displays Sender a notification.
2. Use case ends.

5a. Configuration has no CDOC2 key capsule transmission servers:

1. Client creates a container in the target path and adds a header with key capsules.
2. Use case continues from step 11.

5b. Configuration has a default CDOC2 key capsule transmission server:

1. Use case continues from step 7.

6a. Sender chooses to not use the CDOC2 key capsule transmission server:

1. Client creates a container in the target path and adds a header with key capsules.
2. Use case continues from step 11.

7a. TLS connection cannot be established:

1. Client displays Sender a notification.
2. Use case continues from step 5.

8a. Certificate validation against the configuration fails:

1. Client displays Sender a notification.
2. Use case continues from step 5.

9a. Forwarding key capsules to a CDOC2 key capsule transmission server fails:

1. Client displays Sender a notification.
2. Use case ends.

9b. CDOC2 key capsule transmission server does not return a transaction identifier for each key capsule:

1. Client displays Sender a notification.
2. Use case ends.

10a. Header size is larger than allowed by the specification:

1. Client displays Sender a notification.
2. Use case ends.

11a. Files are not correct:

1. Client displays Sender a notification.
2. Use case ends.

### UC.Client.02 — Decrypt CDOC2 Container with a security token

**Use Case Context**
: CDOC2 Client Application (Client) decrypts the archive in the CDOC2 container provided by Recipient, using a key capsule from either Key Capsule Transmission Server or from inside the container.

**Scope**
CDOC2 Client Application

**Use Case Level**
: User goal

**Primary Actor**
: Recipient

**Preconditions**
: Recipient's security token is connected.

**Success Guarantees**

* Files from the CDOC2 container are decrypted and saved into filesystem.

**Main Success Scenario**

1. Recipient chooses the CDOC2 Container to be decrypted and specifies the target filename and path for the files.
2. Client verifies that the header does not exceed the size limit defined by the specification.
3. Client reads Recipient certificate from the security token.
4. Client verifies that the container has a record of the Recipient.
5. Client verifies that the Recipient record has a Key Capsule Transmission Server reference.
6. Client uses Recipient's eID means to authenticate to KCTS.
7. Client sends the Key Capsule Transmission Server the transaction code from the container.
8. Client receives a key capsule from the Key Capsule Transmission Server.
9. Client decrypts the encrypted archive in the CDOC2 container using the connected security token.
10. Client saves the files into the target path in filesystem and notifies the Recipient.

**Extensions**
2a. Header size is larger than allowed by the specification:

1. Client displays Recipient a notification.
2. Use case ends.

3a. Reading certificate from the security token fails.

1. Client displays Recipient a notification.
2. Use case ends.

4a. Recipient record not found in the container.

1. Client displays Recipient a notification.
2. Use case ends.

5a. Recipient record does not contain a reference to a Key Capsule Transmission Server.

1. Client finds a key capsule from the Recipient record.
2. Use case continues from step 9.

6a. PIN 1 code is required:

1. Client asks user for a PIN 1 code.
2. Recipient enters the PIN code.
3. Client completes the authentication. Use case continues from step 7.

6b. Authentication fails:

1. Client displays user a notification.
2. Use case ends.

8a. No key capsule returned from Key Capsule Transmission Server:

1. Client displays user a notification.
2. Use case ends.

9a. Decryption of the content encryption key fails:

1. Client displays user a notification.
2. Use case ends.

## Use cases for password-based encryption

These use cases are useful when User wishes to protect confidential files by encrypting them with CEK generated from regular password. User may then store CDOC2 Container for longer period, without worrying that security token may not be usable, or public key certificate might be revoked or expired. CDOC2 Container may be later decrypted by Sender itself or Recipient, who knows the shared password.

This group of UCs also include a special use case, when Recipient re-encrypts the content from received Container with a password.

## UC.Client.P.01 — Encrypt CDOC2 container with password for long-term storage

**Use Case Context**
: Encrypt local files for long-term storage using CDOC2 Client Application and password-based cryptography by creating a new CDOC2 Container. This use case is useful for occasions where decryption does not depend on availability of security tokens.

**Scope**
: CDOC2 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: User

**Success Guarantees**

* A new CDOC2 container is created and it can be decrypted with the user's password.

**Main Success Scenario**

1. User chooses the files that are to be encrypted.
2. Client asks User to specify the target name and path.
3. User specifies a target name and path in local filesystem.
4. User enters a password to be used for password-based cryptography.
5. Client verifies that the password satisfies minimal requirements.
6. Client creates a container into filesystem in the chosen target path and adds a header.
7. Client verifies that the header does not exceed the size limit defined by the specification.
8. Client verifies technical file correctness, creates an archive, compresses it and encrypts the compressed archive.
9. Client saves the CDOC2 container and displays Sender a notification.

**Extensions**

1a. Sender chose to encrypt from the Windows Explorer / MacOS Finder / Linux folder explorer context dialog: "Encrypt with eID" and "Encrypt with password":

1. Client asks Sender for the container target name and path.
2. Sender specifies the target name and path.
3. Use case continues from step 2.

5a. Password does not meet minimum requirements:

1. Client notifies the User with instructions to insert a new password.
2. Use case continues from step 4.

6a. Container creation fails:

1. System notifies the User.
2. Use case ends.

7a. Header size is larger than allowed by the specification:

1. Client displays Sender a notification.
2. Use case ends.

8a. Files are not correct:

1. Client displays Sender a notification.
2. Use case ends.

9a. Container saving fails:

1. Client notifies the User.
2. Use case ends.

## UC.Client.P.02 — Decrypt CDOC2 container with password

**Use Case Context**
: CDOC2 Client Application decrypts CDOC2 Container with password-based cryptography.

**Scope**
: CDOC2 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: User, Recipient

**Main Success Scenario**

1. User specifies which CDOC2 container they wish to open.
2. Client opens the container and retrieves the header information. Client verifies that the header does not exceed the limit defined in the specification.
3. Client asks User for the password to decrypt the container.
4. User enters the password.
5. Client reads password salt and key material salt from container header, uses the password and password salt to calculate password key material. Then uses it with the key material salt to derive the key encryption key. Finally Client derives file master key, uses that to derive the content encryption key and finally decodes the archive in the CDOC2 container.
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

## UC.Client.P.04 — Re-encrypt existing CDOC2 container for long-term storage

**Use Case Context**
: CDOC2 Client Application offers Recipient to re-encrypt all files after CDOC2 container decryption and before extracting and saving files locally.

**Scope**
: CDOC2 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: User, in a Recipient role

**Preconditions**

* CDOC2 container is decrypted.

**Success Guarantees**

* Files are re-encrypted.
* The re-encrypted container is saved locally.

**Main Success Scenario**

1. Client suggests Recipient to re-encrypt the decrypted container contents and displays multiple options for encryption.
2. Recipient chooses to re-encrypt and chooses to encrypt with a password.
3. Client asks User to specify the target name and path.
4. User specifies a target name and path in local filesystem.
5. User enters a password to be used for password-based cryptography.
6. Client verifies that the password satisfies minimal requirements.
7. Client adds the files to an archive and creates a new CDOC2 container, which it saves to the target location.

**Extensions**

2a. Recipient chooses to re-encrypt using a security token:

1. Client verifies that the security token is connected.
2. User specifies a target name and path in local filesystem and enters the security token password.
3. Client verifies the password. If password is not correct, the use case continues from the previous step.
4. Use case continues from step 7.

2a. Recipient chooses to re-encrypt using Smart-ID or Mobile-ID:

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

MERGE WITH <https://gitlab.ext.cyber.ee/cdoc2/cdoc20_java#cdoc2-with-symmetric-key-from-password>

# CDOC2 Key Transmission Server Use Case Model

## UC.KTS.01 Forward Key Capsule

**Context of Use**
: CDOC2 Client Application forwards Key Transmission Server a Recipient key capsule, which contains a content encryption key encrypted for a particular Recipient, which is used for decrypting the archive in CDOC2 container. Key Capsule is saved with an expiration time and a unique transaction code is created and returned to the CDOC2 Client Application.

**Scope**
Key Transmission Server (KS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC2 Client Application (Client)

**Success Guarantees**

* Key capsule is saved with an expiration time.
* Transaction code is forwarded to the CDOC2 Client Application.

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
: CDOC2 Client Application requests a Key Capsule from Key Transmission Server, which contains an encrypted content encryption key, used for decrypting the archive in CDOC2 container. Key Capsule is identified by public key in Recipient certificate and the transaction code provided by CDOC2 Client Application.

**Scope**
Key Transmission Server (KS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC2 Client Application (Client)

**Preconditions**

* Recipient is authenticated.

**Success guarantees**

* Key Capsule is forwarded to CDOC2 Client Application.

**Main Success Scenario**

1. Client requests a key capsule using the appropriate API service, providing a transaction code as input.
2. KS validates the transaction code against specification rules.
3. KS finds the correct Key Capsule useing the transaction code and validates that the Recipient public key matches with the one in the Key Capsule.
4. KS sends the Client the Key Capsule.

**Extensions**
2a. Transaction code is too long:

1. KS returns Client an error message.
2. Use case ends.

3a. Key Capsule was not found:

1. KS returns Client an error message.
2. Use case ends.

3b. Recipient public key does not match the one in the Key Capsule:

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
: CDOC2 Client Application (Client)

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
: CDOC2 Client Application (Client) establishes a TLS-connection to Key Transmission Server and forwards Recipient certificate.

**Scope**
Key Transmission Server (KS)

**Use Case Level**
: Subfunction

**Primary Actor**
: CDOC2 Client Application (Client)

**Success guarantees**

* TLS-connection is established.
* Recipient certificate exists and is received.

**Main Success Scenario**

1. Client initiates a TLS-connection and forwards Recipient certificate.
2. KS verifies certificate validity using an OCSP service.
3. KS establishes the TLS connection.

**Extensions**

2a. Recipient certificate is not valid:

1. KS replies to the Client with an error message.
2. Use case ends.
