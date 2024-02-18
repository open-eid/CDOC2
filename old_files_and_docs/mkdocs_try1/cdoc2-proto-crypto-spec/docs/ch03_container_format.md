---
title: 2. CDOC2 container format
---

# CDOC2 container format

## Abstracted format
This section describes the CDOC 2.0 format from an abstract point of view, presenting the data contents and data models used therein without referencing the specifics of the serialized format.
### Basic principles
The basic principles outlined below will provide the user of this specification with points of reference for understanding the details of the specification.

- The abstracted format consists of a header and an encrypted payload.
- The abstracted format contains a single encrypted payload consisting of one or several encrypted files. File information, as well as the sizes and sequence of the files, in case there is more than one file, is also encrypted.
- The payload is encrypted using a single symmetric key (Content Encryption Key; CEK), using AEAD (Authenticated Encryption with Additional Data) encryption.
- The CEK is derived from the CDOC file master key (File Master Key; FMK). See section 6.2. TODO! add link
- The FMK can be encrypted in parallel using one or several key encryption keys (KEK), one per recipient. On KEK generation see section 6.3 TODO! add link.
- The header describes the protection of the FMK (i.e. how the recipients can acquire the KEK required for decrypting the FMK).
- Header integrity is ensured using a message authentication code computed using the message authentication key derived from the FMK (Header HMAC Key; HHK). See section 6.5 TODO! add link.
- To ensure format universality, no elements specific to the Estonian eID infrastructure have been used in the description. Thus, the recipient is described with reference to their public key rather than their certificate.
- Decryption always follows the same pattern: 1) the recipient acquires a KEK, 2) the recipient decrypts the FMK, 3) the recipient derives the HHK and validates the header, 4) the recipient derives the CEK, 5) the recipient decrypts the payload.

### Header structure
Header structure is described with the help of pseudocode that is based on no specific programming or schema language but should be intuitively understood.

The header consists of one or several structures describing a recipient. Each recipient structure contains complete information on how the specific recipient can access the FMK (for identification, access to personal encrypted materials, etc.).

