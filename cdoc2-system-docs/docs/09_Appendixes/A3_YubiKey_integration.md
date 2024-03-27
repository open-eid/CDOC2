---
title: A3 - Yubikey integration possibilities
---

# Appendix 3 - Yubikey integration

## Intro

Company Yubico (<https://www.yubico.com/products/>) offers several security tokens with convenient wired interfaces (USB-A, Apple Lightning, USB-C) and wireless interfaces (Bluetooth, NFC) which makes them viable alternative to smart-cards, which require additional USB card-readers or other USB key tokens, which could be more expensive (<https://portal.skidsolutions.eu/order/certificates?tab=crypto-stick>). This chapter analyses the APIS provided by Yubico products and discusses, how these could be used by CDOC2 Client applications.

## Yubico security tokens

Yubico provides following general family of products:

1. YubiKey 5 series (<https://support.yubico.com/hc/en-us/articles/360016649339-YubiKey-5C-NFC>)
2. YubiKey Bio series (<https://support.yubico.com/hc/en-us/articles/4407743521810-YubiKey-Bio-FIDO-Edition>)
3. Security key series (<https://support.yubico.com/hc/en-us/articles/360013779399-Security-Key-NFC>)

and some legacy products, which are not included in current analysis.

These products offer the following type of credentials and interfaces:

1. Secure Static Passwords
2. FIDO U2F interface
3. FIDO2 CTAP1/CTAP2 interface and WebAuthn credentials (hardware-bound passkey)
4. OATH credentials (OATH-TOTP, OATH-HOTP)
5. Yubico OTP credentials
6. NIST SP 800-73 (PIV) compliant smart-card interface
7. OpenPGP Smart Card

The following sections discuss the possibilities of those interfaces/credentials.

## Interfacing options

### Secure Static Passwords

"Secure Static Passwords" feature is compatible with YubiKey 5 series and not compatible with Security Key and YubiKey Bio.

YubiKey USB token can be programmed by YubiKey Manager application (<https://docs.yubico.com/software/yubikey/tools/ykman/>) to store a randomly generated static password. USB token can act as a virtual USB keyboard and can send the password to the computer, when user presses the physical button on the token. This results in the same effect as the user himself would have entered the password on the physical keyboard. (<https://support.yubico.com/hc/en-us/articles/360016614980-Understanding-Core-Static-Password-Features>, <https://resources.yubico.com/53ZDUYE6/as/9hccqgx9bwwqq96mhkk8jb4h/Static_Password_Function.pdf>).

Unfortunately, YubiKey USB token can only hold one such password. Even though, CDOC2 Client integration with this feature is very easy, using the same password for all CDOC2 Containers wouldn't be advisable. The popular use-case for this feature is to secure the master password of the password manager application, and then let the password manager handle all the individual passwords for other websites and applications.

Therefore, directly using the "Secure Static Passwords" feature by CDOC2 Clients is not recommended and this integration feature is not analyzed further.

### FIDO U2F interface

This feature is compatible with all YubiKey security tokens.

FIDO U2F is an open standard (<https://fidoalliance.org/specs/fido-uaf-v1.2-ps-20201020/fido-uaf-overview-v1.2-ps-20201020.html>, <https://developers.yubico.com/U2F/>), which allows computer and mobile applications to communicate with internal and external authenticators and to use challenge-response authentication flow, based on PKI cryptography. The U2F authenticator has a private key and can sign messages with the private key. Authenticators support using unique key pairs for each application and they can also issue device attestations.

#### FIDO U2F signature capabilities

Unfortunately, the cryptographic API only supports creating signatures (RS256, EdDSA, ES256, and Ed25519, <https://developers.yubico.com/WebAuthn/WebAuthn_Developer_Guide/Algorithms.html>) and no key agreement protocols. This means that Yubico security tokens are facing the same issue as Mobil-ID/Smart-ID eID schemes, which can also provide only signature creation and could be only used for authentication. However, at the same time Mobile-ID/Smart-ID eID schemes also provide subscriber identity management, by following strict registration procedures and issuing X.509 certificates, which bind together subscriber's identity and subscriber's key pair information.

It could be possible to integrate FIDO U2F compliant security tokens into the CDOC2 System by implementing user's account management. A user would need to authenticate to CDOC2 self-service portal with existing strong eID means (ID-card, Mobile-ID, Smart-ID) and associate FIDO U2F compliant security token with their account, by registering the public key of a new key pair. This would enable CDOC2 Capsule Servers to use FIDO U2F tokens for authenticating the user and allowing the user to download capsules. It would be recommended for the user to register multiple FIDO tokens, in order to have redundancy.

CDOC2 Client application could handle such registration by using the operating system's browser to open the CDOC2 System's self-service portal and authentication portal web sites and because browsers are already integrated with FIDO U2F tokens (and WebAuthn and passkeys), the integration would work out-of-box.

#### Reusing RSA signing for encryption/decryption

FIDO U2F specification also supports `ALG_SIGN_RSASSA_PSS_SHA256_RAW` and `ALG_SIGN_RSA_EMSA_PKCS1_SHA256_RAW` signatures (<https://fidoalliance.org/specs/fido-v2.0-id-20180227/fido-registry-v2.0-id-20180227.html#authentication-algorithms>). The availability of unpadded (raw) signatures hints at the possibility that perhaps, YubiKey tokens could be also used for RSA encryption/decryption operation.

From cryptography viewpoint, it might be possible, because internally, the YubiKey token is performing `RSASP1()` operation (<https://datatracker.ietf.org/doc/html/rfc8017#section-5.2.1>), which is exactly the same operation as `RSAEP()` operation (<https://datatracker.ietf.org/doc/html/rfc8017#section-5.1.1>). However, this needs to be experimentally verified.

From CDOC2 System viewpoint, there is still the problem of how the Sender gets access to authentic RSA public key of the Recipient, so that Sender could use the CDOC2 SC02 encryption scheme. Because there's no PKI and no identity management services within FIDO, this is unresolved. Building custom PKI services into the CDOC2 System, which would work on top of FIDO U2F tokens, seems unrealistic.

### FIDO2 CTAP2 interface and WebAuthn credentials

resident credentials (<https://developers.yubico.com/WebAuthn/WebAuthn_Developer_Guide/Resident_Keys.html>)

### OATH credentials

OATH consortium (https://openauthentication.org/about-oath/) is standardising 

### Smart-card API

### OpenPGP Smart Card API



