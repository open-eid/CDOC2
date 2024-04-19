---
title: 3. CDOC2 encryption schemes
---
<!-- markdownlint-disable no-duplicate-heading -->

# CDOC2 encryption schemes

## Introduction

This section discusses encryption schemes, which are supported by CDOC2 system. The purpose of the section is to familiarize the reader with basic principles of encryption schemes and to specify, how the cryptographic primitives and other functions are used to compose CDOC2 encryption schemes. However, in this section, encryption schemes are presented in abstract form and they are missing some details. For example, iteration count of PBKDF2 function is not defined here and additional arguments for the HKDF functions are not defined in this section. Such implementation details are specified in [Cryptographic protocol details](ch05_cryptographic_details.md).

Encryption schemes are presented in an abstract form, where Sender wants to send a message `M` (payload of the CDOC2 Container) to total of `l` Recipients (`Recipient_1`, `Recipient_2`, ... `Recipient_l`) and Recipients are all similar, in a sense that they all have similar RSA key pairs or that they all have established a password with Sender. In the actual CDOC2 system, Sender may mix different kind of Recipients and different encryption schemes may be concurrently used in the same CDOC2 Container. In that sense, encryption schemes defined in this section are not comparable to use-cases, which describe interaction details of user and CDOC2 system software components. Use-cases are discussed in section [Client Application use cases](../01_use_case_model/ch03_use_cases.md).

## Notation and functions

### Notation

For convenience, we repeat here some of the acronyms and shorthand notation, which is used to define cryptographic schemes:

* `M` - Message (payload of CDOC2 Container)
* `C` - Ciphertext (encrypted message M)
* `FMK` - File Master Key. Cryptographic key material for deriving other encryption and HMAC keys.
* `CEK` - Content Encryption Key. Symmetric key used to encrypt the payload of CDOC2 Container.
* `KEK` - Key Encryption Key. Symmetric key used to encrypt (wrap) the FMK, so that FMK could be transmitted inside CDOC2 Capsule (CKC).
* Index `i` is used to denote an instance of key or data structure, which is specific to certain Recipient, for example, `KEK_i`.

### Standard cryptographic functions

Schemes use following standard functions:

