# CDOC2 RP Server changelog

**[0.8.0] Improved error handling, client configurability**

* SmartIdClientException from SK SID service is propagated to application interface as HTTP 400 BAD
  REQUEST
* Removed needless nullability of auth-server well-known public keys
* Added client config parameters to allow modifying session status polling behavior

**[0.7.3] Bug fixes and optimizations**

* SIDClient passes the incoming `interactions` base64-encoded object directly to SmartID servers,
  instead of performing a deserialize-serialize step.
* `interactions` parameter of `sid/authenticate` openapi interface changed to string
* `mid/authenticate` passes the `displayTextFormat` parameter to MobileID servers.

**[0.7.2] Test coverage**

* Improve unit tests code coverage

**[0.7.1] SBOM creation**

* Use CycloneDX Maven plugin for SBOM creation

**[0.7.0] Improved exception handling, info endpoint**

* JWK for /.well-known/jwks.jws configurable from list of PEM-encoded resources. Removed key
  defaults from main classpath, enforcing requirement for externally provided keys.
* Added `/info` endpoint.
* Improved handling of client exceptions from MID/SID REST calls.

**[0.6.0] HTTP counter-signatures**

* Counter-signing of Mobile-ID signatures. Implements HTTP signature standard RFC9421
* Create a job to delete the expired session nonces
* Switched to latest Spring Boot 3 from Spring Boot 4 to resolve constant Jackson version conflicts
  between Spring Boot and SK clients (smart-id-java-client, mid-rest-java-client)
* REST endpoint input validation errors are returned as HTTP 400 Bad Request with problem details.

**[0.5.0] First public release**
