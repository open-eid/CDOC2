---
title: 3. Use Case Model
---
# CDOC2 Client Application Use Case Model

CDOC2 Client Application is an abstract component in the CDOC2 System. CDOC2 Client Applications help users to encrypt files to CDOC2 Container, decrypt received CDOC2 Containers. Specific examples of CDOC2 Client Applications include:

* DigiDoc4 desktop application for Windows, MacOS and Linux operating systems (<https://open-eid.github.io/#desktop-applications>, <https://www.id.ee/en/rubriik/digidoc4-client/>, <https://github.com/open-eid/DigiDoc4-Client>)
* DigiDoc4 mobile application for Android and IOS operating systems (<https://open-eid.github.io/#mobile-applications>)
* CDOC2 Client CLI Application

Use cases specified here are written in a generic form, so that they are applicable to all client applications. Client applications will implement specified use cases and their documentation may include additional information (use case models, UX wireframes, ...) about the implemented functions.
Use cases specified here are written in a generic form, so that they are applicable to all client applications. Client applications will implement specified use cases and their documentation may include additional information (use case models, UX wireframes, ...) about the implemented functions.

## Actors

### Human actors

**User**
: Person, who is using CDOC2 Client Applications for sending encrypted files to somebody else (then as a Sender), or decrypting received CDOC2 Containers (then as a Recipient). In some use cases, the User may encrypt files with symmetric encryption key or password, store the CDOC2 Container for themselves and later decrypt the CDOC2 Container by themselves.

**Sender**
: User, who wishes to send encrypted files, which are packaged into a CDOC2 Container, to one or multiple Recipients

**Recipient**
: User, who wishes to decrypt the received CDOC2 Container and has control over necessary cryptographic key material

**Administrator**
: Person, who is managing CDOC2 Client Application for Users and is creating the configuration data for them

### System components as actors

**CDOC2 Client Application (Client)**
: Desktop or mobile application, which encrypts or decrypts CDOC2 Containers and is used by Users

**CDOC2 Capsule Server (CCS)**
: CCS mediates CDOC2 Server Capsules between Sender and Recipient. Sender's Client can upload a Server Capsule to one or multiple CCS servers. Recipient's Client can download Server Capsule from CCS server after authentication.

**CDOC2 Shares Server (CSS)**
: CDOC2 Shares Server mediates Key Shares between Sender and Recipient. Sender's Client splits Shares Capsule into multiple Key Shares and each Key Share is uploaded into a single Shares Server. Recipient's Client can download Key Shares from Shares Servers after authentication.

**Capsule**
: Data structure, which contains encryption scheme-specific information (encrypted symmetric keys, public keys, salt, server object references, ...)<br/>which Recipient can use to derive, establish or retrieve decryption keys for decrypting the CDOC2 Container. Capsule can either be a Server Capsule or a Container Capsule.

**Server Capsule**
: A Capsule that is mediated by a CDOC2 Capsule Server.

**Container Capsule**
: A Capsule that is created inside a CDOC2 container and is therefore not sent to a CDOC2 Capsule Server.

**Shares Capsule**
: A capsule that stores all Key Shares of a Recipient record.

**Key Share**
: Key Shares are created by splitting cryptographic material required for encrypting/decrypting CDOC2 document. These are stored inside Shares Capsules. Key Shares are always distributed among different Shares Servers and depending on the encryption scheme, all or a certain number of shares are needed to construct the original key value.

**LDAP-server**
: An application used for publishing public keys.

## Use cases for Recipients with hardware security tokens

These use cases are useful, when Sender knows that Recipient has specific hardware security token, and knows the public key certificate which correspond to the asymmetric cryptographic key pair on that security token. CC, which can be decrypted only with Recipient's security token, may be transmitted alongside with the CDOC2 Container itself with the encrypted payload, or with the help of CCS server.

### UC.Client.01 — Encrypt CDOC2 container for sending to Recipient with a security token

**Use Case Context**
: CDOC2 Client Application adds Sender's chosen files into the CDOC2 container and encrypts the container with CEK. CEK is encrypted with KEK, which is generated with key-agreement protocol between Sender and Recipient.

**Scope**
: CDOC2 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: Sender

**Preconditions**
: Client has a long-term access token from CDOC2 authentication server.

**Success Guarantees**

* CDOC2 container is saved into file system.
* A server capsule is sent for each Recipient to the CDOC2 capsule server.
* Client has received a transaction code for each server capsule.

**Main Success Scenario**

1. Sender chooses files to be included in CDOC2 container and specifies the target filename and path for CDOC2 container.
2. Sender enters identifiers for each Recipient.
3. Client creates a capsule for each Recipient.
4. Client displays a list of Capsule Servers to Sender.
5. Sender chooses a CDOC2 Capsule Server.
6. Client creates a TLS-connection with the chosen CDOC2 Capsule Server and receives the server's certificate.
7. Client verifies the server's certificate against the configuration.
8. Client forwards each Recipient's server capsule to the chosen CDOC2 Capsule Server. Client provides a server capsule expiration time from internal application configuration for each capsule. If a Recipient's certificate expiration time is earlier, it uses the certificate expiration time for that Recipient's capsule. Client receives a transaction code for each server capsule.
9. Client creates a container into file system in the chosen target path and adds a header.
10. Client verifies that the header does not exceed the size limit defined by the specification.
11. Client verifies technical file correctness and file name safety rules according to the specification. Client creates an archive, compresses it, encrypts the compressed archive with CEK and adds it to the container as payload.
12. Client saves the CDOC2 container and displays Sender a notification.

**Extensions**

1a. Sender chose to encrypt from the Windows Explorer / MacOS Finder / Linux folder explorer context dialog: "Encrypt with eID" and "Encrypt with password":

1. Client asks Sender for the container target name and path.
2. Sender specifies the target name and path.
3. Use case continues from step 2.

2a. Client chooses to search for Recipient information in LDAP directory:

1. Sender inserts Recipient personal code.
2. Client requests corresponding certificates and displays those.
3. Sender chooses certificate(s).
4. Use case continues from step 2.

2b. Certificate is not readable or is not in proper format:

1. Client displays Sender a notification.
2. Use case ends.

5a. Configuration has no CDOC2 capsule servers:

1. Client creates a container in the target path and adds a header with container capsules for each recipient.
2. Use case continues from step 11.

5b. Configuration has a default CDOC2 capsule server:

1. Use case continues from step 7.

6a. Sender chooses to not use the CDOC2 capsule server:

1. Client creates a container in the target path and adds a header with container capsules for each recipient.
2. Use case continues from step 11.

7a. TLS connection cannot be established:

1. Client displays Sender a notification.
2. Use case continues from step 5.

8a. Certificate validation against the configuration fails:

1. Client displays Sender a notification.
2. Use case continues from step 5.

8b. Client uses an organization-specific external configuration service:

1. Client first syncs default capsule expiration time from an organization-specific external service.
2. External configuration service provides a default capsule expiration time.
3. Client sends a server capsule using the appropriate API service to a CCS using the expiration time from external configuration or when a Recipient's certificate expiration time is earlier, it uses the certificate expiration time for that Recipient's capsule. Client receives a transaction code for each server capsule.
4. Use case continues from step 9.

8c. The expiration time provided by Client is longer than allowed in the CCS system configuration:

1. CCS returns Client an error message.
2. Client notifies Sender.
3. Use case ends.

9a. Forwarding capsules to a CDOC2 capsule server fails:

1. Client displays Sender a notification.
2. Use case ends.

9b. CDOC2 capsule server does not return a transaction identifier for each server capsule:

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
: CDOC2 Client Application (Client) decrypts the archive in the CDOC2 container provided by Recipient, using a server capsule from either CDOC2 Capsule Server or a container capsule from inside the container.

**Scope**
CDOC2 Client Application

**Use Case Level**
: User goal

**Primary Actor**
: Recipient

**Preconditions**

* Recipient's security token is connected.
* Client has a long-term access token from CDOC2 authentication server.

**Success Guarantees**

* Files from the CDOC2 container are decrypted.

**Main Success Scenario**

1. Recipient chooses the CDOC2 Container to be decrypted and specifies the target filename and path for the files.
2. Client verifies that the header does not exceed the size limit defined by the specification.
3. Client reads Recipient certificate from the security token.
4. Client verifies that the container has a record of the Recipient.
5. Client verifies that the Recipient record has a CDOC2 Capsule Server reference.
6. Client uses Recipient's eID means to authenticate to CCS.
7. Client sends the CDOC2 Capsule Server the transaction code from the container.
8. Client receives a capsule from the CDOC2 Capsule Server.
9. Client decrypts the encrypted archive in the CDOC2 container using the connected security token.
10. Continues with UC.Client.P.04 — Re-encrypt existing CDOC2 container for long-term storage.

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

5a. Recipient record does not contain a reference to a CDOC2 Capsule Server.

1. Client finds a container capsule from the Recipient record.
2. Use case continues from step 9.

6a. PIN 1 code is required:

1. Client asks user for a PIN 1 code.
2. Recipient enters the PIN code.
3. Client completes the authentication. Use case continues from step 7.

6b. Authentication fails:

1. Client displays user a notification.
2. Use case ends.

8a. No capsule returned from CDOC2 Capsule Server:

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
3. User specifies a target name and path in local file system.
4. User enters a password to be used for password-based cryptography and a password hint (short one-line text) to be displayed during decryption.
5. Client verifies that the password satisfies minimal requirements.
6. Client creates a container into file system in the chosen target path and adds a header.
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
3. Client asks User for the password to decrypt the container. Client shows a password hint based on the `KeyLabel` value set during encryption.
4. User enters the password.
5. Client verifies the password and decrypts the CDOC2 container.
6. Client asks user for the target location where to save the files.
7. User defines the target location.
8. Client unpacks the archive contents and saves it to the target location.

**Extensions**

2a. Header exceed the length limit according to the specification:

1. Client notifies the user.
2. Use case ends.

5a. Password is not correct:

1. Client notifies the user.
2. Use case continues from step 3.

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

* CDOC2 container was just decrypted.

**Success Guarantees**

* Files are re-encrypted.
* The re-encrypted container is saved locally.

**Main Success Scenario**

1. Client suggests Recipient to re-encrypt the decrypted container contents and displays multiple options for encryption.
2. Recipient chooses to re-encrypt and chooses to encrypt with a password.
3. Client asks Recipient to specify the target name and path.
4. Recipient specifies a target name and path in local file system.
5. Recipient enters a password to be used for password-based cryptography.
6. Client verifies that the password satisfies minimal requirements.
7. Client adds the files to an archive and creates a new CDOC2 container, which it saves to the target location.
8. Client notifies the Recipient.

**Extensions**

2a. Recipient chooses to re-encrypt using a security token:

1. Client verifies that the security token is connected.
2. Recipient specifies a target name and path in local file system and enters the security token password.
3. Client verifies the password. If password is not correct, the use case continues from the previous step.
4. Use case continues from step 7.

5a. Password does not meet minimum requirements.

1. Client notifies the Recipient with instructions to insert a new password.
2. Use case continues from step 3.

7a. Container creation or saving fails.

1. System notifies the Recipient.
2. Use case ends.

## Use cases supporting Recipients authenticating to multiple CDOC2 Shares Servers

These use cases are useful, when Sender knows that Recipient can use eID means that support authentication. These allow Sender to divide the key material into shares according to a [secret-sharing scheme](<https://en.wikipedia.org/wiki/Secret_sharing>) and distribute those among multiple independent CDOC2 Shares Servers (CSS). Recipient would need to authenticate to CSS servers and download all the shares in order to reconstruct the KEK from those.

### UC.Client.03 — Encrypt CDOC2 container using key shares

**Use Case Context**
: CDOC2 Client Application adds Sender's chosen files into the CDOC2 container and encrypts the container with CEK. CEK is encrypted with KEK. KEK is generated by Sender's Client and then divided into Key Shares. Each share is uploaded to different CDOC2 Shares Server.

**Scope**
: CDOC2 Client Application (Client)

**Use Case Level**
: User goal

**Primary Actor**
: Sender

**Success Guarantees**

* CDOC2 container is saved into file system.
* For each server capsule a share is sent to each CDOC2 Shares Server.
* Client has received a share identifier for each Key Share.

**Main Success Scenario**

1. Sender chooses files to be included in CDOC2 container and specifies the target filename and path for CDOC2 container.
2. Sender enters identifiers for each Recipient.
3. Client creates a capsule for each Recipient.
4. Client splits the capsules by creating a share for each CSS.
5. Client creates a TLS-connection with each CSS and receives the server certificates.
6. Client verifies the server certificates against the configuration.
7. Client forwards a share per Recipient together with their natural person identifier to each of the CDOC2 Shares Servers. Client receives a share identifier for each Key Share.
8. Client creates a container into file system in the chosen target path and adds a header.
9. Client verifies that the header does not exceed the size limit defined by the specification.
10. Client verifies technical file correctness and file name safety rules according to the specification. Client creates an archive, compresses it, encrypts the compressed archive with CEK and adds it to the container as payload.
11. Client saves the CDOC2 container and displays Sender a notification.

**Extensions**

1a. Sender chose to encrypt from the Windows Explorer / MacOS Finder / Linux folder explorer context dialog: "Encrypt with eID":

1. Client asks Sender for the container target name and path.
2. Sender specifies the target name and path.
3. Use case continues from step 2.

5a. TLS connection cannot be established:

1. Client displays Sender a notification.
2. Use case ends.

6a. Certificate validation against the configuration fails:

1. Client displays Sender a notification.
2. Use case ends.

6b. Client uses an organization-specific external configuration service:

1. Client first syncs default capsule expiration time from an organization-specific external service.
2. External configuration service provides a default capsule expiration time.
3. Client sends a Key Share to CSS API service using the expiration time from external configuration. Client receives a share identifier for each Key Share.
4. Use case continues from step 9.

6c. The expiration time provided by Client is longer than allowed in the CSS system configuration:

1. CSS returns Client an error message.
2. Client notifies Sender.
3. Use case ends.

7a. Sending capsules to a CDOC2 Shares Server fails:

1. Client displays Sender a notification.
2. Use case ends.

7b. CDOC2 Shares Server does not return a share identifier for each Key Share:

1. Client displays Sender a notification.
2. Use case ends.

8a. Header size is larger than allowed by the specification:

1. Client displays Sender a notification.
2. Use case ends.

9a. Files are not correct:

1. Client displays Sender a notification.
2. Use case ends.

### UC.Client.04 — Decrypt CDOC2 container using multiserver authentication

**Use Case Context**
: CDOC2 Client Application (Client) decrypts the archive in the CDOC2 container provided by Recipient, using the key material constructed from Key Shares obtained from multiple CDOC2 Shares Servers.

**Scope**
CDOC2 Client Application

**Use Case Level**
: User goal

**Primary Actor**
: Recipient

**Preconditions**

* The CDOC2 container has been encrypted using Key Shares and supports authentication-based decryption.

**Success Guarantees**

* Files from the CDOC2 container are decrypted.

**Main Success Scenario**

1. Recipient chooses the CDOC2 Container to be decrypted and specifies the target filename and path for the files.
2. Client verifies that the header does not exceed the size limit defined by the specification.
3. Recipient enters their personal identification number and chooses an eID authentication method.
4. Client finds Capsule Share matching to recipient identification number. Client reads share identifiers and their matching Shares Server URLs from Capsule Share and requests a nonce for each share identifier.
5. Client uses share identifier, Share Server URL and the nonce of each Key Share to generate an AuthenticationToken.
6. Client shows Recipient an authentication form with input options specific to the authentication service (e.g., phone number input field, QR code scanning option). The Recipient initiates authentication using one of the options.
7. Client initiates AuthenticationToken signing with authentication service.
8. Recipient completes the authentication using their eID means which also creates a signature on the authentication hash with authentication key pair.
9. Client reads Recipient certificate from the authentication response.
10. Client verifies that the container has a Recipient record with the same Recipient ID.
11. Client constructs a Share specific authentication ticket and uses it to authenticate itself to download the data of a Key Share.
12. Client receives data for all Key Shares.
13. Client combines the shares into a full secret and derives the KEK. Client uses the key material to decrypt the encrypted archive in the CDOC2 container and calculate HMAC to validate the integrity of the container.
14. Continues with UC.Client.P.04 — Re-encrypt existing CDOC2 container for long-term storage.

**Extensions**
2a. Header size is larger than allowed by the specification:

1. Client displays Recipient a notification.
2. Use case ends.

8a. Authentication is not successful:

1. Client notifies the user and offers to try again.
2. Use case continues from step 6.

10a. A Recipient record does not exist with the same personal identification number:

1. Client displays Recipient a notification.
2. Use case ends.

11a. Authentication validation fails:

1. Client displays Recipient a notification.
2. Use case ends.

12a. Client does not receive shares from each CSS because a request timed out:

1. Client displays user a notification and instructs trying again.
2. Use case continues from step 3.

12a. Client does not receive shares from each CSS because a share is missing or expired:

1. Client displays user a notification that the container cannot be decrypted anymore.
2. Use case ends.

13a. Decryption or HMAC validation fails:

1. Client displays user a notification that the container is corrupted.
2. Use case ends.

# CDOC2 Server Use Case Model

## Use cases where CDOC2 Capsule Servers hold the whole Server Capsule

These use cases are useful, when Sender knows that Recipient has specific hardware security token, and knows the public key certificate which correspond to the asymmetric cryptographic key pair on that security token. Server Capsule, which can be decrypted only with Recipient's security token, is stored on a single CCS server and must be accessed from there. CCS server enables expiration of access to these capsules.

### UC.KTS.01 Forward Capsules

**Context of Use**
: CDOC2 Client Application forwards Server Capsules to CDOC2 Capsule Server (CCS). Server Capsules contain a content encryption key encrypted for a particular Recipient, which is used for decrypting the archive in a CDOC2 container. Server Capsule is saved with an expiration time and a unique transaction ID is created and returned to the CDOC2 Client Application.

**Scope**
CDOC2 Capsule Server (CCS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC2 Client Application (Client)

**Success Guarantees**

* Server Capsules are saved with an expiration time.
* Share identifiers are forwarded to the CDOC2 Client Application.

**Main Success Scenario**

1. Client sends a server capsule using the appropriate API service to a CCS. Client provides a server capsule expiration time from internal application configuration for each capsule. If a Recipient's certificate expiration time is earlier, it uses the certificate expiration time for that Recipient's capsule.
2. CCS validates the server capsules against specification rules.
3. CCS generates a universally unique share identifier (UUID).
4. CCS saves the server capsule, validates the expiration time provided by Client based on its system configuration settings and sets the expiration time of the capsules.
5. CCS returns Client a share identifier for each capsule.

**Extensions**
1a. Client uses an organization-specific external configuration service:

1. Client first syncs default capsule expiration time from an organization-specific external service.
2. External provides a default capsule expiration time.
3. Client sends a server capsule using the appropriate API service to a CCS using the expiration time from external configuration or when a Recipient's certificate expiration time is earlier, it uses the certificate expiration time for that Recipient's capsule.
4. Use case continues from step 2.

2a. Server capsule exceeds the allowed length limit:

1. CCS returns Client an error message.
2. Use case ends.

4a. Client did not provide an expiration time:

1. CCS calculates the expiration time based on system configuration.
2. Use case continues from step 5.

4b. The expiration time provided by Client is longer than allowed in the CCS system configuration:

1. CCS returns Client an error message.
2. Use case ends.

### UC.KTS.02 Request Capsule

**Context of Use**
: CDOC2 Client Application requests a Server Capsule from CDOC2 Capsule Server. Server Capsule contains an encrypted content encryption key, used for decrypting the archive in a CDOC2 container. The Server Capsule is identified by public key in Recipient certificate and the transaction identifier provided by CDOC2 Client Application.

**Scope**
CDOC2 Capsule Server (CCS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC2 Client Application (Client)

**Preconditions**

* Recipient is authenticated (see UC.KTS.04 Authenticate Recipient).

**Success guarantees**

* Server Capsule is forwarded to CDOC2 Client Application.

**Main Success Scenario**

1. Client requests a Server Capsule using the appropriate API service, providing a transaction identifier as input.
2. CCS validates the transaction identifier against specification rules.
3. CCS finds the correct Server Capsule using the transaction identifier and validates that the Recipient public key matches with the one in the Capsule.
4. CCS sends the Client the Capsule.

**Extensions**
2a. transaction identifier is too long:

1. CCS returns Client an error message.
2. Use case ends.

3a. Capsule was not found:

1. CCS returns Client an error message.
2. Use case ends.

3b. Recipient public key does not match the one in the Capsule:

1. CCS returns Client an error message.
2. Use case ends.

### UC.KTS.03 Delete Server Capsules

**Context of Use**
: System timer deletes expired Server Capsules.

**Scope**
CDOC2 Capsule Server (CCS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC2 Client Application (Client)

**Success guarantees**

* Expired Server Capsules are removed from the storing CCS.

**Trigger**

* System timer schedules and initiates the deletion of expired Server Capsules.

**Main Success Scenario**

1. CCS identifies expired Server Capsules.
2. CCS deletes expired Server Capsules.

**Extensions**

1a. No expired Server Capsules found.

1. Use case ends.

### UC.KTS.04 Authenticate Recipient

**Context of Use**
: CDOC2 Client Application (Client) establishes a TLS-connection to CDOC2 Capsule Server and forwards Recipient certificate.

**Scope**
CDOC2 Capsule Server (CCS)

**Use Case Level**
: Subfunction

**Primary Actor**
: CDOC2 Client Application (Client)

**Preconditions**
: Client has a long-term access token from CDOC2 authentication server.

**Success guarantees**

* TLS-connection is established.
* Recipient certificate exists and is received.

**Main Success Scenario**

1. Client initiates a TLS-connection and forwards Recipient certificate.
2. CCS verifies certificate validity using an OCSP service.
3. CCS establishes the TLS connection.

**Extensions**

2a. Recipient certificate is not valid:

1. CCS replies to the Client with an error message.
2. Use case ends.

## Use cases with multiple CDOC2 Shares Servers holding shares of capsules

These use cases are useful, when Sender knows that Recipient can use some eID means for authenticating themselves, but cannot use eID means that support encryption/decryption. These allow Sender to divide the key material into Key Shares according to a [secret-sharing scheme](<https://en.wikipedia.org/wiki/Secret_sharing>) and distribute those among multiple independent CSSs . Recipient would need to authenticate to CSS servers and download all the shares in order to reconstruct the KEK from those.

### UC.KTS.06 Forward Capsule Shares

**Context of Use**
: CDOC2 Client Application forwards Key Shares of all Shares Capsules to CDOC2 Shares Servers (CSS). This use case assumes the n-of-n encryption scheme where the number of shares per capsule is equal to the number of receiving CSS servers. All the shares have to be combined in order to construct a capsule that contains a content encryption key (CEK) encrypted for a particular Recipient. Key Shares are saved, and a unique share identifier is created and returned to the CDOC2 Client Application from each CSS.

**Scope**
CDOC2 Shares Server (CSS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC2 Client Application (Client)

**Success Guarantees**

* Key Shares of all Shares Capsules are saved with Recipient natural person identifier to all receiving CSS servers.
* Share identifiers are forwarded to the CDOC2 Client Application.

**Main Success Scenario**

1. Client sends Key Shares of each Shares Capsule to appropriate CSS servers using an API service. The shares are matched to CSS servers by server IDs. Client provides a natural person identifier corresponding to the Recipient.
2. Each CSS validates the Key Shares against specification rules.
3. Each CSS generates a share identifier.
4. Each CSS saves the Key Share.
5. Each CSS returns Client a share identifier for each Key Share.

**Extensions**
2a. Shares capsule exceeds the allowed length limit:

1. CSS returns Client an error message.
2. Use case ends.

### UC.KTS.07 Request Capsule Shares

**Context of Use**
: CDOC2 Client Application requests Key Shares from all CDOC2 Shares Servers. The Key Share is identified by the share identifier provided by CDOC2 Client Application, the CSS server ID and the Recipient identification (ETSI semantics identifier) that can be matched to Recipient public key.

**Scope**
CDOC2 Shares Server (CSS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC2 Client Application (Client)

**Success guarantees**

* Recipient is authenticated.
* Key Shares from all CDOC2 Shares Servers are forwarded to CDOC2 Client Application.

**Main Success Scenario**

1. Client requests a nonce from each CSS API service, providing the share identifier as input.
2. Client calculates an authentication hash.
3. Client asks the Recipient to authenticate.
4. Recipient signs the authentication token and Client receives Recipient public key that matches the Recipient identification used in the accessed Shares Capsule.
5. Client constructs server-specific authentication tickets and sends one to each CSS.
6. Each CSS validates the received authentication ticket, which includes validating the ticket type, nonce, signature, key pair and public keys.
7. CSS returns the Key Share.

**Extensions**

1a. Capsule share was not found:

1. CSS returns Client an error message.
2. Use case ends.

3a. Client is unable to get the Recipient to sign an authentication hash:

1. Use case ends.

6a. Validation by a CSS finds an error:

1. CSS returns Client an error message.
2. Use case ends.
