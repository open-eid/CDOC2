---
title: Cryptographic details
---

# Cryptographic details

This section provides a detailed description of the cryptographic computations used with the CDOC2 format. Most of these computations are broader technological infrastructure-neutral, but some are specifically related to means of eID used in Estonia (above all, the ID-card). All such situations will be highlighted.

## Security level and used cryptographic algorithms

Recent studies [(1)](https://www.ecrypt.eu.org/csa/documents/D5.4-FinalAlgKeySizeProt.pdf), [(2)](https://doi.org/10.6028/NIST.SP.800-57pt1r5) give cause to assume that 128-bit security should be sufficiently secure even after 2031. This claim is also supported by a new study published in 2022 [(3)](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TG02102/BSI-TR-02102-1.pdf). Based on these results, we use the following algorithms:

- HKDF-SHA-256
- HMAC-SHA-256
- ChaCha20-Poly1305

The SHA2 hash function family is a long-standing standard. [Recent studies](https://www.ria.ee/media/1473/download) show that the SHA2 hash functions are still secure and SHA-256 provides 128-bit security.

The HKDF key derivation function used here (see section [Key derivation](#key-derivation) for more details) has been subject to an [in-depth security analysis](https://ia.cr/2010/264). The use of HKDF with a secure hash function is also recommended in the [aforementioned study](https://www.ecrypt.eu.org/csa/documents/D5.4-FinalAlgKeySizeProt.pdf).

[A 128-bit key is sufficient for HMAC security](https://www.ria.ee/media/1473/download).

ChaCha20-Poly1305 is a secure (IND-CPA and INT-CTXT) authenticating encryption algorithm (see [e.g.](https://ia.cr/2014/613)). As a stream cipher, [ChaCha20 also provides 256-bit security by itself](https://www.ria.ee/media/1473/download).

XOR encryption (one-time pad) providing 256-bit security is used for FMK encryption.

Key lengths used for symmetric keys:

- FMK – 256 bits.
- HHK – 256 bits.
- CEK – depends on the payload encryption algorithm used, 256 bits for ChaCha20-Poly1305.
- KEK – depends on the FMK encryption algorithm used, 256 bits for XOR.

## Key derivation

For key derivation, the CDOC2 format utilizes the HKDF key derivation function, codified as [IETF RFC 5869](https://rfc-editor.org/rfc/rfc5869.txt).

RFC 5869 defines two key derivation functions: ``HKDF-Extrac``t and ``HKDF-Expand``, the use of which will be discussed below. Hereafter, these functions will be referenced using the shorthands ``Extract`` and ``Expand``.

In all cases, key derivation is carried out using the SHA-256 hash function, meaning that the functions return a 256-bit value.
To be used as input in functions, all textual constants must be UTF-8 encoded (in the present case, cryptographic functions take byte arrays and integers as input), quotation marks used in the specification are not part of the strings.

Public symmetric keys are derived as follows.

**File Master Key, FMK**

*FMK ← Extract(”CDOC2salt”, random)*

Where *CDOC2salt* is a constant string and *random* is an at least 256-bit value generated using a cryptographically secure random number generator (CSPRNG).

**Content Encryption Key, CEK**

*CEK ← Expand(FMK, ”CDOC2cek”, L<sub><sub>octets</sub></sub>)*

L<sub>octets</sub> defines the output length of the Expand function in bytes and must be equal to the key length of the used symmetric encryption algorithm (see section [Payload assembly and encryption](#payload-assembly-and-encryption)).

**Header HMAC Key, HHK**

*HHK ← Expand(FMK, ”CDOC2hmac”, 32<sub><sub>octets</sub></sub>)*

Note that the length of the HHK derived in this manner is 256 bits, i.e. equal to the output length of the used SHA-256 hash algorithm. This is based on the recommendations presented in the [HMAC standard](https://rfc-editor.org/rfc/rfc2104.txt).

**Key Encryption Key, KEK**

KEK derivation is immediately tied to the used recipient type, and is described in connection with the relevant format elements:

- ECCPublicKeyCapsule – section [ECCPublicKeyCapsule](#eccpublickeycapsule).
- RSAPublicKeyCapsule – section [RSAPublicKeyCapsule](#rsapublickeycapsule).
- KeyServerCapsule – section [KeyServerCapsule](#keyservercapsule).
- SymmetricKeyCapsule – section [SymmetricKeyCapsule](#symmetrickeycapsule).

## Descriptions of header elements and KEK computation

The abstracted structure of the header is described in section [CDOC2 container format](ch03_container_format.md#cdoc2-container-format). Fields are described in the abstracted structure using primitive data types. The following section describes how to compute the fields and translate values to the primitive data type form.

Key Encryption Key (KEK) computation depends on recipient type. Below, KEK computation is described with reference to each specific recipient type.

### ECCPublicKeyCapsule

``ECCPublicKeyCapsule`` (see [table 2](#table-2-eccpublickeycapsule-elements)) refers to a recipient identified by their ECC public key. The CDOC2 format supports the use of any public key generated on a *secp384r1* elliptic curve as the recipient. For example, the key can be the public key of the Estonian ID-card authentication key pair.
For the *secp384r1* curve, the TLS 1.3 encoding used for elliptic curve points is identical to the encoding used in CDOC 1.0.
The ``ECCPublicKeyCapsule`` structure corresponds to the capsule capsi in the sense of the protocols presented in sections [Direct key agreement-based ECDH](ch02_encryption_schemes.md#direct-key-agreement-based-ecdh) and [Capsule server-based ECDH](ch02_encryption_schemes.md#key-server-based-ecdh).

#### Table 2. *ECCPublicKeyCapsule* elements

Field | Contents | Encoding
 ----------- | ----------- | -----------
Curve | Elliptic curve used; currently only *secp384r1*. | Based on the format used; see scheme description.
RecipientPublicKey | Recipient’s public key, e.g. ID-card key pair 1 public key. | Public key is encoded following [TLS 1.3 rules, section 4.2.8.2](https://rfc-editor.org/rfc/rfc8446.txt).
SenderPublicKey | Sender ephemeral (short-lived or even one-time) key pair public key | Public key is encoded following [TLS 1.3 rules, section 4.2.8.2](https://rfc-editor.org/rfc/rfc8446.txt).

The sender computes the KEK using the secret key of the ephemeral key pair they have generated, and the recipient’s public key, using the elliptic-curve Diffie-Hellman key agreement protocol (ECDH), and passes the result to the specified key derivation function. The recipient performs a similar computation using the sender’s ephemeral public key and the ID-card authentication key pair. Details of the computations are provided below.

The sender’s ephemeral key pair is anonymous, i.e. not tied to the sender’s public identity in any way.

In case there are multiple recipients, the sender can use the same ephemeral key pair over a single CDOC container.

The sender’s ephemeral key pair consists of a public and a secret key:

$$(pk_{eph}, sk_{eph})$$

The recipient holds their ID-card authentication key pair public key *pkrec* (assuming here that the recipient’s private key is not immediately accessible).

This key is also accessible to the sender. Mechanisms for the dissemination of the recipient's public key are outside the scope of this specification.

#### KEK computation during encryption (ECCPublicKeyCapsule)

The shared ECDH secret is computed by the sender as follows:

$$ S_{ecdh} ← (s_{keph} · pk_{rec})_x $$

i.e. the shared secret is the elliptic curve x-coordinate computed in this manner. The shared secret is encoded as a big-endian byte array, the length of which in full bytes corresponds to the modulus length of the used elliptic curve in full bytes. For example, the modulus length of secp384r1 is 48 bytes.

KEK is computed from the shared secret as follows:

$$ KEK_{pm} ← Extract(”CDOC2kekpremaster”, S_{ecdh}) $$

$$ KEK ← Expand(KEK_{pm}, ”CDOC2kek” ∥ algId ∥ pk_{rec} ∥ pk_{eph}, L_{<sub>octets</sub>}) $$

*algId* is the identifier of the cryptographic algorithm used for the encryption of the FMK defined as a string corresponding to the field *Recipient.FMKEncryptionMethod* (section [FMK encryption and decryption](#fmk-encryption-and-decryption)).

*L<sub><sub>octets</sub></sub>* defines the output length of the ``Expand`` function in bytes and is defined by the symmetric encryption algorithm used for FMK encryption.

#### KEK computation during decryption (ECCPublicKeyCapsule)

The Estonian ID-card supports the use of an authentication key pair as one of the ECDH parties.
This functionality can advantageously be used through the PKCS#11 ``C_DERIVEKEY`` function, employing the ``CKM_ECDH1_DERIVE`` mechanism.
Key derivation can also be performed using the Windows ``NCryptSecretAgreement`` and ``NCryptDeriveKey`` encryption functions. ``NCryptSecretAgreement`` computes the *Secdh* and ``NCryptDeriveKey`` computes the *KEKpm*. ``NCryptDeriveKey`` parameters must be set as follows:

- ``hSharedSecret`` – handle returned by ``NCryptSecretAgreement``.
- ``pwszKDF`` – the constant BCRYPT_KDF_HMAC.
- ``pParameterList`` – algorithm parameters:
  - ``KDF_HASH_ALGORITHM`` – the constant ``BCRYPT_SHA256_ALGORITHM``.
  - ``KDF_HMAC_KEY`` – the constant ``CDOC2kekpremaster``.
  - ``KDF_SECRET_PREPEND`` – parameter omitted.
  - ``KDF_SECRET_APPEND`` – parameter omitted.

All ID-cards used today should be able to validate elliptic curve points used as input in ECDH key derivation, but additional validation may be implemented in software supporting the CDOC format to provide more user-friendly error management.

In order to validate whether the point *Q = (x, y)* is located on the curve, it must be verified whether *x* and *y* fall in the interval [0…*p* – 1], whether they satisfy the curve equation, and whether the point falls in the correct subgroup. For example, the formula for the curve P-384 can be presented as

$$ y^2 ≡ x^3 - 3x+b\bmod p\; $$

It must also be verified that *nQ* = 0 and *Q* != 0. The constants *b*, *p*, and *n* are described in the [Digital Signature Standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf).
The ``C_DERIVEKEY`` function takes the sender’s ephemeral public key *pkeph* and a reference to the corresponding ID-card key pair (*pkrec*, *skrec*) as inputs. The recipient computes

$$S_{ecdh}' \leftarrow (sk_{rec}\cdot pk_{eph})_{x}\;$$

Thanks to the algebraic properties of the elliptic curve,
$S_{ecdh}=S_{ecdh}'$.

This shared secret must be used to compute KEK as described above with reference to encryption.

### RSAPublicKeyCapsule

*RSAPublicKeyCapsule* (see [table 3](#table-3-rsapublickeycapsule-elements)) refers to a recipient identified by their RSA public key.
The structure *RSAPublicKeyCapsule* corresponds to the capsule *capsi* in the sense of the protocols presented in sections [Direct key agreement-based ECDH](ch02_encryption_schemes.md#direct-key-agreement-based-ecdh) and [Capsule server-based ECDH](ch02_encryption_schemes.md#key-server-based-ecdh).

The sender generates a random KEK and encrypts it using the recipient’s RSA public key with OAEP padding. The recipient decrypts the encrypted KEK using their RSA private key. Details of the computations are provided below.

The recipient’s public key is also accessible to the sender. Mechanisms for the dissemination of the recipient's public key are outside the scope of this specification.

#### Table 3. RSAPublicKeyCapsule elements

Field | Contents |Encoding
----------- | ----------- | -----------
RecipientPublicKey | RSA public key | Value: DER encoding of the ASN.1 structure *RSAPublicKey* (see [section A.1.1](https://www.rfc-editor.org/rfc/rfc8017))
EncryptedKEK | KEK encrypted using recipient’s public key | XXX

#### KEK computation during encryption (RSAPublicKeyCapsule)

The symmetric encryption algorithm used for the encryption of the FKM defines the KEK length *L<sub>octets</sub>*. The sender generates a random number KEK with a length of *L<sub>octets</sub>*.

For the encryption of the KEK, the sender uses the RSA-OAEP (see [section 7.1](https://www.rfc-editor.org/rfc/rfc8017)) encryption function. RSA-OAEP has three input parameters (see [section A.2.1](https://www.rfc-editor.org/rfc/rfc8017)):
    • ``hashAlgorithm`` – hash function used by the algorithm. We use the SHA-256 hash function (``id-sha256``).
    • ``maskGenAlgorithm`` – mask generation function used by the algorithm. We use the MGF1 function (``id-mgf1``), parametrized by the SHA-256 hash function.
    • ``pSourceAlgorithm`` – label source function. We use an empty label (``pSpecified Empty``).

#### KEK computation during decryption (RSAPublicKeyCapsule)

The recipient decrypts the encrypted KEK using their private key and the same parameters as were used for encryption.

### KeyServerCapsule

The Capsule Server described by the ``KeyServerCapsule`` structure (see [table 4](#table-4-keyservercapsule-elements)) returns the following structures which are handled as described in the referenced sections:

- *ECCPublicKeyCapsule*: section [ECCPublicKeyCapsule](#eccpublickeycapsule).
- *RSAPublicKeyCapsule*: section [RSAPublicKeyCapsule](#rsapublickeycapsule).

The details of using *KeyServerCapsule* are described in section [Capsule server](../03_system_architecture/ch04_capsule_server.md#key-server).

### SymmetricKeyCapsule

*SymmetricKeyCapsule* (see [table 5](#table-5-symmetrickeycapsule-elements)) refers to a recipient identified by a key label.
In this scheme, the sender and recipient are either the same person (use case: storage cryptography) or have previously exchanged a symmetric secret key outside the system (use case: transport cryptography).
In both cases, both the sender and the recipient holds the same secret key, identified by a key label. The specification does not limit the selection of the label in any way.

#### Table 4. KeyServerCapsule elements

Field | Contents | Encoding
----------- | ----------- | -----------
RecipientKey | Information on recipient key used by the recipient for authentication with the capsule server. | -
KeyServerID | Capsule server identifier. | UTF-8 string asssigned by the software trust anchor configuration, see section [Server identification and trust](../03_system_architecture/ch04_capsule_server.md#server-identification-and-trust).
TransactionID | Transaction identifier | UTF-8 string assigned by the capsule server

#### Table 5. SymmetricKeyCapsule elements

Field | Contents | Encoding
----------- | ----------- | -----------
Salt | Random number generated by the sender, used as input for the HKDF-Extract function in KEK derivation | Byte array

#### KEK computation during encryption (SymmetricKeyCapsule)

The sender holds the symmetric key *sym* labelled *label*. The sender generates the random number *salt*. The purpose of this number is to ensure the generation of a new KEK even when reusing the key *sym*. Since no practical upper limit can be set for the reuse of the key, the length of *salt* is chosen with a significant margin, i.e. 256 bits.
KEK is computed from the symmetric key and the generated random number as follows:

$$ KEK_{pm} \leftarrow Extract(salt, sym) $$

$$ KEK     \leftarrow Expand(KEK_{pm}, "CDOC2kek" \parallel algId \parallel label, L_{octets})
$$

Where *algId* is the identifier of the encryption algorithm used for the encryption of the FMK as a string, set as ``Recipient.FMKEncryptionMethod`` (section [FMK encryption and decryption](#fmk-encryption-and-decryption)).

*L<sub>octets</sub>* defines the output length of the ``Expand`` function in bytes, determined by the symmetric encryption algorithm used for the encryption of the FMK.

#### KEK computation during decryption (SymmetricKeyCapsule)

The recipient holds the symmetric key *sym* labelled *label*. The *Salt* field of the *SymmetricKeyCapsule* structure provides the random number *salt* generated by the sender.

This information is used for computing the KEK just as described above with reference to encryption.

## FMK encryption and decryption

The FMK is encrypted using the XOR operation.

The FMK assumes that the KEK and FMK are of equal length, which can be ensured by using the HKDF key derivation method.

For FMK encryption, the XOR operation is applied bitwise to the corresponding bits in the FMK and the KEK.

For decryption, the XOR operation is applied bitwise to the corresponding bits in the cryptogram and the KEK.

## Header authentication code

The header authentication code is computed with the [HMAC algorithm](https://rfc-editor.org/rfc/rfc2104.txt), using the SHA-256 hash function.

The HHK (see section [Key derivation](#key-derivation)) is used as the key.

HHK length must be at least equal to the output length of the used hash function, i.e. 256 bits.

$$ HMACValue_{header} \leftarrow HMAC_{SHA-256}(HHK, header) , $$

where *header* is the serialized header in the form it is added to the envelope.

Validation of the message authentication code requires computing the HHK from the parsed header, then computing a message authentication code for the serialized header read from the container and comparing the computed code with the message authentication code read from the container – the two values must be identical.

## Payload assembly and encryption

NOTE: The section below describes the encryption of the payload as a byte array. The assembly of encrypted files into a single byte array is described in section [Unencrypted payload](ch03_container_format.md#unencrypted-payload).

For payload encryption, [ChaCha20-Poly1305 AEAD encryption](https://www.rfc-editor.org/info/rfc8439) is used with the following parameters:

- Key length: 256 bits
- Nonce length: 96 bits
- Authentication label length: 128 bits

CEK is used as the key.

The nonce (*nonce*) is always generated afresh, using a cryptographically secure random number generator (CSPRNG).

Additional data (*additionalData*) comprises a predetermined UTF-8 encoded string, the serialized header, and the header message authentication code.

$$  additionalData \leftarrow "CDOC2payload" \parallel header \parallel headerHMAC $$

Payload (*payLoad*) encryption is performed using the encryption function below, with an output length of plaintext payload length plus authentication label length.

$$ encryptedPayload \leftarrow encrypt_{cc20p1305}(CEK, nonce, payLoad, additionalData) $$

Decryption of the encrypted payload is performed using the decryption function below.

$$ payload \leftarrow decrypt_{cc20p1305}(CEK, nonce, encryptedPayLoad, additionalData) $$

When processing the payload in streaming mode, the plaintext will be handled before the decryption function has validated the authentication label. Requirements for plaintext processing and error handling are detailed in section [Requirements for payload unpacking](ch03_container_format.md#requirements-for-payload-unpacking). It is critical to delete all files if authentication label validation fails.

The encrypted payload is serialized along with the nonce, as the nonce has to be transmitted to the recipient.

$$ serializedPayload \leftarrow nonce \parallel encryptedPayLoad $$

In the case of the format envelope, payload means an encrypted and serialized payload (*serializedPayload*). Nonce and other details have not been explicated in the description of the envelope as they depend on the encryption method employed.
