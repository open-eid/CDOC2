# API Reference for capsule server

CDOC2 API References are available at the Open Electronic Identity GitHub [CDOC2 Openapi repo](https://github.com/open-eid/cdoc2-openapi)

[Capsule Server Opeanapi spec](https://github.com/open-eid/cdoc2-openapi/blob/develop/cdoc2-key-capsules-openapi.yaml)

## API usage samples

### Create Capsule

Request:

```
POST /key-capsules
Content-Type: application/json
x-expiry-time: 2026-08-10T00:00:00Z

{
"recipient_id": "BHy8k3F2v9pQmR7tL4nW1cXeZ0aB8dY6gH3jK5mN2pQ7rS9tU1vW3xY5zA7bC9dE1fG3hJ5kL7mN9pQ==",
"ephemeral_key_material": "BAy8k3F2v9pQmR7tL4nW1cXeZ0aB8dY6gH3jK5mN2pQ7rS9tU1vW3xY5zA7bC9dE1fG3hJ5kL7mN9pQ==",
"capsule_type": "ecc_secp256r1"
}
```

Response:

```
HTTP/1.1 201 Created
Location: /key-capsules/KC0123456789ABCDEF
x-expiry-time: 2026-08-10T00:00:00Z
x-expiry-time-adjusted: false
```

### Retrieve Capsule

Request:

```
GET /key-capsules/KC0123456789ABCDEF
```

Response:

```
HTTP/1.1 200 OK
Content-Type: application/json
x-expiry-time: 2026-08-10T00:00:00Z

{
  "recipient_id": "BHy8k3F2v9pQmR7tL4nW1cXeZ0aB8dY6gH3jK5mN2pQ7rS9tU1vW3xY5zA7bC9dE1fG3hJ5kL7mN9pQ==",
  "ephemeral_key_material": "BAy8k3F2v9pQmR7tL4nW1cXeZ0aB8dY6gH3jK5mN2pQ7rS9tU1vW3xY5zA7bC9dE1fG3hJ5kL7mN9pQ==",
  "capsule_type": "ecc_secp256r1"
}
```
