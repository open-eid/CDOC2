
# CDOC2 authentication protocol to multiple servers

## Requirements

1. Multiple CCSs (CDOC2 Capsule Servers) hold Capsules, which need to be downloaded by Client.
2. Client need to authenticate to multiple CCSs, in order to download all Capsules.
3. Client can only create one signature with its authentication means (ID-card, Mobile-ID, Smart-ID)
4. CCS must not be able to replay the authentication ticket to another CCS.

## General protocol flow

1. Client retrieves the list of `serverBaseURL` and `shareId` from header of CDOC2 Container
2. Client connects to every server and exchanges `shareId` with `serverNonce`. Every server will reply with different `serverNonce`.
3. Client constructs authentication data to be signed with authentication means.
4. Client signs the data and creates the authentication signature.
5. Client constructs a list of authentication tickets from authentication data and authentication signature, so that every server will have different ticket.
6. Client sends ticket to server, server validates the ticket, makes authentication decision, makes access control decision and gives back the capsule content.

## Authentication data

Let's say that Client will sign the following set of JWT claims with their authentication means (ID- card, Mobile-ID, Smart-ID):

```json
{
    "CDOC2_token_type": "CTS authentication token v0.1",
    "iss": "etsi/PNOEE-48010010101",
    "shareAccessData": [
        {   
            "serverBaseURL": "https://cdoc-ccs.ria.ee:443/key-shares/",
            "shareId": "9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3",
            "serverNonce": "59b314d4815f21f73a0b9168cecbd5773cc694b6"
        },
        {
            "serverBaseURL": "https://cdoc-ccs.smit.ee:443/key-shares/",
            "shareId": "5BAE4603-C33C-4425-B301-125F2ACF9B1E",
            "serverNonce": "9d23660840b427f405009d970d269770417bc769"
        }
    ]
}
```

If user would create (in JWT and SD-JWT terminology, "issue") an ordinary JWT with these claims, the resulting thing would look something like that:

```text
eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9
.
eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFtcGxlLmNvbS9pc19yb290Ijp0cnVlfQ
.
dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

It contains following sections, separated by periods (".")

1. first section is base64 encoded JOSE header (something like `{"typ":"JWT", "alg":"HS256"}`)
2. second section is base64 encoded JWT claims
3. third section is base64 encoded signature value

In the next section, we will explain how to use SD-JWT  to only disclose those elements of the `shareAccessData` array to CCS servers, which are necessary and prevent the replay possibility.

## Intro to SD-JWT standard

SD-JWT standard (<https://sdjwt.js.org>, <https://datatracker.ietf.org/doc/draft-ietf-oauth-selective-disclosure-jwt/>) _defines a mechanism for selective disclosure of individual elements of a JSON object used as the payload of a JSON Web Signature (JWS) structure_. It assumes a ecosystem with following entities:

1. SD-JWT is created by an entity called _Issuer_. Issuer decides, what claims are included in SD-JWT and which claims are individually disclosable. Issuer signs the SD-JWT with its key pair and this way secures the SD-JWT against modifications.
2. SD-JWT is received from Issuer by entity called _Holder_. Holder decides when and where to present the SD-JWT and also decides, which disclosable claims it wishes to reveal and which one it wishes to keep secret.
3. SD-JWT is presented to an entity called _Verifier_. Verifier requests SD-JWT from Holder, checks the Issuer signature and extracts the list of claims from SD-JWT.

We are mapping those SD-JWT-specific entities to CDOC2 world in the following way:

1. SD-JWT data structure is used as both CDOC2 authentication data and CDOC2 authentication signature. In other words, information that is used to create authentication data and authentication signature, is expressed (encoded) as SD-JWT structure. Authentication signature corresponds to Issuer signature.
2. SD-JWT presentation with selectively disclosed claims is used as server-specific CDOC2 authentication ticket.
3. Roles of SD-JWT Issuer and SD-JWT Holder is performed by CDOC2 Client. Client creates the SD-JWT structure, specifies that some claims are disclosable and later creates specific presentations to each CCS server. SD-JWT standard optionally supports the scenario when Holder has its own key pair (separate from Issuer's key pair) and it is possible to verify this key binding during the SD-JWT presentations. In CDOC2 system, we don't use Holder's key binding feature.
4. Role of SD-JWT Verifier is performed by CCS servers. Servers will provide Client with nonces and verify that they will receive a valid signed SD-JWT with server-specific nonce as disclosable claim.

## SD-JWT and selective disclosures

How does this "selective disclosure" magic actually work behind the scenes? The idea is that Issuer will create special kind of `SD-CLAIMS` data items in the ordinary JWT, which are:

```text
SD-CLAIMS = (
    CLAIM-NAME: HASH(SALT | CLAIM-VALUE)
)*
```

where `SALT` is a random salt. This kind of operation effectively "hides" the `CLAIM-VALUE`. But, it allows Verifier to check if the digest was computed from the correct value, if he is provided with the salt and clear-text claim value. Such kind of `SD-CLAIMS` are included in the standard JWT structure, in a special structure, within claim name `_sd`.

In order to reveal the `CLAIM-VALUE` to Verifier, Holder needs to create `SD-RELEASES`, which are:

```text
SD-RELEASES = (
    CLAIM-NAME: (DISCLOSED-SALT, DISCLOSED-VALUE)
)
```

and include such info in a special structure in the JWT, with claim name `sd_release`. So, for example, if the original set of claims are following:

```json
{
  "sub": "6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "given_name": "John",
  "family_name": "Doe",
}
```

Let's say that the Issuer wishes to make claim `given_name` disclosable. It generates a random salt and computes digest value from `SHA-256("eluV5Og3gSNII8EYnsxA_A" + "John")` and includes this value in `_sd` structure:

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

However, this "compact"-encoded JWT doesn't yet contain random salt values. So, SD-JWT Salt/Value Container (SVC) is also added:

```json
{ 
  [
    "given_name": "[\"eluV5Og3gSNII8EYnsxA_A\", \"John\"]",
  ]
}
```

and it is encoded in Base64 and added to the original encoded JWT, after yet another period ("."):

```text
<JWT_header>.<JWT_payload>.<JWT_signature>.<SD-JWT SVC>
```

Now, Holder can decide which disclosable claim information from the SVC it will include, when creating a presentation to Verifier, and which it removes. The signature of the original JWT is still valid, because original JWT will be unchanged.

## Creating SD-JWT structure (authentication data and authentication signature)

1. Client creates an SD-JWT with following header:

```json
{
    "typ": "vnd.cdoc2.CTS-auth-token.v1+sd-jwt",
    "alg": "ES256",
    "x5c": "base64 encoded certificate chain with user's certificate"
}
```

2. and initialises empty SD-JWT payload structure and adds following always-disclosed claims to SD-JWT payload:

```json
    "iat": "1715694253",
    "exp": "1715694293"
