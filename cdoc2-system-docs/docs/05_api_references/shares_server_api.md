# API Reference for shares server

CDOC2 API References are available at the Open Electronic Identity GitHub [CDOC2 Openapi repo](https://github.com/open-eid/cdoc2-openapi)

[Shares Server Openapi spec](https://github.com/open-eid/cdoc2-openapi/blob/develop/cdoc2-key-shares-openapi.yaml)

## API usage samples

### Add Key Share

Request:

```
POST /key-shares
Content-Type: application/json
x-expiry-time: 2026-08-10T00:00:00Z

{
  "share": "c2FtcGxlLWtleS1zaGFyZS1kYXRhLWJhc2U2NC1lbmNvZGVkLXBheWxvYWQ=",
  "recipient": "etsi/PNOEE-48010010101"
}
```

Response:

```
HTTP/1.1 201 Created
Location: /key-shares/9a7c3717d21f5cf19d18fa4fa5adee21
x-expiry-time: 2026-08-10T00:00:00Z
x-expiry-time-adjusted: true
```

### Get Key Share

Request:

```
GET /key-shares/9a7c3717d21f5cf19d18fa4fa5adee21
x-cdoc2-auth-token: eyJhbGciOiJFUzI1NiIsInR5cCI6InZjK3NkLWp3dCJ9...~WyJzYWx0IiwgImNsYWltIiwgInZhbHVlIl0
x-cdoc2-auth-x5c: MIIFijCCBHKgAwIBAgIJAL3NmQGsd536MA0GCSqGSIb3DQEBCwUAMC8...
x-cdoc2-session-token: eyJhbGciOiJFUzI1NiIsInR5cCI6InZjK3NkLWp3dCJ9...~WyJzYWx0IiwgInNlc3Npb24iLCAidmFsdWUiXQ
x-cdoc2-session-x5c: MIIFijCCBHKgAwIBAgIJAL3NmQGsd536MA0GCSqGSIb3DQEBCwUAMC8...
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json
x-expiry-time: 2026-08-10T00:00:00Z

{
  "share": "c2FtcGxlLWtleS1zaGFyZS1kYXRhLWJhc2U2NC1lbmNvZGVkLXBheWxvYWQ=",
  "recipient": "etsi/PNOEE-48010010101"
}
```

### Create Nonce for a Share

Request:

```
POST /key-shares/9a7c3717d21f5cf19d18fa4fa5adee21/nonce
x-cdoc2-session-token: eyJhbGciOiJFUzI1NiIsInR5cCI6InZjK3NkLWp3dCJ9...
x-cdoc2-session-x5c: MIIFijCCBHKgAwIBAgIJAL3NmQGsd536MA0GCSqGSIb3DQEBCwUAMC8...
Content-Type: application/json

{}
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "nonce": "aZ9kLp3qXwT7"
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
    "artifact": "cdoc2-shares-server",
    "name": "cdoc2-shares-server",
    "time": "2026-05-29T07:21:23.869Z",
    "version": "0.6.0",
    "group": "ee.cyber.cdoc2"
  },
  "system.time": "2026-05-29T07:22:50Z"
}
```
