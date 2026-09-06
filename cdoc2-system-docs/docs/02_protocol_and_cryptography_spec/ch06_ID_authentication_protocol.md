---
title: 8. Client authentication protocol
---

# Client authentication protocol

This section describes a protocol and data formats for authenticating to multiple CSS servers (cdoc2-shares-servers) in order to download every `KeySharesCapsule` from them.

> **Note:** This section applies to SiD/MiD only.

## Authentication protocol requirements

1. Multiple CSSs hold Capsules, which all need to be downloaded by Client.
2. Client needs to authenticate to multiple CSSs, in order to download all Capsules.
3. Client should only need to create one signature with its authentication means (Mobile-ID, Smart-ID) for authentication.
4. CSS must not be able to replay the authentication token to another CSS.

## Non-suitable alternatives

Before designing a custom authentication protocol, we should make sure that we cannot re-use existing protocols. Existing protocols may already have proven security properties, and they might be well-supported by existing software libraries.

For example, traditionally, authentication and authorization processes are handled by OpenID Connect and OAuth2 protocols. They are well studied and robust. However, if we try to apply them to our situation and try to map mandatory roles from OpenID Connect and OAuth2 ecosystems to our components (Client, CSSs), the situation becomes cumbersome.

First, the requirement that Client needs to "login" to multiple servers with single use of user's eID means is difficult to achieve. This is usually handled by a single-sign-on service. There's such a service, called GovSSO (<https://e-gov.github.io/GOVSSO/TechnicalSpecification>), but it is more oriented towards web applications, and it is using a generic OpenID Connect protocol without binding the issued `id_tokens` with user's authentication signatures. In case CSS would be accepting such `id_tokens`, there's no cryptographic proof that authentication of the user has actually taken place and that the user's eID means was used. That would mean that the security of such central single-sign-on provider would be critical and in case the security of GovSSO would be breached, it would be able to download every `KeySharesCapsule` on behalf of any user.

Additionally, if we would be using OAuth2 authorization protocols, we would be using OAuth2 "bearer" tokens. This would mean that CSS server can re-use the token and replay it to another CSS server. It might be possible to overcome the threat of token replay with protocols like "OAuth2 Certificate-Bound Access Tokens" (<https://datatracker.ietf.org/doc/html/rfc8705>) and "OAuth2 Demonstrating Proof of Possession" (<https://www.rfc-editor.org/rfc/rfc9449>), but that would require us to create yet another central trusted component which would hand out those access tokens. That kind of component would be a single source of failure and in case the security of such component would be breached, the attacker would be able to download every `KeySharesCapsule` on behalf of any user.

Therefore, introducing additional trusted components to the CDOC2 ecosystem is not desirable at the moment and traditional authentication protocols are not suitable. More tailored approach would be needed to come up with an authentication protocol, that would satisfy all requirements and would depend only on the eID authentication means or eID trust service providers.

## Overview of the generic authentication protocol

In the generalized form, the authentication protocol to access Capsule information at CSS servers, can be explained with the following sequence diagrams below.

This is just an abstract overview of the authentication protocol. In following sections, we describe what kind of data is used as the authentication data, how signing function of eID means is used and how only a minimal set of authentication data is revealed to each CSS server, in order to prevent replay.

```plantuml
@startuml
skinparam ParticipantPadding 20
skinparam BoxPadding 30
hide footbox
autonumber

title Sequence diagram for issuing SD-JWT session_token

actor User
participant "CDOC2 Client" as CLIENT
participant "CDOC2-Auth portal" as AUTH
participant "CDOC2-RP portal" as CRP
participant "CSS servers" as CSS
participant "MiD/SiD API" as SID

User -> CLIENT : Decrypt this CDOC2 container
CLIENT -> User : We need to access CDOC2 infrastructure\nPlease authenticate as user "U"

alt SID
  User -> CLIENT : Agree, start authentication with SiD \nprovide identification code
else MID
  User -> CLIENT : Agree, start authentication with MiD \nprovide identification code and phone number
end

CLIENT -> AUTH : initiate SiD/MiD\n authentication for user U

loop for every CSS server
    AUTH -> CSS : generate session nonce
    CSS --> AUTH : nonce
end
AUTH -> CRP : generate session nonce
CRP --> AUTH: nonce
AUTH -> AUTH : Generate rpChallenge
AUTH -> AUTH : Calculate VC
AUTH -> SID : Start SiD/MiD authentication
SID --> AUTH : SID/MID authentication session id
AUTH -> AUTH : compose session_token SD-JWT

AUTH --> CLIENT : Return authentication process uuid and VC
CLIENT -> User : authenticating to "DigiDoc4", do you consent?

User -> CLIENT : decide that I agree\nwith authentication to "DigiDoc4"
User -> CLIENT : decide VC on CDOC2 Client\nmatches VC on phone
User -> SID : agree, PIN

CLIENT -> AUTH : Get authentication process status
AUTH -> SID : Get authentication process status
SID --> AUTH : signature S
alt SID
    AUTH -> AUTH : Add signature S to session_token SD-JWT
else MID
    AUTH -> AUTH: Validate MID signature S
end 
AUTH -> AUTH : sign session_token SD-JWT with \nauthentication server private key
AUTH --> CLIENT : issued session_token
@enduml
```

### Generating the SD-JWT authentication token and fetching the key shares

```plantuml
@startuml
skinparam ParticipantPadding 20
skinparam BoxPadding 30
hide footbox
autonumber

title Sequence diagram for issuing SD-JWT CDOC2 authentication token and fetching key shares

actor User
participant "CDOC2\nClient" as CLIENT
participant "CDOC2-RP\n portal" as CRP
participant "CSS\nservers" as CSS
participant "MiD/SiD\nAPI" as SID

loop for every CSS server
    CLIENT -> CSS : present SD-JWT session_token,\nget nonces for shares
    CSS -> CSS : Verify that I have issued\npresented session nonce from session_token
    CSS -> CSS : Verify that session_token sub\nis correct for this share
    CSS -> CSS : Verify that session_token is signed\nby CDOC2-auth portal
    CSS --> CLIENT : nonce
end

CLIENT -> CLIENT : compose CDOC2 auth token
CLIENT -> CLIENT : generate rpChallenge
CLIENT -> CLIENT : calculate the VC

CLIENT -> CRP : present SD-JWT session_token \nget hash H signed by user U
CRP -> CRP : Verify that I have issued\npresented challenge from session_token
CRP -> CRP : Verify that session_token sub\nmatches with user U
CRP -> CRP : Verify that session_token is signed\nby CDOC2-auth portal
CRP -> SID : create authentication signature of\nuser U on hash H
SID --> CRP : SiD/MiD authentication session id
CRP --> CLIENT : SiD/MiD authentication session id
CLIENT -> CLIENT : calculate the VC

CLIENT -> User : Do you consent\n "Decrypt container 'something.cdoc'"?
User -> CLIENT : decide that I agree\nwith decrypting container
User -> CLIENT : decide that VC on the CDOC2 Client\nmatches with VC on phone
User -> SID : agree, PIN

loop poll for session status
  CLIENT -> CRP : Get authentication process status
  CRP -> SID : Get authentication process status
  SID --> CRP : signature S
  alt MID
    CRP -> CRP: Countersign the MiD signature with rp key
  end
  CRP --> CLIENT : signature S
  alt MID
    CRP --> CLIENT : RFC9421 HTTP signature headers
  end
end

CLIENT -> CLIENT : create CDOC2 auth token with the signature S

loop for every CSS server
    alt SID
        CLIENT -> CSS : present CDOC2 auth token and RPv3 signature parameters
    else MID
        CLIENT -> CSS : present CDOC2 auth token and HTTP signature headers
    end
    CSS -> CSS : Verify that I have issued\npresented nonce from CDOC2 auth token
    CSS -> CSS : Verify that iss matches\nwith user U
    CSS -> CSS : Verify that authentication signature is\ncreated by CDOC2-RP and details match
    CSS -> CSS : Verify that MiD/SiD signature\ncreated by user U is valid and matches iss
    CSS --> CLIENT : return share
end

CLIENT -> CLIENT : compose capsule
CLIENT -> CLIENT : decrypt container
CLIENT --> User : files
@enduml
```

## SD-JWT based CDOC2 authentication protocol

In this section the details of the authentication protocol are explained.

### Authentication data

In generic protocol, the Client signs a set of information, which expresses the proof of Recipient's identity, and Recipient's intent to download specific Capsule. We can use the JWT standard (<https://www.rfc-editor.org/rfc/rfc7519.html>) for this. Client will sign the following set of JWT claims with their authentication means (Mobile-ID, Smart-ID), using the authentication key pair.

```json
{
    "iss": "etsi/PNOEE-48010010101",
    "aud": [ 
            "https://CSS.example-org1.ee:443/key-shares/9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3?nonce=59b314d4815f21f73a0b9168cecbd5773cc694b6", 
            "https://CSS.example-org2.ee:443/key-shares/5BAE4603-C33C-4425-B301-125F2ACF9B1E?nonce=9d23660840b427f405009d970d269770417bc769"
        ]
}
```

If the Client would create (in JWT and SD-JWT terminology, "issue") an ordinary signed JWT with these claims, the resulting data structure would look (linebreaks are used only for display purposes) something like that:

```text
eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9
.
eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ
.
dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

It contains following sections, separated by periods ("."):

1. first section is Base64-encoded JOSE header (for example `{"typ":"JWT", "alg":"HS256"}`)
2. second section is Base64-encoded JWT claims
3. third section is Base64-encoded binary signature value

Because of the signature, it is not possible to modify JWT claims anymore. If we wish to skip some values from the array of "aud" claim (in order to hide nonce values from other CSS servers and to prevent a replay possibility), this is not possible without breaking the signature.

### Intro to SD-JWT standard

SD-JWT draft standard (<https://sdjwt.js.org>, <https://datatracker.ietf.org/doc/draft-ietf-oauth-selective-disclosure-jwt/>) defines a mechanism for selective disclosure of individual elements of a JSON object, which is used as the payload of a JSON Web Signature (JWS) structure. It assumes an ecosystem with following entities:

1. SD-JWT is created by an entity called _Issuer_. Issuer decides, which claims are included in SD-JWT and which claims will be individually disclosable. Issuer signs the SD-JWT with its key pair and secures the SD-JWT against modifications.
2. SD-JWT is received from Issuer by an entity called _Holder_. Holder decides when and where to present the SD-JWT and also decides, which disclosable claims it wishes to reveal and which claims it wishes to keep secret from Verifier.
3. SD-JWT is presented to an entity called _Verifier_. Verifier requests SD-JWT from Holder, checks the Issuer signature and extracts the list of claims from SD-JWT.

We are mapping those SD-JWT-specific entities to CDOC2 data model in following way:

1. Same SD-JWT data structure is used for CDOC2 authentication data and CDOC2 authentication signature. CDOC2 authentication data is expressed as SD-JWT claims. CDOC2 authentication signature corresponds to the Issuer signature.
2. SD-JWT presentation along with selectively disclosed claims is used as a server-specific
   CDOC2 authentication token.
3. Roles of SD-JWT Issuer and SD-JWT Holder is performed by CDOC2 Client. Client creates SD-JWT structure, specifies that some claims are disclosable and creates specific presentations for each CSS server. SD-JWT standard optionally supports a scenario when Holder has its own key pair (separate from Issuer's key pair) and it is possible to verify the possession of Holder's key pair during the SD-JWT presentations. In CDOC2 system, we don't use Holder's key binding feature.
4. Role of SD-JWT Verifier is performed by CSS servers. Servers will provide Client with nonces and verify that they will receive a valid signed SD-JWT with server-specific nonce as disclosable claim.

### SD-JWT and selective disclosures

How does this "selective disclosure" feature actually work behind the scenes? The idea is that Issuer will create special kind of `SD-CLAIMS` data items in the ordinary JWT, which are:

```text
SD-CLAIMS = (
    HASH(SALT | CLAIM-NAME | CLAIM-VALUE)
)*
```

where `SALT` is a random salt. This kind of operation effectively "hides" `CLAIM-NAME` and
`CLAIM-VALUE`. But, it allows Verifier to check if the digest was computed from the correct data,
if they are provided with the values of `SALT`, clear-text `CLAIM-NAME` and `CLAIM_VALUE`.
Such `SD-CLAIMS` are included in the JWT structure, inside a special JOSE array with name `_sd`.

In order to reveal the `CLAIM-VALUE` to Verifier, Holder needs to create `SD-DISCLOSURE` data items, which are:

```text
SD-DISCLOSURE = (
    SALT, CLAIM-NAME, CLAIM-VALUE
)*
```

The resulting disclosure items are appended to the JWT using the tilde character `~` as a separator

So, for example, let's take the original set of claims:

```json
{
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "given_name": "John",
  "family_name": "Doe"
}
```

Let's say that the Issuer wishes to make claim `given_name` disclosable. They generate a random salt (e.g., `eluV5Og3gSNII8EYnsxA_`) and compute a digest value `SHA-256("eluV5Og3gSNII8EYnsxA_A" + "John")` and include such `SD_CLAIM` data item in the `_sd` structure:

```json
{
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "family_name": "Doe",
  "_sd": [
    "PvU7cWjuHUq6w-i9XFpQZhjT-uprQL3GH3mKsAJl0e0"
  ]
}
```

JWT header and JWT payload is then signed and following JWT is created:

```text
<JWT_header>.<JWT_payload>.<JWT_signature>
```

However, this "compact"-encoded JWT doesn't yet disclosure information. So, an SD-DISCLOSURE
object is also added:

```json
  [
    "eluV5Og3gSNII8EYnsxA_A", "given_name", "John"
  ]
```

It is encoded in Base64 and appended to the original encoded JWT, separated and terminated by a
tilde  ("~"):

```text
<JWT_header>.<JWT_payload>.<JWT_signature>~<SDJWT_disclosure>~
```

Now, Holder can decide which claims to disclose by selectively appending `<SDJWT_disclosure>`
objects when creating a presentation to Verifier. The signature of the original JWT is still valid, because original JWT will be unchanged.

### Creating SD-JWT structure (authentication data and authentication signature)

Applying SD-JWT data structure to CDOC2 authentication protocol, we get following specification:

1. Client creates an SD-JWT with following example header:

   ```json
   {
       "typ": "vnd.cdoc2.auth-token.v1+sd-jwt",
       "alg": "ES256"
   }
   ```

   The values for the `alg` claim depend on the signature algorithm that the user's eID means authentication key pair is using:
   - Mobile-ID uses `ES256` (ECDSA with SHA-256).
   - Smart-ID RP API v3 uses `RSASSA-PSS+ACSP_V2`. This is a non-standard algorithm which
     describes the combination of algorithms in use by SID RPv3 and is interpreted as such by
     the CDOC2 infrastructure token authentication logic.

2. Client initialises empty SD-JWT payload structure and adds always-disclosed claims to SD-JWT payload. The `iss` claim is added directly to the payload. The `aud` claim is added as a selectively disclosable claim via the `_sd` mechanism and is therefore not present as a plain claim in the base payload.

   ```json
   {
     "iss": "etsi/PNOEE-48010010101"
   }
   ```

3. Client creates disclosable entries for the `aud` claim for each CSS server. Each entry is a URL string identifying the specific key share and nonce. These entries are stored as selectively disclosable array elements — only their digest hashes are placed in the `_sd` structure of the JWT payload. For example, the `aud` claim values are:

   ```json
   [
       "https://CSS.example-org1.ee:443/key-shares/9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3?nonce=59b314d4815f21f73a0b9168cecbd5773cc694b6", 
       "https://CSS.example-org2.ee:443/key-shares/5BAE4603-C33C-4425-B301-125F2ACF9B1E?nonce=9d23660840b427f405009d970d269770417bc769"
   ]
   ```

4. Client signs the SD-JWT structure (with the header, payload and disclosable claims information in `_sd` structure), as SD-JWT Issuer with user's authentication means.

### Presenting SD-JWT (creating authentication token)

For each server, Client creates SD-JWT presentation and discloses only that `aud` array element, which contains `key-share` and `nonce`, which are specific to that server.

Resulting SD-JWT is formatted as (elements separated by "~"):

```text
<Issuer-signed JWT>~<Disclosure 1>~
```

where `<Issuer-signed JWT>` contains following elements (separated by "."):

```text
<SD-JWT header>.<SD-JWT payload>.<Issuer signature>
```

Actual SD-JWT in compact representation looks something like that (the example below is for illustrative purposes; actual Base64url values will differ):

```text
eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0IiwgIng1YyI6ICJNSUlDOFRDQ0FkbWdBLi4uVnQ1NDMyR0E9PSJ9.eyJfc2QiOiBbIjFTVGpGbEJINmptRjI3MElmeTJTdFhuTXpaMlREcklLSlg1Qnk2NWd2LTQiXSwgImlhdCI6ICIxNzE1Njk0MjUzIiwgImV4cCI6ICIxNzE1Njk0MjYzIiwgIl9zZF9hbGciOiAic2hhLTI1NiJ9.0EXb6QCwNL19ZWieDHDWZsm2W_bO2tCH8QBr1ftcTFh2t2P77qEimYjrattAHMah5FPAD3otdDARzh4DfWcuVg~WyJrLTRFYVpwQWctMTdRbk1mT3dNYk93IiwgInNoYXJlQWNjZXNzRGF0YSIsIFt7Ii4uLiI6ICJFRXNfNWVmWUN5WVNjaDB6ZTJKZ1VsV0VpSVhzcTZic1o4UXFBdnlqZXVNIn0sIHsiLi4uIjogIkZfLTZuc0RDT0NvSmNOS2ZhODdWZ0FNVFRzODdLRjN6WXlzbUpnQzF3ckUifV1d~WyJMUTN0eUxONHZVbDRFakR0ekdmRVFnIiwgeyJzZXJ2ZXJCYXNlVVJMIjogImh0dHBzOi8vY2RvYy1jY3MucmlhLmVlOjQ0My9rZXktc2hhcmVzLyIsICJzaGFyZUlkIjogIjlFRTkwRjJELUQ5NDYtNEQ1NC05QzNELUY0QzY4RjdGRkFFMyIsICJzZXJ2ZXJOb25jZSI6ICI0MiJ9XQ~
```

if we decode the individual parts, we get following data items:

1. Protected header:

   ```json
   {
       "alg": "ES256",
       "typ": "vnd.cdoc2.auth-token.v1+sd-jwt"
   }
   ```

2. Protected payload:

   ```json
   {
       "iss": "etsi/PNOEE-48010010101",
       "_sd": [
           "1STjFlBH6jmF270Ify2StXnMzZ2TDrIKJX5By65gv-4"
       ],
       "_sd_alg": "sha-256"
   }
   ```

3. Binary signature:

   ```text
   0EXb6QCwNL19ZWieDHDWZsm2W_bO2tCH8QBr1ftcTFh2t2P77qEimYjrattAHMah5FPAD3otdDARzh4DfWcuVg
   ```

4. Disclosure for the selectively disclosable `aud` claim (outer disclosure), containing digests of the individual array element disclosures:

   ```json
   [
       "k-4EaZpAg-17QnMfOwMbOw",
       "aud",
       [
           {"...": "EEs_5efYCyYSch0ze2JgUlWEiIXsq6bsZ8QqAvyjeuM"},
           {"...": "F_-6nsDCOCoJcNKfa87VgAMTTs87KF3zYysmJgC1wrE"}
       ]
   ]
   ```

5. Disclosure for a single `aud` array element (one per CSS server, only the relevant one is included in each presentation):

   ```json
   [
       "LQ3tyLN4vUl4EjDtzGfEQg",
       "https://CSS.example-org1.ee:443/key-shares/9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3?nonce=59b314d4815f21f73a0b9168cecbd5773cc694b6"
   ]
   ```

### Verifying SD-JWT (verifying authentication token)

CSS server receives compact SD-JWT presentation (`<Issuer-signed JWT>~<Disclosure 1>~<Disclosure 2>~`) and performs following authentication and authorization checks:

1. Verify that SD-JWT is signed by the key pair, whose public key is included in the X.509 certificate, which is transmitted in the API method "GET /key-shares/{shareId}" parameter "x-cdoc2-auth-x5c". The verification method depends on the signing means used:
   - For **Mobile-ID** (ES256 algorithm): verify the JWT signature using the EC public key from the certificate, and additionally verify the RP counter-signature transmitted in the HTTP request headers.
   - For **Smart-ID RP API v3** (RSASSA-PSS+ACSP_V2 algorithm): verify the JWT signature and additionally verify the Smart-ID RP API v3 signature parameters transmitted alongside the auth token.
2. Verify that certificate is issued by trustworthy CA.
3. Verify that certificate is valid at current point of time and is not revoked.
4. Verify that the disclosed `aud` claim is an array containing exactly one URL string.
5. Parse `aud` value (it should be something like "<https://CSS.example-org1.ee:443/key-shares/9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3?nonce=59b314d4815f21f73a0b9168cecbd5773cc694b6>") into components `serverBaseURL`, `shareId` and `nonce`.
6. Verify that `serverBaseURL` is correct for this CSS server.
7. Verify that this CSS server has a Capsule with identifier `shareId`, and it is not deleted.
8. Verify that this CSS server has previously generated a nonce for this `shareId` and one of the nonce values matches with `nonce` component value and that nonce wasn't generated too long ago (configuration parameter, for example 300 seconds).
9. Verify that `recipient_id` from the `KeySharesCapsule` matches with the `subjectDN` from the X.509 certificate from API parameter "x-cdoc2-auth-x5c".

If all checks are positive, then the authentication and access control decision is positive, and CSS server can return the capsule.

## Session Token based CDOC2 authentication protocol

Before authenticating to CSS servers (cdoc2-shares-servers), a valid session token is needed. Session token is valid up to 24 hours.

Session tokens use the type identifier `vnd.cdoc2.session-token.v2+sd-jwt`. Unlike auth tokens —
which are signed directly by the user's eID means — session tokens are signed by the
Authentication Server. In the case of Smart-ID RPv3 authentication, the signature is embedded within the
session token as a claim, along with the parameters needed to verify it.

### Session Token structure

Session token header:

```json
{
    "kid": "<auth-server-key-id>",
    "typ": "vnd.cdoc2.session-token.v2+sd-jwt",
    "alg": "ES256"
}
```

Session token payload includes:

- `iss`: Authentication Server URL (e.g., `"https://cdoc2-auth-server.ee"`)
- `sub`: User's ETSI identifier (e.g., `"etsi/PNOEE-48010010101"`)
- `iat` / `exp`: Issuance and expiry timestamps
- `_sd` / `_sd_alg`: Selectively disclosable `aud` claim (same URL format as in auth tokens)

Additionally for SID RPv3 authentication:

- `signatureProtocol`: RPv3 signature protocol
- `rpChallenge`: Relying party challenge value
- `interactionsDigest`: SHA-256 digest of the serialized interactions object
- `interactionTypeUsed`: Actual interaction that was used to create the signature
- `rpName`: Auth server relying party name
- `schemeName`: Name of scheme that was used to create the signature (e.g., `smart-id`)
- `signature`: Embedded user eID signature with algorithm parameters.

### Verifying Session Token

CSS server receives the session token presentation and performs the following checks:

1. Verify that the session token is signed by the Authentication Server, using the key identified by the `kid` header parameter.
2. Verify that the token type header is `vnd.cdoc2.session-token.v2+sd-jwt`.
3. Verify that `iat` is not in the future and `exp` is not in the past.
4. Verify that `sub` matches the identity from the signing certificate.
5. Verify the `aud` claim following the same steps 4–9 as for the auth token verification above.
6. Only for **Smart-ID RP API v3** : Verify the embedded user eID signature in the `signature` claim

## Security of the protocol

We are analyzing security of the authentication protocol from following aspects.

### Protection against the passive network read

In case the network between the CDOC2 Client and CSS servers is compromised and attacker is able to read network connections, the attacker is simply able to observe the values of the capsule shares as they are downloaded from CSS servers. The authentication protocol itself doesn't have built-in protection against this and assumes that connection from CDOC2 Client to every CSS server is authenticated and transmission is encrypted with HTTPS protocol.

### Protection against the MITM attack with connection hijacking

In case the attacker is able to hijack the network connections between the CDOC2 Client and CSS servers and redirect the connection attempts from the real CSS servers to attacker itself, attacker is also able to masquerade to Client as real CSS server and is also observe the values of the transmitted capsule shares. Attacker might be able to present a self-signed X.509 HTTPS certificate, or it might be able to present a valid X.509 HTTPS certificate from the real CA as well. In case the CDOC2 Client doesn't verify the identity of the CSS server, it is not able to tell a difference between the attacker and real CSS server.

It is essential that CDOC2 Clients authenticate, which servers they are connecting to and that they are verifying the HTTPS X.509 certificates against the whitelisted values in the configuration file.

### Protection against compromised CSS servers

In case the attacker has compromised some CSS servers, the following attack scenario should be considered.

1. Client connects to CSS-1 and asks for nonce `nonce1`. CSS-1 is controlled by attacker, and they return the value of `nonce1`.
2. Client connects to CSS-2 and asks for nonce `nonce2`. CSS-2 is secure and returns the value of `nonce2`.
3. Client creates authentication signature, in the form of issuing SD-JWT.
4. Client creates presentation of SD-JWT for CSS-1 with the disclosure of the value of `nonce1` and sends this to CSS-1. The value of `nonce2` is not revealed.
5. Attacker uses the signed SD-JWT and tries to create another presentations for CSS-2. However, since the attacker doesn't know the salt value and clear-text value of the second component of the `aud` claim, it is not able to create valid presentation.

Therefore, the protocol is secure against compromise of some CSS servers.

### Protection against CSS server compromise and nonce reuse

In case the attacker has compromised some CSS servers and tries to confuse Client by mixing nonces from different servers, the following attack scenario should be considered.

1. Attacker has knowledge of all capsule share identification values, `shareId1` and `shareId2`, for example, from the captured CDOC2 container.
2. Client connects to CSS-1 and asks for nonce value of the `shareId1`. CSS-1 is controlled by attacker and instead of returning freshly generated `nonce1`, attacker connects to CSS-2 and asks for the nonce value of the `shareId2` and returns this as `nonce2_1` to Client.
3. Client connects to CSS-2 and asks for nonce value of the `shareId2`. CSS-2 generates another `nonce2_2` and returns this to Client.
4. Client creates authentication signature, in the form of issuing a SD-JWT.
5. Client creates presentation of SD-JWT for CSS-1 with the disclosure of the value of `nonce2_1` and sends this to CSS-1. The value of `nonce2_2` is not revealed.
6. Attacker takes the SD-JWT presentation and replays it to CSS-2. Because it contains the value of `nonce2_1`, which is generated by CSS-2, attacker is hoping that CSS-2 responds with value of the capsule share.
7. CSS-2 verifies that `nonce2_1` is associated with the wrong share identifiers, `shareId1`, which doesn't match with the share identifier that CSS-2 has and denies the request.

Therefore, the protocol is secure against compromise of some CSS servers, which might be trying mixing and reusing nonces.

### Protection against DOS attacks

Protocol doesn't have a built-in protection against DOS attacks. When deploying CDOC2 system components, components in the network infrastructure, such as load balancers or application servers need to use DOS protection mechanisms, such as limiting the number of service requests from single IP-address or others.

### Formal analysis

Even though we have carefully designed the protocol with security requirements in mind, and it has been reviewed multiple times, and it includes protection against common network attacks, we are not able to prove the security of the solution.

However, we can increase the confidence by using formal analysis methods. We have implemented the protocol flow as a model of ProVerif (<https://bblanche.gitlabpages.inria.fr/proverif/>) tool. ProVerif is an automated verification tool for cryptographic protocols, which works in the formal logic model Dolev-Yao and can mathematically verify and prove, if the protocol has some security properties, such as confidentiality, authentication, etc. Proving such properties may involve finding proof of not-existence of some other property and verification of all possible combinations. Therefore, using manual methods can be very time-consuming and doesn't usually give full confidence.

Model has been presented in appendix A, and it verifies the following properties.

1. Described attacker is not able to download shares of capsules from CSS servers:

   ```text
           Query not attacker(capsule[]) is true
   ```

2. Described attacker is not able to authenticate on behalf of the Client:

   ```text
           Query event(FinishHandshake(x1,x2,x3,x4)) ==> 
                   event(StartHandshake(x1,x2,x3,x4)) is true.
   ```

Therefore, the described protocol should be secure against such properties. However, because ProVerif cannot analyze exactly the same CSS and CDOC2 Client source code. Therefore, there might be still unknown vulnerabilities in those areas. Still, this kind of additional formal analysis increases the confidence that protocol design doesn't have major security issues.

### Weakness against MITM signature

In case the MITM attacker has been able to compromise the path between the CDOC2 Client and the user's authentication means (Mobile-ID, Smart-ID) and is able to trick user to sign attacker's submitted hash with the user's authentication key pair, it is possible to attack the CDOC2 system.

Following authentication means have this potential weakness:

1. ID-card when used via PKCS#11 interface
2. Mobile-ID REST API
3. Smart-ID RP-API v2

Following authentication means or APIs do not have this weakness:

1. ID-card when used via web-eID JS interface
2. Smart-ID RP-API v3 (supported in CDOC2 via the RSASSA-PSS+ACSP_V2 signature verification)
3. Mobile-ID REST API with an RP counter signature. This is implemented in CDOC2 as an HTTP
   signature scheme ( [RFC 9421](https://datatracker.ietf.org/doc/html/rfc9421) )

In order to mitigate against this weakness, CDOC2 system can benefit from following countermeasures:

1. Informing the users about risks of using non-trusted software/services (desktop applications, mobile applications, websites). This countermeasure is already in use in practice.
2. Vetting and limiting RPs, who can use the Mobile-ID and Smart-ID APIs. This countermeasure is already used in practice.

## Appendix A - Formal model for authentication protocol

```ocaml
(*************************************************************
Execution: 
Execution: 
proverif -in pitype threeservers.pv
**************************************************************)

free c: channel.

type host.
type nonce.
type pkey.
type skey.
type expc.
type dhpc.
type exps.
type dhps.
type transactionid.

fun nonce_to_bitstring(nonce): bitstring [data,typeConverter].

(* Signatures *)

fun spk(skey): pkey.
fun sign(bitstring, skey): bitstring.
reduc forall m: bitstring, k: skey; getmess(sign(m,k)) = m.
reduc forall m: bitstring, k: skey; checksign(sign(m,k), spk(k)) = m.

(* Hash function *)

fun h(bitstring) : bitstring.

(* Secure channels *)
fun gpowc(expc): dhpc.
fun gpows(exps): dhps.
fun mkChannelc1(expc, dhps): channel.
fun mkChannels1(exps, dhpc): channel.
fun mkChannelc2(expc, dhps): channel.
fun mkChannels2(exps, dhpc): channel.
equation forall x : expc, y : exps; 
    mkChannelc2(x, gpows(y)) = mkChannels2(y, gpowc(x)).
equation forall x : expc, y : exps; 
    mkChannelc1(x, gpows(y)) = mkChannels1(y, gpowc(x)).

table honestUser(pkey).
table transidtable(exps, transactionid, nonce).
table honestServer(dhps).

(* Queries *)

free capsule : bitstring [private].
query attacker(capsule).

event StartHandshake(pkey, dhps, channel, transactionid).
event FinishHandshake(pkey, dhps, channel, transactionid).

query x1 : pkey, x2 : dhps, x3 : channel, x4 : transactionid; 
    event(FinishHandshake(x1,x2,x3,x4)) ==> 
        event(StartHandshake(x1,x2,x3,x4)).


let clientInstance(pkS1 : dhps, pkS2 : dhps, pkS3 : dhps, skME : skey) =
  get honestServer(=pkS1) in
  get honestServer(=pkS2) in
  get honestServer(=pkS3) in
  new transID1 : transactionid;
  new transID2 : transactionid;
  new transID3 : transactionid;
  new chs1 : expc;
  new chs2 : expc;
  new chs3 : expc;
  let cto1 = mkChannelc1(chs1, pkS1) in
  let cfrom1 = mkChannelc2(chs1, pkS1) in
  let cto2 = mkChannelc1(chs2, pkS2) in
  let cfrom2 = mkChannelc2(chs2, pkS2) in
  let cto3 = mkChannelc1(chs3, pkS3) in
  let cfrom3 = mkChannelc2(chs3, pkS3) in ( (
  !out(c, gpowc(chs1)) |
  !out(cto1, transID1) |
  !out(c, gpowc(chs2)) |
  !out(cto2, transID2) |
  !out(c, gpowc(chs3)) |
  !out(cto3, transID3) 
  ) | (
  in(cfrom1, challenge1 : nonce);
  in(cfrom2, challenge2 : nonce);
  in(cfrom3, challenge3 : nonce);
  let tobesigned = (
    (transID1, h(nonce_to_bitstring(challenge1))), 
    (transID2, h(nonce_to_bitstring(challenge2))),
    (transID3, h(nonce_to_bitstring(challenge3)))) in
  let tkt1 = (
        (transID1, challenge1), 
        (transID2, h(nonce_to_bitstring(challenge2))), 
        (transID3, h(nonce_to_bitstring(challenge3)))) in
  let tkt2 = (
        (transID1, h(nonce_to_bitstring(challenge1))), 
        (transID2, challenge2), 
        (transID3, h(nonce_to_bitstring(challenge3)))) in
  let tkt3 = (
        (transID1, h(nonce_to_bitstring(challenge1))), 
        (transID2, h(nonce_to_bitstring(challenge2))), 
        (transID3, challenge3)) in
  let smsg = sign(tobesigned, skME) in
  new chs4 : expc;
  new chs5 : expc;
  new chs6 : expc;
  let cto4 = mkChannelc1(chs4, pkS1) in
  let cto5 = mkChannelc1(chs5, pkS2) in
  let cto6 = mkChannelc1(chs6, pkS3) in
  let pkME = spk(skME) in
  ( (
  event StartHandshake(spk(skME), pkS1, cto4, transID1);
  (!out(c, gpowc(chs4)) | 
  !out(cto4, (tkt1, smsg, pkME)))
  ) | (
  event StartHandshake(spk(skME), pkS2, cto5, transID2);
  (!out(c, gpowc(chs5)) |
  !out(cto5, (tkt2, smsg, pkME)))
  ) | (
  event StartHandshake(spk(skME), pkS3, cto6, transID3);
  (!out(c, gpowc(chs6)) |
  !out(cto6, (tkt3, smsg, pkME)))
  ) ) ) ).
  
let serverInstance1(sk : exps) =
  in(c, dhc : dhpc);
  let cfrom = mkChannels1(sk, dhc) in
  let cto = mkChannels2(sk, dhc) in
  in(cfrom, transID : transactionid);
  new ch : nonce;
  insert transidtable(sk, transID, ch);
  out(cto, ch).

let serverInstance2(sk : exps) =
  in(c, dhc : dhpc);
  let cfrom = mkChannels1(sk, dhc) in
  let cto = mkChannels2(sk, dhc) in
  in(cfrom, (tkt : bitstring, msgsig : bitstring, userpk : pkey));
  let ((tID1 : transactionid, v1 : bitstring), 
    (tID2 : transactionid, v2 : bitstring), 
    (tID3 : transactionid, v3 : bitstring)) = tkt in
  ((
    get transidtable(=sk, =tID1, v1prim) in
    if nonce_to_bitstring(v1prim) = v1 then
    let sgndmsg1 = ((tID1, h(v1)), (tID2, v2), (tID3, v3)) in
    if checksign(msgsig, userpk) = sgndmsg1 then
    get honestUser(=userpk) in
    event FinishHandshake(userpk, gpows(sk), cfrom, tID1);
    out(cto, capsule)
  ) | (
    get transidtable(=sk, =tID2, v2prim) in
    if nonce_to_bitstring(v2prim) = v2 then
    let sgndmsg2 = ((tID1, v1), (tID2, h(v2)), (tID3, v3)) in
    if checksign(msgsig, userpk) = sgndmsg2 then
    get honestUser(=userpk) in
    event FinishHandshake(userpk, gpows(sk), cfrom, tID2);
    out(cto, capsule)
  ) | (
    get transidtable(=sk, =tID3, v3prim) in
    if nonce_to_bitstring(v3prim) = v3 then
    let sgndmsg3 = ((tID1, v1), (tID2, v2), (tID3, h(v3))) in
    if checksign(msgsig, userpk) = sgndmsg3 then
    get honestUser(=userpk) in
    event FinishHandshake(userpk, gpows(sk), cfrom, tID3);
    out(cto, capsule)
  )).

let mkHonestUser =
  new s : skey;
  let p = spk(s) in
  insert honestUser(p);
  out(c, p);
  !(
    in(c, (s1 : dhps, s2 : dhps, s3 : dhps));
    clientInstance(s1, s2, s3, s)
  ).

let mkHonestServer =
  new s : exps;
  let p = gpows(s) in
  insert honestServer(p);
  out(c, p);
  ((!(
    serverInstance1(s)
  )) | (!(
    serverInstance2(s)
  ))).

process
  !mkHonestUser | !mkHonestServer
```