```

TODO: Add the OCSP response about certificate validity as well?

TODO: other useful claims?

2. Client adds to SD-JWT structure the following disclosable object:

```json
    "shareAccessData": []
```

3. Client adds disclosable JSON structure objects to the disclosable array `shareAccessData` for each capsule that it wishes to download from CCS servers. For example, the structure may contain following info:

```json
{
    "serverBaseURL": "https://cdoc-ccs.ria.ee:443/key-shares/",
    "shareId": "9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3",
    "serverNonce": "649a44d6cd9827cae3f3df04fd5eda98246d2dde"
}
```

4. Client signs the SD-JWT structure as SD-JWT Issuer with its authentication means.

## Presenting SD-JWT (creating authentication ticket)

For each server, Client creates SD-JWT presentation and discloses only the corresponding JSON structure object, which contains the `shareId` and `serverNonce`, specific to that server.

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
    "typ": "example+sd-jwt",
    "x5c": "MIIC8TCCAdmgA...Vt5432GA=="
}
```

2. Protected payload:

```json
{
    "_sd": [
        "1STjFlBH6jmF270Ify2StXnMzZ2TDrIKJX5By65gv-4"
    ],
    "_sd_alg": "sha-256",
    "exp": "1715694263",
    "iat": "1715694253"
}
```

3. Binary signature:
   
```text
0EXb6QCwNL19ZWieDHDWZsm2W_bO2tCH8QBr1ftcTFh2t2P77qEimYjrattAHMah5FPAD3otdDARzh4DfWcuVg
```

4. SVC container with salts and hashes:
   
```json
[
    "k-4EaZpAg-17QnMfOwMbOw",
    "shareAccessData",
    [
        {
            "...": "EEs_5efYCyYSch0ze2JgUlWEiIXsq6bsZ8QqAvyjeuM"
        },
        {
            "...": "F_-6nsDCOCoJcNKfa87VgAMTTs87KF3zYysmJgC1wrE"
        }
    ]
]
```

5. Disclosures:

```json
[
    "LQ3tyLN4vUl4EjDtzGfEQg",
    {
        "serverBaseURL": "https://cdoc-ccs.ria.ee:443/key-shares/",
        "serverNonce": "42",
        "shareId": "9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3"
    }
]
```

## Verifying SD-JWT (verifying authentication ticket)

CCS server receives the compact SD-JWT presentation (`<Issuer-signed JWT>~<Disclosure 1>~`) and performs following checks:

1. Verify that SD-JWT is signed by the key pair, whose public key is included in the certificate, presented in the SD-JWT header claim `x5c`.
2. Verify that certificate is issued by trustworthy CA.
3. Verify that certificate is valid at current point of time and is not revoked.
4. Verify that SD_JWT contains claims `iat` and `exp` and current point of time is between those timestamps.
5. Verify that SD-JWT contains claim `shareAccessData`, which is an array, which contains one JSON structure with following claims: `serverBaseURL`, `shareId` and `serverNonce`.
6. Verify that `serverBaseURL` is correct for this CCS server.
7. Verify that this CCS server has a share with identifier `shareId` and it is not expired or deleted.
8. Verify that this CCS server has previously generated a nonce for this `shareId` and the nonce value matches with `serverNonce` claim value.
9. Verify that `RecipientInfo` from the capsule matches with the subjectInfo from the certificate. (TODO: Is `RecipientInfo` the correct field name?)

If all checks are positive, then the authentication and access control decision is successful and CCS server can return the capsule.
