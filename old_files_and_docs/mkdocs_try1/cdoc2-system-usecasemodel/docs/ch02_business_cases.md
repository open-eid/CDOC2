---
title: 2. Business case model
---

# Business case model

## Stakeholders

## BUC.01 Setup CDOC2 infrastructure

New thing, need to write

## BUC.02 Add CDOC2 key transmission server

Existing content from "CDOC2 kasutusmallimudel", Section 2.21 "BUC.01 Lisa Võtmeedastusserver"

## Additional BUCs?

### BUC.03 Encrypt CDOC2 Container

**Use Case Context**
: CDOC2 Client Application (Client) helps Sender to choose Recipients and best encryption scheme for them. No support for secret-sharing CKCs yet.

**Main Success Scenario**

1. Sender chooses files to be included in CDOC2 Container and specifies the target filename for CDOC2 Container
1. Client generates FMK, CEK, encrypts files with CEK, adds them to CDOC2 Container
1. Sender specifies, who is able to decrypt the CDOC2 Container, by choosing one or multiple options:
   1. Sender specifies national identity code for a Recipient
   1. Sender specifies the password for the encryption
   1. Sender specifies the shared symmetric key for the encryption
1. Client searches for Recipients in public LDAP directory and finds all possible ID-card and Mobile-ID certificates
1. In case Recipient has a valid ID-card certificate:
    1. Client uses CDOC2 encryption scheme SC01 or SC02 to create CKC, which contains encrypted KEK. CKC can be decrypted with ID-card key pair.
    1. Client queues CKC to be included in CDOC2 Container
1. In case Recipient has a valid Mobile-ID certificate:
    1. Client uses CDOC2 encryption scheme SC06 to create CKC, which contains plaintext KEK
    1. Client queues CKC to be uploaded to CKCTS server
1. In case Recipient has Smart-ID account (assuming we can somehow detect the Smart-ID account status):
    1. Client uses CDOC2 encryption scheme SC06 to create CKC, which contains plaintext KEK
    1. Client queues CKC to be uploaded to CKCTS server
1. Client adds all required CKCs into the CDOC2 Container:
   1. Client adds CKC for each Recipient with ID-card certificate into the CDOC2 Container
   1. If Sender specified password, Client adds CKC for password-based encryption key into the CDOC2 Container
   1. If Sender specified shared symmetric key, Client adds CKC for shared symmetric key into the CDOC2 Container
1. Client verifies technical requirements (size of CDOC2 Container header, file correctness, ...)
1. Client uploads every queued CKC to CKCTS server
1. Client saves CDOC2 Container and notifies Sender

### BUC.04 Encrypt CDOC2 Container with secret-sharing scheme

**Use Case Context**
: CDOC2 Client Application (Client) helps Sender to choose Recipients and best encryption scheme for them. This UC supports secret-sharing.

**Main Success Scenario**

1. Sender chooses files to be included in CDOC2 Container and specifies the target filename for CDOC2 Container
1. Client generates FMK, CEK, encrypts files with CEK, adds them to CDOC2 Container
1. Sender specifies, who is able to decrypt the CDOC2 Container, by choosing one or multiple options:
   1. Sender specifies national identity code for a Recipient
   1. Sender specifies the password for the encryption
   1. Sender specifies the shared symmetric key for the encryption
1. Client searches for Recipients in public LDAP directory and finds all possible ID-card and Mobile-ID certificates
1. In case Recipient has a valid ID-card certificate:
    1. Client uses CDOC2 encryption scheme SC01 or SC02 to create CKC, which contains encrypted KEK. CKC can be decrypted with ID-card key pair.
    1. Client queues CKC to be included in CDOC2 Container
1. In case Recipient has a valid Mobile-ID certificate:
    1. Client uses CDOC2 encryption scheme SC06 to create CKC, which contains plaintext KEK
    1. Client queues CKC to be uploaded to CKCTS servers in a secret-sharing scheme
1. In case Recipient has Smart-ID account (assuming we can somehow detect the Smart-ID account status):
    1. Client uses CDOC2 encryption scheme SC06 to create CKC, which contains plaintext KEK
    1. Client queues CKC to be uploaded to CKCTS servers in a secret-sharing scheme
1. Client adds all required CKCs into the CDOC2 Container:
   1. Client adds CKC for each Recipient with ID-card certificate into the CDOC2 Container
   1. If Sender specified password, Client adds CKC for password-based encryption key into the CDOC2 Container
   1. If Sender specified shared symmetric key, Client adds CKC for shared symmetric key into the CDOC2 Container
