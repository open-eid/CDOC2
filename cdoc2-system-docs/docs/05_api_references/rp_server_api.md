# API Reference for RP server

CDOC2 API References are available at the Open Electronic Identity GitHub [CDOC2 Openapi repo](https://github.com/open-eid/cdoc2-openapi)

[Relying Party Server Openapi spec](https://github.com/open-eid/cdoc2-openapi/blob/develop/cdoc2-rp-server-openapi.yaml)

## API usage samples

### Start Smart-ID Authentication

Request:

```
POST /sid/authenticate
x-cdoc2-session-token: eyJhbGciOiJFUzI1NiIsInR5cCI6InZjK3NkLWp3dCJ9...
x-cdoc2-session-x5c: MIIFijCCBHKgAwIBAgIJAL3NmQGsd536MA0GCSqGSIb3DQEBCwUAMC8...
Content-Type: application/json

{
  "semanticsIdentifier": "PNOEE-30001010004",
  "certificateLevel": "QUALIFIED",
  "signatureProtocol": "ACSP_V2",
  "signatureProtocolParameters": {
    "rpChallenge": "S480uRoCX4pAb1tWqAy8WGl/AWE1RnqaP2y5iamCDhlCyQrMTVa5d8Dh34sZ+UePHXRNKTwz7QTvsIL1ls05AQ==",
    "signatureAlgorithm": "rsassa-pss",
    "signatureAlgorithmParameters": {
      "hashAlgorithm": "SHA-512"
    }
  },
  "interactions": "W3sidHlwZSI6ImNvbmZpcm1hdGlvbk1lc3NhZ2UiLCJkaXNwbGF5VGV4dDIwMCI6IkRlY3J5cHRpbmcgY29udGFpbmVyIGZpbGUgXCJ0ZXN0LnR4dFwiIn1d",
  "vcType": "numeric4"
}
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "sessionID": "7f2e9c1a-3b4d-4e5f-9a8b-1c2d3e4f5a6b"
}
```

### Poll Smart-ID Session Status

Request:

```
GET /sid/session/7f2e9c1a-3b4d-4e5f-9a8b-1c2d3e4f5a6b
x-cdoc2-session-token: eyJhbGciOiJFUzI1NiIsInR5cCI6InZjK3NkLWp3dCJ9...
x-cdoc2-session-x5c: MIIFijCCBHKgAwIBAgIJAL3NmQGsd536MA0GCSqGSIb3DQEBCwUAMC8...
```

Response — Still Running:

```
HTTP/1.1 200 OK
Content-Type: application/json

{ "state": "RUNNING" }
```

Response — Complete/OK::

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "state": "COMPLETE",
  "result": {
    "endResult": "OK",
    "documentNumber": "PNOEE-30001010004-BVFM-Q"
  },
  "signatureProtocol": "ACSP_V2",
  "signature": {
    "value": "Vak2Q0NiFnh6+lW+YaJuB8yMYM7k3I5QfsUxS3Y1Ddm3qy6HvebLl0/t17dq289/...",
    "serverRandom": "+wVP2U/SMKVkVrggDjNTXFV/",
    "userChallenge": "TLSjYRH2oYw8tW2bq0it0IUb7WIFkCLgF8NTc7-4Zq4",
    "flowType": "Notification",
    "signatureAlgorithm": "rsassa-pss",
    "signatureAlgorithmParameters": {
      "hashAlgorithm": "SHA-512",
      "maskGenAlgorithm": {
        "algorithm": "id-mgf1",
        "parameters": { "hashAlgorithm": "SHA-512" }
      },
      "saltLength": 64,
      "trailerField": "0xbc"
    }
  },
  "cert": {
    "value": "MIIFijCCBHKgAwIBAgIJAL3NmQGsd536MA0GCSqGSIb3DQEBCwUAMC8...",
    "certificateLevel": "QUALIFIED"
  },
  "interactionTypeUsed": "displayTextAndPIN"
}
```

### Start Mobile-ID Authentication

Request:

```
POST /mid/authenticate
x-cdoc2-session-token: eyJhbGciOiJFUzI1NiIsInR5cCI6InZjK3NkLWp3dCJ9...
x-cdoc2-session-x5c: MIIFijCCBHKgAwIBAgIJAL3NmQGsd536MA0GCSqGSIb3DQEBCwUAMC8...
Content-Type: application/json

{
  "phoneNumber": "+3726234566",
  "nationalIdentityNumber": "38412319871",
  "hash": "0nbgC2fVdLVQFZJdBbmG8B+kXnZtX1FSTM59UVDQ4Gc=",
  "hashType": "SHA256",
  "language": "ENG",
  "displayText": "Decrypting container file \"test.txt\"",
  "displayTextFormat": "GSM-7"
}
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "sessionID": "4c1e2a3b-9d7e-4f8a-b2c1-6e5d4f3a2b1c"
}
```

### Poll Mobile-ID Session Status

Request:

```
GET /mid/session/4c1e2a3b-9d7e-4f8a-b2c1-6e5d4f3a2b1c
x-cdoc2-session-token: eyJhbGciOiJFUzI1NiIsInR5cCI6InZjK3NkLWp3dCJ9...
x-cdoc2-session-x5c: MIIFijCCBHKgAwIBAgIJAL3NmQGsd536MA0GCSqGSIb3DQEBCwUAMC8...
```

Response — Still Running:

```
HTTP/1.1 200 OK
Content-Type: application/json

{ "state": "RUNNING" }
```

Response — Complete/OK:

```
HTTP/1.1 200 OK
x-rp-signed-hash: B+C9XVjIAZnCHH9vfBSv...
x-rp-name: cdoc2-RP.example.ee
Signature-Input: sig1=("x-rp-signed-hash" "x-rp-name");created=1715269200;keyid="f4e8b6b4-6a8e-4f77-987c-0957d1dc7f73"
Signature: sig1=:<Base64-encoded-signature>:
Content-Type: application/json

{
  "state": "COMPLETE",
  "result": "OK",
  "signature": {
    "value": "B+C9XVjIAZnCHH9vfBSvXgFN2oT4RuCvYLkE==",
    "algorithm": "SHA256WithECEncryption"
  },
  "cert": "MIIFijCCBHKgAwIBAgIJAL3NmQGsd536MA0GCSqGSIb3DQEBCwUAMC8...",
  "time": "2026-09-07T10:52:20Z",
  "traceId": "d8de38e7bb5d8f8a"
}
```

### Server Info

Request:

```
GET /info
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "build": {
    "artifact": "cdoc2-rp-server-webapp",
    "name": "cdoc2-rp-server-webapp",
    "time": "2026-05-29T07:21:23.869Z",
    "version": "0.6.0",
    "group": "ee.cyber.cdoc2"
  },
  "system.time": "2026-05-29T07:22:50Z"
}
```
