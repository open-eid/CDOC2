# CDOC2 Auth Server changelog

**[0.8.0] Improved input language handling, client configurability**

* Language parameter for `auth/start` is constrained by openapi spec to be a nullable two character
  string. Actual validation of the input value is moved to app api implementation. Unrecognized
  language will result in HTTP 400 BAD REQUEST. Configured default language is applied only when
  language is not specified in request.
* Added client config parameters to allow modifying session status polling behavior

**[0.7.3] Improved error handling, dependency updates**

* `/auth/status` returns `HTTP 404 NOT FOUND` for non-existent auth process instead of `HTTP 400`
* Dependency updates

**[0.7.2] Test coverage**

* Improve the tests coverage
* Small refactor to `startauth` usecase code to allow verification code creation testing.

**[0.7.1] Improved error handling, SBOM creation**

* Give more informative Internal Server Error results when auth/start/ encounters a problem
  collecting session nonces from CDOC2 servers
* Use CycloneDX Maven plugin for SBOM creation

**[0.7.0] Configurable display text, general improvements**

* Made the authentication display text configurable.
* JWK for /.well-known/jwks.jws configurable from list of PEM-encoded resources. Removed key
  defaults from main classpath, enforcing requirement for externally provided keys.
* Added `/info` endpoint.
* Improved handling of client exceptions from MID/SID REST calls
* Made the issuer value for the session token configurable with the configuration parameter `app.session-token.issuer`.

**[0.6.0] Mobile-ID support, general improvements**

* Mobile-ID support for session token creation
* Expired authorization processes are cleaned by a scheduled job.
* HTTP 404 Not Found returned by `/auth/status/{authProcessUuid}` when no auth process matching
  authProcessUuid found in database
* Switched to latest Spring Boot 3 from Spring Boot 4 to resolve constant Jackson version conflicts
  between Spring Boot and SK clients (smart-id-java-client, mid-rest-java-client)
* REST endpoint input validation errors are returned as HTTP 400 Bad Request with problem details.
* SID and MID processes can be configured to use different RP name and UUID values

**[0.5.0] First public release**
