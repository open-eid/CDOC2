<!-- Title: 04. CDOC2 encryption schemes -->

# CDOC2 encryption schemes

<!-- Include: ac:toc -->

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3 "Krüpteerimisskeemid" beginning

## Definitions and notation

TODO: This currently taken from existing spec. We probably need to rework them and align the notation and terms with rest of the document.

* `FMK` - File Master Key
* `CEK` - Content Encryption Key (used to encrypt the payload)
* `KEK` - FMK Encryption Key (used to encrypt the FMK)
* `M` - Message (payload of CDOC2 Container)
* `C` - Ciphertext (encrypted message M)
* `CK` - Encrypted FMK
* `Capsule` - CDOC2 Key Capsule (originally `caps`)
* ...

## Direct encryption schemes with recipients asymmetric key pairs

These schemes are usable in case the recipient has asymmetric key pair (RSA or EC) and CEK decryption key (KEK) is derived between sender and recipient with some kind of key establishment protocol. CEK and key capsule is transmitted directly to the recipient, together with the encrypted payload.

There are following schemes:

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
   