1. Client verifies technical requirements (size of CDOC2 Container header, file correctness, ...)
1. Client executes secret-sharing scheme (to be specified) and splits every queued CKC to $n$ shares and uploads them to CKTS servers, which are specified in the configuration file.
1. Client saves CDOC2 Container and notifies Sender

### BUC.05 Decrypt CDOC2 Container

**Use Case Context**
: CDOC2 Client Application (Client) helps Recipient to decrypt the CDOC2 Container.

**Main Success Scenario**

1. Recipient opens CDOC2 Container with Client.
1. Client parses CDOC2 Container header and finds out how to decrypt or how to download the CKC for the Container:
   1. If CKC is encrypted with ID-card key pair, Client asks Receiver to insert ID-card and decrypts CKC with ID-card.
   1. If CKC is encrypted with password, Client asks Receiver to enter the password.
   1. If CKC is encrypted with symmetric pre-shared key, Client asks Receiver to enter the symmetric key.
   1. If CKC is available from CKTS servers, Client asks Receiver to sign authentication ticket for CKTS servers.
      1. If KEK is secret-shared between multiple CKCs uploaded to different CKTS servers, Client will download all CKCs from available CKTS servers and will reconstruct the KEK.
1. Client will use KEK to decrypt the CEK of CDOC2 Container.

### Questions and notes

#### Not using TARA for CKTS authentication

Do I remember correctly. At the moment, we don't plan to use TARA for CKTS authentication. We ask Recipient to sign the special  authentication token with whatever authentication means Recipient has available (ID-card, Mobile-ID, Smart-ID). With Mobile-ID and Smart-ID authentication services, we will use "MID/SID proxy" to start authentication transactions.

We only use TARA for authenticating End-User and for issuing long-term OAuth2 access token for accessing the "MID/SID proxy".

#### LDAP search and Smart-ID

1. LDAP search for ID-card and Mobile-ID certificates

```bash
$ LDAPTLS_REQCERT=allow ldapsearch -L -v -H ldaps://esteid.ldap.sk.ee/ -x -b "c=EE" "(serialNumber=PNOEE-37807156011)"
```

2. LDAP search for Smart-ID - not possible?

#### Do we always use CKCTS servers anyway?

Let's assume that Recipient has multiple eID means available (ID-card + MID or SID). Does this mean that:

1. we always need to send one CKC with plaintext KEK to CKCTS servers anyway, so that Recipient could authenticate to CKCTS servers and download it. Recipient could authenticate with ID-card or Mobile-ID or Smart-ID.
2. do we also send one CKC with KEK encrypted to ID-card key pair to CKCTS servers as well?
3. do we also include one CKC with KEK encrypted to ID-card key pair to CDOC2 Container, for off-line decryption as well?

Does this mean that we should aim to use CKCTS servers every time anyway, to upload "CKC with plaintext KEK"?

#### Always include CKC for ID-card inside CDOC2 Container?

In BUC.04 step 8 - "In case Recipient has a valid ID-card certificate". In case the Client configuration file includes CKCTS servers, does this mean that:

1. we always create one CKC (associated with ID-card key pair) to be sent to CKCTS server as well, even in the case one CKC is added to CDOC2 Capsule as well?
2. we always create one CKC to be added to CDOC2 Capsule anyway, even in the case one CKC (associated with ID-card key pair) is uploaded to CKCTS server as well?

#### Authentication/Authorization scheme to CKTS servers

At the moment, we have custom authentication/authorization protocol for CKTS servers planned, where we ask Recipient to sign the special CKTS authentication token with whatever authentication means Recipient has available (ID-card, Mobile-ID, Smart-ID). Client then combines authentication token into special/unique authentication tickets, which will be presented to CKTS servers. CKTS servers are not able to replay the authentication ticket, because they are unique and not accepted by other CKTS servers. 

It might be possible that we can use standard-compliant OAuth2 authorization protocol. CKTS servers are "resource servers", some component will issue OAuth2 Bearer Token to Client and Client presents the token to CKTS server. To prevent one CKTS server to replay bearer token to another CKTS server, we could use OAuth2 DPOP security measure (https://oauth.net/2/dpop/), which binds the bearer token with cryptographic key pair.

Work-in-progress.

#### SC05: Direct encryption scheme for recipient with pre-shared symmetric key ?

"3.5 Sümmeetrilise võtmega skeem"

What is the planned usage for encryption scheme with pre-shared symmetric key?