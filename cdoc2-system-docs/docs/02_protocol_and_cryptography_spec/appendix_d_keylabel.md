# Appendix D: Keylabel field specificiation version 1

KeyLabel field specification version 1 lists the following fields.

**Note!** This is work in progress and additional values may be added!
**Note!** V1 doesn't support key managers yet, these may be added once implementation is added.

Implementers may define their own vendor-specific field specification, but its recommended to share it publically.

## eID

| field         | description                                              | example                          | required |
|---------------|----------------------------------------------------------|----------------------------------|----------|
| v             | Version                                                  | 1                                | X        |
| type          | eID type: `ID-card` or `Digi-ID` or `Digi-ID E-RESIDENT` | ID-card                          | X        |
| cn            | Recipient common name as it is appears in certificate    | JÕEORG,JAAK-KRISTJAN,38001085718 | X        |
| serial_number | SerialNumber as it appears in LDAP server                | PNOEE-38001085718                | X        |
| last_name     | Recipient last name                                      | Jõeorg                           |          |
| first_name    | Recipient first name                                     | Jaak-Kristjan                    |          |

## Certificate from file (type=cert)

| field     | description                     | example                                  | required |
|-----------|---------------------------------|------------------------------------------|----------|
| v         | Version                         | 1                                        | X        |
| type      | Certificate from file           | cert                                     | X        |
| file      | Recipient x509 certificate file | 37101010021_cert.pem                     |          |
| cn        | Common Name from certificate    | ŽAIKOVSKI,IGOR,37101010021               |          |
| cert_sha1 | Certificate SHA1 Fingerprint    | 7F193CBFFA6A8D52C710FE961077817567449C59 |          |

## Public key from file (type=pub_key)

| field     | description           | example     | required |
|-----------|-----------------------|-------------|----------|
| v         | Version               | 1           | X        |
| type      | Public key from file  | pub_key     | X        |
| file      | Public key input file | bob_pub.pem |          |

## Symmetric key (type=secret)

| field | description                                                              | example     | required |
|-------|--------------------------------------------------------------------------|-------------|----------|
| v     | Version                                                                  | 1           | X        |
| type  | symmetric key                                                            | secret      | X        |
| label | label to identify symmetric key from other keys, user-given or generated | yHqkRsP3kbQ | X        |
| file  |                                                                          |             |          |

## Password (type=pw)

| field | description                                                              | example | required |
|-------|--------------------------------------------------------------------------|---------|----------|
| v     | version                                                                  | 1       | X        |
| type  | user-given password                                                      | pw      | X        |
| label | label to identify password from other passwords, user-given or generated | Arno    | X        |
