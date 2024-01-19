---
title: 2. CDOC2 encryption schemes
---

# CDOC2 encryption schemes

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3 "Krüpteerimisskeemid" beginning

## Direct encryption schemes with recipients asymmetric key pairs

These schemes are usable in case the recipient has asymmetric key pair (RSA or EC) and CEK decryption key (KEK) is derived between sender and recipient with some kind of key establishment protocol. CEK and key capsule is transmitted directly to the recipient, together with the encrypted payload.

There are following schemes:

### SC01: Direct encryption scheme for recipient with EC keys

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3.1 "Otsesuhtlusega ECDH skeem"

### SC02: Direct encryption scheme for recipient with RSA keys

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3.3 "Otsesuhtlusega RSA-OAEP skeem"

## Schemes using key transmission servers

These schemes are usable, in case the sender wishes to use KEK transmission servers. 

### SC03: Key transmission server scheme for recipients with EC keys

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3.2 "Võtmeedastusserveriga ECDH skeem"

### SC04: Key transmission server scheme for recipients with RSA keys

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3.4 "Võtmeedastusserveriga RSA-OAEP skeem"

## Schemes without recipient asymmetric key pairs

### SC05: Direct encryption scheme for recipient with pre-shared symmetric key

TO-TRANSLATE "CDOC2.0 spetsifikatsioon", version 0.9, Section 3.5 "Sümmeetrilise võtmega skeem"

### SC05: Direct encryption scheme for recipient with pre-shared password

New content. Merge with <https://gitlab.cyber.ee/cdoc-2.0/cdoc20_java/-/tree/rm55854#cdoc-20-with-symmetric-key-from-password>

## Schemes with recipient authentication

These schemes use key transmission servers for sending encrypted CEK from sender to recipient. Recipient will be authenticated with whatever means by key transmission servers. 

### SC06: Key transmission server scheme with one server

New content

### SC07: Key transmission server scheme with secret shared CEK

New content
