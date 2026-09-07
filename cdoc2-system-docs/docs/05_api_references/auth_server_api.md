# API Reference for auth server

CDOC2 API References are available at the Open Electronic Identity GitHub [CDOC2 Openapi repo](https://github.com/open-eid/cdoc2-openapi)

[Authentication Server Openapi Spec](https://github.com/open-eid/cdoc2-openapi/blob/develop/cdoc2-auth-server-openapi.yaml)

## API usage samples

### Start Auth Process

Request:

```
POST /auth/start
Content-Type: application/json

{
  "identifier": "etsi/PNOEE-48010010101",
  "mobileNr": "+3726234566",
  "language": "en"
}
```

Response:

```
HTTP/1.1 201 Created
Location: /auth/status/9a7c3717d21f5cf19d18fa4fa5adee21
Content-Type: application/json

{
  "vc": "5702"
}
```

### Get Auth Process Status

Request:

```
GET /auth/status/9a7c3717d21f5cf19d18fa4fa5adee21
```

Response — In Progress:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "PENDING"
}
```

Response — Complete/OK:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "COMPLETE",
  "endResult": "OK",
  "sessionToken": "eyJhbGciOiJFUzI1NiIsInR5cCI6InZjK3NkLWp3dCJ9...~WyJzYWx0IiwgImNsYWltIiwgInZhbHVlIl0",
  "signingCertificate": "MIIFijCCBHKgAwIBAgIJAL3NmQGsd536MA0GCSqGSIb3DQEBCwUAMC8tYQmVzUdt0..."
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
    "artifact": "cdoc2-auth-server-webapp",
    "name": "cdoc2-auth-server-webapp",
    "time": "2026-05-29T07:21:23.869Z",
    "version": "0.6.0",
    "group": "ee.cyber.cdoc2"
  },
  "system.time": "2026-05-29T07:22:50Z"
}
```
