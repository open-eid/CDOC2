# CDOC2 Shares Server changelog

**[0.8.0] Refactoring, dependency updates and test coverage**

* Updated cdoc2-client version
* Updated cdoc2-auth-token version
* Code refinements and test coverage

**[0.7.3] Dependency updates**

* Updated dependencies to latest stable versions
* Migrated code for breaking API changes in Spring Boot `AntPathRequestMatcher` -> `PathPatternRequestMatcher`

**[0.7.2] Test coverage**

* Additional unit tests

**[0.7.1] SBOM creation**

* Use CycloneDX Maven plugin for SBOM creation

**[0.7.0] Key Share expiry**

* Added optional `x-expiry-time` header to `POST` `/key-shares` request. If omitted, key share
  expiry will be determined by a server-configured default value.
* Added optional `x-expiry-time`, `x-expiry-time-adjusted` headers to `POST` `/key-shares`
  response. `x-expiry-time` in response is the actual applied expiry time, which may differ from
  the requested time if the requested time exceeds the servers configured maximum allowable key
  share expiration time. If the server adjusted the expiry time, `x-expiry-time-adjusted` will
  be set to `true`.
* Added `x-expiry-time` header to `GET` `/key-shares/{shareId}` response.
* Added `/info` endpoint.

**[0.6.0]  SID/MID authentication/security improvements**

* Create job for expired session nonce removal
* RFC9421 HTTP signature validation for /key-share/{shareId} endpoint
* Upgraded Spring Boot 4.0.3 -> 4.0.6

**[0.5.0]  SID/MID authentication/security improvements**

* Create new `/session_nonce` endpoint
* Use [cdoc2-auth-token:0.5.0-SNAPSHOT]
* Auth token verification accepts SID RPv3 token signatures
* header `x-cdoc2-auth-ticket` renamed to `x-cdoc2-auth-token`
* header `x-cdoc2-auth-x5c` changed to expect a Base64Url-encoded DER certificate
* new headers `x-cdoc2-session-token`, `x-cdoc2-session-x5c` applied to endpoints
  `GET /key-shares/{shareId}`, `POST /key-shares/{shareId}/nonce`
* new header `x-cdoc2-sid-rpv3-signature-parameters` applied to endpoint `/key-shares/{shareId}`.
  Used when `x-cdoc2-auth-token` is signed with SID RPv3

**[0.4.3]  Handle empty "" GET /key-shares header parameters better. (2025-03-26)**

* Handle empty ("") "x-cdoc2-auth-x5c" and "x-cdoc2-auth-ticket" header parameters better (no long stacktrace in log), return HTTP 400
* Spring Boot 3.4.1 -> 3.4.3 + other dependency updates
* Upgrade dependency `ee.cyber.cdoc2.openapi:cdoc2-key-shares-openapi` `1.0.1-draft` -> `1.0.1` (no changes besides version)

**[0.4.2] Bug fix for config property initialization (2025-02-27)**

* Bug fix for config property initialization inside `KeyShareApiService` and unit tests.

**[0.4.2-SNAPSHOT] Added index on `key_material_share_nonce` table**

* Added index on `key_material_share_nonce` table columns to increase query performance

**[0.4.1-SNAPSHOT] Support for JWT tokens signed with Mobile-ID (ES256)**

* Use [cdoc2-auth-token:0.3.3-SNAPSHOT](https://github.com/open-eid/cdoc2-auth) that adds support
  for ES256 (Mobile-ID)
* Certificates updates + added script that downloads and creates truststore
* Spring Boot 3.3.3 -> 3.4.1 + other dependency updates
* Tag `cdoc2-shares-server-liquibase` with `latest` when built using `build-image.sh` script

**[0.3.0-SNAPSHOT] First public release**

* use [auth-token:0.2.0-SNAPSHOT](https://github.com/open-eid/cdoc2-auth) (SDJWT.body: `"aud":"https://server:port/key-shares/{shareID}?nonce={nonce}"`)
* Fix Disclosure decoding (previously Disclosure were incorrectly decoded even when digest
  didn't match )
* Use `"aud"` list of `{server}/key-shares/{shareID}?nonce={nonce}` URLs instead of custom
  `shareAccessData` json object.
* remove `"kid"` from JWT header (duplicate of "iss" in JWT body)
* remove `"iat"` and `"exp"` claims. Nonce creation time is checked by `cdoc2-shares-server`
* Move x5c certificate issuer check into cdoc2-auth-token module (from `cdoc2-shares-server`)
