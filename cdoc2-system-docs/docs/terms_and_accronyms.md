# Terms and Acronyms

* `AEAD` - Authenticated Encryption with Additional Data

* `Authentication Server`, `cdoc2-auth` - SID/MID. Generates session tokens to presented to other CDOC2 SID/MID infrastructure servers.

* `Capsule` - Data structure, which contains encryption scheme-specific information (encrypted symmetric keys, public keys, salt, server object references, ...)<br/>which Recipient can use to derive, establish or retrieve decryption keys for decrypting the CDOC2 Container. Capsule can either be a Server Capsule, a Container Capsule or a Shares Capsule.

* `CC` - CDOC2 Capsule. Data structure inside CDOC2 Container. CC contains information for decrypting the payload of CDOC2 Container. <br/> That information could be a symmetric cryptographic key, a share of symmetric cryptographic key, <br/> or necessary data for establishing such key with key derivation algorithm or key-agreement protocol, for example, with ECDH.

* `CDOC` - Crypto Digidoc, encrypted file transmission format used in the Estonian eID ecosystem.

* `CDOC 1.0` - Unofficial term for all (XML-ENC based) CDOC formats preceding this specification.

* `CDOC2 Authentication Token` - SID/MID. Credential constructed by the Client containing CSS server nonces, signed by the Recipient via SID/MID. Presented to CSS servers to authorize Key Share downloads for a specific CDOC2 Container. Encoded as an SD-JWT.

* `CDOC2 Client Application` - Software used by Sender and Recipient to create and decrypt CDOC2 Containers, interact with CCS and CSS servers, and handle eID authentication.

* `ChaCha20-Poly1305` - Authenticated encryption algorithm (AEAD) used to encrypt the payload of a CDOC2 Container. Uses a 256-bit CEK and a 96-bit nonce.

* `CDOC2 Container` - File format for transmitting the encrypted payload and metadata information, <br/>including the capsule from Sender to Recipient.

* `CDOC2 System` - IT system, which allows users to send encrypted files to each other with the help of CDOC2 Client Applications and CDOC2 Capsule Servers.

* `CCS` - CDOC2 Capsule Server, which mediates CDOC2 Server Capsules between Sender and Recipient.

* `CEK` - Content Encryption Key. Symmetric key used to encrypt the payload of CDOC2 Container.

* `Container Capsule` - A Capsule that is created inside a CDOC2 Container and is therefore not sent to a CDOC2 Capsule Server.

* `CSPRNG` - Cryptographically Secure Pseudo-Random Number Generator. Used throughout the system to generate key material such as the FMK, ephemeral key pairs, KEK shares, and salts.

* `CSS` - SID/MID. CDOC2 Shares Server, which mediates Key Shares between Sender and Recipient.

* `ECC` - Elliptic-Curve Cryptography

* `ECC DH` - Elliptic-Curve Cryptography Diffie Hellman key-establishment algorithm

* `ECC CDH` - Elliptic-Curve Cryptography Co-factor Diffie Hellman key-establishment algorithm

* `ECDH` - Elliptic-curve Diffie–Hellman. Key-agreement protocol that allows two parties, each having an EC public–private key pair, to establish a shared secret over an insecure channel.

* `eID` - Electronic identity. An umbrella term for digital identification means such as the Estonian ID-card, Mobile-ID, and Smart-ID.

* `FMK` - File Master Key. Cryptographic key material for deriving other encryption and HMAC keys.

* `hardware security token` - Smart-card (for example, the Estonian eID ID-card) or FIDO authenticator with asymmetric cryptographic keys.

* `HHK` - Header HMAC Key.

* `HMAC` - Hash-Based Message Authentication Code. Protects the integrity of the CDOC2 Container.

* `HKDF` - HMAC-based Key Derivation Function (RFC 5869). Used to derive CEK, HHK, and KEK from the FMK.

* `KEK` - Key Encryption Key. Symmetric key used to encrypt (wrap) the FMK, so that the FMK could be transmitted inside the CDOC2 Container to Recipient.

* `Key Share` - SID/MID. Key Shares are created by splitting cryptographic material required for encrypting/decrypting a CDOC2 document. These are stored inside Shares Capsules. Key Shares are always distributed among different Shares Servers and depending on the encryption scheme, all or a certain number of shares are needed to construct the original key value.

* `PBKDF2` - Password-Based Key Derivation Function 2 (RFC 2898). Used to derive key material from a pre-shared password in symmetric key encryption schemes.

* `Recipient` - The party who receives a CDOC2 Container and decrypts its payload using their key material (e.g. ID-card private key, pre-shared secret, or Key Shares from CSS servers).

* `RP Server`, `cdoc2-rp` - SID/MID. Relying Party Server. Mediates Smart-ID RP API and Mobile-ID REST API calls to SK services

* `RSA` - Rivest–Shamir–Adleman. Asymmetric encryption algorithm supported as a recipient key type in CDOC2 (used in schemes SC02 and SC04) via RSA-OAEP.

* `SD-JWT` - Selective Disclosure JSON Web Token. Token format that supports selective disclosure of claims. Used as the encoding format for Session Token and CDOC2 Authentication Token.

* `Sender` - The party who creates a CDOC2 Container, encrypts the payload, and distributes Capsules to one or more Recipients.

* `Server Capsule` - A Capsule that is mediated by a CDOC2 Capsule Server.

* `Session Token`- SID/MID. Short-lived credential issued by cdoc2-auth to the Client upon successful MID/SID authentication. Presented to CDOC2 infrastructure servers to prove Recipient identity. Valid for 24 hours. Encoded as an SD-JWT.

* `Shares Capsule` - Encryption/decryption key material which is split into Key Shares in order to distribute it to multiple CSS servers.
