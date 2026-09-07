# CDOC2 Integrator Guide

*For developers building client software (desktop, mobile, or CLI) that creates or opens CDOC2
encrypted containers*

This chapter is a practical companion to the full CDOC2 System Documentation, aimed specifically at
**Integrators** — teams who are not modifying the CDOC2 protocol itself, but need to embed CDOC2
encrypt/decrypt capability into their own end-user software. It summarizes what you need to know to
plan an implementation and points back to the authoritative chapters for the details you'll need
while coding.

## What you're building

A **CDOC2 Client Application** is the umbrella term the specification uses for any software that
lets a user encrypt files into a CDOC2 Container or decrypt one — it is described as an abstract
component in the CDOC2 System that helps users encrypt files into a CDOC2 Container and decrypt
received CDOC2 Containers, with DigiDoc4 desktop and mobile applications and a CDOC2 CLI application
given as concrete examples. The use cases in the specification are deliberately written generically
so that any client — yours included — can implement them, and the specification notes that a
specific client's own documentation may add implementation-specific detail such as UX wireframes on
top of these generic use cases.

Before writing code, it helps to internalize the four roles a user can play: a **User** who runs
your client, acting as **Sender** when packaging files for someone else, as **Recipient** when
opening a container addressed to them, and occasionally as their own Recipient when they encrypt
something for their own long-term storage. An **Administrator** role also exists in the model, for
whoever manages configuration (trusted server lists, capsule servers, key material) for a fleet of
clients.

## Core vocabulary

- **CDOC2 Container** — the file format used to transmit the encrypted payload and metadata,
  including the capsule, from Sender to Recipient.
- **Capsule** — the data structure containing encryption-scheme-specific information (encrypted
  symmetric keys, public keys, salt, server references, etc.) that the Recipient uses to derive,
  establish, or retrieve the decryption key. A capsule is either a **Container Capsule** (travels
  inside the file itself) or a **Server Capsule** (mediated by a Capsule Server).
- **FMK / CEK / KEK / HHK** — the File Master Key is the root key material from which the Content
  Encryption Key (used to encrypt the payload) and the Header HMAC Key (used to protect container
  integrity) are derived, while the Key Encryption Key is the symmetric key used to wrap the FMK so
  it can travel safely to each recipient inside the container.

## The backend components your client may need to call

| Component                                 | Role                                                                                                                                                                                                                                                                  | Relevant to Integrators                       |
|-------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|
| CDOC2 Capsule Server (CCS)                | Stores encryption/decryption key material and provides endpoints for auth-ticket creation and key material upload/download                                                                                                                                            | Used for the "server-mediated" EC/RSA schemes |
| CDOC2 Shares Server (CSS)                 | Returns share identifiers to the client application, stores key shares, and requires the recipient to authenticate before downloading shares; shares are spread across multiple independent CSS instances so that compromising one server doesn't expose key material | Used for Smart-ID/Mobile-ID-based decryption  |
| CDOC2 Authentication server (auth-server) | Used in the Smart-ID/Mobile-ID context to compose and issue a session token, an SD-JWT structure sent with its signing certificate as a header on subsequent requests                                                                                                 | Needed only if you support SID/MID recipients |
| CDOC2 Relying party server (rp-server)    | Mediates and validates client requests to Smart-ID/Mobile-ID relying-party services, including verifying the session token                                                                                                                                            | Needed only if you support SID/MID recipients |

## The encryption schemes you need to support

CDOC2 isn't one algorithm — it's a family of six schemes (SC01–SC06), chosen per recipient, so a
single container can mix recipient types. As an integrator, your encryption flow needs to pick the
right scheme based on what the recipient has available:

| Scheme | Recipient has…                                    | Mechanism                                                                                                                                                                 |
|--------|---------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SC01   | An EC key pair on a hardware token (e.g. ID-card) | Diffie-Hellman key exchange generates a shared secret between sender and recipient, used to protect the FMK; the capsule travels inside the container itself              |
| SC02   | An RSA key pair                                   | RSA-OAEP is used to wrap a randomly generated KEK, carried over from CDOC1 for compatibility with existing RSA-based eID tokens                                           |
| SC03   | An EC key pair, capsule via CCS                   | Same DH mechanism as SC01, but the capsule is transmitted via a Capsule Server rather than embedded in the container                                                      |
| SC04   | An RSA key pair, capsule via CCS                  | Same as SC02, but capsule delivered via CCS                                                                                                                               |
| SC05   | A pre-shared symmetric key, no eID token          | Useful for long-term storage independent of hardware tokens or PKI validity, or for sending to recipients who have no eID means but have previously received a shared key |
| SC06   | A pre-shared password                             | Similar to SC05 but derives the KEK from a password via PBKDF2 instead of a raw shared key                                                                                |
| SC07   | No local private key material at all              | Smart-ID / Mobile-ID (n-of-n shared secret)                                                                                                                               |

Practical guidance: default to **SC01**/ **SC02** (with a CCS, i.e. **SC03**/ **SC04**) whenever the
recipient has a known certificate on a hardware or smart-card-backed token — this gives forward
secrecy against future compromise of the recipient's private key, because an attacker who is only
monitoring the public channel cannot recover the symmetric key from a broken public-key algorithm or
a later-compromised private key, since the key is transmitted separately through the Capsule Server.
Fall back to password-based (**SC06**) or shared-key (**SC05**) schemes only when no eID means
exists for a recipient, or for archival use where you don't want decryption to depend on a
certificate remaining valid.

