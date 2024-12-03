---
title: ID authentication protocol
---

# ID authentication protocol

This section describes a protocol and data formats for authenticating to multiple CSS servers (cdoc2-shares-servers) in order to download every `KeySharesCapsule` from them.

## Authentication protocol requirements

1. Multiple CSSs hold Capsules, which all need to be downloaded by Client.
2. Client needs to authenticate to multiple CSSs, in order to download all Capsules.
3. Client should only need to create one signature with its authentication means (ID-card, Mobile-ID, Smart-ID) for authentication.
4. CSS must not be able to replay the authentication ticket to another CSS.

## Non-suitable alternatives

Before designing a custom authentication protocol, we should make sure that this is really needed and we cannot re-use existing protocols. Existing protocols may already have proven security properties and they might be well supported by existing software libraries.

For example, traditionally, authentication and authorization processes are handled by OpenID Connect and OAuth2 protocols. They are well studied and robust. However, if we try to apply them to our situation and try to map the mandatory roles from OpenID Connect and OAuth2 ecosystems to our components (Client, CSSs), it becomes cumbersome.

First, the requirement that Client needs to "login" to multiple servers with single use of user's eID means is tricky. This is usually handled by single-sign-on services. There's such a service called GovSSO (<https://e-gov.github.io/GOVSSO/TechnicalSpecification>), but it is more oriented towards web applications and it is using a generic OpenID Connect protocol without binding the issued `id_tokens` with user's authentication signatures. In case CSS would be accepting such `id_tokens`, there's no cryptographic guarantee that the user's authentication has actually taken place and that the user's eID means was actually involved. That would mean that the security of such central single-sign-on provider would be critical and in case the security of GovSSO would be breached, it would be able to download all KeyShares on behalf of any user.

Additionally, if we would be using OAuth2 authorization protocols, we would be using OAuth2 "bearer" tokens and this would mean that CSS server can re-use the token and replay it to another CSS server. Possibility to replay tokens might be overcome with protocols like "OAuth2 Certificate-Bound Access Tokens" (<https://datatracker.ietf.org/doc/html/rfc8705>) and "OAuth2 Demonstrating Proof of Possession" (<https://www.rfc-editor.org/rfc/rfc9449>), but that would require us to create a central trusted component which would hand out those access tokens. That kind of component would be a single source of failure and in case the security of such component would be breached, the attacker would be able to download all KeyShares on behalf of any user.

Therefore, introducing additional trusted components to the CDOC2 ecosystem is not desirable at the moment. More tailored approach would be needed to come up with authentication protocol, that would satisfy all the requirements and would depend only on the eID authentication means or eID trust service providers.

## Overview of the generic authentication protocol

In the generalized form, the authentication protocol for downloading a Capsule information from servers can be explained with the following sequence diagram below.

This is just an abstract overview of the authentication protocol. In the next sections, we describe what kind of data is used as the authentication data, how the eID means signing function is used and how only a minimal set of authentication data is revealed to each CSS server, in order to prevent replay.

```plantuml
@startuml
skinparam ParticipantPadding 20
skinparam BoxPadding 30
hide footbox
autonumber

box "User"
Actor Recipient as R
participant Client as C
participant Authenticator as A
end box

box "cdoc2-shares-servers (CSSs)"
collections CCS as S
end box

box "Trust infrastructure"
participant "PKI/OCSP" as PKI
end box

R -> C: Decrypt Container
C -> C: Read information about \n Capsules from Container
loop for each CSS
    C -> S: Authentication request for shareId of Capsule
    S --> C: Nonce for shareId
end
C -> C: Create \n authentication signature data
C -> A: Create signature on \n authentication data
A -> R: Authorize eID use for signature generation
R -> A: Authorized
A --> C: Authentication signature
loop for each CSS
    C -> C: Create authentication token \n specific for a CSS server
    C -> S: Present token with \n authentication signature \n and request Capsule
    S -> PKI: Recipient's certificate \n not revoked?
    PKI --> S: Recipient's certificate \n is valid
    S -> S: AuthN: Verify authentication token \n and authentication signature
    S -> S: AuthZ: Verify that Recipient is \n allowed to download Capsule
    S --> C: Capsule
end
@enduml
```

## SD-JWT based CDOC2 authentication protocol

In this section the details of the authentication protocol are explained.

### Authentication data

In the generic protocol, there's a idea that Client signs a set of information, which expresses the proof of Recipient's identity and intent to download specific Capsule information. We will use the JWT standard (https://www.rfc-editor.org/rfc/rfc7519.html). Client will sign the following set of JWT claims with their authentication means (ID- card, Mobile-ID, Smart-ID), using the authentication key pair.

```json
{
    "iss": "etsi/PNOEE-48010010101",
    "aud": [ 
            "https://CSS.example-org1.ee:443/key-shares/9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3?nonce=59b314d4815f21f73a0b9168cecbd5773cc694b6", 
            "https://CSS.example-org2.ee:443/key-shares/5BAE4603-C33C-4425-B301-125F2ACF9B1E?nonce=9d23660840b427f405009d970d269770417bc769"
        ]
}
```

If the Client would create (in JWT and SD-JWT terminology, "issue") an ordinary signed JWT with these claims, the resulting thing would look something like that:

```text
eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9
.
eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ
.
dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

It contains following sections, separated by periods ("."):

1. first section is base64-encoded JOSE header (for example `{"typ":"JWT", "alg":"HS256"}`)
2. second section is base64-encoded JWT claims
3. third section is base64-encoded signature value

It is not possible to modify the JWT claims anymore and to leave out some values from the "aud" claim, in order to not reveal the nonce values to some CSS servers and to prevent the replay possibility.

### Intro to SD-JWT standard

SD-JWT standard (<https://sdjwt.js.org>, <https://datatracker.ietf.org/doc/draft-ietf-oauth-selective-disclosure-jwt/>) defines a mechanism for selective disclosure of individual elements of a JSON object used as the payload of a JSON Web Signature (JWS) structure. It assumes a ecosystem with following entities:

1. SD-JWT is created by an entity called _Issuer_. Issuer decides, what claims are included in SD-JWT and which claims are individually disclosable. Issuer signs the SD-JWT with its key pair and this way secures the SD-JWT against modifications.
2. SD-JWT is received from Issuer by entity called _Holder_. Holder decides when and where to present the SD-JWT and also decides, which disclosable claims it wishes to reveal and which one it wishes to keep secret.
3. SD-JWT is presented to an entity called _Verifier_. Verifier requests SD-JWT from Holder, checks the Issuer signature and extracts the list of claims from SD-JWT.

We are mapping those SD-JWT-specific entities to CDOC2 world in the following way:

1. SD-JWT data structure is used as both CDOC2 authentication data and CDOC2 authentication signature. In other words, information that is used to create authentication data and authentication signature, is expressed (encoded) as SD-JWT structure. Authentication signature corresponds to Issuer signature.
2. SD-JWT presentation with selectively disclosed claims is used as server-specific CDOC2 authentication ticket.
3. Roles of SD-JWT Issuer and SD-JWT Holder is performed by CDOC2 Client. Client creates the SD-JWT structure, specifies that some claims are disclosable and later creates specific presentations to each CSS server. SD-JWT standard optionally supports the scenario when Holder has its own key pair (separate from Issuer's key pair) and it is possible to verify this key binding during the SD-JWT presentations. In CDOC2 system, we don't use Holder's key binding feature.
4. Role of SD-JWT Verifier is performed by CSS servers. Servers will provide Client with nonces and verify that they will receive a valid signed SD-JWT with server-specific nonce as disclosable claim.

### SD-JWT and selective disclosures

How does this "selective disclosure" feature actually work behind the scenes? The idea is that Issuer will create special kind of `SD-CLAIMS` data items in the ordinary JWT, which are:

```text
SD-CLAIMS = (
    CLAIM-NAME: HASH(SALT | CLAIM-VALUE)
)*
```

where `SALT` is a random salt. This kind of operation effectively "hides" the content of the `CLAIM-VALUE`. But, it allows Verifier to check if the digest was computed from the correct value, if he is provided with the salt and clear-text claim value. Such kind of `SD-CLAIMS` are included in the JWT structure, in a special claim with name `_sd`.

In order to reveal the `CLAIM-VALUE` to Verifier, Holder needs to create `SD-RELEASES` data items, which are:

```text
SD-RELEASES = (
    CLAIM-NAME: (DISCLOSED-SALT, DISCLOSED-VALUE)
)
```

and include such info in the JWT, in a special claim with name `sd_release`. So, for example, if the original set of claims are following:

```json
{
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "given_name": "John",
  "family_name": "Doe",
}
```

Let's say that the Issuer wishes to make claim `given_name` disclosable. It generates a random salt and computes digest value from `SHA-256("eluV5Og3gSNII8EYnsxA_A" + "John")` and includes such `SD_CLAIM` data item in the `_sd` claim:

```json
{
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "family_name": "Doe",
  "_sd_": {
    "given_name": "PvU7cWjuHUq6w-i9XFpQZhjT-uprQL3GH3mKsAJl0e0"
  }
}
```

This JOSE is then signed as `<JWT_payload` and following JWT is created:

```text
<JWT_header>.<JWT_payload>.<JWT_signature>
```

However, this "compact"-encoded JWT doesn't yet contain random salt values. So, SD-JWT Salt/Value Container, which is simply a JSON array of `SD-RELEASES` data items, is also added:

```json
{ 
  [
    "given_name": "[\"eluV5Og3gSNII8EYnsxA_A\", \"John\"]",
  ]
}
```

and it is encoded in Base64 and added to the original encoded JWT, after yet another period ("."):

```text
<JWT_header>.<JWT_payload>.<JWT_signature>.<SD-JWT Salt/Value Container>
```

Now, Holder can decide which disclosable claim information from the Salt/Value Container it will include, when creating a presentation to Verifier, and which it removes. The signature of the original JWT is still valid, because original JWT will be unchanged.

### Creating SD-JWT structure (authentication data and authentication signature)

Applying SD-JWT data structure to the CDOC2 authentication protocol situation, we will reach the following specification:

1. Client creates an SD-JWT with following example header:

```json
{
    "typ": "vnd.cdoc2.auth-token.v1+sd-jwt",
    "alg": "ES256",
    "kid": "PNOEE-48010010101"
}
```

The values for the "alg" claim depend on the signature algorithm that the user's eID means authentication key pair is using. For example, the ID-card produces signatures with ES256 algorithm, Smart-ID produces signatures with RS256 algorithm.

2. Client initialises empty SD-JWT payload structure and adds always-disclosed claims to SD-JWT payload. Examples is provided here. Note that the `aud` claim contains only empty array at the moment.

```json
{
    "aud": [],
    "iss": "etsi/PNOEE-48010010101"
}
```

3. Client adds disclosable JSON strings to the array `aud` for each CSS server. For example, the `aud` claim may contain following StringOrURI values:

```json
[
    "https://CSS.example-org1.ee:443/key-shares/9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3?nonce=59b314d4815f21f73a0b9168cecbd5773cc694b6", 
    "https://CSS.example-org2.ee:443/key-shares/5BAE4603-C33C-4425-B301-125F2ACF9B1E?nonce=9d23660840b427f405009d970d269770417bc769"
]
```

4. Client signs the SD-JWT structure as SD-JWT Issuer with the user's authentication means.

### Presenting SD-JWT (creating authentication ticket)

For each server, Client creates SD-JWT presentation and discloses only that `aud` array element, which contains the `key-share` and `nonce`, which is specific to that server.

Resulting SD-JWT is formatted as (elements separated by "~"):

```text
<Issuer-signed JWT>~<Disclosure 1>~
```

where `<Issuer-signed JWT>` contains following elements (separated by "."):

```text
<SD-JWT header>.<SD-JWT payload>.<Issuer signature>
```

Actual SD-JWT in compact representation looks something like that:
```text
eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0IiwgIng1YyI6ICJNSUlDOFRDQ0FkbWdBLi4uVnQ1NDMyR0E9PSJ9.eyJfc2QiOiBbIjFTVGpGbEJINmptRjI3MElmeTJTdFhuTXpaMlREcklLSlg1Qnk2NWd2LTQiXSwgImlhdCI6ICIxNzE1Njk0MjUzIiwgImV4cCI6ICIxNzE1Njk0MjYzIiwgIl9zZF9hbGciOiAic2hhLTI1NiJ9.0EXb6QCwNL19ZWieDHDWZsm2W_bO2tCH8QBr1ftcTFh2t2P77qEimYjrattAHMah5FPAD3otdDARzh4DfWcuVg~WyJrLTRFYVpwQWctMTdRbk1mT3dNYk93IiwgInNoYXJlQWNjZXNzRGF0YSIsIFt7Ii4uLiI6ICJFRXNfNWVmWUN5WVNjaDB6ZTJKZ1VsV0VpSVhzcTZic1o4UXFBdnlqZXVNIn0sIHsiLi4uIjogIkZfLTZuc0RDT0NvSmNOS2ZhODdWZ0FNVFRzODdLRjN6WXlzbUpnQzF3ckUifV1d~WyJMUTN0eUxONHZVbDRFakR0ekdmRVFnIiwgeyJzZXJ2ZXJCYXNlVVJMIjogImh0dHBzOi8vY2RvYy1jY3MucmlhLmVlOjQ0My9rZXktc2hhcmVzLyIsICJzaGFyZUlkIjogIjlFRTkwRjJELUQ5NDYtNEQ1NC05QzNELUY0QzY4RjdGRkFFMyIsICJzZXJ2ZXJOb25jZSI6ICI0MiJ9XQ~
```

if we decode the individual parts, we get the following pieces.

1. Protected header:

```json
{
    "alg": "ES256",
    "typ": "vnd.cdoc2.auth-token.v1+sd-jwt",
}
```

2. Protected payload:

```json
{
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

4. Salt/Value Container with salts and hashes:
   
```json
[
    "k-4EaZpAg-17QnMfOwMbOw",
    "aud",
    [
        ...
    ]
]
```

5. Disclosures:

```json
[
    "LQ3tyLN4vUl4EjDtzGfEQg",
    {
        ...
    }
]
```

### Verifying SD-JWT (verifying authentication ticket)

CSS server receives the compact SD-JWT presentation (`<Issuer-signed JWT>~<Disclosure 1>~`) and performs following authentication and authorization checks:

1. Verify that SD-JWT is signed by the key pair, whose public key is included in the X.509 certificate, which is transmitted in the API method "GET /key-shares/{shareId}" parameter "x-cdoc2-auth-x5c".
2. Verify that certificate is issued by trustworthy CA.
3. Verify that certificate is valid at current point of time and is not revoked.
4. Verify that SD-JWT contains claim `aud`, which is an array, which contains exactly one JSON string.
5. Parse the `aud` value (something like "https://CSS.example-org1.ee:443/key-shares/9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3?nonce=59b314d4815f21f73a0b9168cecbd5773cc694b6") into components `serverBaseURL`, `shareId` and `nonce`.
6. Verify that `serverBaseURL` is correct for this CSS server.
7. Verify that this CSS server has a Capsule with identifier `shareId` and it is not expired or deleted.
8. Verify that this CSS server has previously generated a nonce for this `shareId` and the stored nonce value matches with `nonce` component value and that nonce wasn't generated too long ago (configuration parameter, for example 300 seconds).
9. Verify that `recipient_id` from the `KeySharesCapsule` matches with the `subjectDN` from the X.509 certificate from API parameter "x-cdoc2-auth-x5c".

If all checks are positive, then the authentication and access control decision is successful and CSS server can return the capsule.
