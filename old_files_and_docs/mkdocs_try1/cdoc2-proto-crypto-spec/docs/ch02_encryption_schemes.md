---
title: 2. CDOC2 encryption schemes
---

# CDOC2 encryption schemes

TO-TRANSLATE "CDOC2 spetsifikatsioon", version 0.9, Section 3 "Krüpteerimisskeemid" beginning

## Direct encryption schemes with recipients asymmetric key pairs

These schemes are usable in case the recipient has asymmetric key pair (RSA or EC) and CEK decryption key (KEK) is derived between sender and recipient with some kind of key establishment protocol. CEK and key capsule is transmitted directly to the recipient, together with the encrypted payload.

There are following schemes:

### SC01: Direct encryption scheme for recipient with EC keys

TO-TRANSLATE "CDOC2 spetsifikatsioon", version 0.9, Section 3.1 "Otsesuhtlusega ECDH skeem"

### SC02: Direct encryption scheme for recipient with RSA keys

TO-TRANSLATE "CDOC2 spetsifikatsioon", version 0.9, Section 3.3 "Otsesuhtlusega RSA-OAEP skeem"

## Schemes using key transmission servers

These schemes are usable, in case the sender wishes to use CKCTS servers.

### SC03: Key transmission server scheme for recipients with EC keys

TO-TRANSLATE "CDOC2 spetsifikatsioon", version 0.9, Section 3.2 "Võtmeedastusserveriga ECDH skeem"

### SC04: Key transmission server scheme for recipients with RSA keys

TO-TRANSLATE "CDOC2 spetsifikatsioon", version 0.9, Section 3.4 "Võtmeedastusserveriga RSA-OAEP skeem"

## Schemes without recipient asymmetric key pairs

### SC05: Direct encryption scheme for recipient with pre-shared symmetric key

TO-TRANSLATE "CDOC2 spetsifikatsioon", version 0.9, Section 3.5 "Sümmeetrilise võtmega skeem"

### SC05: Direct encryption scheme for recipient with pre-shared password

New content. Merge with <https://gitlab.ext.cyber.ee/cdoc2/cdoc20_java#cdoc2-with-symmetric-key-from-password>

## Schemes with recipient authentication

These schemes use CKCTS servers for sending KEK from sender to recipient. Recipient will be authenticated with whatever means by CKCTS servers and would download the CKC from servers.

### SC06: Key transmission server scheme with one server

New content

### SC07: Key transmission server scheme with secret shared CEK

New content

IDEA: We could add one share of KEK into such CKC, which would be included in the CDOC2 Capsule at all times. This way, the CKCTS servers doesn't need to be trustworthy at all?

Does this idea add any security? Because, even without such a share, the attacker, who has eavesdropped CDOC2 Capsule, can still download other CKCs from CKCTS servers.

It would work perhaps, if we could invent such secret-sharing scheme, where the CDOC2 Capsule included share can only be decrypted with some kind of eID means. But in this case, what is the added benefit, of distributing other shares to CKCTS servers?
