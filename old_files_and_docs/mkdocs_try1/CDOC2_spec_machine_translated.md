# Introduction

^0a0015

## Purpose

The purpose of this specification is to describe the CDOC2 data format for file classification.

## Handling area

Specification describes:

- supported encryption schemes
- abstract and sequenced data format
- details of cryptographic operations
- use of a key transfer server
- execution instructions

## Definitions and abbreviations

**CDOC** "Crypto Digidoc," the format used in the Estonian eID ecosystem for transmitting encrypted files.

**CDOC 1.0** unofficial term for all pre-CDOC vor (XML-ENC-based) pre-specifications.

**CDOC2** version of the CDOC format described in this specification.

**CEK** Content Encryption Key. A key used to encrypt the cargo of the container.

**ECC** Elliptic Curve Cryptography, cryptography of elliptic curves.

**ECDH** Elliptic-curve Diffie-Hellman, key application protocol

**FMK** File Master Key, the base key from which the CEK content encryption key is formed.

**HKDF** HMAC-based Key Derivation Function, a function that, with sufficient entropy, delivers keys suitable for cryptographic operation.

**KEK** Key Encryption Key, a key encryption key that encrypts the CEK content encryption key.

**KEM** key encapsulation mechanism, key encapsulation mechanism

**Container** single CDOC2 format file.

**Last** Payload, a set of files transmitted using the CDOC2 format. This term refers to this set in the form of an open text.

**OAEP** Optimal Asymmetric Encryption Padding, Filling Scheme, usable with RSA for Encryption

**Header** CDOC2 format part describing container receivers and applicable cryptographic measures.

**RSA** Rivest-Shamir-Adleman, a public key crypto-system

**Receiver** party targeted by the CDOC2 container and controlled by key materials that can decrypt the contents of the container.

**The receiver identifier** is a cryptographic public key, personal identification code, identification name of the certificate holder, or other data mentor that allows you to decide whether a party is among the recipients of a particular container.

**Key capsule** The part of the CDOC2 format that contains the key for decrypting the encrypted cargo, the part of that key, or the data required for calculation by the receiver of that key. The sender may add the key capsule to the envelope or transmit it via the key transfer server.

**Envelope** The outermost layer of the CDOC2 format, which describes the encoding of a header and cargo into a single con second.

## Review

\[This section showed describe what the rest of the document contacts and plain how the document is organised.\]

# Problem setting

CDOC2 solves the problem related to CDOC 1.0 specifications [1, 2] and realizations based on the solution options proposed in the previous analysis [3].

CDOC2 solves the following CDOC 1.0 issues:

- CDOC 1.0 offers no future security. An attacker who has stored a CDOC container can open it in the future by compromising the keys or crypto algorithms used to create the container. The ROCA case [4] showed that this is not merely a theoretical problem.
- The CDOC 1.0 format and the software created for its processing do not distinguish between document encryption for transport between parties and document encryption for storage by one party.
- The CDOC 1.0 format does not allow sending an encrypted document to a receiver using only a mobile eID tool (Mobile-ID or Smart-ID).

## CDOC2 Encryption Schemes

The specification describes the following encryption schemes:

**SC.01**

Encryption for the public key of the receiver's ECC ID card, with all the material from the deck-kiv ECC KEM (Key Encapsulation Mechanism) included in the CDOC container. Does not provide additional security compared to the CDOC1.0 format. Used for both transport and storage cryptography.

**SC.02**

Encryption on the public key of the receiver's ECC ID card, with all the material from the deck rock ECC KEM being transmitted through the key transfer server. Provides additional security (partial future security) provided that the communication canal used to transmit the CDOC container and the content and communication channels of the key transmission server are both not readable by the attacker. Used for transport cryptography.

**SC.03**

Encryption for the public key of the receiver's RSA crypto stick, with all RSA-encrypted key material generated in the process being included in the CDOC container. Does not provide additional security compared to CDOC1.0 format. Usable for both transport and storage cryptography.

**SC.04**

Encryption for the public key of the receiver's RSA crypto stick, with all the RSA-encrypted key material generated in the process being transmitted through the key transfer server. Provides full-davat security (partial future security) provided that the communication channel that can be transmitted to the CDOC container and the content or communication channels of the key transmission server are not both readable by the attacker. Used for transport cryptography.

**SC.05**

Encryption for symmetrical key. Usable for both transport and storage cryptography. Use for transport cryptography requires prior transmission of the key through eavesdropping-proof non-systemic channels.

## Assumptions and requirements for communication channels

Similar to the previous specification CDOC 1.0, CDOC2 provides protection for data transmission through public and potentially attacker-readable communication channels (e.g. e-mail, USB memory device, file exchange services).

CDOC2 does not make any assumptions about the communication channel used to transmit the container and ensures the confidentiality of the data contained therein during the transmission of the container. As a general rule, CDOC2 does not guarantee future security of the forward message - i.e. an attacker who intercepts and stores the container may be able to decrypt it in the future.

CDOC2 also describes encryption schemes (SC.02 and SC.04) that offer partial future security, where some of the key material is transmitted from the sender to the receiver via key distribution server(s). The requirements for key transmission servers and their communication channels are described in section 4 separately for each scheme.

## Functionality that is out of scope

CDOC2 does not provide solutions for the following needs:

- Transmitter authentication. CDOC2 does not authenticate the sender. In order to authenticate the sender, the encrypted information may be signed before it is encrypted.

# Encryption Schemes

This section presents all supported encryption schemes in abstract form, describing the content of messaging and messages exchanged between the parties. The section is useful for an overview of the principles of action of different schemes.

In all scenarios, the sender (Alice, _A_) wants to send the message _M_ encrypted to the receiver (Bob, _B_). It can do this either directly or by using the key transmission server _S_ (or the servers _S1_, _S2_, . . . , _S$_n$_) help. Also, receivers can generally be several, in which case we will mark them B1, B2, . . . , Bl.

Alice uses Sym, a symmetrical cryptographic system with the following components.

