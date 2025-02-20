---
title: Client authentication protocol
---

# Client authentication protocol

This section describes a protocol and data formats for authenticating to multiple CSS servers (cdoc2-shares-servers) in order to download every `KeySharesCapsule` from them.

## Authentication protocol requirements

1. Multiple CSSs hold Capsules, which all need to be downloaded by Client.
2. Client needs to authenticate to multiple CSSs, in order to download all Capsules.
3. Client should only need to create one signature with its authentication means (ID-card, Mobile-ID, Smart-ID) for authentication.
4. CSS must not be able to replay the authentication ticket to another CSS.

## Non-suitable alternatives

Before designing a custom authentication protocol, we should make sure that we cannot re-use existing protocols. Existing protocols may already have proven security properties and they might be well supported by existing software libraries.

For example, traditionally, authentication and authorization processes are handled by OpenID Connect and OAuth2 protocols. They are well studied and robust. However, if we try to apply them to our situation and try to map mandatory roles from OpenID Connect and OAuth2 ecosystems to our components (Client, CSSs), the situation becomes cumbersome.

First, the requirement that Client needs to "login" to multiple servers with single use of user's eID means is difficult to achieve. This is usually handled by a single-sign-on service. There's such a service, called GovSSO (<https://e-gov.github.io/GOVSSO/TechnicalSpecification>), but it is more oriented towards web applications and it is using a generic OpenID Connect protocol without binding the issued `id_tokens` with user's authentication signatures. In case CSS would be accepting such `id_tokens`, there's no cryptographic proof that authentication of the user has actually taken place and that the user's eID means was used. That would mean that the security of such central single-sign-on provider would be critical and in case the security of GovSSO would be breached, it would be able to download every `KeySharesCapsule` on behalf of any user.

Additionally, if we would be using OAuth2 authorization protocols, we would be using OAuth2 "bearer" tokens. This would mean that CSS server can re-use the token and replay it to another CSS server. It might be possible to overcome the threat of token replay with protocols like "OAuth2 Certificate-Bound Access Tokens" (<https://datatracker.ietf.org/doc/html/rfc8705>) and "OAuth2 Demonstrating Proof of Possession" (<https://www.rfc-editor.org/rfc/rfc9449>), but that would require us to create yet another central trusted component which would hand out those access tokens. That kind of component would be a single source of failure and in case the security of such component would be breached, the attacker would be able to download every `KeySharesCapsule` on behalf of any user.

Therefore, introducing additional trusted components to the CDOC2 ecosystem is not desirable at the moment and traditional authentication protocols are not suitable. More tailored approach would be needed to come up with an authentication protocol, that would satisfy all requirements and would depend only on the eID authentication means or eID trust service providers.

## Overview of the generic authentication protocol

In the generalized form, the authentication protocol to access Capsule information at CSS servers, can be explained with the following sequence diagram below.

This is just an abstract overview of the authentication protocol. In following sections, we describe what kind of data is used as the authentication data, how signing function of eID means is used and how only a minimal set of authentication data is revealed to each CSS server, in order to prevent replay.

```plantuml
@startuml
skinparam ParticipantPadding 20
skinparam BoxPadding 30
hide footbox
autonumber

box "User"
Actor Recipient as R
participant "CDOC2 Client" as C
participant "eID means \n (ID-card, Mobile-ID, Smart-ID)" as A
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
C -> C: Create \n authentication data
C -> A: Create signature on \n authentication data
A -> R: Authorize eID use for signature generation
R -> A: Authorized
A --> C: Signature
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

In generic protocol, the Client signs a set of information, which expresses the proof of Recipient's identity, and Recipient's intent to download specific Capsule. We can use the JWT standard (<https://www.rfc-editor.org/rfc/rfc7519.html>) for this. Client will sign the following set of JWT claims with their authentication means (ID- card, Mobile-ID, Smart-ID), using the authentication key pair.

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
2. SD-JWT presentation along with selectively disclosed claims is used as a server-specific CDOC2 authentication ticket.
3. Roles of SD-JWT Issuer and SD-JWT Holder is performed by CDOC2 Client. Client creates SD-JWT structure, specifies that some claims are disclosable and creates specific presentations for each CSS server. SD-JWT standard optionally supports a scenario when Holder has its own key pair (separate from Issuer's key pair) and it is possible to verify the possession of Holder's key pair during the SD-JWT presentations. In CDOC2 system, we don't use Holder's key binding feature.
4. Role of SD-JWT Verifier is performed by CSS servers. Servers will provide Client with nonces and verify that they will receive a valid signed SD-JWT with server-specific nonce as disclosable claim.

### SD-JWT and selective disclosures

How does this "selective disclosure" feature actually work behind the scenes? The idea is that Issuer will create special kind of `SD-CLAIMS` data items in the ordinary JWT, which are:

```text
SD-CLAIMS = (
    CLAIM-NAME: HASH(SALT | CLAIM-VALUE)
)*
```

where `SALT` is a random salt. This kind of operation effectively "hides" the content of the `CLAIM-VALUE`. But, it allows Verifier to check if the digest was computed from the correct value, if they are provided with the values of `SALT` and clear-text `CLAIM_VALUE`. Such kind of `SD-CLAIMS` are included in the JWT structure, inside a special JOSE object with name `_sd`.

In order to reveal the `CLAIM-VALUE` to Verifier, Holder needs to create `SD-RELEASES` data items, which are:

```text
SD-RELEASES = (
    CLAIM-NAME: (DISCLOSED-SALT, DISCLOSED-VALUE)
)
```

and add such data items in the JWT, in a special JOSE object with name `sd_release`.

So, for example, let's take the original set of claims:

```json
{
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "given_name": "John",
  "family_name": "Doe",
}
```

Let's say that the Issuer wishes to make claim `given_name` disclosable. They generate a random salt (e.g., `eluV5Og3gSNII8EYnsxA_`) and compute a digest value `SHA-256("eluV5Og3gSNII8EYnsxA_A" + "John")` and include such `SD_CLAIM` data item in the `_sd` structure:

```json
{
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "family_name": "Doe",
  "_sd_": {
    "given_name": "PvU7cWjuHUq6w-i9XFpQZhjT-uprQL3GH3mKsAJl0e0"
  }
}
```

JWT header and JWT payload is then signed and following JWT is created:

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

It is encoded in Base64 and added to the original encoded JWT, after yet another period ("."):

```text
<JWT_header>.<JWT_payload>.<JWT_signature>.<SD-JWT Salt/Value Container>
```

Now, Holder can decide which disclosable claim information from the `<SD-JWT Salt/Value Container>` they will include, when creating a presentation to Verifier, and which disclosable claims they don't include. The signature of the original JWT is still valid, because original JWT will be unchanged.

### Creating SD-JWT structure (authentication data and authentication signature)

Applying SD-JWT data structure to CDOC2 authentication protocol, we get following specification:

1. Client creates an SD-JWT with following example header:

   ```json
   {
       "typ": "vnd.cdoc2.auth-token.v1+sd-jwt",
       "alg": "ES256",
       "kid": "PNOEE-48010010101"
   }
   ```

   The values for the `alg` claim depend on the signature algorithm that the user's eID means authentication key pair is using. For example, the ID-card produces signatures with ES256 algorithm, Smart-ID produces signatures with RS256 algorithm.

2. Client initialises empty SD-JWT payload structure and adds always-disclosed claims to SD-JWT payload. Example is provided here. Note that the `aud` claim contains only empty array at the moment.

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

4. Client signs the SD-JWT structure (with the header, payload and disclosable claims information in `_sd` structure), as SD-JWT Issuer with user's authentication means.

### Presenting SD-JWT (creating authentication ticket)

For each server, Client creates SD-JWT presentation and discloses only that `aud` array element, which contains `key-share` and `nonce`, which are specific to that server.

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

if we decode the individual parts, we get following data items:

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

CSS server receives compact SD-JWT presentation (`<Issuer-signed JWT>~<Disclosure 1>~`) and performs following authentication and authorization checks:

1. Verify that SD-JWT is signed by the key pair, whose public key is included in the X.509 certificate, which is transmitted in the API method "GET /key-shares/{shareId}" parameter "x-cdoc2-auth-x5c".
2. Verify that certificate is issued by trustworthy CA.
3. Verify that certificate is valid at current point of time and is not revoked.
4. Verify that SD-JWT contains claim `aud`, which is an array, which contains exactly one JSON string.
5. Parse `aud` value (it should be something like "<https://CSS.example-org1.ee:443/key-shares/9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3?nonce=59b314d4815f21f73a0b9168cecbd5773cc694b6>") into components `serverBaseURL`, `shareId` and `nonce`.
6. Verify that `serverBaseURL` is correct for this CSS server.
7. Verify that this CSS server has a Capsule with identifier `shareId` and it is not expired or deleted.
8. Verify that this CSS server has previously generated a nonce for this `shareId` and one of the nonce values matches with `nonce` component value and that nonce wasn't generated too long ago (configuration parameter, for example 300 seconds).
9. Verify that `recipient_id` from the `KeySharesCapsule` matches with the `subjectDN` from the X.509 certificate from API parameter "x-cdoc2-auth-x5c".

If all checks are positive, then the authentication and access control decision is positive and CSS server can return the capsule.

## Security of the protocol

We are analyzing security of the authentication protocol from following aspects.

### Protection against the passive network read

In case the network between the CDOC2 Client and CSS servers is compromised and attacker is able to read network connections, the attacker is simply able to observe the values of the capsule shares as they are downloaded from CSS servers. The authentication protocol itself doesn't have built-in protection against this and assumes that connection from CDOC2 Client to every CSS server is authenticated and transmission is encrypted with HTTPS protocol.

### Protection against the MITM attack with connection hijacking

In case the attacker is able to hijack the network connections between the CDOC2 Client and CSS servers and redirect the connection attempts from the real CSS servers to attacker itself, attacker is also able to masquerade to Client as real CSS server and is also observe the values of the transmitted capsule shares. Attacker might be able to present a self-signed X.509 HTTPS certificate or it might be able to present a valid X.509 HTTPS certificate from the real CA as well. In case the CDOC2 Client doesn't verify the identity of the CSS server, it is not able to tell a difference between the attacker and real CSS server.

It is essential that CDOC2 Clients authenticate, which servers they are connecting to and that they are verifying the HTTPS X.509 certificates against the whitelisted values in the configuration file.

### Protection against compromised CSS servers

In case the attacker has compromised some of the CSS servers, the following attack scenario should be considered.

1. Client connects to CSS-1 and asks for nonce `nonce1`. CSS-1 is controlled by attacker and they return the value of `nonce1`.
2. Client connects to CSS-2 and asks for nonce `nonce2`. CSS-2 is secure and returns the value of `nonce2`.
3. Client creates authentication signature, in the form of issuing SD-JWT.
4. Client creates presentation of SD-JWT for CSS-1 with the disclosure of the value of `nonce1` and sends this to CSS-1. The value of `nonce2` is not revealed.
5. Attacker uses the signed SD-JWT and tries to create another presentations for CSS-2. However, since the attacker doesn't know the salt value and clear-text value of the second component of the `aud` claim, it is not able to create valid presentation.

Therefore, the protocol is secure against compromise of some CSS servers.

### Protection against CSS server compromise and nonce reuse

In case the attacker has compromised some of the CSS servers and tries to confuse Client by mixing nonces from different servers, the following attack scenario should be considered.

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

Even though we have carefully designed the protocol with security requirements in mind and it has been reviewed multiple times and it includes protection against common network attacks, we are not able to prove the security of the solution.

However, we can increase the confidence by using formal analysis methods. We have implemented the protocol flow as a model of ProVerif (<https://bblanche.gitlabpages.inria.fr/proverif/>) tool. ProVerif is an automated verification tool for cryptographic protocols, which works in the formal logic model Dolev-Yao and can mathematically verify and prove, if the protocol has some security properties, such as confidentiality, authentication, etc. Proving such properties may involve finding proof of not-existence of some other property and verification of all possible combinations. Therefore, using manual methods can be very time-consuming and doesn't usually give full confidence.

Model has been presented in appendix A and it verifies the following properties.

1. Described attacker is not able to download shares of capsules from CSS servers:

   ```text
           Query not attacker(capsule[]) is true
   ```

2. Described attacker is not able to authenticate on behalf of the Client:

   ```text
           Query event(FinishHandshake(x1,x2,x3,x4)) ==> 
                   event(StartHandshake(x1,x2,x3,x4)) is true.
   ```

Therefore, the described protocol should be secure against such properties. However, because ProVerif cannot analyse exactly the same CSS and CDOC2 Client source code. Therefore, there might be still unknown vulnerabilities in those areas. Still, this kind of additional formal analysis increases the confidence that protocol design doesn't have major security issues.

### Weakness against MITM signature

In case the MITM attacker has been able to compromise the path between the CDOC2 Client and the user's authentication means (ID-card, Mobile-ID, Smart-ID) and is able to trick user to sign attacker's submitted hash with the user's authentication key pair, it is possible to attack the CDOC2 system.

Following authentication means have this potential weakness:

1. ID-card when used via PKCS#11 interface
2. Mobile-ID REST API
3. Smart-ID RP-API v2

Following authentication means or APIs (some of them are in development) do not have this weakness:

1. ID-card when used via web-eID JS interface
2. Smart-ID RP-API v3

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