1. `Enc(CEK, M)` means encryption of message `M` with symmetric key `CEK`.
2. `HKDF()`, `HKDF-Extract()`, `HKDF-Expand()` are key derivation functions as defined in RFC5869 (<https://datatracker.ietf.org/doc/html/rfc5869>).
3. `ECSVDP-DH(SecretKey, PublicKey)` is Elliptic Curve Secret Value Derivation Primitive, Diffie-Hellman version, as defined in IEEE standard P1363 and in RFC5349 (<https://datatracker.ietf.org/doc/html/rfc5349>). Note that this is little-bit different from "ECC Cofactor Diffie-Hellman (ECC CDH)" as defined in NIST SP800-56A, section 5.7.1.2.
4. `RSAES-OAEP-ENCRYPT(PK, M)` means encryption of message `M` with RSA public key `PK` according to RFC8017, section 7.1.1 (<https://datatracker.ietf.org/doc/html/rfc8017#section-7.1.1>).
5. `RSAES-OAEP-DECRYPT(SK, C)` means decryption of ciphertext `C` with RSA private key `SK` according to RFC8017, section 7.1.2 (<https://datatracker.ietf.org/doc/html/rfc8017#section-7.1.2>)
6. `PBKDF2(Password, Salt)` is key material derivation function as defined in RFC2898 (<https://www.ietf.org/rfc/rfc2898.txt>).
7. `XOR(Key1, Key2)` is bitwise exclusive-or operation on symmetric keys.

## Generic CDOC2 encryption scheme

In general, CDOC2 system implements encryption of payload of CDOC2 Container with the following generic steps:

1. Sender generates a random FMK, which is used as a master key material for deriving other specific cryptographic keys.
2. From FMK, Sender derives a CEK, which is used for encrypting the payload of CDOC2 Container, and additional HMAC keys, which are used to protect the integrity of CDOC2 Container.
3. FMK is encrypted (wrapped) with a recipient-specific key encryption key (KEK) and added to the CDOC2 Container. It now depends on the capabilities of the Recipient, how this KEK is made available to Recipient, so that they could decrypt the encrypted FMK and in turn, the whole Container. For example, some Recipients may be able to use eID means, which are capable of Diffie-Hellman key exchange, some may be able to use authentication-only eID means and some may only be able to use pre-shared password.
4. Suitable encryption scheme for each Recipient is used and required information to execute key-establishment protocol or key-derivation protocol is put into data structure called "capsule" (Capsule). In some cases, the Capsule is transmitted along the CDOC2 Container itself and in some cases, Capsule Server(s) could be used.

An example activity diagram about creating CDOC2 Container with multiple recipients, is given below:

```plantuml title="Example diagram about creating CDOC2 Container with multiple recipients"
@startuml
start
: Generate random FMK;
: Derive CEK and HMAC keys; 
fork
   : ... ;
fork again
   : ... ;
fork again
   : Create KEK_i and capsule_i
      for recipient i;
   if (Encryption scheme uses \n Capsule Servers?) then (yes)
      : Upload Capsule to server(s);
   else (no)
      : Add Capsule to container;
   endif
fork again
   : ... ;
end fork
: Encrypt the payload of container with CEK;
stop
@enduml
```

<!--- no good place for this text: 

## Capsule

In summary, the `Capsule_i` could be such Capsule, which contains all necessary information locally,

1. `Capsule_i = {Curve, RecipientPublicKey, SenderPublicKey}`
2. `Capsule_i = {RecipientPublicKey, EncryptedKEK}`
3. `Capsule_i = {Salt}`
4. `Capsule_i = {PasswordSalt_i, KeyMaterialSalt_i}`

or such Capsule, which contains information, where to retrieve information to reconstruct the KEK:

1. `Capsule_i = {RecipientKey, KeyServerID, TransactionID}`

--->

## Encryption schemes with key-establishment algorithms

These schemes are usable in case Recipients have eID means with some type of asymmetric key pair (such as RSA or EC), and this key pair could be used do derive the FMK decryption key (KEK) between Sender and Recipient, with some kind of key-establishment protocol. CDOC2 Container will contain the encrypted payload and capsule, which contains necessary information to execute the key-establishment protocol. Container and capsule will be transmitted to Recipient in the same communication channel.

### SC01: Encryption scheme for Recipients with EC key pair

This scheme can be used for transmitting encrypted messages to Recipients holding a EC key pair. Scheme uses Diffie-Hellman key exchange algorithm to generate same secret value for both Sender and Recipient, which is used to protect the FMK of CDOC2 Container.

The key exchange algorithm is almost the same as NIST key-establishment scheme `C(1e, 1s, ECC CDH)` (SP 800-56A Rev3, Section 6.2.2.2 - "(Cofactor) One-Pass Diffie-Hellman, C(1e, 1s, ECC CDH) Scheme"), with the only difference that NIST describes a key-establishment scheme with cofactor ECC CDH primitive, but we are using ECC DH primitive without a cofactor.

#### Encryption steps by Sender

Sender knows the ECC public keys `PK_1`, `PK_2`, ..., `PK_l` of recipients `B_1`, `B_2`, ..., `B_l`. Recipients hold corresponding ECC secret keys `SK_1`, `SK_2`, ..., `SK_l`.

```py linenums="1"
FMK = HKDF-Extract(StaticFMKSalt, CSRNG())
CEK = HKDF-Expand(FMK)
C = Enc(CEK, M)
{EphemeralPK, EphemeralSK} = CSRNG()
KEK_i = HKDF(StaticKEKSalt, ECSVDP-DH(EphemeralSK, PK_i))
Capsule_i = {EllipticCurveInfo, EphemeralPK, PK_i}
EncryptedFMK_i = XOR(FMK, KEK_i)
```

#### Decryption steps by Recipients

Recipient `i` receives the CDOC2 `Container_i` with data `{C, EncryptedFMK_i, Capsule_i}` and has ECDSA public key `PK_i` and corresponding ECDSA secret key `SK_i`.

```py linenums="1"
EncryptedFMK_i = Container_i.EncryptedFMK_i
SenderEphemeralPK = Capsule_i.EphemeralPK
KEK_i = HKDF(StaticKEKSalt, ECSVDP-DH(SK_i, EphemeralPK))
FMK = XOR(KEK_i, EncryptedFMK_i)
CEK = HKDF-Expand(FMK)
M = Dec(CEK, C)
```

## Encryption schemes with asymmetric public key encryption system

### SC02: Encryption scheme for recipients with RSA key pair

This scheme can be used for transmitting encrypted messages to Recipients holding a RSA key pair. Scheme uses RSA-OAEP encryption scheme to protect the FMK decryption key (KEK). Wrapped KEK is included in the capsule, which is transmitted to the Recipient within the CDOC2 Container.

Note that, while it is also possible to use Diffie-Hellman key exchange algorithm with RSA key pair, in order to derive the KEK between Sender and Recipient, a direct RSAES-PKCS1-v1_5 or RSA-OAEP encryption scheme has been traditionally used with CDOC1 applications and therefore, support for this scheme has been carried over to CDOC2 system as well.

#### Encryption steps by Sender

Sender knows the RSA public keys `PK_1`, `PK_2`, ..., `PK_l` of recipients `B_1`, `B_2`, ..., `B_l`. Recipients hold corresponding RSA secret keys `SK_1`, `SK_2`, ..., `SK_l`.

```py linenums="1"
FMK = HKDF-Extract(StaticFMKSalt, CSRNG())
CEK = HKDF-Expand(FMK)
C = Enc(CEK, M)
KEK_i = CSRNG()
EncryptedKEK_i = RSAES-OAEP-ENCRYPT(PK_i, KEK_i)
Capsule_i = {EncryptedKEK_i, PK_i}
EncryptedFMK_i = XOR(FMK, KEK_i)
```

#### Decryption steps by Recipients

Recipient `i` receives the CDOC2 `Container_i` with data `{C, EncryptedFMK_i, Capsule_i}` and has RSA public key `PK_i` and corresponding RSA secret key `SK_i`.

```py linenums="1"
EncryptedFMK_i = Container_i.EncryptedFMK
EncryptedKEK_i = Capsule_i.EncryptedKEK
KEK_i = RSAES-OAEP-DECRYPT(SK_i, EncryptedKEK_i)
FMK = XOR(KEK_i, EncryptedFMK_i)
CEK = HKDF-Expand(FMK)
M = Dec(CEK, C)
```

## Encryption schemes using Capsule Servers

These schemes are usable, in case the Sender wishes to use Capsule Server as a separate transmission channel for sending key capsules to Recipients. CDOC2 Container itself is still transmitted within the usual transmission channel.

### SC03: Encryption scheme with capsule server for recipients with EC key pairs

This scheme uses same kind of key-establishment algorithm, as [scheme SC01](#sc01-encryption-scheme-for-recipients-with-ec-key-pair), but Capsule is transmitted via the Capsule Servers.

#### Encryption steps by Sender

Sender knows the ECC public keys `PK_1`, `PK_2`, ..., `PK_l` of recipients `B_1`, `B_2`, ..., `B_l`. Recipients hold corresponding ECC secret keys `SK_1`, `SK_2`, ..., `SK_l`.

```py linenums="1"
FMK = HKDF-Extract(StaticFMKSalt, CSRNG())
CEK = HKDF-Expand(FMK)
C = Enc(CEK, M)
{EphemeralPK, EphemeralSK} = CSRNG()
KEK_i = HKDF(StaticKEKSalt, ECSVDP-DH(EphemeralSK, PK_i))
KeyServerCapsule_i = {EphemeralPK, PK_i}
ContainerCapsule_i = {KeyServerCapsuleID_i}
EncryptedFMK_i = XOR(FMK, KEK_i)
```

#### Decryption steps by Recipients

Recipient `i` receives the CDOC2 `Container_i` with data `{C, EncryptedFMK_i, ContainerCapsule_i}` and has ECDSA public key `PK_i` and corresponding ECDSA secret key `SK_i`. Recipient reads `KeyServerCapsuleID_i` from `ContainerCapsule_i` and downloads corresponding `KeyServerCapsule_i` from Capsule Server.

Decryption steps are exactly the same:

```py linenums="1"
EncryptedFMK_i = Container_i.EncryptedFMK_i
SenderEphemeralPK = KeyServerCapsule_i.EphemeralPK
KEK_i = HKDF(StaticKEKSalt, ECSVDP-DH(SK_i, EphemeralPK))
FMK = XOR(KEK_i, EncryptedFMK_i)
CEK = HKDF-Expand(FMK)
M = Dec(CEK, C)
```

### SC04: Encryption scheme with Capsule Server for recipients with RSA key pairs

This scheme uses same kind of RSA-OAEP encryption scheme, as [scheme SC02](#sc02-encryption-scheme-for-recipients-with-rsa-key-pair), but Capsule is transmitted via Capsule Server.

#### Encryption steps by Sender

Sender knows the RSA public keys `PK_1`, `PK_2`, ..., `PK_l` of recipients `B_1`, `B_2`, ..., `B_l`. Recipients hold corresponding RSA secret keys `SK_1`, `SK_2`, ..., `SK_l`.

```py linenums="1"
FMK = HKDF-Extract(StaticFMKSalt, CSRNG())
CEK = HKDF-Expand(FMK)
C = Enc(CEK, M)
KEK_i = CSRNG()
EncryptedKEK_i = RSAES-OAEP-ENCRYPT(PK_i, KEK_i)
KeyServerCapsule_i = {{EncryptedKEK_i, PK_i}
ContainerCapsule_i = {KeyServerCapsuleID_i, PK_i}
EncryptedFMK_i = XOR(FMK, KEK_i)
```

#### Decryption steps by Recipients

Recipient `i` receives the CDOC2 `Container_i` with data `{C, EncryptedFMK_i, ContainerCapsule_i}` and has RSA public key `PK_i` and corresponding RSA secret key `SK_i`. Recipient reads `KeyServerCapsuleID_i` from `ContainerCapsule_i` and downloads corresponding `KeyServerCapsule_i` from Capsule server. Recipient authenticates to Capsule Server with RSA key pair `(SK_i, PK_i)`.

Decryption steps are exactly the same:

```py linenums="1"
EncryptedFMK_i = Container_i.EncryptedFMK
EncryptedKEK_i = KeyServerCapsule_i.EncryptedKEK
KEK_i = RSAES-OAEP-DECRYPT(SK_i, EncryptedKEK_i)
FMK = XOR(KEK_i, EncryptedFMK_i)
CEK = HKDF-Expand(FMK)
M = Dec(CEK, C)
```

## Encryption schemes with pre-shared secrets

Previous schemes SC01, SC02, SC03, and SC04 all use some form of pair-wise key-establishment protocols and they are relying on the fact that recipients have access to RSA or EC key pairs, usually in the form of eID means. In addition to these schemes, CDOC2 system have to support situations, where Recipients don't have any such tokens, or when the storage requirements of CDOC2 Container exceed usable lifetime of such tokens. In these cases, it is possible to use pre-shared symmetric encryption key or pre-shared password.

### SC05: Encryption scheme for recipients with pre-shared symmetric secret

This scheme is used, when Sender wishes to use an externally generated symmetric encryption key for:

* long-term storage of CDOC2 Container, so that decryption of it doesn't depend on availability of hardware tokens or validity of PKI certificates, and/or
* transmitting CDOC2 Container to such Receivers, who doesn't have any eID means, but who have previously received the symmetric encryption key.

Encryption scheme can be used with multiple Recipients, who each may know different encryption key. This encryption scheme is very similar to [scheme SC06](ch02_encryption_schemes.md#sc06-direct-encryption-scheme-with-pre-shared-passwords), which uses pre-shared password or passphrase.

#### Encryption steps by Sender

Sender knows symmetric keys `S_1`, `S_2`, ..., `S_l` for each Recipient `B_1`, `B_2`, ..., `B_l`.

```py linenums="1"
FMK = HKDF-Extract(StaticFMKSalt, CSRNG())
CEK = HKDF-Expand(FMK)
C = Enc(CEK, M)
KeyMaterialSalt_i = CSRNG()
KEK_i = HKDF(KeyMaterialSalt_i, S_i)
EncryptedKEK_i = Enc(S_i, KEK_i)
Capsule_i = {EncryptedKEK_i, KeyMaterialSalt_i}
EncryptedFMK_i = XOR(FMK, KEK_i)
```

#### Decryption steps for Recipients or Sender

Recipient `i` receives the CDOC2 `Container_i` with data `{C, EncryptedFMK_i, Capsule_i}` and knows symmetric key `S_i`. Also, Sender may assume the role of any Recipient `i`.

```py linenums="1"
EncryptedKEK_i = Capsule_i.EncryptedKEK
KeyMaterialSalt_i = Capsule_i.KeyMaterialSalt
EncryptedFMK_i = Container_i.EncryptedFMK
KEK_i = HKDF(KeyMaterialSalt_i, S_i)
FMK = XOR(KEK_i, EncryptedFMK_i)
CEK = HKDF-Expand(FMK)
M = Dec(CEK, C)
```

### SC06: Direct encryption scheme with pre-shared passwords

This scheme is used, when Sender wishes to use a password-based encryption for:

* long-term storage of CDOC2 Container, so that decryption of it doesn't depend on availability of hardware tokens or validity of PKI certificates, and/or
* transmitting CDOC2 Container to such Receivers, who doesn't have any eID means.

Password-based encryption scheme can be used with multiple Recipients, who each may know a different password for decryption. This encryption scheme is very similar to [scheme SC05](#sc05-encryption-scheme-for-recipients-with-pre-shared-symmetric-secret), which uses pre-shared encryption key(s).

#### Encryption steps by Sender

Sender knows passwords `Password_1`, `Password_2`, ..., `Password_l` for each Recipient `B_1`, `B_2`, ..., `B_l` and follows steps for encryption:

```py linenums="1"
FMK = HKDF-Extract(StaticFMKSalt, CSRNG())
CEK = HKDF-Expand(FMK)
C = Enc(CEK, M)
PasswordSalt_i = CSRNG()
PasswordKeyMaterial_i = PBKDF2(Password_i, PasswordSalt_i)
KeyMaterialSalt_i = CSRNG()
KEK_i = HKDF(KeyMaterialSalt_i, PasswordKeyMaterial_i)
Capsule_i = {KeyMaterialSalt_i, PasswordSalt_i}
EncryptedFMK_i = XOR(FMK, KEK_i)
```

Sender creates a CDOC Container for each Recipient with `{C, EncryptedFMK_i, Capsule_i}`, including other technical details, and sends the Container to Recipient or places in long-term storage for themself.

#### Decryption steps for Recipient or Sender

After some time, Sender may wish to decrypt the Container themself (assuming the role of any Recipient `i`) or the Recipient `i` wishes to decrypt the Container.

Recipient `i` receives CDOC2 `Container_i` with data `{C, EncryptedFMK, Capsule}` and has password `Password_i` and follows steps for decryption:

```py linenums="1"
PasswordSalt_i = Capsule_i.PasswordSalt
PasswordKeyMaterial_i = PBKDF2(Password_i, PasswordSalt_i)
KeyMaterialSalt_i = Capsule_i.KeyMaterialSalt
EncryptedFMK_i = Container_i.EncryptedFMK
KEK_i = HKDF(KeyMaterialSalt_i, PasswordKeyMaterial_i)
FMK = XOR(KEK_i, EncryptedFMK_i)
CEK = HKDF-Expand(FMK)
M = Dec(CEK, C)
```

## Encryption schemes with secret sharing

### SC07: Encryption scheme with (n-of-n) secret shared decryption key

This scheme is used, when Sender wishes to use multiple CKCTS servers do distribute the key material necessary to decrypt CDOC2 Container among the servers and this way to reduce the need to trust a single CKCTS server. Scheme uses simple n-of-n solution, where recipient needs to download all `n` shares in order to reconstruct the key material.

#### Encryption steps by Sender

Following steps outline how to create CDOC Container with a Recipient header structure and a Capsule for Recipient `i`. Index `i` is for enumerating over Recipients from `(1, 2, 3, ..., l)`. Index `j` is for enumerating over shares from `(1, 2, 3, ..., n)` of `KEK_i`.

```py linenums="1"
FMK = HKDF_Extract(Static_FMK_Salt, CSRNG())
CEK = HKDF_Expand(FMK)
C = Enc(CEK, M)

for i in (1, 2, ... l): 
   KeyMaterialSalt_i = CSRNG()
   KEK_i = HKDF_Expand(HKDF_Extract(KeyMaterialSalt_i, CSRNG()))
   for j in (2, 3, ..., n):
      KEK_i_share_j = CSRNG() 
   KEK_i_share_1 = XOR(KEK_i, KEK_i_share_2, KEK_i_share_3,..., KEK_i_share_n)
   # Client uploads all shares of KEK_i to CKCTS servers and 
   # gets corresponding Capsule_i_Share_j_ID for each KEK_i_share_j
   RecipientInfo_i = "etsi/PNOEE-48010010101"
   DistributedKEKInfo_i = {CKCTS_ID, Capsule_i_Share_j_ID}
   Capsule_i = {RecipientInfo_i, DistributedKEKInfo_i}
   EncryptedFMK_i = XOR(FMK, KEK_i)

Container = {C, EncryptedFMK_i [1..l], Capsule_i [1..l]}
```

Sender has created a CDOC Container containing `{C, EncryptedFMK_i [1..l], Capsule_i [1..l]}` for transmitting to Recipients `(1..l)`.

#### Decryption steps by Recipient

Recipient `i` receives a CDOC Container containing `{C, EncryptedFMK_i [1..l], Capsule_i [1..l]}`, where `Capsule_i = {RecipientInfo_i, DistributedKEKInfo_i}` and `DistributedKEKInfo_i = {CKCTS_ID, Capsule_i_Share_j_ID} [1..n]`.

Authentication signature data format and authentication token details are specified in section [Capsule Server](ch_04_capsule_server.md).

```py linenums="1"
# Recipient sends `Capsule_i_Share_j_ID` to corresponding CKCTS servers
# and receives `nonce_i_j` from each server
auth_data = {Capsule_i_Share_j_ID, SHA256(nonce_i_j)}
auth_hash = SHA256(auth_data)
# Recipient performs ID-card/Mobile-ID/Smart-ID authentication
# and creates a signature `auth_signature` on `auth_hash` 
# with authentication key pair.
auth_signature = sign(auth_hash) 
for j in [1, 2, 3, ... n]: 
   auth_token_j = auth_data_for_server_j + auth_signature
KEK_i = XOR(KEK_i_share_1, KEK_i_share_2, KEK_i_share_3,..., KEK_i_share_n)
FMK = XOR(KEK_i, EncryptedFMK_i)
CEK = HKDF_Expand(FMK)
M = Dec(CEK, C)
```
<!---
Commented out until we start working on this 

### SC08: (WIP) Encryption scheme with t-of-n secret shared decryption key

This scheme is used, when Sender wishes to use multiple CKCTS servers do distribute the key material necessary to decrypt CDOC2 Container among the servers and to reduce the need to trust a single CKCTS server. Scheme uses Shamir's Secret Sharing scheme, where recipient needs to download only `t` shares from a total of `n` shares, in order to reconstruct the key material.

This scheme is not fully specified. We don't have functions `SplitSecrets()` and `CombineSecrets()` yet.

#### Encryption steps by Sender

Following steps outline how to create CDOC Container with a Recipient header structure and a Capsule for Recipient `i`. Index `i` is for enumerating over Recipients from `(1, 2, 3, ..., l)`. Index `j` is for enumerating over shares from `(1, 2, 3, ..., n)` of `KEK_i`.

```py linenums="1"
FMK = HKDF_Extract(Static_FMK_Salt, CSRNG())
CEK = HKDF_Expand(FMK)
C = Enc(CEK, M)

for i in (1, 2, ... l): 
   KeyMaterialSalt_i = CSRNG()
   KEK_i = HKDF_Expand(HKDF_Extract(KeyMaterialSalt_i, CSRNG()))
   # TODO: undefined SplitSecrets()
   {KEK_i_share_1, KEK_i_share_2, ..., KEK_i_share_n} = SplitSecrets(KEK_i, n, t)
   # Client uploads all shares of KEK_i to CKCTS servers and 
   # gets corresponding Capsule_i_Share_j_ID for each KEK_i_share_j
   RecipientInfo_i = "etsi/PNOEE-48010010101"
   DistributedKEKInfo_i = {CKCTS_ID, Capsule_i_Share_j_ID}
   Capsule_i = {RecipientInfo_i, DistributedKEKInfo_i}
   EncryptedFMK_i = XOR(FMK, KEK_i)

Container = {C, EncryptedFMK_i [1..l], Capsule_i [1..l]}
```

Sender has created a CDOC Container containing `{C, EncryptedFMK_i [1..l], Capsule_i [1..l]}` for transmitting to Recipients `(1..l)`.

#### Decryption steps by Recipient

Recipient `i` receives a CDOC Container containing `{C, EncryptedFMK_i [1..l], Capsule_i [1..l]}`, where `Capsule_i = {RecipientInfo_i, DistributedKEKInfo_i}` and `DistributedKEKInfo_i = {CKCTS_ID, Capsule_i_Share_j_ID} [1..n]`.

Authentication signature data format and authentication token details are specified in section [Capsule Server](ch_04_capsule_server.md).

```py linenums="1"
# Recipient i sends `Capsule_i_Share_j_ID` to corresponding CKCTS servers
# and receives `nonce_i_j` from each server
auth_data = {Capsule_i_Share_j_ID, SHA256(nonce_i_j)}
auth_hash = SHA256(auth_data)
# Recipient performs ID-card/Mobile-ID/Smart-ID authentication
# and creates a signature `auth_signature` on `auth_hash` 
# with authentication key pair.
auth_signature = sign(auth_hash) 
for j in [1, 2, 3, ... n]: 
   auth_token_j = auth_data_for_server_j + auth_signature
# Recipient downloads at least t shares KEK_i_share_j from CKCTS servers
# TODO: undefined CombineSecrets()
KEK_i = CombineSecrets(KEK_i_share_1, ..., KEK_i_share_t)
FMK = XOR(KEK_i, EncryptedFMK_i)
CEK = HKDF_Expand(FMK)
M = Dec(CEK, C)
```
-->