1. Key Generating Algorithm _GenKeySym_ - This will generate a secret key. Section [[Specification translated#^08927b]]
1. _EncSym_, an encryption algorithm, is a function that requires a key and input (which we want to encrypt) as an argument and issues a cryptogram.
1. Decryption algorithm _DecSym_ - this is a function that requires a key and a cryptogram as an argument. If the argument is given as the key by which the cryptogram is encrypted, then the output-dix is the original input. Otherwise, the output is a random possible input.

The HKDF (extract, then expand) design is used to generate the keys. In the extract phase of HKDF, the _GenKeyExtractSym_ base key (File Master Key, FMK) is generated, from which the _GenKeyExpandSym_ content encryption key (CEK) is further derived in the expand phase. The latter is used as a secret key for symmetrical encryption. Symmetric encryption and decryption uses the ChaCha20-Poly1305 algorithm. Further details can be found in sections 6.2 and 6.6.
Alice encrypts the base key for each receiver individually using the Symmetrical-Rile Key Encryption Key (KEK) from the receiver.
The scenarios described below differ from each other in how KEK is created and when-das the key capsules containing the encrypted base key FMK are transferred to the receivers.

## Direct communication ECDH scheme

This scheme is used to send encrypted messages to receivers who are in possession of an ECC private key. Alice protects messaging with the Key Encapsulation Mechanism (KEM), which consists of _EncapsKEM_ and _DecapsKEM_.

Before encapsulation, Alice learns the receiver's public key as an elliptical curve point. Next, the drink-sets Alice with the receiver in the ECDH keying protocol.

**EncapsKEM** takes the receiver's public key for input and issues the key and capsule. The key is the key encryption key KEK, the derivation of which is described in section 6.3.1 and the cap ECDH realization is Alice's ephemeral public key.

**DecapsKEM** takes the key capsule and the receiver's secret key for input, verifies that the sent elliptic curve point is correct, carries out the other party's actions in the ECDH key-setting protocol, and reminds KEK. A more detailed explanation is given in section 6.3.1, "Calculation of CDE in decryption."

Direct communication scheme used:

1. A: fmk ← GenKeyExtractSym (Nonss)
1. A: cek ← GenKeyExpandSym (fmk)
1. A: c ← EncSym (cek,M)
1. A obtains public keys for receivers B1,B2,...,Bl PK1,PK2,...,PKl; receivers have the corresponding secret keys SK1, SK2, . . . , SKL
1. A: (keki,capsi) ← EncapsKEM (PKi) (i = 1,2,...,l)
1. A: cki ← XOR (keki,fmk) (i = 1,2,...,l)
1. A → Bi: c,cki,capsi (i = 1,2,...,l) [^1]
1. Bi: keki ← DecapsKEM (capsi, SKi)
1. Bi:fmk←XOR (keki,cki) [^2]
1. Bi: cek ← GenKeyExpandSym (fmk)
1. Bi: M ← DecSym (cek,c)

## ECDH schema with key transfer server

Also in this scheme, Alice protects message confidentiality with the ECDH key encapsulation mechanism, but the only difference here is that the capsule is transmitted via the key transfer server, thus providing additional security, provided that the key transfer server behaves regularly. Additional security is provided by using the authentication protocol Auth, which allows the server to authenticate the receiver.

Chart to be used with the key transmission server:

1. A: fmk ← GenKeyExtractSym (Nonss)
1. A: cek ← GenKeyExpandSym (fmk)
1. A: c ← EncSym (cek,M)
1. A obtains public keys for receivers B1,B2,...,Bl PK1,PK2,...,PKl; receivers have the corresponding secret keys SK1, SK2, . . . , SKL
1. A: (keki,capsi) ← EncapsKEM (PKi) (i = 1,2,...,l)
1. A: cki ← XOR (keki,fmk) (i = 1,2,...,l)
1. A → Bi: c,cki (i = 1,2,...,l)
1. A → S: capsi (i = 1, 2, . . . , (l)
1. Bi → S: Auth [^3]
1. S → Bi: capsi [^4]
1. Bi: keki ← DecapsKEM (capsi, SKi)
1. Bi: fmk ← XOR (keki,cki) [^5]
1. Bi: cek ← GenKeyExpandSym (fmk)
1. Bi: M ← DecSym (cek,c)

[^1]: When receiving the information, the receiver checks that the point of the sent ellipt curve is correct. If not, the error message "the emphatic public key generated by the sender is not correct" is issued and the protocol stops.

[^2]: In addition to decryption of fmk, the receiver verifies that the message authentication code received from the header is correct (more information in section 6.5). If not, a "message authentication failed" error message is issued and the protocol stops.

[^3]: Server authenticates the receiver. The server returns only the key capsule sent to the receiver.

[^4]: See footnote 1.

[^5]: See footnote 2.

## Direct communication RSA-OAEP scheme

This scheme is used to send encrypted messages to receivers who are in possession of a private RSA key.

Alice wants to protect the message security with an RSA-OAEP scheme that uses the _EncRSA_ encryption algorithm and _DecRSA_ decryption algorithm.

To declassify the key transfer key, the sender encrypts it with the receiver's public key. The key capsule is a cryptogram that the receiver decrypts with its private key.

1. A: fmk ← GenKeyExtractSym (Nonss)
1. A: cek ← GenKeyExpandSym (fmk)
1. A: c ← EncSym (cek,M)
1. A: keki ← GenKeySym (i = 1,2,...,l)
1. A: cki ← XOR (keki,fmk) (i = 1,2,...,l)
1. A obtains public keys for receivers B1,B2,...,Bl PK1,PK2,...,PKl; receivers have the corresponding secret keys SK1, SK2, . . . , SKL
1. A: capsi ← EncRSA (PKi,keki) (i = 1,2,...,l)
1. A → Bi: c,cki,capsi (i = 1,2,...,l)
1. Bi: keki ← DecRSA (SKi, capsi)
1. Bi:fmk←XOR (keki,cki)
1. Bi: cek ← GenKeyExpandSym (fmk)
1. Bi: M ← DecSym (cek, c)

## RSA-OAEP schema with the key transfer server

Similar to the previous schema, but the sender transmits the key capsule to the receiver via the key transfer server.

1. A: fmk ← GenKeyExtractSym (Nonss)
1. A: cek ← GenKeyExpandSym (fmk)
1. A: c ← EncSym (cek,M)
1. A: keki ← GenKeySym (i = 1,2,...,l)
1. A: cki ← XOR (keki,fmk) (i = 1,2,...,l)
1. A → Bi: c,cki (i = 1,2,...,l)
1. A obtains public keys for receivers B1,B2,...,Bl PK1,PK2,...,PKl; receivers have the corresponding secret keys SK1, SK2, . . . , SKL
1. A: capsi ← EncRSA (PKi,keki) (i = 1,2,...,l)
1. A → S: capsi (i = 1, 2, . . . , (l)
1. Bi → S: Auth
1. S → Bi: capsi
1. Bi: keki ← DecRSA (SKi, capsi)
1. Bi:fmk←XOR (keki,cki)
1. Bi: cek ← GenKeyExpandSym (fmk)
1. Bi: M ← DecSym (cek, c)

## Symmetrical key scheme

Alice protects the secret with a key-reference mechanism consisting of the algorithms _EncapsHKDF_ and _DecapsHKDF_ . Before encapsulation, Alice knows the symmetrical secret key of the receiver and its ni-me (the name will be agreed between the transmitter and the receiver, the name will help differentiate between the keys). _EncapsHKDF_ takes the receiver's symmetrical secret key and its name for input, and issues the key and the capsule. The key is the key encryption key KEK, the derivation of which is described in section 6.3.4, and the capsule is a data structure containing the caps decryption key tag and the random number used to derive the key. _DecapsHKDF_ takes the symmetrical secret key of the receiver, its name and key capsule for a si-cent. In the case of the correct inputs, the KEK will be derived from it. For further explanation, see Section 6.3.4, "Calculation of CDEs in decryption."

Symmetrical key diagram used:

1. A: fmk ← GenKeyExtractSym (Nonss)
1. A: cek ← GenKeyExpandSym (fmk)
1. A: c ← EncSym (cek,M)
1. A holds the symmetrical keys S1, S2, . . . , Sl marked with L1, L2, . . . , Ll
1. A: (keki,capsi) ← EncapsHKDF (Si,Li) (i = 1,2,...,l)
1. A: cki ← XOR (keki,fmk) (i = 1,2,...,l)
1. A → Bi: c,cki,capsi (i = 1,2,...,l)
1. Bi: keki ← DecapsHKDF (capsi, Si)
1. Bi:fmk←XOR (keki,cki) [^6]
1. Bi: cek ← GenKeyExpandSym (fmk)
1. Bi: M ← DecSym (cek,c)

## Security Prerequisites

The most general security goal of encryption is that _no one but the designated receiver (B) can decrypt the message M._

In order to achieve this objective, appropriate assumptions should be allowed for the schemes under consideration. It is always necessary _to allow the symmetrical cryptographic system used, Sym, not to break._

A diagram using asymmetric cryptography from section 3.1 uses the assumption that _the asymmetric crypto algorithm used does not break_.

A diagram using asymmetric cryptography from Section 3.2 uses the assumption that _usable asymmetric crypto algorithm does not break_.

The key transfer server works according to the rules.

# Container format

CDOC2 container format description is divided into two parts: abstract and specific. The abstract section describes the data elements and their relationships, the specific section describes how to sequence these data elements.

## Abstract Format

This section describes the CDOC2 format from an abstract view, giving data formations and and memos, but not a description of the serialized format.

### Basic principles

The principles set out here give the user of the specification a point of reference for the purpose of a more detailed specification.

- The abstract format consists of a header and encrypted cargo.
- The abstract format contains one encrypted cargo with one to several files encrypted inside. Information about the names of these files, as well as what their sizes and sequences are for several files, is also encrypted.
- The child is encrypted with a single symmetrical key (CEK) using the AEAD (Authenticated Encryption with Additional Data) encryption method.
- CEK is obtained by key query from the CDOC file base key (File Master Key; FMK). See section 6.2.
- FMK can be encrypted in parallel with one to several key encryption keys (Key En-encryption Key; KEK), one for each receiver. For the generation of KEK, see section 6.3.
- The header describes how FMK is protected (how receivers can acquire the KEK needed to decrypt FMK).
- The integrity of the header is ensured by a message authentication code, which is calculated using a message authentication key (HHK) inherited from FMK. See Section 6.5.
- In order to ensure the universality of the format, elements of the EES eID infrastructure have not been directly used in this description. For example, the receiver is described using his public key, not a certificate.
- Decryption always corresponds to one pattern: 1) receiver acquires KEK, 2) receiver decrypts FMK, 3) receiver inherits HHK and validates header, 4) receiver inherits CEK, 5) receiver decrypts cargo.

### Header Structure

_A pseudocode is used to describe the header structure, which does not correspond to any programming or schematic language, but which could be intuitive._

The header consists of one to several structures describing the receiver. The structure of each receiver contains complete information on how a particular receiver can access FMK (in the case of identification of a person, access to cryptographic material, etc.).

