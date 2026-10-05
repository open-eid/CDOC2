# CDOC2 RP Server changelog

**[0.8.2] Cleanup and minor fixes**

* removed all classpath resources
* requesting a non-existent MID session through `/mid/session` will produce an HTTP-404 NOT FOUND response
* Session token verification failures produce correct 400-series responses
* logging and tracing improvements


**[0.8.1] Logging and tracing**

* added `logstash-logback-encoder` dependency to enable JSON logging
* ensured all client, validation and unexpected server errors are logged
* Add support for tracing (`micrometer-tracing-bridge-otel`, `opentelemetry-exporter-otlp`)
* Add Spring Security configuration (`spring-boot-starter-security`) requiring HTTP Basic
  authentication for `/actuator/prometheus`
* `/sid/session` request for non-existent session will produce 404 NOT FOUND
* Reduce `warn` level logging verbosity for session token verification failures
* Dependency updates

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
