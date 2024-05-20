
# CDOC2 authentication protocol to multiple servers

## Requirements

1. Multiple CCSs (CDOC2 Capsule Servers) hold Capsules, which need to be downloaded by Client.
2. Client need to authenticate to multiple CCSs, in order to download all Capsules.
3. Client can only create one signature with its authentication means (ID-card, Mobile-ID, Smart-ID)
4. CCS must not be able to replay the authentication ticket to another CCS.

## General protocol flow

1. Client retrieves the list of `serverID` and `capsuleID` from header of CDOC2 Container
2. Client connects to every server and exchanges `capsuleID` with `serverNonce`. Every server will reply with different `serverNonce`.
3. Client constructs authentication data to be signed with authentication means.
4. Client signs the data and creates the authentication signature.
5. Client constructs a list of authentication tickets from authentication data and authentication signature, so that every server will have different ticket.
6. Client sends ticket to server, server validates the ticket, makes authentication decision, makes access control decision and gives back the capsule content.

## Authentication data

Let's say that Client will sign the following set of JWT claims with their authentication means:

```json
{
    "CDOC2_token_type": "CTS authentication token v0.1",
    "iss": "etsi/PNOEE-48010010101",
    "capsule_access_data": [
        {   
            "serverURL": "https://cdoc.ria.ee:443/capsules",
            "capsuleID": "9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3",
            "serverNonce": "59b314d4815f21f73a0b9168cecbd5773cc694b6"
        },
        {
            "serverURL": "https://cdoc.smit.ee:443/capsules",
            "capsuleID": "5BAE4603-C33C-4425-B301-125F2ACF9B1E",
            "serverNonce": "9d23660840b427f405009d970d269770417bc769"
        }
    ]
}
```

If user would create (in JWT and SDJWT terminology, "issue") an ordinary JWT with these claims, the resulting thing would look something like that:

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

In the next section, we will explain how to use SD-JWT  to only disclose those elements of the `capsule_access_data` array to CCS servers, which are necessary and prevent the replay possibility.

## Intro to SD-JWT standard

