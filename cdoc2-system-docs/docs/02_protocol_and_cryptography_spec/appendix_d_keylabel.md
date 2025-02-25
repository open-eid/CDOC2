# Appendix D: KeyLabel field specification

`KeyLabel` field specification lists the following fields.

Implementers may define their own vendor-specific field specification, but it's recommended to share it publicly.

## Versioning

In current specification `type` and `v` fields are required, rest of fields are `type` specific. `type` and `v` together define a KeyLabel type.

`v` describes type version. Version should only increase when there are breaking changes to type (basically define a new type). Adding/removing optional fields doesn't increase the version.

Required fields are required only for UI. When `KeyLabel` parsing fails, then CDOC2 decryption should still succeed as required fields for decryption are in `FlatBuffers` structure.

Exception to this (decryption should succeed without `KeyLabel`) is symmetric key, when there is more than 1 symmetric key recipient in CDOC2 header (key label needs to be unique to differentiate between symmetric key recipients).

## eID v1

| field         | description                                                       | example                          | required | comments       |
|---------------|-------------------------------------------------------------------|----------------------------------|----------|----------------|
| v             | Version                                                           | 1                                | X        |                |
| type          | eID type: `ID-card` or `Digi-ID` or `Digi-ID E-RESIDENT`          | ID-card                          | X        |                |
| cn            | Recipient common name as it is appears in certificate             | JÕEORG,JAAK-KRISTJAN,38001085718 | X        |                |
| serial_number | SerialNumber as it appears in LDAP server                         | PNOEE-38001085718                | X        |                |
| last_name     | Recipient last name                                               | Jõeorg                           |          |                |
| first_name    | Recipient first name                                              | Jaak-Kristjan                    |          |                |
| server_exp    | Set expiration date in capsule server as Unix timestamp (seconds) | 1730992802                       |          | Added 18.11.24 |

## Certificate from file v1 (type=cert)

| field      | description                                                       | example                                  | required | comments       |
|------------|-------------------------------------------------------------------|------------------------------------------|----------|----------------|
| v          | Version                                                           | 1                                        | X        |                |
| type       | Certificate from file                                             | cert                                     | X        |                |
| file       | Recipient x509 certificate file                                   | 37101010021_cert.pem                     |          |                |
| cn         | Common Name from certificate                                      | ŽAIKOVSKI,IGOR,37101010021               |          |                |
| cert_sha1  | Certificate SHA1 Fingerprint                                      | 7F193CBFFA6A8D52C710FE961077817567449C59 |          |                |
| server_exp | Set expiration date in capsule server as Unix timestamp (seconds) | 1730992802                               |          | Added 18.11.24 |

## Public key from file v1 (type=pub_key)

| field | description                                                           | example          | required | comments         |
|-------|-----------------------------------------------------------------------|------------------|----------|------------------|
| v     | Version                                                               | 1                | X        |                  |
| type  | Public key from file                                                  | pub_key          | X        |                  |
| file  | Public key input file                                                 | bob_pub.pem      |          |                  |
| label | label to identify public key from other keys, user-given or generated | file:bob_pub.pem |          | Addeded 18.11.24 |

## Symmetric key v1 (type=secret)

| field | description                                                              | example     | required |
|-------|--------------------------------------------------------------------------|-------------|----------|
| v     | Version                                                                  | 1           | X        |
| type  | symmetric key                                                            | secret      | X        |
| label | label to identify symmetric key from other keys, user-given or generated | yHqkRsP3kbQ | X        |
| file  |                                                                          |             |          |

## Password v1 (type=pw)

| field | description                                                              | example | required |
|-------|--------------------------------------------------------------------------|---------|----------|
| v     | version                                                                  | 1       | X        |
| type  | user-given password                                                      | pw      | X        |
| label | label to identify password from other passwords, user-given or generated | Arno    | X        |

## Smart-ID/Mobile-ID v1 (type=auth)

| field | description                | example(s)                | required |
|-------|----------------------------|------------------------|----------|
| v     | Version                    | 1                      | X        |
| type  | Smart-ID/Mobile-ID         | auth                   | X        |
| sn    | Serial number - could be a (national) personal number or [private company issuer identifier](ch05_shares_server.md#private-company-issuer-identifier) | ETSI:PNOEE-48010010101 ; private/vnd/serial | X        |