A message authentication code is computed for the header using a key derived from the FMK. This is necessary for preventing the manipulation of the header by the senders, e.g. for the purpose of concealing some recipient. The header authentication code is computed for a header serialized in a specific manner (see section [Serialized format](#serialized-format)).

    Header = {
        Recipients              = :Recipient[](1..k)
        PayloadEncryptionMethod = :enum(CHACHA20-POLY1305)
    }

A message authentication code is computed for the header (see section 6.5 for details TODO! link):

    Checksum = {
        value = HMAC(HHK, Serialize(Header))
    }

The recipient is described using the structure ``Recipient``. The format of the structure allows for quick and unambiguous decisions on whether the reader can decrypt the payload using the specific instance of ``Recipient``.

    Recipient = {
        Capsule = Union(:ECCPublicKeyCapsule | :KeyServerCapsule | 
                :SymmetricKeyCapsule | :RSAPublicKeyCapsule )
        KeyLabel = :string
        EncryptedFMK = :byte[]
        FMKEncryptionMethod = :enum(XOR)
    }

The ``Recipient`` structure consists of a key capsule, a recipient key label, an encrypted FMK, and an FMK encryption method identifier.

- ``Capsule`` – encryption method specific data that the recipient can use to decrypt the FMK.
- ``KeyLabel`` – human-readable label of the private or secret key required for decrypting the FMK. This label is necessary for building a sensible user interface. The sender fills this field based on the key or the related certificate. No concrete method for achieving this is indicated in the specification as this is not relevant to cryptographic processing. ``KeyLabel`` is a UTF-8 string.
- ``EncryptedFMK`` – encrypted FMK.
- ``FMKEncryptionMethod`` –FMK encryption method type.

Successful processing of the Capsule structure returns a cryptographic key for decrypting the FMK using the method defined as ``FMKEncryptionMethod``. See section 6.4 on the details of cryptographic operations.
The following key capsule types have been specified to ensure the support of a variety of encryption methods ([CDOC2 encryption schemes](ch02_encryption_schemes.md)).

- ``ECCPublicKeyCapsule`` – the recipient is identified by ECC public key ``RecipientPublicKey`` (e.g. the public key of the first ID-card key pair). The KEK is derived using ECDH. Used in the [SC.01 encryption method](ch02_encryption_schemes.md#sc01-direct-encryption-scheme-for-recipient-with-ec-keys). 
- ``RSAPublicKeyCapsule`` – the recipient is identified by RSA public key ``RecipientPublicKey``. The KEK is derived by decrypting the key capsule using the RSA private key. Used in the [SC.03 encryption method](ch02_encryption_schemes.md#sc03-key-transmission-server-scheme-for-recipients-with-ec-keys). 
- ``KeyServerCapsule`` – the recipient is identified by ECC or RSA public key ``RecipientPublicKey``, used by the recipient for authentication on a key server. The key server returns an ``ECCPublicKeyCapsule`` or a ``RSAPublicKeyCapsule`` used as described above. Used in the  [SC.02](ch02_encryption_schemes.md#sc02-direct-encryption-scheme-for-recipient-with-rsa-keys) and [SC.04](ch02_encryption_schemes.md#sc04-key-transmission-server-scheme-for-recipients-with-rsa-keys) encryption methods. 
- ``SymmetricKeyCapsule`` – the recipient is identified by key label ``KeyLabel``. The KEK is derived using HKDF from a symmetric key provided by the user. Used in the [SC.05 encryption method](ch02_encryption_schemes.md#sc05-direct-encryption-scheme-for-recipient-with-pre-shared-symmetric-key). 

This list may be expanded in future versions of the specification.

### Key capsule types
ECC public key capsule. The recipient is identified by ECC public key ``RecipientPublicKey``.

    ECCPublicKeyCapsule = {
        Curve              = :enum(secp384r1)
        RecipientPublicKey = :byte[]
        SenderPublicKey    = :byte[]
    }

- ``Curve`` – identifier of the elliptic curve employed.
- ``RecipientPublicKey`` – recipient’s ECC public key, used by the recipient to establish the corresponding recipient record.
- ``SenderPublicKey`` – sender’s public key used by the recipient to derive the KEK using ECDH.

RSA public key capsule. The recipient is identified by RSA public key ``RecipientPublicKey``.

    RSAPublicKeyCapsule = {
        RecipientPublicKey = :byte[]
        EncryptedKEK       = :byte[]
    }

- ``RecipientPublicKey`` - recipient’s RSA public key, used by the recipient to establish the corresponding recipient record.
- ``EncryptedKEK`` -  key encryption key encrypted with the receipient's public key.

Key server capsule. The receipient is identified by ECC or RSA public key ``RecipientPublicKey``.

    KeyServerCapsule = {
        RecipientKey = Union(:EccKeyDetails | :RsaKeyDetails)
        KeyServerID         = :string
        TransactionID       = :string
    }

    RsaKeyDetails = {
        RecipientPublicKey  = :byte[]
    }

    EccKeyDetails = {
            Curve              = :enum(secp384r1)
            RecipientPublicKey = :byte[]
    }

- ``RecipientKey`` – information on the recipient key, used by the recipient for authentication on the key server.
- ``KeyServerID`` – key server identifier. The recipient must be able to use this to establish the key server’s network address and connect to the server.
- ``TransactionID`` – identifier of the key capsule sent to the key exchange server by the sender for transmission to the recipient.

Symmetric key capsule. The recipient is identified by the label of the symmetric key held by the user, ``KeyLabel``.

    SymmetricKeyCapsule = {
        Salt   = :byte[]
    }

- ``Salt`` – random number generated by the sender, used by the sender as input for the HKDF-Extract function.

### Format extension
To allow for format extension and ensure general forward compatibility, the union type field Capsule is included in the header structure Recipient. Each type of the union describes a specific type of recipient along with corresponding cryptographic primitives and key management tools. Types can be added to the format as necessary both in abstracted and concrete forms.

## Serialized format
The specification describes the implementation of the abstracted format using the FlatBuffers format.

### General description of the format
The format consists of an envelope, which is essentially made up of a serialized and concatenated header, a message authentication code, and a payload.
The message authentication code and payload are serialized using simple serialization.
For the sake of extensibility and the necessity of transmitting messages identical to the header from the point of view of processing logic via the key server, the header is described here with reference to the FlatBuffers format.
Aside from the header extension mechanism, the envelope used in this format also defines another point of extension.
This point of extension is provided by the version identifier, set as 2 (byte value) in the specification. The identifier must be changed in the descriptions of new versions.

### Envelope
The envelope consists of the following data elements, presented sequentially as bytes. The designation of the start and end of the envelope is outside the scope of the specification, insofar as the main and natural use case of the format is one where a CDOC file contains a single envelope.

- 4 bytes: the string “CDOC” – format designator (prelude), UTF-8 encoded.
- 1 byte: version identifier, set as 2 in the specification.
- 4 bytes: length of the following header, big-endian order. Header length is a 32-bit signed integer, i.e. the maximum header size is 2 GB. For the sake of the simplicity of implementation, header size is limited to 1 MB (220 B in base 2).
- x bytes, where x is as defined above: serialized FlatBuffers header.
- 32 bytes: header message authentication code (see section 6.5).
- The rest of the bytes, until the end of the envelope: payload encrypted using the method and key specified in the header.

Table 1 presents an overview of the envelope structure.
Table 1. Envelope structure

Field | “CDOC” | Version | Header length | Header | HMAC | Payload 
------------ | ------------- | ------------ | ------------ | ------------- | ------------ | ------------
Length | 4 | 1 | 4 | Header length | 32 | Until end of envelope
Start | 1 | 5 | 6 | 10 | 10 + header length | 10 + header length + 32


### Header and HMAC
The technical description (schema) of the FlatBuffers format can be found in the reference implementation source code repository, under `cdoc20-schema/`.
The schema is described in two files and reproduced as appendices to the specification.

- ``src/main/fbs/header.fbs`` Description of the FlatBuffers header.

- ``src/main/fbs/recipients.fbs`` Descriptions of recipient types; can be shared with schemas presented in other files.

The header, serialized following the FlatBuffers rule set, is written to the envelope, preceded a 4-byte length field as per the envelope description.
The Header Message Authentication Code (HMAC) is computed as described in section 6.5 TODO! link and written, bytewise, immediately after the header. The message authentication code algorithm and, consequently, HMAC length are defined in this specification.

### Payload
Lastly, the payload is written to a container composed following the CDOC format, immediately after the HMAC. The format presumes that the end-of-payload indicator is defined outside the format, e.g. as end-of-file.

Note that the end-of-payload indicator is purely optional: the true integrity of the payload is determined by whether the payload can be completely decrypted.

The composition of the payload plaintext is described in section 4.3. TODO! link

The encryption of the payload is described in section 6.6. TODO! link

### Format composition procedure
This section makes reference to the reference implementation source code, using Java package names and identifiers. References to source code are styled as monotype.
The following steps are needed to compose a CDOC 2.0 container.

-  Compile the list of all recipients.
-  Generate FMK, HHK, and CEK.
-  Compose the header along with all corresponding cryptographic operations.
-  Compute the HMAC.
-  Generate the payload plaintext.
-  Encrypt the payload.
-  Generate the serialized envelope.
-  Securely delete the FMK, HHK, and CEK values used during the procedure.

Generation of the payload plaintext is described in section 4.3 TODO!, ``container.Tar.archiveFiles()``.

Next, the cryptographic material used for the protection of the header and payload must be prepared. Generation and derivation of the corresponding keys (FMK, HHK, CEK) is described in section 6.2 TODO!, ``container.Envelope.prepare()`` and ``container.Envelope()``.

The list of all desired recipients must then be compiled and serialized, as the cryptographic methods used for ensuring the integrity of the container operate with an integral serialized header.

The requisite cryptographic procedures described in sections 6.3 TODO! and 6.4 TODO! must be executed for each recipient.

The HMAC is then computed as per section 6.5.
Payload encryption TODO! is described in section 6.6 TODO!, ``crypto.ChaChaCipher.encryptPayload()`` and ``crypto.ChaChaCipher.initChaChaOutputStream()``.

The detailed serialized envelope format is presented in section [Envelope](#envelope).

At the end of the encryption process, the employed cryptographic materials (symmetric keys, ephemeral private keys) must be securely deleted. Secure deletion significantly depends on the operational environment; in some cases (e.g. in JVM) it might not be possible. The developer must evaluate what options for secure deletion are provided by the employed programming language and operational environment.

### Format parsing procedure
This section makes reference to the reference implementation source code, using Java package names and identifiers. References to source code are styled as monotype.

The container parsing reference implementation is found in the function ``container.Envelope.decrypt()``. This functions serves as the primary entry point into the decryption logic and its main purpose is to take the encrypted container provided as input and write all the files contained therein to the selected folder.

The function does the following and all its alternative implementations must do the same while employing all relevant security checks.

- Parsing the envelope and decoding the envelope header.
- Decrypting/deriving the KEK.
- Decrypting/deriving the container-specific keys, i.e. FMK, HHK, and CEK.
- Checking the HMAC.
- Decrypting the archive.
- Extracting files from the encrypted archive and writes the files to the selected folder. In stream processing mode, decryption and extraction form a single operation.

The envelope parsing and header decryption reference implementation is found in the function ``container.Envelope.readFBSHeader()``.

The header must be parsed using the FlatBuffers library, utilizing the root type fbs.header.Header (in the reference implementation, this is implemented as the function ``fbs.header.Header.getRootAsHeader()`` generated from the FlatBuffers schema).

Parsing of the complete header is implemented as the reference implementation function ``container.Envelope.deserializeFBSHeader()``.

A recipient (Recipient) corresponding to the party processing the container must be found in the header and the KEK, FMK, and HHK must be derived or decrypted. 

Recipient identification methods corresponding to each encryption method are described in section 6.3. TODO! In case no recipient corresponding to the processing party is not found, the container cannot be decrypted. In this case, the algorithm must return a “container not meant for opening by the processor” error and terminate.

KEK computation is described in section 6.3. TODO! Should an error occur during KEK computation (e.g. the point is not located on the ellipse curve), the algorithm must return an error and terminate. KEK computation functions are found in the class ``crypto.KekTools``.

FMK decryption is described in section 6.4, TODO! ``crypto.Crypto.xor()``.

HHK derivation procedure is described in section 6.2, TODO! ``crypto.Crypto.deriveHeaderHmacKey(``).

The HHK and the original serialized form of the header must be used to check the HMAC using ``container.Envelope.checkHmac()``.

After a successful message authentication code check, the payload may be decrypted. In case the HMAC check was unsuccessful, the algorithm must return an error and terminate.

Decryption requires deriving the CEK. The corresponding procedure is described in section 6.2 TODO!, ``Crypto.deriveContentEncryptionKey()``.

Payload decryption is carried out in three stages: decryption, cryptogram authentication, and unpacking the decrypted archive.

Decryption and cryptogram authentication are described in section 6.6. TODO!
Archive unpacking is described in section 4.3.2. TODO!

