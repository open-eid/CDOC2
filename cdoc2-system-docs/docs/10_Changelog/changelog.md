# CDOC2 Capsule Server changelog

**[1.7] Added support for secp521r1**

* Added support for the elliptic curve secp521r1

**[1.6] Added support for secp256r1**

* Added support for the elliptic curve secp256r1
* Add `x-expiry-time-adjusted` header to `GET /key-capsules/{transactionId}` result as specified in [cdoc2-key-capsules 2.2.0 OAS](https://github.com/open-eid/cdoc2-openapi)
* Changed the behavior of the `x-expiry-time` header in the `POST /key-capsules/{transactionId}`.
  Now if the `x-expiry-time` is larger than the maximum allowed expiry time, then the expiry
  time is set as the maximum allowed value.
  If the expiry time value was adjusted, then the header `x-expiry-time-adjusted` in the endpoint `GET /key-capsules/{transactionId}`
  will be set to `true`.

**[1.5] Add `x-expiry-time` header to `POST /key-capsules/{transactionId}` response**

* Add `x-expiry-time` header to `POST` `/key-capsules/{transactionId}` result as specified in [cdoc2-key-capsules 2.2.0 OAS](https://github.com/open-eid/cdoc2-openapi)

**[1.4] Return `x-expiry-time` header to `GET /key-capsules/{transactionId}`**

* Return `x-expiry-time` header to `GET` `/key-capsules/{transactionId}` as specified in
  [cdoc2-key-capsules 2.1.0 OAS](https://github.com/open-eid/cdoc2-openapi/blob/04eac9013b919c405eee6e88f497897758af29a0/cdoc2-key-capsules-openapi.yaml#L38)

**[1.3] Add new optional HTTP header 'x-expiry-time'**

* Implement '/key-capsules' OAS version 2.1.0 (Support for optional 'x-expiry-time' HTTP header)

**[1.2] Repository split and maintenance**

* Use 'cdoc2' instead of 'cdoc20' everywhere (packages, documents etc). Salt strings remain unchanged (cdoc20kek, cdoc20cek and so)

**[1.1] added re-encrypt functionality**

* Added possibility to encrypt and decrypt CDOC2 container with password.
* Added CDOC2 container re-encryption functionality for long-term cryptography.

**[1.0] First major release**

# CDOC2 schema changes

**[2.1] Added new elliptic cure `secp521r1` to EllipticCurve enum in recipients.fbs**

**[2.0] Added new elliptic cure `secp256r1` to EllipticCurve enum in recipients.fbs**

**[1.4] SID/MID changes to the schema**

* Add Create new tables KeySharesCapsule and KeyShare in recipients.fbs
* Add KeySharesCapsule to Capsule in header.fbs

# cdoc2 key-capsules OAS changelog

**[3.1] Added `ecc_secp521r1` to capsule_type enum**

**[3.0] Added `ecc_secp256r1` to capsule_type enum**

* Added new curve `ecc_secp256r1` to capsule_type enum
* Changed the `recipient_id` `minLength` from 97 to 65
* Made the `capsule_type` a x-extensible-enum

**[2.2] Added new header values to `POST /key-capsules`**

* values `x-expiry-time` and `x-expiry-time-adjusted`
