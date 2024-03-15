---
title: 3. CDOC2 encryption schemes
---

# CDOC2 encryption schemes

This section discusses encryption schemes, which are supported by CDOC2 system. The purpose of the section is to familiarize the reader with basic principles of various encryption schemes and to specify, how the cryptographic primitives and other functions are used to compose CDOC2 encryption schemes. However, in this section, encryption schemes are presented in abstract form and they are missing some details. For example, iteration count of PBKDF2 function is not defined here and additional arguments for the HKDF functions are not defined in this section. Such implementation details are specified in [Cryptographic protocol details](ch05_cryptographic_details.md).

Encryption schemes are presented in an abstract form, where Sender wants to send a message `M` (payload of the CDOC2 Container) to total of `l` Recipients (`Recipient_1`, `Recipient_2`, ... `Recipient_l`) and Recipients are all similar, in a sense that they all have similar RSA key pairs or that they all have established a password with Sender. In the actual CDOC2 system, Sender may mix and match different kind of Recipients and various encryption schemes may be concurrently used. In that sense, encryption schemes defined in this section are not use-cases, which are discussed in section [CDOC 2.0 Client Application use cases](ch03_use_cases.md).

## Generic CDOC2 encryption scheme principles

In general, CDOC2 system implements the encryption of the payload of CDOC2 Container payload with the following principles:

1. Sender generates a random FMK, which is used as a key material for deriving other necessary keys.
2. Sender derives CEK, which is used for encrypting the payload of CDOC2 Container. Somehow, Recipient must have
3. Depending on the type of Recipient, CDOC2 Client uses some kind of encryption scheme to securely transmit 
3. Alice generates a separate master key for each recipient, using a recipient-specific key encryption key (*KEK*).
The scenarios described in the following sections differ by the methods used for generating the *KEK* and transmitting the key capsules containing the encrypted master key *FMK* to the recipients.

## Supported schemes

1. SC01 - Encryption scheme for recipients with EC key pair
2. SC02 - Encryption scheme for recipients with RSA key pair
3. SC03 - Encryption scheme with key transmission server for recipients with EC key pairs
4. SC04 - Encryption scheme with key transmission server for recipients with RSA key pairs
5. SC05 - Encryption scheme for recipients with pre-shared symmetric secret
6. SC06 - Encryption scheme for recipients with pre-shared passwords
7. SC07 - Encryption scheme with (n-of-n) secret shared decryption key
8. SC08 - Encryption scheme with (t-of-n) secret shared decryption key

## Notation

This chapter uses some shorthand notation to define cryptographic schemes:

* `M` - Message (payload of CDOC2 Container)
* `C` - Ciphertext (encrypted message M)
* `CEK` - Content Encryption Key. Symmetric key used to encrypt the payload of CDOC2 Container.
* `KEK` - Key Encryption Key. Symmetric key used to encrypt (wrap) the CEK, so that CEK could be transmitted inside CKC.
* `FMK` - File Master Key. Cryptographic key material for deriving the CEK.

## Direct key agreement-based ECDH

This method can be used for transmitting encrypted messages to recipients holding the relevant ECC private key.
Alice protects message secrecy using a key encapsulation mechanism (*KEM*) consisting of the algorithms ``EncapsKEM`` and ``DecapsKEM``.
Prior to the encapsulation, Alice receives the recipient’s public key in the form of a an elliptic curve point. Alice and the recipient then run the ECDH key establishment protocol.

