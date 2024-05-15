
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

In the next section, we will explain how to use SD-JWT (<https://sdjwt.js.org>, <https://datatracker.ietf.org/doc/draft-ietf-oauth-selective-disclosure-jwt/>) to only disclose those elements of the `capsule_access_data` array to CCS servers, which are necessary and prevent the replay possibility.

## SD-JWT model

SD-JWT "defines a mechanism for selective disclosure of individual elements of a JSON object used as the payload of a JSON Web Signature (JWS) structure". It works in the following ecosystem:

1. SD-JWT is created by an entity called "Issuer". Issuer decides, what claims are included in SD-JWT, which claims are individually disclosable. Issuer signs the SD-JWT with its key pair and secures the SD-JWT against modifications.
2. SD-JWT is received from Issuer by entity called "Holder". Holder decides when and where to present the SD-JWT and also decides, which disclosable claims it wishes to reveal and which one it wishes to keep secret. 
3. SD-JWT is presented to an entity called "Verifier". Verifier requests SD-JWT from Holder and checks and extracts the list of claims from SD-JWT.


In CDOC2, we are mapping those entities in the following way:

1. SD-JWT data structure is used as CDOC2 authentication data. Information that is used to create authentication data and authentication signature, is expressed as SD-JWT.
2. SD-JWT presentation with selectively disclosed claims is used as server-specific CDOC2 authentication ticket.
3. Client is performing the actions of both, the Issuer and Holder. Client creates the SD-JWT structure, specifies that some claims are disclosable and later creates specific presentations to each CCS server. SD-JWT standard optionally supports the scenario when Holder has its own key pair and it is possible to verify this key binding during the SD-JWT presentations. In CDOC2 system, we don't use Holder key binding.
4. CCS server is performing the action of Verifier. It will provide Client with nonce and requests SD-JWT and verifies that it has received a valid signed SD-JWT with server-specific nonce as disclosable claim.

## Creating SD-JWT (authentication data and authentication signature)

1. Client creates SD-JWT with following always-disclosed claims:

```json
    "CDOC2_token_type": "CTS authentication token v0.1",
    "iss": "etsi/PNOEE-48010010101",
    "iat": "1715694253"
```

TODO: Somehow, client needs to express what is the certificate that it was using. Can we use "x5c" claim? <https://mojoauth.com/glossary/jwt-x.509-certificate-chain/>

2. Client creates SD-JWT with following disclosable object:

```json
    "capsule_access_data": []
```

3. Client adds following individually disclosable structures to the disclosable array `capsule_access_data` for each capsule that it wishes to download from CCS servers:

```json
{
    "serverURL": "https://cdoc.ria.ee:443/capsules",
    "capsuleID": "9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3",
    "serverNonce": "649a44d6cd9827cae3f3df04fd5eda98246d2dde"
}
```

4. Client signs the SD-JWT with the authentication means.
5. Client creates