SD-JWT standard (<https://sdjwt.js.org>, <https://datatracker.ietf.org/doc/draft-ietf-oauth-selective-disclosure-jwt/>) _defines a mechanism for selective disclosure of individual elements of a JSON object used as the payload of a JSON Web Signature (JWS) structure_. It assumes a ecosystem with following entities:

1. SD-JWT is created by an entity called "Issuer". Issuer decides, what claims are included in SD-JWT, which claims are individually disclosable. Issuer signs the SD-JWT with its key pair and secures the SD-JWT against modifications.
2. SD-JWT is received from Issuer by entity called "Holder". Holder decides when and where to present the SD-JWT and also decides, which disclosable claims it wishes to reveal and which one it wishes to keep secret.
3. SD-JWT is presented to an entity called "Verifier". Verifier requests SD-JWT from Holder and checks and extracts the list of claims from SD-JWT.

We are mapping those SD-JWT specific entities to CDOC2 world in the following way:

1. SD-JWT data structure is used as both CDOC2 authentication data and CDOC2 authentication signature, in other words, information that is used to create authentication data and authentication signature, is expressed as SD-JWT structures.
2. SD-JWT presentation with selectively disclosed claims is used as server-specific CDOC2 authentication ticket.
3. Roles of SD-JWT Issuer and SD-JWT Holder is performed by CDOC2 Client. Client creates the SD-JWT structure, specifies that some claims are disclosable and later creates specific presentations to each CCS server. SD-JWT standard optionally supports the scenario when Holder has its own key pair and it is possible to verify this key binding during the SD-JWT presentations. In CDOC2 system, we don't use Holder key binding.
4. Roles of SD-JWT Verifiers is performed by CCS servers. Servers will provide Client with nonces and verify that they will receive a valid signed SD-JWT with server-specific nonce as disclosable claim.

## Creating SD-JWT structure (authentication data and authentication signature)

1. Client creates an empty SD-JWT structure and adds following always-disclosed claims:

```json
    "CDOC2_token_type": "CTS authentication token v0.1",
    "iss": "etsi/PNOEE-48010010101",
    "iat": "1715694253",
    "exp": "1715694293"
```
TODO: Perhaps we should use official JWT header "typ" claims instead, because [SD-JWT section 10.12](https://www.ietf.org/archive/id/draft-ietf-oauth-selective-disclosure-jwt-08.html#name-explicit-typing) recommends applications to invent their own values, like "application/example+sd-jwt" be used, where "example" is replaced by the identifier for the specific kind of SD-JWT. So, perhaps something like `cdoc2-auth-token+sd-jwt`. Still, how about versioning?

TODO: Somehow, client needs to express what is the certificate that it was using. Can we use "x5c" claim? <https://mojoauth.com/glossary/jwt-x.509-certificate-chain/>

TODO: Add the OCSP response about certificate validity as well?

TODO: other useful claims?

2. Client adds to SD-JWT structure the following disclosable object:

```json
    "capsule_access_data": []
```

3. Client adds disclosable JSON structure objects to the disclosable array `capsule_access_data` for each capsule that it wishes to download from CCS servers. For example, the structure may contain following info:

```json
{
    "serverURL": "https://cdoc.ria.ee:443/capsules",
    "capsuleID": "9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3",
    "serverNonce": "649a44d6cd9827cae3f3df04fd5eda98246d2dde"
}
```

TODO: is this enough? Too much? Do we wish to use `serverID` instead?

4. Client signs the SD-JWT structure as SD-JWT Issuer with its authentication means.

## Presenting SD-JWT (creating authentication ticket)

For each server, Client creates SD-JWT presentation and discloses only the corresponding JSON structure object, which contains the `capsuleID` and `serverNonce`, specific to that server.

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
eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0In0.eyJfc2QiOiBbIl9URVhpZmkzZF9OdzRGYjNjOVI5WjN1ZGpVTTFGNTFIdWozeUkwOEsxbnMiXSwgIkNET0MyX3Rva2VuX3R5cGUiOiAiQ1RTIGF1dGhlbnRpY2F0aW9uIHRva2VuIHYwLjEiLCAiaXNzIjogImV0c2kvUE5PRUUtNDgwMTAwMTAxMDEiLCAiaWF0IjogIjE3MTU2OTQyNTMiLCAiX3NkX2FsZyI6ICJzaGEtMjU2In0.pXgj9fqVtplw8k9W7Lqn7PTg8JFkbB7AeoEQK83FRTLLqnHJ1PorL4M32o2iurqA6JVlg6ijDDCKAqLuPmRnwA~WyJtQy1CcC1GSUszQUVxSVJQZG1IeWF3IiwgImNhcHN1bGVfYWNjZXNzX2RhdGEiLCBbeyIuLi4iOiAiaEN3bFh2c1RNc21mTEI1Y2k3ckpaczgwazk0d014M2o2LXVUMTFhOWNMQSJ9LCB7Ii4uLiI6ICJYRGJnQm1IbDZkdkRHTERheVprNnVQNFRGT2F4RDdKeG9BdUxCb21WdmZjIn1dXQ~WyJBcmtKUHJrN0hGWXI4dl9FQmNrdEF3IiwgeyJzZXJ2ZXJVUkwiOiAiaHR0cHM6Ly9jZG9jLnJpYS5lZTo0NDMvY2Fwc3VsZXMiLCAiY2Fwc3VsZUlEIjogIjlFRTkwRjJELUQ5NDYtNEQ1NC05QzNELUY0QzY4RjdGRkFFMyIsICJzZXJ2ZXJOb25jZSI6ICI0MiJ9XQ~
```

## Verifying SD-JWT (verifying authentication ticket)

CCS server receives the compact SD-JWT presentation (`<Issuer-signed JWT>~<Disclosure 1>~`) and performs following checks:

1. Verify that SD-JWT is signed by the key pair, whose public key is included in the certificate, presented in the SD-JWT claim `x5c`.
2. Verify that certificate is issued by trustworthy CA
3. Verify that certificate is valid at current point of time and is not revoked.
4. Verify that SD_JWT contains claims `iat` and `exp` and current point of time is between those timestamps.
5. Verify that SD-JWT contains claim `iss` and the personal code is the same as within the `x5c` certificate (TODO: This is actually redundant. Perhaps we can drop the `iss` claim?)
6. Verify that SD-JWT contains claim `capsule_access_data`, which is an array, which contains a single JSON structure with the following claims: `serverURL`, `capsuleID` and `serverNonce`.
7. Verify that `serverURL` is correct for this CCS server.
8. Verify that this CCS server has `capsuleID` and it is not expired or deleted.
9. Verify that this CCS server has previously generated a nonce for this `capsuleID` and the nonce value matches with `serverNonce` claim value.
10. Verify that `RecipientInfo` from the capsule matches with the subjectInfo from the certificate. (TODO: Is `RecipientInfo` the correct field name?)

If all checks are positive, then the authentication and access control decision is successful and CCS server can return the capsule.