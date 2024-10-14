---
title: 3. Use Case Model
---

# CDOC2 Client Application Use Case Model

CDOC2 Client Application is an abstract component in the CDOC2 System. CDOC2 Client Applications help users to encrypt files to CDOC2 Container, decrypt received CDOC2 Containers. Specific examples of CDOC2 Client Applications include:

* DigiDoc4 desktop application for Windows, MacOS and Linux operating systems (<https://open-eid.github.io/#desktop-applications>, <https://www.id.ee/en/rubriik/digidoc4-client/>, <https://github.com/open-eid/DigiDoc4-Client>)
* DigiDoc4 mobile application for Android and IOS operating systems (<https://open-eid.github.io/#mobile-applications>)
* CDOC2 Client CLI Application

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

**Capsule**
: Data structure, which contains encryption scheme-specific information (encrypted symmetric keys, public keys, salt, server object references, ...)<br/>which Recipient can use to derive, establish or retrieve decryption keys for decrypting the CDOC2 Container. Capsule can either be a Server Capsule or a Container Capsule.

**Server Capsule**
: A Capsule that is mediated by a CDOC2 Capsule Server.

**Container Capsule**
: A Capsule that is created inside a CDOC2 container and is therefore not sent to a CDOC2 Capsule Server.

**LDAP-server**
: An application used for publishing public keys.

## Use cases for Recipients with hardware security tokens

These use cases are useful, when Sender knows that Recipient has specific hardware security token, and knows the public key certificate which correspond to the asymmetric cryptographic key pair on that security token. KC, which can be decrypted only with Recipient's security token, may be transmitted alongside with the CDOC2 Container itself with the encrypted payload, or with the help of CCS server.

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

1. Sender inserts Recipient personal code (natural person) or name / business registry code (juridical person).
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

1. Client first syncs default capsule expiration time from an organization-specific external service using a long-term authentication token.
2. External configuration service provides a default capsule expiration time.
3. Client sends a server capsule using the appropriate API service to a CCS using the expiration time from external configuration or when a Recipient's certificate expiration time is earlier, it uses the certificate expiration time for that Recipient's capsule. Client receives a transaction code for each server capsule.
4. Use case continues from step 9.

8c. The expiration time provided by Client is longer than allowed in the CCS system configuration:

1. CCS returns Client a error message.
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
4. User enters a password to be used for password-based cryptography.
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
8. Client asks Recipient whether to delete the server capsule that was used during the previous decryption process. The purpose is to make it impossible that anybody could ever again decrypt the original message.
9. Recipient chooses to delete the server capsule.
10. Client, still having access to the original container decrypted container, reads again the recipient record from it and makes a request to CCS to delete the server capsule by providing the same transaction code.
11. CCS deletes the server capsule and replies with a confirmation response.
12. Client notifies the Recipient.

**Extensions**

2a. Recipient chooses to re-encrypt using a security token:

1. Client verifies that the security token is connected.
2. Recipient specifies a target name and path in local file system and enters the security token password.
3. Client verifies the password. If password is not correct, the use case continues from the previous step.
4. Use case continues from step 7.

2a. Recipient chooses to re-encrypt using eID means (e.g., Smart-ID or Mobile-ID):

1. Continues use case UC.Client.03 — Encrypt CDOC2 container using Server Capsules shares.

5a. Password does not meet minimum requirements.

1. Client notifies the Recipient with instructions to insert a new password.
2. Use case continues from step 3.

7a. Container creation or saving fails.

1. System notifies the Recipient.
2. Use case ends.

9a. Recipient does not want to delete the server capsule:

1. Use case ends.

10a. Recipient's authentication has expired:

1. Client completes the use case UC.KTS.04 Authenticate Recipient.
2. Use case resumes from step 10.

11a. No non-expired Server Capsules found with the corresponding transaction ID:

1. Server returns an error message.
2. Client assumes that the server capsule does no longer exist and notifies the Recipient.
3. Use case ends.

11a. Establishing a connection to the CCS fails:

1. Client notifies the Recipient.
2. Recipient chooses whether to try again. If yes then use case continues from step number 3. Otherwise, use case ends.

## Use cases supporting Recipients authenticating to multiple CDOC2 Capsule Servers

These use cases are useful, when Sender knows that Recipient can use eID means that support authentication. These allow Sender to divide the key material into shares according to a [secret-sharing scheme](<https://en.wikipedia.org/wiki/Secret_sharing>) and distribute those among multiple independent CDOC2 Capsule Servers. Recipient would need to authenticate to CCS servers and download all the shares in order to reconstruct the KEK from those.

### UC.Client.03 — Encrypt CDOC2 container using Server Capsules shares 

**Use Case Context**
: CDOC2 Client Application adds Sender's chosen files into the CDOC2 container and encrypts the container with CEK. CEK is encrypted with KEK, which is generated with key-agreement protocol between Sender and Recipient. Key material is divided into shares and uploaded to multiple CCS-s.

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
* For each server capsule a share is sent to each CDOC2 capsule server.
* Client has received a transaction code for each server capsule share.

**Main Success Scenario**

1. Sender chooses files to be included in CDOC2 container and specifies the target filename and path for CDOC2 container.
2. Sender enters identifiers for each Recipient. 
3. Client creates a capsule for each Recipient.
4. Client splits the capsule into the same number of shares that there are configured CDOC2 Capsule Servers. 
5. Client creates a TLS-connection with each CCS and receives the server certificates.
6. Client verifies the server certificates against the configuration.
7. Client forwards each Recipient's server capsule share and Recipient's natural person identifier to each of the CDOC2 Capsule Servers. Client provides a server capsule expiration time from internal application configuration for each capsule share. If a Recipient's certificate expiration time is earlier, it uses the certificate expiration time for that Recipient's capsule share. Client receives a transaction code for each server capsule share.
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

1. Sender inserts Recipient personal code (natural person) or name / business registry code (juridical person).
2. Client requests corresponding certificates and displays those.
3. Sender chooses certificate(s).
4. Use case continues from step 2.

2b. Certificate is not readable or is not in proper format:

1. Client displays Sender a notification.
2. Use case ends.

5a. TLS connection cannot be established:

1. Client displays Sender a notification.
2. Use case ends.

6a. Certificate validation against the configuration fails:

1. Client displays Sender a notification.
2. Use case ends.

6b. Client uses an organization-specific external configuration service:

1. Client first syncs default capsule expiration time from an organization-specific external service using a long-term authentication token.
2. External configuration service provides a default capsule expiration time.
3. Client sends a server capsule share using the appropriate API service to a CCS using the expiration time from external configuration or when a Recipient's certificate expiration time is earlier, it uses the certificate expiration time for that Recipient's capsule share. Client receives a transaction code for each server capsule share.
4. Use case continues from step 9.

6c. The expiration time provided by Client is longer than allowed in the CCS system configuration:

1. CCS returns Client an error message.
2. Client notifies Sender.
3. Use case ends.

7a. Forwarding capsules to a CDOC2 capsule server fails:

1. Client displays Sender a notification.
2. Use case ends.

7b. CDOC2 capsule server does not return a transaction identifier for each server capsule share:

1. Client displays Sender a notification.
2. Use case ends.

8a. Header size is larger than allowed by the specification:

1. Client displays Sender a notification.
2. Use case ends.

9a. Files are not correct:

1. Client displays Sender a notification.
2. Use case ends.

### UC.Client.04 — Decrypt CDOC2 Container by authenticating on multiple CDOC2 Capsule Servers

**Use Case Context**
: CDOC2 Client Application (Client) decrypts the archive in the CDOC2 container provided by Recipient, using a server capsule constructed from shares obtained from multiple CDOC2 Capsule Servers.

**Scope**
CDOC2 Client Application

**Use Case Level**
: User goal

**Primary Actor**
: Recipient

**Preconditions**

* Client has a long-term access token from CDOC2 authentication server.

**Success Guarantees**

* Files from the CDOC2 container are decrypted.

**Main Success Scenario**

1. Recipient chooses the CDOC2 Container to be decrypted and specifies the target filename and path for the files.
2. Client verifies that the header does not exceed the size limit defined by the specification.
3. Recipient enters their personal identification number and chooses an eID authentication method that corresponds to a Recipient record in the header.
4. Client sends the correct CDOC2 Capsule Server the transaction code for each server capsule share and receives a nonce from each server.
5. Client uses the nonce to calculate an authentication hash for each CSS.
6. Client forwards Recipient to the authentication page. Recipient initiates authentication.
7. Authentication proxy (a server component that acts a responsible party) initiates authentication with the authentication provider and provides the authentication hash as a request parameter to be signed during authentication.
**_NOTE:_** In case of Smart-ID, using the document number RP API endpoint with the correct document number would ensure that the correct Smart-ID account will be used. The document number could be from `KeyLabel`.
8. Recipient completes the authentication using their eID means which also creates a signature on the authentication hash with authentication key pair.
9. Client reads Recipient certificate from the authentication response.
10. Client verifies that the container has a record with the same Recipient certificate.
11. Client constructs server-specific authentication tickets and sends one to each CSS. Each CSS validates the received authentication ticket.
12. Client receives the server capsule share from each CCS. 
13. Client combines the shares into a full secret and derives the KEK. Client uses the key material to decrypt the encrypted archive in the CDOC2 container and calculate HMAC to validate the integrity of the container.
14. Continues with UC.Client.P.04 — Re-encrypt existing CDOC2 container for long-term storage.

**Extensions**
2a. Header size is larger than allowed by the specification:

1. Client displays Recipient a notification.
2. Use case ends.

8a. Authentication is not successful:

1. Client notifies the user and offers to try again.
2. Use case continues from step 6.

10a. Recipient record does not contain the same certificate:

1. Client displays Recipient a notification.
2. Use case ends.

11a. Authentication ticket validation fails because of expired nonce:

1. Client displays Recipient a notification and instructs Recipient to try again.
2. Use case continues from step 3.

11a. Authentication validation fails for other reasons:

1. Client displays Recipient a notification.
2. Use case ends.

12a. Client does not receive shares from each CCS because of network reasons:

1. Client displays user a notification and instructs trying again.
2. Use case continues from step 3.

12a. Client does not receive shares from each CCS because a share is missing or expired:

1. Client displays user a notification that the container cannot be decrypted anymore.
2. Use case ends.

13a. Decryption or HMAC validation fails:

1. Client displays user a notification that the container is corrupted.
2. Use case ends.

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

# CDOC2 Capsule Server Use Case Model

## Use cases where CDOC2 Capsule Servers hold the whole Server Capsule

These use cases are useful, when Sender knows that Recipient has specific hardware security token, and knows the public key certificate which correspond to the asymmetric cryptographic key pair on that security token. Server Capsule, which can be decrypted only with Recipient's security token, is stored on a single CCS server and must be accessed from there which enables expiration.

### UC.KTS.01 Forward Capsules

**Context of Use**
: CDOC2 Client Application forwards Server Capsules to CDOC2 Capsule Server (CCS), which contain a content encryption key encrypted for a particular Recipient, which is used for decrypting the archive in CDOC2 container. Server Capsule is saved with an expiration time and a unique transaction code is created and returned to the CDOC2 Client Application.

**Scope**
CDOC2 Capsule Server (CCS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC2 Client Application (Client)

**Success Guarantees**

* Server Capsules are saved with an expiration time.
* Transaction codes are forwarded to the CDOC2 Client Application.

**Main Success Scenario**

1. Client sends server capsules using the appropriate API service to a CCS. Client provides a server capsule expiration time from internal application configuration for each capsule. If a Recipient's certificate expiration time is earlier, it uses the certificate expiration time for that Recipient's capsule.
2. CCS validates the server capsules against specification rules.
3. CCS generates a universally unique transaction code (UUID).
4. CCS saves the server capsule, validates the expiration time provided by Client based on its system configuration settings and sets the expiration time of the capsules.
5. CCS returns Client a transaction code for each capsule.

**Extensions**
1a. Client uses an organization-specific external configuration service:

1. Client first syncs default capsule expiration time from an organization-specific external service using a long-term authentication token.
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
: CDOC2 Client Application requests a Server Capsule from CDOC2 Capsule Server, which contains an encrypted content encryption key, used for decrypting the archive in CDOC2 container. The Server Capsule is identified by public key in Recipient certificate and the transaction code provided by CDOC2 Client Application.

**Scope**
CDOC2 Capsule Server (CCS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC2 Client Application (Client)

**Preconditions**

* Recipient is authenticated.
* Client has a long-term access token from CDOC2 authentication server.

**Success guarantees**

* Server Capsule is forwarded to CDOC2 Client Application.

**Main Success Scenario**

1. Client requests a Server Capsule using the appropriate API service, providing a transaction code as input.
2. CCS validates the transaction code against specification rules.
3. CCS finds the correct Server Capsule using the transaction code and validates that the Recipient public key matches with the one in the Capsule.
4. CCS sends the Client the Capsule.

**Extensions**
2a. Transaction code is too long:

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

### UC.KTS.05 Request To Delete Server Capsule

**Context of Use**
: Client requests the CSS to delete a server capsule.

**Scope**
CDOC2 Capsule Server (CCS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC2 Client Application (Client)

**Success guarantees**

* Server capsule is removed from the storage of the CCS.

**Preconditions**

* Recipient has received a server capsule from a CCS.
* Recipient has completed the re-encryption flow in the Client.

**Main Success Scenario**

1. Client asks Recipient whether to delete server capsule and thus make it impossible that anybody could ever again decrypt the original message.
2. Recipient chooses to delete the server capsule.
3. Client makes request to CCS to delete the server capsule by providing the same transaction code as when originally requesting the capsule.
4. CCS deletes the server capsule.

**Extensions**
2a. Recipient does not want to delete the server capsule:

1. Use case ends.

3a. Recipient's authentication has expired:

1. Client completes the use case UC.KTS.04 Authenticate Recipient.
2. Use case resumes from step 3.

4a. No non-expired Server Capsules found with the corresponding transaction ID:

1. Server returns an error message.
2. Client assumes that the server capsule does no longer exist and notifies the Recipient.
3. Use case ends.

4a. Establishing a connection to the CCS fails:

1. Client notifies the Recipient.
2. Recipient chooses whether to try again. If yes then use case continues from step number 3. Otherwise, use case ends.

## Use cases with multiple CDOC2 Capsule Servers holding shares of capsules

These use cases are useful, when Sender knows that Recipient can use eID means that support authentication. These allow Sender to divide the key material into shares according to a [secret-sharing scheme](<https://en.wikipedia.org/wiki/Secret_sharing>) and distribute those among multiple independent CCS-s. Recipient would need to authenticate to CCS servers and download all the shares in order to reconstruct the KEK from those.

### UC.KTS.05 Forward Capsule Shares

**Context of Use**
: CDOC2 Client Application forwards shares of all Server Capsules to CDOC2 Capsule Servers (CCS). This use case assumes the n-of-n encryption scheme where the number of shares per capsule is equal to the number of receiving CCS servers. All shares have to be combined in order to construct a capsule that contains a content encryption key (CEK) encrypted for a particular Recipient. Server Capsule shares are saved with an expiration time and a unique transaction code is created and returned to the CDOC2 Client Application from each CCS.

**Scope**
CDOC2 Capsule Server (CCS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC2 Client Application (Client)

**Success Guarantees**

* Shares of all Server Capsules are saved with Recipient natural person identifier and an expiration time to all receiving CCS servers.
* Transaction codes are forwarded to the CDOC2 Client Application.

**Main Success Scenario**

1. Client sends a share per capsule to each CCS server using the appropriate API service. Shares are matched to CCS servers by server IDs. Client provides a natural person identifier corresponding to the Recipient. Client provides a server capsule expiration time from internal application configuration for each capsule share. If a Recipient's certificate expiration time is earlier, it uses the certificate expiration time for that Recipient's capsule.
2. Each CCS validates the server capsule shares against specification rules.
3. Each CCS generates a universally unique transaction code (UUID).
4. Each CCS saves the server capsule share, validates the expiration time provided by Client based on its system configuration settings and sets the expiration time of the capsules.
5. Each CCS returns Client a transaction code for each capsule.

**Extensions**
1a. Client uses an organization-specific external configuration service:

1. Client first syncs default capsule expiration time from an organization-specific external service using a long-term authentication token.
2. External provides a default capsule expiration time.
3. Client sends a server capsule share using the appropriate API service to all CCS-s using the expiration time from external configuration or when a Recipient's certificate expiration time is earlier, it uses the certificate expiration time for that Recipient's capsule share.
4. Use case continues from step 2.

2a. Server capsule exceeds the allowed length limit:

1. CCS returns Client an error message.
2. Use case ends.

4a. Client did not provide an expiration time:

1. CCS calculates the expiration time based on system configuration.
2. Use case continues from step 5.

4b. The expiration time provided by Client is longer than allowed in CCS system configuration:

1. CCS returns Client an error message.
2. Use case ends.

### UC.KTS.06 Request Capsule Shares

**Context of Use**
: CDOC2 Client Application requests Server Capsule shares from all CDOC2 Capsule Servers. The Server Capsule share is identified by the transaction code provided by CDOC2 Client Application, the CSS server ID and the public key in Recipient certificate.

**Scope**
CDOC2 Capsule Server (CCS)

**Use Case Level**
: User goal

**Primary Actor**
: CDOC2 Client Application (Client)

**Preconditions**

* Recipient is authenticated.
* Client has a long-term access token from CDOC2 authentication server.

**Success guarantees**

* Server Capsule shares from all CDOC2 Capsule Servers are forwarded to CDOC2 Client Application.

**Main Success Scenario**

1. Client requests a nonce from each CSS using the appropriate API service, providing the share transaction code as input.
2. Client uses the nonce to calculate an authentication hash for each CSS.
3. Client redirects the Recipient to authenticate with the authentication method corresponding to a Recipient certificate or other Recipient information in the CDOC2 container. Recipient performs authentication and creates a signature on the authentication hash with authentication key pair.
4. Client constructs server-specific authentication tickets and sends one to each CSS.
5. Each CSS validates the received authentication ticket, which includes validating the ticket type, nonce, signature, key pair and public keys.
6. CSS returns the server capsule share. 

**Extensions**

1a. Capsule share was not found:

1. CCS returns Client an error message.
2. Use case ends.

3a. Client is unable to get the Recipient to sign an authentication hash:

1. Use case ends.

5a. Validation by a CCS finds an error:

1. CCS returns Client an error message.
2. Use case ends.