The encapsulation function ``EncapsKEM`` takes a key capsule and the recipient’s public key as inputs and returns a key and a capsule. The key is the key encryption key (KEK), derived as per section [ECCPublicKeyCapsule](ch05_cryptographic_details.md#eccpublickeycapsule); in the ECDH implementation, the capsule *caps* is Alice’s ephemeral public key.

The decapsulation function ``DecapsKEM`` takes a key capsule and the recipient’s secret key as inputs, verifies that the transmitted elliptic curve point is valid, runs the counterparty activities of the ECDH key establishment protocol, and derives the KEK. For more details, see subsection [KEK computation during encryption](ch05_cryptographic_details.md#kek-computation-during-encryption).

Direct key agreement-based ECDH:

1. *A : fmk ← GenKeyExtractSym(Nonss)*
2. *A : cek ← GenKeyExpandSym(fmk)*
3. *A : c ← EncSym(cek, M)*
4. *A* receives the public keys *PK1, PK2, . . . , PKℓ* of recipients *B1, B2, . . . , Bℓ*; recipients hold corresponding secret keys *SK1, SK2, . . . , SKℓ*
5. *A : (keki, capsi) ← EncapsKEM(PKi) (i = 1, 2, . . . , ℓ)*
6. *A : cki ← XOR(keki, fmk) (i = 1, 2, . . . , ℓ)*
7. *A → Bi : c, cki, capsi (i = 1, 2, . . . , ℓ)*
8. *Bi : keki ← DecapsKEM(capsi, SKi)*
9. *Bi : fmk ← XOR(keki, cki)*
10. *Bi : cek ← GenKeyExpandSym(fmk)*
11. *Bi : M ← DecSym(cek, c)*

## Key server-based ECDH

In this method, Alice also protects message secrecy using ECDH key encapsulation, except in this case the capsule is transmitted via a key server, thus providing an additional layer of security, assuming that the key server is operating properly. Additional security is ensured by the use of an authentication protocol *Auth* enabling the server to authenticate the recipient.

Key-server based ECDH:

1. *A : fmk ← GenKeyExtractSym(Nonss)*
2. *A : cek ← GenKeyExpandSym(fmk)*
3. *A : c ← EncSym(cek, M)*
4. *A* receives the public keys *PK1, PK2, . . . , PKℓ* of recipients *B1, B2, . . . , Bℓ*; recipients hold corresponding secret keys *SK1, SK2, . . . , SKℓ*
5. *A : (keki, capsi) ← EncapsKEM(PKi) (i = 1, 2, . . . , ℓ)*
6. *A : cki ← XOR(keki, fmk) (i = 1, 2, . . . , ℓ)*
7. *A → Bi : c, cki (i = 1, 2, . . . , ℓ)*
8. *A → S : capsi (i = 1, 2, . . . , ℓ)*
9. *Bi → S : Auth3*
10. *S → Bi : capsi*
11. *Bi : keki ← DecapsKEM(capsi, SKi)*
12. *Bi : fmk ← XOR(keki, cki)*
13. *Bi : cek ← GenKeyExpandSym(fmk)*
14. *Bi : M ← DecSym(cek, c)*

## Direct key agreement-based RSA-OAEP

This method can be used for transmitting encrypted messages to recipients holding an RSA private key.
Alice wishes to protect message secrecy using an RSA-OAEP scheme comprising the encryption algorithm ``EncrRSA`` and the decryption algorithm ``DecRSA``.
To ensure the secrecy of the key encryption key, the sender encrypts the KEK using the recipient’s public key. The key capsule comprises the resulting cryptogram that the recipient can decrypt using their private key.

1. *A : fmk ← GenKeyExtractSym(Nonss)*
2. *A : cek ← GenKeyExpandSym(fmk)*
3. *A : c ← EncSym(cek, M)*
4. *A : keki ← GenKeySym (i = 1, 2, . . . , ℓ)*
5. *A : cki ← XOR(keki, fmk) (i = 1, 2, . . . , ℓ)*
6. *A* receives the public keys *PK1, PK2, . . . , PKℓ* of recipients *B1, B2, . . . , Bℓ*; recipients hold corresponding secret keys *SK1, SK2, . . . , SKℓ*
7. *A : capsi ← EncRSA(PKi, keki) (i = 1, 2, . . . , ℓ)*
8. *A → Bi : c, cki, capsi (i = 1, 2, . . . , ℓ)*
9. *Bi : keki ← DecRSA(SKi, capsi)*
10. *Bi : fmk ← XOR(keki, cki)*
11. *Bi : cek ← GenKeyExpandSym(fmk)*
12. *Bi : M ← DecSym(cek, c)*

## Key server-based RSA-OAEP

Identical to the previous method, except the sender transmits the key capsule to the recipient via a key server.

1. *A : fmk ← GenKeyExtractSym(Nonss)*
2. *A : cek ← GenKeyExpandSym(fmk)*
3. *A : c ← EncSym(cek, M)*
4. *A : keki ← GenKeySym (i = 1, 2, . . . , ℓ)*
5. *A : cki ← XOR(keki, fmk) (i = 1, 2, . . . , ℓ)*
6. *A → Bi : c, cki (i = 1, 2, . . . , ℓ)*
7. *A* receives the public keys *PK1, PK2, . . . , PKℓ* of recipients *B1, B2, . . . , Bℓ*; recipients hold corresponding secret keys *SK1, SK2, . . . , SKℓ*
8. *A : capsi ← EncRSA(PKi, keki) (i = 1, 2, . . . , ℓ)*
9. *A → S : capsi (i = 1, 2, . . . , ℓ)*
10. *Bi → S : Auth*
11. *S → Bi : capsi*
12. *Bi : keki ← DecRSA(SKi, capsi)*
13. *Bi : fmk ← XOR(keki, cki)*
14. *Bi : cek ← GenKeyExpandSym(fmk)*
15. *Bi : M ← DecSym(cek, c)*

## Symmetric key-based method

For the protection of message secrecy, Alice uses a key derivation mechanism comprising the algorithms ``EncapsHKDF`` and ``DecapsHKDF`` . Prior to encapsulation, Alice knows the recipient’s symmetric secret key and the label of this key (agreed by the sender and recipient; the label helps identify different keys). The encapsulation function ``EncapsHKDF`` takes the recipient’s symmetric secret key and its label as inputs and returns a key and a capsule. The key is the key encryption key KEK, derived as per section [SymmetricKeyCapsule](ch05_cryptographic_details.md#symmetrickeycapsule), and the capsule *caps* is a data structure containing a decryption key label and the random number used for the derivation of the key. The decapsulation function ``DecapsHKDF`` takes the recipient’s symmetric public key, its label, and a key capsule as inputs. In case the inputs are valid, the function derives the KEK. For more details, see subsection [KEK computation during decryption](ch05_cryptographic_details.md#kek-computation-during-decryption).

Symmetric key-based method:

1. *A : fmk ← GenKeyExtractSym(Nonss)*
2. *A : cek ← GenKeyExpandSym(fmk)*
3. *A : c ← EncSym(cek, M)*
4. *A* holds the symmetric keys *S1, S2, . . . , Sℓ* labelled *L1, L2, . . . , Lℓ*
5. *A : (keki, capsi) ← EncapsHKDF (Si, Li) (i = 1, 2, . . . , ℓ)*
6. *A : cki ← XOR(keki, fmk) (i = 1, 2, . . . , ℓ)*
7. *A → Bi : c, cki, capsi (i = 1, 2, . . . , ℓ)*
8. *Bi : keki ← DecapsHKDF (capsi, Si)*
9. *Bi : fmk ← XOR(keki, cki)*
10. *Bi : cek ← GenKeyExpandSym(fmk)*
11. *Bi : M ← DecSym(cek, c)*

## Encryption schemes with key-establishment algorithms

These schemes are usable in case Recipients have some type of asymmetric key pair (RSA or EC) and these could be used do derive FMK decryption key (KEK) Sender and Recipients, with some kind of key establishment protocol. CDOC2 container will contain the encrypted payload and key capsule, which contains necessary information to execute the key establishment protocol. Container and capsule will be transmitted to Recipient in single communication channel.

### SC01: Encryption scheme for Recipients with EC key pair

This scheme can be used for transmitting encrypted messages to Recipients holding a EC key pair. Scheme uses Diffie-Hellman key exchange algorithm to generate same secret value for both Sender and Recipient, which us used to protect the FMK of CDOC2 Container.

The key exchange algorithm is almost the same as NIST key-establishment scheme `C(1e, 1s, ECC CDH)` (SP 800-56A Rev3, Section 6.2.2.2 - "(Cofactor) One-Pass Diffie-Hellman, C(1e, 1s, ECC CDH) Scheme"), with the only difference that NIST describes a key establishment scheme with cofactor ECC CDH primitive, but we are using ECC DH primitive without a cofactor.

Scheme uses following standard functions:

1. `HKDF()`, `HKDF-Extract`, `HKDF-Expand()` as defined in RFC5869 (<https://datatracker.ietf.org/doc/html/rfc5869>).
2. `Enc(CEK, M)` mean encryption of message `M` with symmetric key `CEK`.
3. `ECSVDP-DH(SecretKey, PublicKey)` is Elliptic Curve Secret Value Derivation Primitive, Diffie-Hellman version, as defined in IEEE standard P1363 and in RFC5349 (<https://datatracker.ietf.org/doc/html/rfc5349)>). Note that this is different from "ECC Cofactor Diffie-Hellman (ECC CDH)" as defined in NIST SP800-56A section 5.7.1.2.

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

Recipient `i` receives the CDOC2 `Container_i` with data `{C, EncryptedFMK, Capsule}` and has ECDSA public key `PK_i` and corresponding ECDSA secret key `SK_i`.

```py linenums="1"
EncryptedFMK_i = Container_i.EncryptedFMK
SenderEphemeralPK = Capsule.EphemeralPK
KEK_i = HKDF(StaticKEKSalt, ECSVDP-DH(SK_i, EphemeralPK))
FMK = XOR(KEK_i, EncryptedFMK_i)
CEK = HKDF-Expand(FMK)
M = Dec(CEK, C)
```

### SC02: Encryption scheme for recipients with RSA key pair

This scheme can be used for transmitting encrypted messages to Recipients holding a RSA key pair. Scheme uses RSA-OAEP encryption scheme to protect the FMK decryption key (KEK), which is transmitted to the Recipient within the CDOC2 container.

Scheme uses following standard functions:

1. `HKDF()`, `HKDF-Extract`, `HKDF-Expand()` as defined in RFC5869 (<https://datatracker.ietf.org/doc/html/rfc5869>).
2. `Enc(CEK, M)` means encryption of message `M` with symmetric key `CEK`.
3. `Dec(CEK, C)` means decryption of ciphertext `C` with summetric key `CEK`.
3. `RSAES-OAEP-ENCRYPT(PK, M)` means encryption of message `M` with RSA public key `PK` according to RFC8017 Section 7.1.1 (<https://datatracker.ietf.org/doc/html/rfc8017#section-7.1.1>).
4. `RSAES-OAEP-DECRYPT(SK, C)` means decryption of ciphertext `C` with RSA private key `SK` according to RFC8017 Section 7.1.2 (<https://datatracker.ietf.org/doc/html/rfc8017#section-7.1.2>)

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

## Schemes using key transmission servers

These schemes are usable, in case the Sender wishes to use capsule transmission server as separate transmission channel for sending key capsules to Recipients. CDOC2 Container itself is still transmitted in the usual transmission channel.

### SC03: Encryption scheme with capsule transmission server for recipients with EC key pairs

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3.2 "Võtmeedastusserveriga ECDH skeem"

### SC04: Encryption scheme with capsule transmission server for recipients with RSA key pairs

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3.4 "Võtmeedastusserveriga RSA-OAEP skeem"

## Schemes without asymmetric key pairs

Previous schemes SC01, SC02, SC03, and SC04 all use some form of pair-wise key-establishment protocols and they are relying on the fact that recipients have access to RSA or EC key pairs, in the form of eID tokens. In addition to such schemes, CDOC2 system have to support situations, where Recipients don't have such tokens.

### SC05: Encryption scheme for recipients with pre-shared symmetric secret

This scheme is used, when Sender wishes to use a externally generated symmetric encryption key for:

* long-term storage of CDOC2 Container, so that decryption of it doesn't depend on availability of hardware tokens or validity of PKI certificates, or
* transmitting CDOC2 Container to such Receivers, who doesn't have any eID means, but who have previously received the symmetric encryption key.

Encryption scheme can be used for multiple Recipients, who each may know different encryption key. This encryption scheme is very similar to scheme SC06, which uses pre-shared password or passphrase.

Scheme uses following standard functions:

1. `HKDF()`, `HKDF-Extract`, `HKDF-Expand()` as defined in RFC5869 (<https://datatracker.ietf.org/doc/html/rfc5869>).
2. `Enc(CEK, M)` means encryption of message `M` with symmetric key `CEK`.
3. `Dec(CEK, C)` means decryption of ciphertext `C` with symmetric key `CEK`.

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

* long-term storage of CDOC2 Container, so that decryption of it doesn't depend on availability of hardware tokens or validity of PKI certificates, or
* transmitting CDOC2 Container to such Receivers, who doesn't have any eID means.

Password-based encryption scheme can be used for multiple Recipients, who each may know a different password for decryption. This encryption scheme is very similar to scheme SC05, which uses pre-shared encryption key(s).

Scheme uses following standard functions:

1. `HKDF()`, `HKDF-Extract`, `HKDF-Expand()` as defined in RFC5869 (<https://datatracker.ietf.org/doc/html/rfc5869>).
2. `PBKDF2(Password, Salt)` as defined in RFC2898 (<https://www.ietf.org/rfc/rfc2898.txt>).
2. `Enc(CEK, M)` means encryption of message `M` with symmetric key `CEK`.
3. `Dec(CEK, C)` means decryption of ciphertext `C` with symmetric key `CEK`.

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

### SC07: Encryption scheme with (n-of-n) secret shared decryption key

This scheme is used, when Sender wishes to use multiple CKCTS servers do distribute the key material necessary to decrypt CDOC2 Container among the servers and this way to reduce the need to trust a single CKCTS server. Scheme uses simple N-of-N solution, where recipient needs to download all `n` shares in order to reconstruct the key material.

#### Encryption steps by Sender

We will create $n$ shares. $k$ shares are needed to reconstruct the KEK.

Index $i$ is for enumerating over Recipients $(1..l)$
Index $j$ is for enumerating over shares $(1..n)$ of `KEK_i`

1. `FMK = HKDF_Extract(Static_FMK_Salt, CSRNG())`
2. `CEK = HKDF_Expand(FMK)`
3. `C = Enc(CEK, M)`
4. `KeyMaterialSalt_i = CSRNG()`
5. `KEK_i = HKDF_Expand(HKDF_Extract(KeyMaterialSalt_i, CSRNG())`
6. `{KEK_i_share_1, KEK_i_share_2, KEK_i_share_3, ..., KEK_i_share_n} = SSS_divide(KEK_i, n)`
7. Client uploads all shares to available CKCTS servers and gets corresponding `transactionID` values for each `KEK_i_share_j`
8. `RecipientInfo_i = "etsi/PNOEE-48010010101"`
9. `DistributedKEKInfo_i = {CKCTS_ID, transactionID} [1..n]`
10. `Capsule_i = {RecipientInfo_i, DistributedKEKInfo_i}`
11. `EncryptedFMK_i = XOR(FMK, KEK_i)`

Sender gets a CDOC Container containing `{C, EncryptedFMK_i [1..l], Capsule_i [1..l]}`.

TODO: `{KEK_i_share_1, KEK_i_share_2, KEK_i_share_3, ..., KEK_i_share_n} = SSS_divide(KEK_i, n)` is undefined. We could use Jan's help here.

#### Draft for reconstructing from shares

Recipient receives a CDOC Container containing `{C, EncryptedFMK_i [1..l], Capsule_i [1..l]}`, where `Capsule_i = {RecipientInfo_i, DistributedKEKInfo_i}` and `DistributedKEKInfo_i = {CKCTS_ID, transactionID} [1..n]`.

1. Recipient contacts CKCTS servers, sends `transactionID_i_j` and receives `nonce_i_j` (`j = 1..n`)
2. Recipient creates authentication data `auth_data = {transactionID_i_j, SHA256(nonce_i_j)} [1..n]`
3. Recipient computes `auth_hash = SHA256(auth_data)`
4. Recipient performs ID-card/Mobile-ID/Smart-ID authentication and creates a signature `auth_signature` on `auth_hash` with authentication key pair.
5. Recipient creates authentication ticket for each CKCTS server `auth_ticket_j = ... + auth_signature`
   1. TODO: `auth_ticket_j` structure is too complex to show here, need to create another section
6. Recipient downloads `share_i_j` from CKCTS server `j` with `auth_ticket_j`
7. `KEK_i = SSS_reconstruct(share_i_j) (j = 1..n)`
8. `FMK = XOR(KEK_i, CK_i)`
9. `CEK = GenKeyExpand(FMK)`
10. `M = Dec(CEK, C)`

TODO: `KEK_i = SSS_reconstruct(share_i_j) (j = 1..n)` is undefined. We could use Jan's help here.

### SC08: Encryption scheme with t-of-n secret shared decryption key

This scheme is used, when Sender wishes to use multiple CKCTS servers do distribute the key material necessary to decrypt CDOC2 Container among the servers and this way to reduce the need to trust a single CKCTS server. Scheme uses Shamir Secret Sharing scheme,where recipient needs to download only `t` shares from a total of `n` shares, in order to reconstruct the key material.

#### Creating CDOC2 Container

Index $i$ is for enumerating over Recipients $(1..l)$
Index $j$ is for enumerating over shares $(1..n)$ of `KEK_i`

```py linenums="1"
FMK = HKDF-Extract(StaticFMKSalt, CSRNG())
CEK = HKDF-Expand(FMK)
C = Enc(CEK, M)
KeyMaterialSalt_i = CSRNG()
KEK_i = HKDF(KeyMaterialSalt_i, CSRNG()
{KEK_i_share_1, KEK_i_share_2, KEK_i_share_3, ..., KEK_i_share_n} = XOR_divide(KEK_i, n)
# Client uploads all shares to available CKCTS servers and gets corresponding `transactionID` values for each `KEK_i_share_j`
RecipientInfo_i = "etsi/PNOEE-48010010101"
DistributedKEKInfo_i = {CKCTS_ID, transactionID} [1..n]
Capsule_i = {RecipientInfo_i, DistributedKEKInfo_i}
EncryptedFMK_i = XOR(FMK, KEK_i)
```

Sender gets a CDOC2 containers `Container_i [1..l]` containing `{C, EncryptedFMK_i, Capsule_i}`.

TODO: `{KEK_i_share_1, KEK_i_share_2, KEK_i_share_3, ..., KEK_i_share_n} = SSS_divide(KEK_i, n)` is undefined. We could use Jan's help here.

#### Draft for reconstructing from shares

Recipient receives a CDOC Container containing `{C, EncryptedFMK_i [1..l], Capsule_i [1..l]}`, where `Capsule_i = {RecipientInfo_i, DistributedKEKInfo_i}` and `DistributedKEKInfo_i = {CKCTS_ID, transactionID} [1..n]`.

1. Recipient contacts CKCTS servers, sends `transactionID_i_j` and receives `nonce_i_j` (`j = 1..n`)
2. Recipient creates authentication data `auth_data = {transactionID_i_j, SHA256(nonce_i_j)} [1..n]`
3. Recipient computes `auth_hash = SHA256(auth_data)`
4. Recipient performs ID-card/Mobile-ID/Smart-ID authentication and creates a signature `auth_signature` on `auth_hash` with authentication key pair.
5. Recipient creates authentication ticket for each CKCTS server `auth_ticket_j = ... + auth_signature`
   1. TODO: `auth_ticket_j` structure is too complex to show here, need to create another section
6. Recipient downloads `share_i_j` from CKCTS server `j` with `auth_ticket_j`
7. `KEK_i = SSS_reconstruct(share_i_j) (j = 1..n)`
8. `FMK = XOR(KEK_i, CK_i)`
9. `CEK = GenKeyExpand(FMK)`
10. `M = Dec(CEK, C)`

TODO: `KEK_i = SSS_reconstruct(share_i_j) (j = 1..n)` is undefined. We could use Jan's help here.


#### TODO: leftover material, move elsewhere

The `Capsule_i` could be either such Capsule, which contains all necessary information locally:

1. `Capsule_i = {Curve, RecipientPublicKey, SenderPublicKey}`
2. `Capsule_i = {RecipientPublicKey, EncryptedKEK}`
3. `Capsule_i = {Salt}`
4. `Capsule_i = {PasswordSalt_i, KeyMaterialSalt_i}`

or such Capsule, which contains information, where to retrieve information to reconstruct the KEK:

1. `Capsule_i = {RecipientKey, KeyServerID, TransactionID}`