The message authentication code is calculated on the header using a key derived from FMK. This is necessary to prevent the header from being manipulated by its transmitters, for example to hide part receivers. The message authentication code shall be calculated on the header in a specific way sequenced (see section 4.2).

```
Header = {
    Recipients              = :Recipient[](1..k)
    PayloadEncryptionMethod = :enum(CHACHA20-POLY1305)
}
```

A message authentication code is calculated for the header (see section 6.5 for details):

```
Checksum = {
    value = HMAC(HHK, Serialize(Header))
}
```

The recipient is described by the `Recipient` structure. The structure of the structure gives the reader the opportunity to decide quickly and unambiguously whether he or she has the possibility to decrypt the cargo on the basis of a specific copy of the `Recipient`.

```
Recipient = {
    Capsule = Union(:ECCPublicKeyCapsule | :KeyServerCapsule |
            :SymmetricKeyCapsule | :RSAPublicKeyCapsule )
    KeyLabel = :string
    EncryptedFMK = :byte[]
    FMKEncryptionMethod = :enum(XOR)
}
```

Structure `Recipient` consists of key capsule, receiver key name, encrypted FMK, and FMK encryption method identifier.

- `Capsule` - encryption scheme-specific data by which the receiver can decrypt FMK.
- `KeyLabel` - FMK decryption requires private or secret key human-readable name. Its presence is necessary to build a reasonable user interface. The sender shall complete this field on the basis of the key or related certificate. The specification does not specify how this is done, as it is not relevant for cryptographic processing. The format is a UTF-8 string.
- `EncryptedFMK` - encrypted FMK.
- `FMKEncryptioMethod` - FMK encryption methods type.
The successful processing of the `Capsule` structure results in a cryptographic key with which to decrypt FMK using a method determined by the `FMKEncryptionMethod` field. See section 6.4 for details of cryptographic operat ions.

The following types of key capsules are specified to support different encryption schemes (Section 3).

- `ECCPublicKeyCapsule` - The receiver's feature is the ECC public key `RecipientPublicKey` (such as the public key for the first pair of ID cards). KEK is inherited using ECDH. Use an encryption scheme for SC.01. See Section 3.1.
- `RSAPublicKeyCapsule` - The receiver's feature is the RSA public key `RecipientPublicKey`. KEK is obtained by decrypting the key capsule using a private RSA key. Used for the encryption mode SC.03. See Section 3.3.
- `KeyServerCapsule` - The recipient's public key is used to authenticate the recipient to the key distribution server. The key distribution server issues an `ECCPublicKeyCapsule` or `RSAPublicKeyCapsule` object, which is used according to its description. Used for the encryption schemes SC.02 and SC.04. See Section 3.2 and Section 3.4.
- `SymmetricKeyCapsule` - KeyLabel is the key name of the receiver. KEK is inherited by means of HKDF from a symmetrical key provided by the user. Used for the encryption scheme SC.05. See Section 3.5.
- Future versions of the specification may supplement this list.

### Key capsule types

ECC public key capsule. `RecipientPublicKey` is the public key of the ECC.

```
ECCPublicKeyCapsule = {
    Curve              = :enum(secp384r1)
    RecipientPublicKey = :byte[]
    SenderPublicKey    = :byte[]
}
```

- `Curve` - the characteristic of the elliptic curve used.
- `RecipientPublicKey` - the receiver's ECC public key for finding the receiver's thought-dud receiver record.
- `SenderPublicKey` - the transmitter's public key used by the receiver to derive KEK using ECDH.

RSA Public Key Capsule. `RecipientPublicKey` is the public key of the ECC.

```
RSAPublicKeyCapsule = {
    RecipientPublicKey = :byte[]
    EncryptedKEK       = :byte[]
}
```

- `RecipientPublicKey` - the receiver's RSA public key for finding the receiver's thought-dud receiver record.
- `EncryptedKEK` - a key transfer key encrypted by the receiver's public key.

Key server capsule. The receiver is identified by his ECC or RSA public key `RecipientPublicKey`.

```
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
```

- `RecipientKey` - the data of the receiver key with which the receiver authenticates itself to the key transfer server.
- `KeyServerID` - key transfer server identifier. On this basis, the recipient must be able to connect and connect to the network address of the lei-da key transmission server.
- `TransactionID` - the identifier of the key capsule sent by the sender to the receiver for transmission to the key exchange server.

Symmetrical key capsule. The receiver identifier is the name of the symmetrical key in the user's possession `KeyLabel`.

```
SymmetricKeyCapsule = {
    Salt   = :byte[]
}
```

- `Salt` - a random number generated by the transmitter and used as the inside of the HKDF-Extract function.

### Format ending

To extend the format and ensure greater compatibility, one approach has been proposed. This involves a union type field Capsule in the header structure of the Recipient – each type of the union describes some kind of recipient with its cryptographic primitives and key management components. The format, both in its abstract and concrete form, allows the addition of these types according to the needs.

## Sequenced format

