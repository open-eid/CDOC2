# CDOC2 encryption schemes

This section presents the abstracted forms of all supported encryption methods, providing descriptions of messaging between the parties and the contents of exchanged messages. The purpose of the section is to familiarize the reader with the basic principles of various encryption schemes.
In all scenarios, the sender (Alice, *A*) wants to send a message *M* to the recipient (Bob, *B*) in an encrypted form. They can achieve this either directly or by using a key server S (or servers *S1*, *S2*, … , *Sn*). The number of recipients may also be higher than one, in which case they will be designated as *B1*, *B2*, … ,*Bl*.

<-- REVIEW: Proposal. Let's use UTF-8 subscripts, like S₁ and Sₙ. This way, output looks nicer and the source code is also readable? -->

Alice uses symmetric encryption system ``Sym``, comprising the following components.

The C_DERIVEKEY function takes the sender’s ephemeral public key pkeph and a reference to the corresponding ID-card key pair (pkrec, skrec) as inputs. The recipient computes:

1. Key generation algorithm GenKey<sub>Sym</sub> – used for generating the secret key. See section [KEK computation during encryption](ch05_cryptographic_details.md#kek-computation-during-encryption).
2. Encryption algorithm $$Enc_{Sym}$$ – a function taking a key and an input (to be encrypted) as arguments and returning a cryptogram.
3. Decryption algorithm $$ Dec_{Sym} $$ – a function taking a key and a cryptogram as arguments. If the function is called with the key used for encrypting the cryptogram as argument, it will return the original input. Otherwise it will return a random valid input.

The keys are generated using HKDF (extract, then expand). In the extract phase, a file master key (*FMK*) is generated using the function ``GenKeyExtractSym`` that is then used for deriving the content encryption key (*CEK*) in the expand phase. The *CEK* is used as the secret key in symmetric encryption. Symmetric encryption and decryption utilize the ChaCha20-Poly1305 algorithm. For more details, see sections [Key derivation](ch05_cryptographic_details.md#key-derivationn) and [Payload assembly and encryption](ch05_cryptographic_details.md#payload-assembly-and-encryption).

Alice generates a separate master key for each recipient, using a recipient-specific key encryption key (*KEK*).
The scenarios described in the following sections differ by the methods used for generating the *KEK* and transmitting the key capsules containing the encrypted master key *FMK* to the recipients.

## Definitions and notation

* `CDOC` - Crypto Digidoc, encrypted file transmission format used in the Estonian eID ecosystem.

* ``CDOC 1.0`` - Unofficial term for all (XML-ENC based) CDOC formats preceding this specification.

* ``CDOC2 System`` - IT system, which allows users to send encrypted files to each other with the help of CDOC2 Client Applications and CDOC2 Capsule Transmission Servers.

* `CK` - Encrypted FMK

* ``CKCTS`` - CDOC2 Key Capsule Transmission Server.

* ``CDOC2 authentication server`` - Web service to generate access tokens for CKCTS and RIA SID/MID proxy.

* ``SID/MID proxy`` - Proxy provided by RIA to provide access to Smart-ID RP API and Mobile-ID REST API.

* ``Hardware security token`` - Smart-card (for example Estonian eID ID-card) or FIDO authenticator with asymmetric cryptographic keys.

* ``ECDH`` - Elliptic-curve Diffie–Hellman. Key-agreement protocol that allows two parties, each having an elliptic-curve public–private key pair, to establish a shared secret over an insecure channel. (<https://en.wikipedia.org/wiki/Elliptic-curve_Diffie–Hellman>)

* ``AEAD`` - Authenticated Encryption with Additional Data.

* ``ECC`` - Elliptic-Curve Cryptography.

* ``HMAC`` - Header Message authentication Code.

* ``CEK`` - Content Encryption Key. Symmetric key used to encrypt the payload of CDOC2 Container.

* ``KEK`` - Key Encryption Key. Symmetric key used to encrypt (wrap) the CEK, so that CEK could be transmitted inside CKC.

* ``FMK`` - File Master Key. Cryptographic key material for deriving the CEK.

* ``CKC`` - CDOC2 Key Capsule. Data structure inside CDOC2 Container. CKC contains information for decrypting the payload of CDOC2 Container. <br/> That information could be a symmetric cryptographic key, a share of symmetric cryptographic key, <br/> or necessary data for establishing such key with key derivation algorithm or key-agreement protocol, for example, with ECDH.

* ``HHK`` - Header HMAC Key.

* `M` - Message (payload of CDOC2 Container)

* `C` - Ciphertext (encrypted message M)

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

## Security assumptions

The most basic security objective of encryption is that

	nobody other than the specified recipient (B) can decrypt the message M.

The achievement of this objective requires making corresponding security assumptions in the methods discussed herein. It must always be presumed that

	the utilized symmetric encryption system Sym will not be broken.

The asymmetric cryptography-based method from section [Direct key agreement-based ECDH](#direct-key-agreement-based-ecdh) assumes that

	the utilized asymmetric encryption algorithm will not be broken.

The asymmetric cryptography-based method from section [Key server-based ECDH](#key-server-based-ecdh) assumes that

	the utilized asymmetric encryption algorithm will not be broken

or

	the key server is operating properly.

## Direct encryption schemes with recipients asymmetric key pairs

These schemes are usable in case the recipient has asymmetric key pair (RSA or EC) and CEK decryption key (KEK) is derived between sender and recipient with some kind of key establishment protocol. CEK and key capsule is transmitted directly to the recipient, together with the encrypted payload.

### SC01: Direct encryption scheme for recipient with EC keys

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3.1 "Otsesuhtlusega ECDH skeem"

### SC02: Direct encryption scheme for recipient with RSA keys

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3.3 "Otsesuhtlusega RSA-OAEP skeem"

## Schemes using key transmission servers

These schemes are usable, in case the sender wishes to use CKCTS servers.

### SC03: Key transmission server scheme for recipients with EC keys

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3.2 "Võtmeedastusserveriga ECDH skeem"

### SC04: Key transmission server scheme for recipients with RSA keys

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3.4 "Võtmeedastusserveriga RSA-OAEP skeem"

## Schemes without recipient asymmetric key pairs

### SC05: Direct encryption scheme for recipient with pre-shared symmetric key

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3.5 "Sümmeetrilise võtmega skeem"

### SC06: Direct encryption scheme for recipients with pre-shared passwords

TODO: Experiment with embedded LaTeX to see if this displays better than Markdown `code`

This scheme is used, when Sender wishes to use a password-based encryption for:

* long-term storage of CDOC2 Container, so that decryption of it doesn't depend on availability of hardware tokens or validity of PKI certificates, or
* transmitting CDOC2 Container to such Receivers, who doesn't have any eID means.

Password-based encryption scheme can be used for multiple Recipients, who each may know a different password for decryption. This encryption scheme is very similar to scheme SC05, which uses pre-shared encryption key(s).

Sender steps for encryption:

1. `FMK = HKDF_Extract(Static_FMK_Salt, CSRNG())`
2. `CEK = HKDF_Expand(FMK)`
3. `C = Enc(CEK, M)`
4. `Password_i` is provided by Sender
5. `PasswordSalt_i = CSRNG()`
6. `PasswordKeyMaterial_i = PBKDF(Password_i, PasswordSalt_i)`
7. `KeyMaterialSalt_i = CSRNG()`
8. `{KEK_i, Capsule_i} = ENCAPS_HKDF(PasswordKeyMaterial_i, KeyMaterialSalt_i)`
9. `EncryptedFMK_i = XOR(FMK, KEK_i)`

Sender creates a CDOC Container for each Recipient with `{C, EncryptedFMK_i, Capsule_i}`, including other technical details, and sends the Container to Recipient or places in long-term storage of themself.

After some time, Sender may wish to decrypt the Container themselves (assuming the role of Recipient) or the Recipient wishes to decrypt the Container.

Recipient steps for decryption:

1. Recipient receives CDOC2 Container along with data `{C, EncryptedFMK_i, Capsule_i}`
2. `Password_i` is provided by Recipient itself
3. `PasswordSalt_i` is retrieved from header of received container
4. `PasswordKeyMaterial_i = PBKDF(Password_i, PasswordSalt_i)`
5. `KeyMaterialSalt_i` is retrieved from header of received container
6. `{KEK_i, Capsule_i} = DECAPS_HKDF(PasswordKeyMaterial_i, KeyMaterialSalt_i)`
7. `FMK = XOR(KEK_i, CK_i)`
8. `CEK = GenKeyExpand(FMK)`
9. `M = Dec(CEK, C)`

## Schemes with recipient authentication

These schemes use CKCTS servers for sending KEK from sender to recipient. Recipient will be authenticated with whatever means by CKCTS servers and would download the CKC from servers.

### SC07: Key transmission server scheme with one server

New content

### SC07: Key transmission server scheme with secret shared KEK

This scheme is used, when Sender wishes to use multiple CKCTS servers do distribute the information necessary to decrypt CDOC2 Container among the servers and this way to reduce the need to trust a single CKCTS server. Scheme uses Shamir's Secret Sharing algorithm.

Scheme requirements:

1. Scheme must support threshold option. For example, with $(2,3)$ scheme, when there are three CKCTS servers, the decryption key material is divided into three shares. The Recipient may only need to download two shares and can reconstruct the decryption key. This achieves natural fault-tolerance and individual CKCTS servers could have lower availability requirements.
2. It must be possible to combine this scheme with any other previous encryption schemes, i.e. it must be possible to divide and reconstruct any Capsule information.
   1. TODO: No. This doesn't make sense. First of all, we cannot distribute `KeyServerCapsule` anyway.
   2. TODO: And there's no point to distribute `ECCPublicKeyCapsule` or `RSAPublicKeyCapsule`, because they don't contain any confidential information anyway?
   3. TODO: We need another encryption scheme, so that KEK information is distributed to Recipients in clear-text.
3. TODO: more requirements?
  
#### Draft for dividing into shares

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

#### TODO: leftover material, move elsewhere

The `Capsule_i` could be either such Capsule, which contains all necessary information locally:

1. `Capsule_i = {Curve, RecipientPublicKey, SenderPublicKey}`
2. `Capsule_i = {RecipientPublicKey, EncryptedKEK}`
3. `Capsule_i = {Salt}`
4. `Capsule_i = {PasswordSalt_i, KeyMaterialSalt_i}`

or such Capsule, which contains information, where to retrieve information to reconstruct the KEK:

1. `Capsule_i = {RecipientKey, KeyServerID, TransactionID}`