**SC07** is the only path for recipients who authenticate purely via Smart-ID/Mobile-ID with no
local key pair. Implementing it requires your client to talk to Auth Server, RP Server, and multiple
independent Shares Server instances.

## Talking to a Capsule Server

If your client is going to use CCS-mediated schemes (SC03/SC04) or support recipients without local
tokens, you need to implement two client-side roles against the CCS API:

**As Sender** — the sender's interface is unauthenticated and open to any sender: your client
transmits the capsule and a recipient identifier and receives a transaction identifier back, which
you embed in the container header alongside the CCS's identifier and the recipient identifier.

**As Recipient** — the client authenticates to the server and presents the transaction identifier
found in the container; the server looks up the capsule and compares the recipient identity
established during authentication against the recipient identifier attached to that capsule before
releasing it. For the currently specified capsule type, authentication is done via mutual TLS: the
server validates the client's certificate (e.g. via OCSP) and compares the public key presented in
that certificate against the public key tied to the stored capsule — meaning if a recipient's
certificate is later revoked, the CCS will refuse to hand over the capsule to whoever now holds that
revoked key.

Two integration details are easy to overlook and matter for security:

- **Trust configuration, not discovery.** Clients must ship (or be able to fetch from a trusted
  source) a list of trusted Capsule Servers — including each server's identifier, supported capsule
  type, sender/recipient interface URLs, operating organization, and public keys/certificates — and
  this same list is used for TLS key pinning. Do not let a sender's client dynamically trust a
  server URL supplied only by data inside an incoming container; only the server's identifier
  travels with the container, precisely so a malicious party cannot redirect the recipient to an
  untrusted endpoint.
- **Expiration is negotiated, not assumed.** When forwarding a capsule, your client supplies a
  requested expiration time, but if the recipient's certificate expires sooner than the requested
  capsule lifetime, the certificate's expiration takes precedence, and the CCS will reject a request
  whose expiration exceeds what its own configuration allows. Handle that rejection path explicitly
  rather than assuming your requested TTL will always be honored.

For the exact request/response shapes, generate client stubs from the published OpenAPI
specification rather than hand-rolling the API — the specification maintains machine-readable
schemas for exactly this purpose, and versioned artifacts are published as Maven packages under the
`open-eid` organization for JVM-based integrators.

## Supporting recipients without a hardware token: key-shares, Smart-ID and Mobile-ID

Not every recipient owns a smart card. The CDOC2 ecosystem addresses this with a **key-shares**
architecture that lets a recipient decrypt after proving their identity remotely via Smart-ID or
Mobile-ID rather than presenting a certificate over mTLS. If your client needs to support this path,
be aware of the additional components involved:

- A **CDOC2 authentication server** and an **SID/MID proxy** (RP server) sit between your client and
  the identity providers — the authentication server issues access tokens, while the proxy gives
  your client access to RIA's Smart-ID RP API and Mobile-ID REST API without your client integrating
  those APIs directly.
- Instead of a single Capsule Server, decryption key material can be split across multiple
  **key-share servers**; a recipient authenticates once and presents a signed authentication ticket
  to each share server in turn to reassemble their key. The auth ticket format is an SD-JWT
  (selectively disclosable JWT), and support for ES256 and RS256 signature algorithms is required to
  accommodate both Mobile-ID and Smart-ID signing.
- The typical flow your client will need to drive is: request a nonce per key-share from that share
  server's `/key-shares/{shareId}/nonce` endpoint, use that nonce (with the SID/MID proxy) to
  produce a signed auth ticket, then present that ticket in an `x-cdoc2-auth-ticket` header when
  calling `GET /key-shares/{shareId}` to retrieve each share.

## Reference building blocks — build vs. reuse

You are not expected to reimplement the cryptography from the specification text.

- **`cdoc2-java-ref-impl`** — a Java library implementing client-side CDOC2 functionality
  (encrypt/decrypt, capsule handling), plus a **`cdoc2-cli`** command-line tool built on it. If your
  client targets the JVM, or you want a reference to test your own implementation against, start
  here.
- **`libcdoc`** — a C/C++ library covering the same functionality for native clients, used by the
  DigiDoc4 desktop application itself.
- **`cdoc2-openapi`** — versioned OpenAPI definitions for the Capsule Server and key-shares APIs,
  published as Maven artifacts, for generating client stubs in any language with tooling support.
- **`cdoc2-auth`** — the SD-JWT based authentication library/protocol implementation for the
  key-shares flow described above.

Unless you have a specific reason to write your own cryptographic implementation (e.g. targeting a
platform with no JVM/C++ interop), integrating one of the reference libraries is the lower-risk
path — it keeps you aligned with corrections to the specification as the format matures, and CDOC1
and CDOC2 are explicitly **not** wire-compatible, so any home-grown parser needs to be
format-version aware from day one.

## Security responsibilities checklist for Integrators

- **Never** invent your own trust list mechanism for Capsule Servers — ship or securely fetch the
  canonical list and pin against its certificates.
- Validate header size limits and file-name/content safety rules before writing or unpacking a
  container; the use cases treat both as explicit failure paths your UI must handle, not edge cases
  to ignore.
- Enforce minimum password strength client-side for SC06/`UC.Client.P.01`-style flows; the spec
  expects this check before a password is accepted.
- Prefer OCSP-checked, short-lived trust decisions for capsule server TLS certificates over
  long-cached trust.
- If you support the key-shares/Smart-ID/Mobile-ID path, do not persist SD-JWT auth tickets beyond
  their intended single use, and treat the auth-server and rp-server as no more
  trusted than any other network dependency — mTLS/OCSP habits apply there too.