This specification describes how to realize an abstract format based on Flat-Buffers^[https://google.github.io/flatbuffers/].

### General format description

The format consists of an envelope which is essentially sequenced and joined after each other by a header, a message authentication code and a cargo.

The message authentication code and the cargo are sequenced in a simple way.

The header, due to its expansion needs and the need to transport the same incorrect messages through the key transfer server from the header processing logic view, is described on the basis of the format FlatBuffers.

In addition to the header extension mechanism, the envelope of a specific format defines another extension point.

In the fifth position of the envelope is a version identifier, which is fixed to the value "2" in the context of this specification (the byte value). When describing new versions, this identifier must be changed.

### Envelope

The envelope consists of the following data elements, presented one after the other as bytes. The marking of the beginning and end of the envelope is not within the scope of this specification, as the main and natural use is that of which there is exactly one envelope in one CDOC file.

- 4 bytes: string "CDOC" - format marker (i.k. prelude), encoded by UTF-8.
- 1 byte: version identifier, according to its specification with the value 2.
- 4 bytes: length of the following header, big endian performance. The length of the header is a 32-bit integer with a mark, i.e. the maximum size of the header could be 2 GB. For ease of realization, the header size is limited to 1MB ($2^{20}$) byte.
- Previously specified amount of bytes: sequenced FlatBuffers header.
- 32 bytes: message authentication code for the header (see section 6.5).
- Rest of bytes until the end: the chart and key-encrypted cargo specified by the header.
Table 1 represents the envelope structure.

| Gap?   | CDOC" | Version | Header length | header        | HMAC               | The rest                |
| ------ | ----- | ------- | ------------- | ------------- | ------------------ | ----------------------- |
| Length | 4     | 1       | 4             | header length | 32                 | Fill the envelope       |
| Offset | 1     | 5       | 6             | 10            | 10 + header length | 10 + header length + 32 |

Table 1. Envelope Structure

### Basic message authentication code

The technical description (scheme) of the FlatBuffers format scheme is provided in the reference realization source code repository, directory `cdoc2-schema/`.

The scheme is described in two files, which are given in the annexes to this specification.

1. **src/main/fbs/header.fbs** - FlatBuffers header description.
1. **src/main/fbs/recipients.fbs** - Descriptions of receiver types, shared by schemes in other files.

The header, sequenced according to the FlatBuffers rules, is written in an envelope and, according to the description of the envelope, a 4-byte length field is written in front of it.

The message authentication code for the header shall be calculated in accordance with Section 6.5 and written by bytes directly after the header. the algorithm and therefore the length of the message authentication code is determined by its specification ion.

### The rest

The last entry in a container composed according to CDOC formatting is the message authentication code, at the very end. The format assumes that the last token is determined externally, for example by the file ending.

It is important to note that the trait of the end of the cargo is only indicative - the actual integrity of the cargo is determined by whether the cargo can be decrypted in its entirety or not.

The formation of the cargo opening text is described in section 4.3.

Cargo encryption is described in section 6.6.

### Formatting Instructions

_This section refers to the reference realization source code using Java package names and other identifiers. Such references are_ `given in a continuous step`.

The following steps should be taken when preparing the CDOC2 container:

- Collect a list of all recipients.
- Generate FMK, HHK and CEK.
- Create a header with all accompanying cryptographic operations.
- Calculate a message authentication code for the header.
- Prepare the opening text of the cargo.
- Encrypt the child.
- Create a sequential shape of the envelope.
- Securely delete FMK, HHK and CEK values used during work.

Preparation of the cargo opening text is described in section 4.3. `container.Tar.archiveFiles()`

The following is the preparation of cryptographic material to protect the header and cargo. The generation and derivation of the relevant keys (FMK, HHK and CEK) are described in section 6.2. `container.Envelope.prepare()` and `container.Envelope()`

The list of all desired receivers must then be collected and sequenced, as the cryptographic methods used to ensure the integrity of the container operate with a complete sequenced header.

For each receiver, the required cryptographic procedures described in sections 6.3 and 6.4 shall then be calculated for the message authentication code of the header, in accordance with section 6.5.

Cargo encryption is described in section 6.6. `Crypto.ChaCipher.encryptPayload()` and `crypto.ChaCipher.initChaChaOutputStream()`

The exact serialized envelope format is listed in section 4.2.2.

Upon completion of the encryption process, the used cryptomaterial (symmetric keys, ephemeral private keys) must be securely deleted. Secure deletion depends heavily on the runtime environment used, in some cases (e.g. JVM) it may not be possible. The developer must assess what options are available for this in the programming language and runtime environment used.

### Format Parsing Instructions

_This section refers to the reference realization source code using Java package names and other identifiers. Such references are given `in a continuous step`_.

Container Parsing Reference Realization is a function of `container.Envelope.decrypt()`. This is the primary input point into the decryption logic, and its purpose is to take the encrypted container given as input and write the files contained in it into a predetermined folder.

This function does the following, and all alternative realizations must do so by implementing all appropriate security controls.

- Pars the envelope and decodes the header from the envelope
- Decrypts/derives the KEK.
- Decrypts/derives container-specific keys FMK, HHK and CEK.
- Verifies the message authentication code for the header.
- Decrypts the archive.
- Separates files from the encrypted file archive and writes them in a predetermined folder. Streaming mode-that is decryption and file separation in one operation.

The reference realization of envelope parsing and header decoding is the container function. `Envelope.readFBSHeader()`.

The header must be parsed using the Flatbuffers library using the `fbs.header.Header` root type (in the reference realization, the function generated by the FlatBuffers scheme is `fbs.header.Header.getRootAsHeader()`).

Full header parsing is given in the reference realization function `container.Envelope. deserializeFBSHeader()`.

The header shall contain a receiver (`Recipient`) corresponding to the processing party of the container and be inherited or decrypted by KEK, FMK and HHK. The method of identification of the receiver is described in section 6.3 for each encryption scheme. If a receiver corresponding to the processing party has not been found, it is not possible to decrypt the container. In this case, the algorithm must issue an error that the container is not designed to open to the processor and stop working.

The calculation of KEK is described in section 6.3. If an error occurs during the calculation of the KEK (for example, the point is not on the elliptic curve), then the algorithm must issue an error and stop the work. The KEK calculation functions are in the class `crypto.KekTools`

FMK decryption is described in section 6.4. The process of inheriting `crypto.Crypto.xor()`

HHK is described in section 6.2. `crypto.Crypto.deriveHeaderHmacKey()`

HHK, and the message authentication code of the header must be checked based on the original serialized shape of the `header.container.Envelope.checkHmac()`

Only after successful verification of the message authentication code can the cargo be decrypted. If the header's message authentication code check failed, then the algorithm must issue an error and stop working.

For decryption, the CEK must be inherited, the corresponding procedure is described in section 6.2. `crypto.Crypto.deriveContentEncryptionKey()`

Decrypting consists of three different steps: decrypting, cryptogram authentication, and unpacking the decrypted archive.

Decryption and cryptogram authentication are described in section 6.6.

Unpacking the file archive is described in section 4.3.2

## Unencrypted cargo

This section describes in more detail the format and processing of unencrypted cargo.

Main features of the format:

- Transfer files are archived using POSIX tar format [5].
- Archived files are packed using the ZLIB method, standardised as IETF RFC 1950 [6].

The open text of the container cargo is formed in the following way: from the files (or also from one file) to be transmitted, a POSIX tar archive is formed, which is packaged in the ZLIB format as a whole.

> Reality note: The DD4 client uses the corresponding wrap point zions of Qt to address the zlib library. Since they cannot be used in flow mode (streaming mode), the specification includes a recommendation to replace the use of Qt diapers with zlib flow mode challenges. This becomes particularly important in storage crypto, where volumes can be large and single-use encryption of data in memory buffers is not possible.

### Requirements for POSIX tar archival drafting

Since the format `tar` has a long history and several variations, it is described here which requirements must be met by the archive prepared for CDOC2. The purpose of these requirements is to reduce compatibility problems with different client applications and/or management systems and to allow files to be written into the file system as safely as possible from the archive.

- A standardised POSIX tar dialect [5] is used. This format is also known as "POSIX 1003.1- 2001" or "PAX."
- All file names are provided in the UTF-8 encoding.
- More than 100B file names are supported by the PAX header extension [5]
- Files over 8GiB are supported by the PAX header extension [5]
- File names are written into the archive without directory paths (basename).
- Permissions and other security arguments written in the archive are ignored (they can be written but not read).
- Only regular files (type 0) are written into the archive.
- Files are treated as binary files.

### Requirements for unpacking cargo

The packaging of the payload has been selected such that it can be unpacked in streaming mode. This means that the entire encrypted payload does not need to be loaded into memory for processing. The payload can be decrypted, unpacked, and written to the disk in plain form sequentially.

In the case of decryption, encrypted data is used before the cryptographic checksum is checked. When unpacking, it must be taken into account that the package may be corrupted and does not comply with the rules specified in the specification or is maliciously assembled by the attacker. Since the sender of the CDOC2 container is not authenticated, it must always be taken into account that the package may have been assembled by an attacker - even if the cryptographic checksum matches.

Errors (wrapping or archiving errors) arising from the processing of open text shall not be treated in flow mode until the entire cargo has been passed and the cryptogram authenticated. If cryptogram authentication failed, this error must be reported. Only when cryptogram authentication has succeeded can an error in the processing of the open text be reported. In the event of an error, all created files must be deleted.

According to the specification, software must build protection measures against the following two attacks.

> The list of possible attacks is not final - for example, the content of the file may be a virus or malware, and must be controlled with an antivirus before it is used - but this attack is not CDOC2 specific, but applies to the use of any file obtained from an unreliable source, and therefore it is not described here for longer.

First attack: An attacker can create a packed cargo, which, when unpacked, forms a giant file. If the receiver processes the cargo in memory, the application may crash. If the receiver writes the cargo on the disk, the disk can be full. When unpacking, it is reasonable to set the maximum allowable size for unpacked files and to check the size of the free memory or free disk space when unpacking. If the files to be unpacked are larger than allowed or the free memory or the free disk space has shrunk below the permitted limit, the unpacking must be interrupted, the files written on the disk must be removed and the error reported.

Second attack: the attacker can manipulate the attributes of files contained in the tar file - names, permissions, security arguments and types. If such a tar file is unpacked without additional checks, the attacker may be able to overwrite existing system files, add new files, create files that are not visible to the average user but may be necessary for carrying out some attack, etc.

Since the CDOC2 container is not intended to be a universal archive format, but simply to offer the possibility of simultaneously encrypting multiple files while preserving the original names of the file for the convenience of users, a number of rules have been established for unpacking the tar file, the following of which provides protection against the aforementioned manipulations:

- When creating files, you must ignore the permission abits in the archive, the characteristics of the file owner and group, and other security arguments - all files must be created as non-launched, as the user who started the application, and as readable and writeable to him.
- Only regular files (type 0) should be created. If there is another type of file in the archive, it is necessary to interrupt the unpacking, remove the files written on the disk so far, and make a mistake. A correct CDOC2 client program must not create files that contain other types of files.
- Check the safety of the file name before writing the file to the disk. If you find a file name that contains unauthorized symbols, stop unpacking, remove the files that have been written on the disk so far, and make a mistake.
Checking file name safety has the following objectives:
- Avoid a directory jump (Path traversal) [7] attack and create files outside the user's specified directory.
- Avoid creating files with names that are inaccessible to the user or difficult to access, containing special characters.

Pathvalidate^[[GitHub - thombashi/pathvalidate: A Python library to sanitize/validate a string such as filenames/file-paths/etc.](https://github.com/thombashi/pathvalidate)] is a very comprehensive Python library for checking filenames - similar checks must be made when ramming in other languages.

The SEI CERT directory [8] describes an additional way to protect against catalogue jumps.

List in the reference realization `container.FileNameValidator`:

- must not start with a space or a hyphen;
- must not end with a space or a dot;
- must not include any of the following: CON, PRN, AUX, NUL, COM[1-9], LPT[1-9];
- must not contain the following symbols: <, >,:, \, /, ,?, *;
- must not contain control symbols [9].
- must not contain Unicode Right-To-Left Override (U+202E)

# Key transfer server

This section defines the key transfer server (here also in the section: server), its external interfaces and rules of use.

## Introduction

A key transfer server is a subsystem designed to transfer the key capsule required for decrypting a CDOC container from the transmitter to the receiver, following the rules described in Section 3 for a specific crypt sharpening scheme.

The communication channel provided by the key transmission server is more secure than the public communication channels, whose folder is transmitted to CDOC2 containers. A normally functioning key transfer server ensures the future security of the data transmitted in a crypto-directed manner, since an attacker who monitors a public communication channel cannot possess symmetrical encryption keys classified by means of crypto-algorithms with a public key - they move through the key transfer server in a secure manner. Thus, in the future, after breaking crypto algorithms with a public key or compromising private keys, an attacker cannot break crypto keys. The key transfer server does not have to mediate large encrypted documents - so the cost of operating it is low.

A number of key transmission servers may be used at any one time, and may be operated by different organisations. Security requirements established in the course of the investigation may require the operation of each individual key transmission server by independent organisations.

## Server operating principle

In the simplest case, the server works as follows:

1. In the course of encryption, the sender creates a key capsule designed for a particular receiver.
1. The sender selects the server, connects to it and sends it a key capsule with the receiver identifier.
1. The server generates a transaction identifier and stores it together with the recipient's identifier in the capsule.
1. Place the server identifier, transaction identifier and recipient identifier on the data container.
1. The shipper sends the container to the receiver.
1. The receiver will find information about the key capsule for him/her in the container.
1. The receiver connects to the server selected by the sender and authenticates itself to it.
1. The receiver sends the transaction identifier received from the container to the server.
1. The recipient's identifier based on the authentication process of the server transaction identifier is taken from the capsule.
1. The server returns the key capsule to the receiver.
1. The receiver uses the information in the key capsule to decrypt the container.

## Server status

The server status is formed by the key capsules given to the server for transmission together with the monthly luva information.

- Key capsule, byte array. No meaning for the key server.
- Transaction ID - a UUID generated by the server itself using a cryptographically strong random number generator.
- Receiver identifier - a kind of identifier that the server receives as the output of the authentication process of the receiver.
- Period of validity. The key transfer server holds the key capsule only for a specified period of time, which is determined by the cooperation between the transmitter and the key management politics applied by the key transfer server. After this time the capsule is deleted.

## Server Interfaces

The server offers two interfaces: one for transferring the key capsule to the server and one for transferring the key capsule to the receiver.

The interfaces are formally described in OpenAPI [10] (see Annex C).

### Transmitter interface

The transmitter interface of the key transmission server is used by the transmitter to transfer the key capsule to the server and receive the transaction identifier that it inserts into the container header.

The sender sends the key capsule and receiver identifier to the server and receives the transaction identifier generated by the server.

This interface is not authenticated - it can be used by all transmitters.

### Receiver interface

The receiver interface of the key transmission server is used by the receiver to receive the key capsule from the server.

The receiver authenticates itself to the server and sends the transaction identifier. The server will find the key capsule based on this. The capsule must have been sent to the same receiver that authenticated the server - the server compares the receiver identifier obtained as a result of authentication with the receiver identifier specified by the sender of the key capsule. The server returns the key capsule to the receiver.

### Interface security

The TLS 1.3 protocol shall be used to secure the Interfaces. The server holds a certificate taken from a public, recognized CA. Customers check the validity of this certificate from CA using the OCSP protocol at each connection.

In order to ensure the security of the protocol, it is important to ensure that the key capsule can only reach the key transmission server. This is done by embedding (pinning) the TLS keys on the server. This ensures that the TLS inspection^[[https\_interception.pdf](https://zakird.com/papers/https_interception.pdf)] common today does not violate the confidentiality of key material.

## Receiver Authentication

Each key capsule type using the key transfer server describes the way the receiver is identified and authenticated.

This version of the specification defines one key capsule type that uses the key date server: `KeyServerCapsule`.

Future versions of the specification may supplement this list. There may be several different authentication schemes at the same time.

### `KeyServerCapsule` authentication scheme

In this scheme, the receiver is identified by its public key, which it uses to decrypt the container. The public key is assigned to the `KeyServerCapsule` structure by using `RecipientKey`

Server uses TLS Client Authentication (mTLS) to authenticate the receiver. The server is configured to check the validity of the client certificate (e.g. using the OCSP protocol). If the Vas host loses control of its decryption key and revokes its certificate, the key transfer server will not issue the key capsule to the new card holder (attacker) and the attacker will not be able to decrypt the container.

After successful authentication, the server reads the client's public key from the certificate used by the client and compares it to the public key associated with the key capsule referenced by the transaction identifier. If they coincide, the server returns the key capsule. Otherwise, the server returns the error.

## Server identification and trust

The additional security features provided by CDOC2 apply to the identification and trust of servers only if the key capsule is transmitted via the server rite with the features provided by the specific encryption scenario (see section 3).

In order for the receiver and sender to be sure which servers they are communicating with, either in the DigiDoc software installation package or otherwise, a list of trusted key-transmission servers must be distributed to each client using the CDOC2 format. The list is also used to embed TLS keys.

This list contains the following elements:

- Server identifier.
- Type of key capsule supported by the server.
- Recipient interface URL.
- Recipient interface URL.
- Identification of the organization that manages the server.
- Server public keys that allow the client to cryptographically contrast the server's identity. Public keys are in the form of certificates.
The sender never transmits the server's technical access point to the receiver, but only an identifier from that list. This is necessary to prevent attacks where the receiver is attracted to communicate with an unreliable server.
If several independent key transmission server infrastructures are ever set up that do not coordinate the attribution of identifiers to the servers and the same identifier is used to designate different servers in both systems, then a situation may arise where a client using one infrastructure creates a container that is attempted to open by a client using another information structure.
In this case, the receiver will contact the wrong key transfer server, authenticate itself to it and send the transaction identifier from the container. The server cannot find the key capsule corresponding to this transaction identifier and returns the error - decryption fails.

The key transfer server used by the receiver will know the transaction identifier, but since it does not have the ability to authenticate to the correct key transfer server on behalf of the receiver, it cannot download the key capsule from there either. The key capsule type supported by the server allows the sender to select the correct key capsule type and allows the receiver to authenticate itself to the server with the correct protocol.

Since the servers are light-weight, if one organization wants to support several different types of receiver, it will have to run several key-transmission servers. This allows each key transfer server to be made easy-to-tax and thus safer. This is particularly important at the receiver interface, where authentication protocols with very different features can be used, which are difficult to securely connect.

The identifier of the organization managing the server need not be associated with the name of the organization as disclosed, but it must enable the identification of which servers are controlled by the same organization. This information is needed to support future CRSs.

More than one public key may be assigned to each server - this is necessary for the smooth exchange of certificates and keys. When contacting the server, the client must always account for the server's use of one of the listed certificates. This helps to exclude mediation attacks.

# Cryptographic Details

This section describes all cryptographic calculations in CDOC2 format. Most of these calculations are neutral with regard to the wider technological infrastructure, but in some cases there are specific links with the eID tools used in Estonia (e.g. ID-card) - these links are indicated in the respective places.

## Security level and cryptographic algorithms used

Recent studies [11] and [12] estimate that 128-bit security will continue to provide protection beyond 2031. This offer is also confirmed by a fresh 2022 study [13]. Based on this, we use the following algorithms:

- HKDF-SHA-256,
- HMAC-SHA-256,
- ChaCha20-Poly1305.
The hashtag family SHA2 has been standardized for a long time. Based on recent studies (see [14]), the hashtag family SHA2 remains secure and SHA-256 provides 128-bit security.

A thorough security analysis has been carried out for the key query function used, HKDF (more detailed presentation in section 6.2) [15]. HKDF also recommends the use of a secure hash function [11].

A 128-bit key is sufficient for HMAC security [14].

ChaCha20-Poly1305 is a secure (IND-CPA and INT-CTXT) authentication encryption algorithm (see e.g. [16]). ChaCha20 as a serial shifter also provides 256-bit security [14].

For FMK encryption, XOR-operated encryption (one-time pad) is used, providing 256-bit security.

Key lengths used for symmetrical keys.

- FMK - 256 bits
- HHK - 256 bits
- CEK - depends on the cargo encryption algorithm used, 256 bits for ChaCha20-Poly1305.
- KEK - depends on the FMK encryption algorithm used, 256 bits for XOR.

## Succession of keys

In order to inherit keys, the CDOC2 format uses the HKDF key query function, which is specified as IETF RFC 5869 [17].

RFC 5869 defines two key query functions: `HKDF-Extract` and `HKDF-Expand`, the benefits of which are described below. In the future, the shorter `Extract` and `Expand` variants will be used to mark these features.

The key query uses the SHA-256 hash function everywhere, so the output of these functions is a 256-bit value.

All textual constants must be encoded by the UTF-8 encoding before they are given input to the functions (cryptographic function input here is byte arrays and integers), the quotation marks in the specification are not part of strings.

Commonly used symmetrical keys are inherited as follows:

**File Master Key, FMK** _FMK ← Extract ("CDOC20salt,"random)_

Where the _CDOC20salt_ has a constant string and the _random_ has a value of at least 256-bit, which is generated by cryptographically strong random number generator (CSPRNG).

**Content Encryption Key, CEK** _CEK ← Expand (FMK,"CDOC20cek,"Loctets)_ The _Loctets_ function determines the output length of _Expand_ in bytes and must be the same as the key length of the symmetrical encryption algorithm that is to be forced (see section 6.6).

**Header HMAC Key, HHK** _HHK ← Expand (FMK,"CDOC20hmac,"32octets)_

It is important to note that the length of HHK inherited in this way is 256 bits, or as much as the output of the used SHA-256 hash algorithm. This is due to the recommendations of the HMAC standard [18].

**Key Encryption Key, KEK** Succession of KEK depends directly on the type of receiver used and is described in the corresponding format elements:

- `ECCPublicKeyCapsule` - p. 6.3.1.
- `RSAPublicKeyCapsule` - p. 6.3.2.
- `KeyServerCapsule` - p. 6.3.3.
- `SymmetricKeyCapsule` - p. 6.3.4.

## Description of the header elements and calculation of KEK

The abstract structure of the header is described in section 4. Fields are described in an abstract structure with primitive data types. This section describes how to calculate fields and bring values into the shape of a primitive data type.

_Key Encryption Key_ (KEK) calculation depends on the type of receiver. Below, KEK is calculated separately for each receiver type.

### ECCPublicKeyCapsule

`ECCPublicKeyCapsule` (see Table 2) refers to a receiver identified by its ECC public key. The CDOC2 format supports the use of any public key generated by the secp384r1 ellipt curve as the recipient. For example, this key may be the public key of the Estonian ID-card authentication key couple.

The TLS 1.3 encoding used for the ellipt curve points is identical to the CDOC 1.0 for the secp384r1 curve.

The structure of `ECCPublicKeyCapsule` corresponds to the key capsule within the meaning of the protocols in sections 3.1 and 3.2 of the caps.

| Field                | Content                                                                                 | Coding                                                                           |
| -------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `Curve`              | The ellipt curve used, currently only secp384r1.                                        | According to the format used, see the description of the scheme.                 |
| `RecipientPublicKey` | Public key for the receiver. For example, the public key of ID-card 1. key pairs        | The public key is coded according to TLS 1.3 rules [19, p. 4.2.8.2].             |
| `SenderPublicKey`    | Public key for the ephemeral (short-lived or even one-off) key pair of the transmitter. | The public key shall be coded in accordance with TLS 1.3 rules [19, p. 4.2.8.2]. |

The transmitter calculates the KEK self-generated ephemer key pair using the secret key and the receiving and public key using the Diffie-Hellman Keying (ECDH) defined on ellipsears and applies the key query function assigned to the result obtained. The receiver shall perform a similar calculation using the emphatic public key of the sender and the authentic team key pair of the ID-card. Details of the calculations are given below.

The ephemeral key pair of the sender is anonymous, i.e. it has nothing to do with the public identity path of the sender.

In the case of multiple receivers, the transmitter may use the same ephemeral set-up within one CDOC container.

The ephemeric key pair of the transmitter consists of a public and secret key: _(pkeph, skeph)_.

The receiver has the public key _pkrec_ of his ID-card authentication key pair (we assume that the receiver's pri-key is not directly accessible).

This key is also available to the sender. The mechanisms for disseminating the receiver's public key are not within the scope of this specification.

#### Calculation of KEK in the course of encryption

The secret of shared ECDH is calculated by the sender as follows: _Secdh ← (skeph · pkrec) x_, i.e. the x-coordinate of the ellipt curve point thus calculated is a shared secret. The shared secret is coded as a big-endian byte array whose length in full bytes corresponds to the length of the used ellipt curve module in full bytes. For example, for the secp384r1 curve, it is 48 bytes.

KEK is calculated from the shared secret as follows:

_KEKpm ← Extract ("CDOC20kekpremaster," Secdh)_

_KEK ← Expand (KEKpm, "CDOC20kek" || algId || pkrec || pkeph, Loctets)_

Here _algId_ of the crypto algorithm used for FMK encryption is defined as a string according to the `Recipient.FMKEncryptionMethod` field (section 6.4).

_Loctets_ determines the output length of _Expand_ in bytes and is determined by the symmetrical encryption algorithm used for FMK encryption.

#### Calculation of KEK during decryption

The Estonian ID-card supports the use of the authentication keypad as one of the ECDH parties.

A suitable way to use this functionality is through the PKCS#11 function `C_DERIVEKEY`, also by suturing the mechanism `CKM_ECDH1_DERIVE`.

You can also use the Windows crypto functions `NCryptSecretAgrement` and `NCryptDeriveKey`. `NCryptSecretAgrement` computes _Secdh_ and `NCryptDeriveKeyar`- quails KEKpm to derive the key. The parameters of NCryptDeriveKey should be set as follows:

You can also use the Windows crypto functions `NCryptSecretAgrement` and `NCryptDeriveKey` to derive the key. `NCryptSecretAgrement` calculates _Secdh_ and `NCryptDeriveKey` calculates _KEKpm_. The parameters of `NCryptDeriveKey` shall be set as follows:

- `hSharedSecret` - a handle returned by `NCryptSecretAgrement`.
- `pwszKDF` - constant `BCRYPT_KDF_HMAC`.
- `pParameterList` - algorithm parameters:
    - `KDF_HASH_ALGORITHM` - constant `BCRYPT_SHA256_ALGORITHM`.
    - `KDF_HMAC_KEY` - constant `CDOC20kekpremaster`.
    - `KDF_SECRET_PREPEND` - this parameter should be omitted.
    - `KDF_SECRET_APPEND` - this parameter should be omitted.

All ID-cards in use today are known to validate the ellipt curve point in the ECDH Keyboard Input, but this control can be realized in the CDOC support software to improve the user-friendliness of the error management.

In order to check that the point _Q = (x, y)_ is on the curve, it is necessary to check that _x_ and _y_ are the range from which _[0..p - 1]_, satisfy the equation of the curve, and whether the point is in the right subgroup. For example, the equation for curve P-384 is _y2 == x3 -3x + b mod p_.

In addition, it shall be verified that _nQ = 0_ and _Q != 0._ Constants _b_, _p_ and _n_ are described in standard [20].

The `C_DERIVEKEY` function input must be provided with the efemeric public key _pkeph_ of the transmitter and a reference to the vas practice ID-card key pair _(pkrec, skrec)_. Receiver calculates _S'ecdh ← (skrec · pkeph) x_ .

Due to the algebraic properties of the elliptic curve, the equation _Secdh = S'ecdh_ applies.

From this shared secret, KEK must be calculated in exactly the same way as described in the encryption.

### RSAPublicKeyCapsule

`RSAPublicKeyCapsule` (see Table 3) refers to a receiver that is identified by its RSA open-link key.

The structure of `RSAPublicKeyCapsule` corresponds to the key capsule in terms of protocols in sections 3.1 and 3.2 of the caps.

The transmitter generates random KEK and encrypts this receiver with the RSA public key using OAEP filling. The receiver decrypts the encrypted KEK with its RSA private key. Details of the calculations are given below.

The receiver's public key is also available to the sender. The recipient's public key distribution mechanisms are not within the scope of this specification.

| Field                | Content        | Encoding                                                                               |
| -------------------- | -------------- | -------------------------------------------------------------------------------------- |
| `RecipientPublicKey` | RSA Public Key | The value is the RSAPublicKey DER encoding of the ASN.1 structure, see [21, p. A.1.1]. |
| `EncryptedKEK`       | Key transfer key encrypted by the receiver's public key.               |   XXX                                                                                     |

#### Calculation of KEK

^08927b

The symmetrical encryption algorithm used to encrypt FMK during encryption determines the length of KEK _Loctets_. The transmitter generates a random number of _Loctets_ length KEK.

The transmitter uses the RSA-OAEP (see [21, p. 7.1]) encryption function to encrypt KEK. RSA- OAEP requires three parameters (see [21, p. A.2.1]):

- `hashAlgorithm` - hash function used by the algorithm. We use the hash function SHA-256 (`id-sha256`)
- `maskGenAlgorithm` - a mask generation function used by the algorithm. We use the MGF1 (`id-mgf1`) function, which is parametrized with the SHA-256 hash function.
- `pSourceAlgorithm` - tag source function. We use a blank tag (`pSpecified Empty`).

#### Calculation of KEK during decryption

The recipient decrypts the encrypted KEK using its private key using the same parameters as used for encryption.

### KeyServerCapsule

The key server described by the `KeyServerCapsule` structure (see Table 4) issues the following structural winds, the processing of which is described in the corresponding sections:

- `ECCPublicKeyCapsule`, Section 6.3.1.
- `RSAPublicKeyCapsule`, section 6.3.2.

Details of how to use `KeyServerCapsule` are described in section 5.

### SymmetricKeyCapsule

`SymmetricKeyCapsule` (see Table 5) refers to a receiver identified by the key name.

When using this scheme, the sender and receiver are either the same person (a storage cryptography benefit case) or have previously exchanged a symmetrical secret key (a transport cryptography use case) outside the system.

In any case, both the sender and the receiver are in possession of the same secret key identified by the key name. The specification does not restrict how to choose a name.

Table 4. `KeyServerCapsule` elements

| Field           | Content                                                                                         | Encoding                                                         |
| --------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `RecipientKey`  | Data of the receiver key by which the receiver authenticates itself to the key transfer server. | XXX                                                              |
| `KeyServedID`   | Key transfer server identifier.                                                                 | UTF-8 string defined by software trust anchor configuration 5.6. |
| `TransactionID` | Transaction identifier.                                                                         | UTF-8 string defined by the key transfer server.                 |

Table 5. `SymmetricKeyCapsule` elements

| Feild  | Content                                                                               | Encoding       |
| ------ | ------------------------------------------------------------------------------------- | -------------- |
| `Salt` | Sender-generated random number used as input for HKDF-Extract function to derive KEK. | Baidi sequence |

#### Calculation of KEK in the course of encryption

The transmitter has a symmetrical key with a _sym_ called _label_. The transmitter generates a random number from the line. The front sign of this number is to secure a new KEK even if the _sym_ key is reused. Since it is not possible to give a reasonable upper limit to the re-use of the key, we take the value from the line to the length with a strong margin of 256 bits.

KEK is calculated from the symmetrical key and the generated random number as follows:

_KEKpm ← Extract (salt, sym)_

_KEK ← Expand (KEKpm, "CDOC20kek" algId label, Loctets)_

Here _algId_ is the identifier of the crypto algorithm used for FMK encryption as a string, according to the `Recipient.FMKencryptionMethod` field (Section 6.4).

_Loctets_ determines the output length of _Expand_ in bytes and is determined by the symmetrical encryption algorithm used for FMK encryption.

#### Calculation of KEK during decryption

The receiver has a symmetrical key with a _sym_ tagged _label_. From the `SymmetricKeyCapsule` field `Salt` receives a random number generated by the receiver transmitter.

From these data, the KEK must be calculated exactly as described in the encryption.

## FMK encryption and decryption

For FMK encryption, XOR operation is used.

FMK assumes that KEK is the same length as FMK and this can be achieved by using the key query method HKDF.

For FMK encryption, XOR operation is applied bit by bit to the corresponding bits of FMK and KEK.

For decryption, the XOR operation is applied bit by bit to the corresponding bits of the cryptogram and KEK.

## Header Message Authentication Code

The Header Message Authentication Code is calculated using the HMAC [18] algorithm using the SHA-256 hash function.

The key used is HHK (see section 6.2).

The length of the HHK shall be at least the same as the output length of the hash function used, i.e. 256 bits.

_HMACV alueheader ← HMACSHA-256 (HHK, header)_,

where the _header_ is a sequenced header in the form it is written as part of the envelope.

When checking the message authentication code, you must calculate the message authentication code from the parsed header HHK and then the serialized header read from the number-tada container and compare it with the message authentication code read from the container - these two values must be equal.

## Cargo Formation and Encryption

_Attention! This section describes cargo as the encryption of a byte sequence. The formation of a single byte array from the encrypted files is described in section 4.3._

ChaCha20-Poly1305 AEAD encryption scheme [22] is used to encrypt cargo with the following parameters:

- Key length: 256 bits.
- Nonce length: 96 bits.
- Length of authentication mark: 128 bits.

The key is the CEK. Nonce is always generated fresh using a cryptographically strong random number generator (CSPRNG).

Additional information (_additionalData_) is used in the UTF-8 encoding of a predetermined string, a sequenced header, and a message authentication code for the header.

_additionalData ← "CDOC20payload" || header || headerHMAC_

An open text (_payLoad_) encryption function with output length of open text plus length of authentication mark is applied.

_encryptedPayload ← encryptcc20p1305 (CEK, nonce, payLoad, additionalData)_

The decryption function is applied to decrypt the encrypted cargo.

_payload ← decryptcc20p1305 (CEK, nonce, encryptedP ayLoad, additionalData)_

> When processing cargo in flow mode, the open text shall be treated before the decryption function has checked the authenticity of the authentication mark. The requirements for the processing of open text and the handling of errors are set out in section 4.3.2. It is important that all files are deleted in the event of a failure to verify the authenticity of the authentication mark.

Encrypted data is transmitted along with a nonce, how the nonce needs to be delivered to the recipient.

_serializedPayload ← nonce || encryptedPayLoad_

In the context of an envelope, a serialized payload is a response to the cipher and transmitted to the recipient. The details of the nonce, etc. are not shown in the description of the envelope, depending on the encryption method used.

# Realization instructions

## Reference realization

CDOC2 etalonrealisatsioon (reference implementation) is a command-line application implemented in the programming language Java, which is available at https://stash.ria.ee/projects/CDOC2/repos/cdoc20_java/.

The reference realization is written by the authors of the CDOC2 specification and its source code is strongly recommended for other realizers of the specification to read.

The reference realization can also be used for compatibility tests.

## Test vectors

Test vectors are sets of data that allow testing of CDOC2 realizations. Test vectors are included in the reference realization, in the `test/testvectors/` catalogue.

# References

[1] Encrypted DigiDoc Format Specification. AS Certification Centre, https://www.id. ee/wp-content/uploads/2020/06/sk-cdoc-1.0-20120625_en.pdf. June 2012.

[2] Required modifications to CDOC for elliptical curve support. Cybernetica AS, Report number A-101-7, https://www.ria.ee/media/1974/download. September 2017.

[3] Kristjan Krips, Mart Oruaas and Jan Willemson. CDOC2 analysis. Technical report. Cyber-netica, 2020.

[4] Mats Nemec et al. "The Return of Coppersmith's Attack: Practical Factorization of Widely Used RSA Moduli." In: Proceedings of the 2017 ACM SIGSAC Conference on Com- Puter and Communications Security, CCS 2017, Dallas, TX, USA, October 30 - November 03, 2017. That's the thing. Bhavani Thuraisingham et al. ACM, 2017, p. 1631-1648. DOI: 10.1145/ 3133956.3133969. URL: https://doi.org/10.1145/3133956.3133969.

[5] The IEEE and The Open Group. Portable archive interchange. https://pubs.opengroup. org/onlinepubs/9699919799/utilities/pax.html. 2018.

[6] L. Peter Deutsch and Jean-loup Gailly. ZLIB Compressed Data Format Specification version 3.3. RFC 1950. May 1996. URL: https://rfc-editor.org/rfc/rfc1950.txt.

[7] MITRE. CAPEC-126: Path Traversal. https://capec.mitre.org/data/definitions/ 126.html. 2021.

[8] SEI CERT. SEI CERT Oracle Coding Standard for Java. https://wiki.sei.cmu.edu/ confluence/display/java/IDS04-J.+Safely+extract+files+from+ZipInputStream. 2018.

[9] Control character. https://en.wikipedia.org/wiki/Control_character. 2022.

[10] The Linux Foundation. OpenAPI Specification v3.1.0. https://spec.openapis.org/oas/latest.html. 2022.

[11] Algorithms, Key Size and Protocol Report. ECRYPT CSA D5.4. Veebruar 2018. URL: https://www.ecrypt.eu.org/csa/documents/D5.4-FinalAlgKeySizeProt.pdf.

[12] Elaine Barker. Recommendation for Key Management: Part 1 – General. 2020. DOI: 10.6028/NIST.SP.800-57pt1r5.

[13] Cryptographic Mechanisms: Recommendations and Key Lengths. BSI - Technical Gui- deline TR-02102-1. Jaanuar 2022. URL: https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TG02102/BSI-TR-02102-1.pdf.

[14] Krüptoalgoritmid ning nende tugi teekides ja infosüsteemides. Cybernetica AS, Report number T-184-7, https://www.ria.ee/media/1473/download. Märts 2021.

[15] Hugo Krawczyk. Cryptographic Extraction and Key Derivation: The HKDF Scheme. Cryp- tology ePrint Archive, Report 2010/264. https://ia.cr/2010/264. 2010.

[16] Gordon Procter. A Security Analysis of the Composition of ChaCha20 and Poly1305. Cryp- tology ePrint Archive, Report 2014/613. https://ia.cr/2014/613. 2014.

[17] Dr. Hugo Krawczyk ja Pasi Eronen. HMAC-based Extract-and-Expand Key Derivation Func- tion (HKDF). RFC 5869. Mai 2010. URL: https://rfc-editor.org/rfc/rfc5869.txt.

[18] Dr. Hugo Krawczyk, Mihir Bellare ja Ran Canetti. HMAC: Keyed-Hashing for Message Aut- hentication. RFC 2104. Veebruar 1997. URL: https://rfc-editor.org/rfc/rfc2104. txt.

[19] Eric Rescorla. The Transport Layer Security (TLS) Protocol Version 1.3. RFC 8446. August 2018. URL: https://rfc-editor.org/rfc/rfc8446.txt.

[20] Digital Signature Standard (DSS). National Institute of Standards and Technology, https: //nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf. 2013.

[21] K. Moriarty et al. PKCS #1: RSA Cryptography Specifications Version 2.2. RFC 8017. RFC. November 2016.

[22] Yoav Nir ja Adam Langley. ChaCha20 and Poly1305 for IETF Protocols. RFC 8439. Juuni 2018. DOI: 10.17487/RFC8439. URL: https://www.rfc-editor.org/info/rfc8439.

# APPENDIX A header.fbs

```fbs
include "recipients.fbs";
namespace Header;

// Union for communicating the recipient type
union Capsule {
    recipients.ECCPublicKeyCapsule,
    recipients.RSAPublicKeyCapsule,
    recipients.KeyServerCapsule,
    recipients.SymmetricKeyCapsule
}

// FMK encryption method enum.
enum FMKEncryptionMethod:byte {
    UNKNOWN,
    XOR
}

// Payload encryption method enum.
enum PayloadEncryptionMethod:byte {
    UNKNOWN,
    CHACHA20POLY1305
}

// Intermediate record, some languages act very poorly when it comes
// to an array of unions.
// Thus it is better to have an an array of tables that
// contains the union as a field.
table RecipientRecord {
    capsule:                   Capsule;
    key_label:                 string (required)
    fmk_encryption_method:     FMKEncryptionMethod = UNKNOWN
}

// Header structure.
table Header {
    recipients:                [RecipientRecord];
    payload_encryption_method: PayloadEncryptionMethod = UNKNOWN;
}

root_type Header;
```

# APPENDIX B recipients.fbs

```fbs
namespace Recipients;

//for future proofing and data type
union KeyDetailsUnion {
    EccKeyDetails, RsaKeyDetails
}

// Elliptic curve type enum for ECCPublicKey recipient
enum EllipticCurve:byte {
    UNKNOWN,
    secp384r1
}

table RsaKeyDetails {
    //RSA pub key in DER
    recipient_public_key:   [ubyte] (required);
}

table EccKeyDetails {
    // Elliptic curve type enum
    curve:                 EllipticCurve = UNKNOWN;

    //EC pub key in TLS format
    //for secp384r1 curve: 0x04 + X 48 coord bytes + Y coord 48 bytes)
    recipient_public_key:  [ubyte] (required);
}

// ECC public key recipient
table ECCPublicKeyCapsule {
    curve:                 EllipticCurve = UNKNOWN;
    recipient_public_key:  [ubyte] (required);
    sender_public_key:     [ubyte] (required);
}

table RSAPublicKeyCapsule {
    recipient_public_key:  [ubyte] (required);
    encrypted_kek:         [ubyte] (required);
}

table KeyServerCapsule {
    recipient_key_details: KeyDetailsUnion;
    keyserver_id:          string (required);
    transaction_id:        string (required);
}

// symmetric long term crypto
table SymmetricKeyCapsule {
    salt:                 [ubyte] (required);
}
```

# APPENDIX C cdoc2-key-capsules.yaml

```yaml
# Key Capsules API, version 2.0 of cdoc2services API
openapi: 3.0.3
info:
    contact:
        url: http://cyber.ee
    title: cdoc2-key-capsules
    version: '2.0'
    description: API for exchanging CDOC2 ephemeral key material in key capsules
servers:
    - url: 'https://cdoc2-keyserver-01.test.riaint.ee:8443'
    description: RIA test TLS
    - url: 'https://cdoc2-keyserver-01.test.riaint.ee:8444'
    description: RIA test mutualTLS

paths:
    '/key-capsules/{transactionId}':
        get:
            summary: Get key capsule for transactionId
            description: Get key capsule for transactionId
            tags:
                - cdoc2-key-capsules
            parameters:
                - name: transactionId
                in: path
                schema:
                    type: string
                    minLength: 18
                    maxLength: 34
              required: true
              description: transaction id from recipients.KeyServerCapsule.transaction_id (fbs)
            responses:
                '200':
                    description: OK
                    content:
                        application/json:
                            schema:
                                $ref: '#/components/schemas/Capsule'
                '400':
                    description: 'Bad request. Client error.'
                '401':
                    description: 'Unauthorized. Client certificate was not presented with the request.'
                '404':
                    description: 'Not Found. 404 is also returned, when recipient id in record does not match  public key in client certificate.'
            operationId: getCapsuleByTransactionId
            security:
                - mutualTLS: []
    '/key-capsules':
        post:
            summary: Add Key Capsule
            description: Save Capsule and generate transaction id using secure random. Generated transactionId is returned in Location header
            operationId: createCapsule
            responses:
                '201':
                    description: Created
                    headers:
                    Location:
                        schema:
                            type: string
                            example: /key-capsules/KC0123456789ABCDEF
                        description: 'URI of created resource. TransactionId can be extracted from URI as it follows pattern /key-capsules/{transactionId}'
                '400':
                    description: 'Bad request. Client error.'
            requestBody:
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Capsule'
            security: []
            tags:
                - cdoc2-key-capsules
components:
    schemas:
        Capsule:
            title: Capsule
            type: object
            properties:
                recipient_id:
                    type: string
                    format: byte
                    minLength: 97 # EC public key
                    maxLength: 2100 # 16 K RSA public key = 2086 bytes
                    description: 'Binary format is defined by capsule_type'
                ephemeral_key_material:
                    type: string
                    format: byte
                    maxLength: 2100
                    description: 'Binary format is defined by capsule_type'
                capsule_type:
                    type: string
                    enum:
                        - ecc_secp384r1
                        - rsa
                    description: |
                        Depending on capsule type, Capsule fields have the following contents:
                            - ecc_secp384r1:
                                * recipient_id is EC pub key with secp384r1 curve in TLS format (0x04 + X coord 48 bytes + Y coord 48 bytes) (https://www.rfc-editor.org/rfc/rfc8446#section-4.2.8.2)
                                * ephemeral_key_material contains sender public EC key (generated) in TLS format.
                            - rsa:
                                * recipient_id is DER encoded RSA recipient public key - RsaPublicKey encoding [https://www.rfc-editor.org/rfc/rfc8017#page-54](RFC8017 RSA Public Key Syntax A.1.1)
                                * ephemeral_key_material contains KEK encrypted with recipient public RSA key
            required:
                - recipient_id
                - ephemeral_key_material
                - capsule_type

    securitySchemes:
        mutualTLS:
            # since mutualTLS is not supported by OAS 3.0.x, then define it as http basic auth. MutualTLS must be implemented manually anyway
            #type: mutualTLS
            type: http
            scheme: basic
tags:
  - name: cdoc2-key-capsules
```
