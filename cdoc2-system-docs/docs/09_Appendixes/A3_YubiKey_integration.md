---
title: A3 - Yubikey integration possibilities
---

# Appendix 3 - Yubikey integration

## Introduction

Yubico offers several security tokens (<https://www.yubico.com/products/>) with convenient wired interfaces (USB-A, Apple Lightning, USB-C) and wireless interfaces (Bluetooth, NFC) which makes them viable alternative to smart-cards or other USB security tokens. Smart-cards usually require additional USB card-readers, which is inconvenient. Other USB key tokens (for example, SafeNet eToken 5110) could be more expensive (<https://portal.skidsolutions.eu/order/certificates?tab=crypto-stick>). This chapter analyses the APIs provided by Yubico products and discusses, how these could be used by CDOC2 Client Applications.

## Yubico security tokens

Yubico provides following general family of products:

1. YubiKey 5 series (<https://support.yubico.com/hc/en-us/articles/360016649339-YubiKey-5C-NFC>)
2. YubiKey Bio series (<https://support.yubico.com/hc/en-us/articles/4407743521810-YubiKey-Bio-FIDO-Edition>)
3. Security key series (<https://support.yubico.com/hc/en-us/articles/360013779399-Security-Key-NFC>)

and some HSM families and legacy products, which are not included in current analysis.

In summary, these security tokens offer the following types of APIs/interfaces or support these kinds of hosted credentials:

1. Secure Static Passwords
2. FIDO U2F interface
3. FIDO2 CTAP1/CTAP2 interface and WebAuthn credentials (hardware-bound passkeys)
4. OATH credentials (OATH-TOTP, OATH-HOTP) and Yubico OTP credentials
5. NIST SP 800-73 (PIV) compliant smart-card interface
6. OpenPGP Smart Card

The following sections discuss the possibilities of those interfaces/credentials.

## Interfacing options

### Secure Static Passwords

"Secure Static Passwords" feature is compatible with YubiKey 5 series and not compatible with Security Key and YubiKey Bio.

YubiKey USB token can be programmed by YubiKey Manager application (<https://docs.yubico.com/software/yubikey/tools/ykman/>) to store a randomly generated static password. USB token can act as a virtual USB keyboard and can send the password to the computer, when user presses the physical button on the token. This results in the same effect as the user himself would have entered the password on the physical keyboard. (<https://support.yubico.com/hc/en-us/articles/360016614980-Understanding-Core-Static-Password-Features>, <https://resources.yubico.com/53ZDUYE6/as/9hccqgx9bwwqq96mhkk8jb4h/Static_Password_Function.pdf>).

Unfortunately, YubiKey USB token can only hold one such password. Even though, CDOC2 Client integration with this feature could be very easy, using the same password for all CDOC2 Containers wouldn't be advisable. The popular use-case for this feature is to secure the master password of the password manager application, and then let the password manager handle all the individual passwords for other websites and applications.

Therefore, directly using the "Secure Static Passwords" feature by CDOC2 Clients is not recommended and this integration feature is not analyzed further.

### FIDO U2F interface

This feature is compatible with all YubiKey security tokens.

FIDO U2F is an open standard (<https://fidoalliance.org/specs/fido-uaf-v1.2-ps-20201020/fido-uaf-overview-v1.2-ps-20201020.html>, <https://developers.yubico.com/U2F/>), which allows computer and mobile applications to communicate with internal or external authenticators (e.g. YubiKey tokens) and to use challenge-response authentication flow, based on PKI cryptography. The U2F authenticator has a private key and can sign messages with the private key. Authenticators support using unique key pairs for each application and they can also issue device attestations.

#### FIDO U2F signature capabilities

Unfortunately, the cryptographic API only supports creating signatures (RS256, EdDSA, ES256, and Ed25519, <https://developers.yubico.com/WebAuthn/WebAuthn_Developer_Guide/Algorithms.html>) and no key agreement protocols. This means that Yubico security tokens are facing the same issue as Mobil-ID/Smart-ID eID schemes, which can also provide only signature creation and could be only used for authentication. However, at the same time Mobile-ID/Smart-ID eID schemes also provide subscriber identity management, by following strict identity proofing and registration procedures and issuing X.509 certificates, which bind together subscriber's identity and subscriber's key pair information.

It could be possible to integrate FIDO U2F compliant security tokens into the CDOC2 System by additionally implementing user's account management as well. A user would need to authenticate to CDOC2 self-service portal with existing strong eID means (ID-card, Mobile-ID, Smart-ID) and associate FIDO U2F compliant security token with their account, by registering the public key of a new key pair. This would enable CDOC2 Capsule Servers to use FIDO U2F tokens for authenticating the user and allowing the user to download capsules. It would be recommended for the user to register multiple FIDO tokens, in order to have redundancy.

CDOC2 Client Application could handle such registration by using the operating system's browser to open the CDOC2 System's self-service portal and authentication portal web sites and because browsers are already integrated with FIDO U2F tokens (and WebAuthn and passkeys), the integration would work out-of-box.

#### Reusing RSA signing for encryption/decryption

FIDO U2F specification also supports `ALG_SIGN_RSASSA_PSS_SHA256_RAW` and `ALG_SIGN_RSA_EMSA_PKCS1_SHA256_RAW` signatures (<https://fidoalliance.org/specs/fido-v2.0-id-20180227/fido-registry-v2.0-id-20180227.html#authentication-algorithms>). The availability of unpadded (raw) signatures hints at the possibility that perhaps, YubiKey tokens could be also used for RSA encryption/decryption operation.

From cryptography viewpoint, it might be possible, because internally, the YubiKey token is performing `RSASP1()` operation (<https://datatracker.ietf.org/doc/html/rfc8017#section-5.2.1>), which is exactly the same operation as `RSAEP()` operation (<https://datatracker.ietf.org/doc/html/rfc8017#section-5.1.1>). However, this needs to be experimentally verified.

From CDOC2 System viewpoint, there is still the problem of how the Sender gets information about authentic RSA public key of the Recipient, so that Sender could use the CDOC2 SC02 encryption scheme. Because there's no X.509 certificates and no identity management services within FIDO, this is unresolved. Building custom PKI services into the CDOC2 System, which would work on top of FIDO U2F tokens, seems unrealistic.

### FIDO CTAP2 interface and WebAuthn credentials

This feature is compatible with all YubiKey security tokens.

FIDO CTAP1 interface provides same features as FIDO U2F interface, using APDU-like binary structure for transmitting messages between computer and authenticators.

FIDO CTAP2 interface (<https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-errata-20220621.html>) provides FIDO CTAP1 interface features and some extra, while also using CBOR encoding for transmitting the messages between computer and authenticators.

WebAuthn2 standard (<https://www.w3.org/TR/webauthn-2/>) provides JavaScript API for web sites running inside browser, in order to use FIDO authenticators, over U2F, CTAP1, or CTAP2 interfaces.

Security tokens, which comply with WebAuthn2 and CTAP2, could be also referred as FIDO2 tokens. At the moment, YubiKey 5 Series tokens can hold up to 25 resident keys (also called discoverable credentials).

#### FIDO CTAP2 signature capabilities

In the same way as U2F, CTAP2 provides assertion signature creation function `authenticatorGetAssertion (0x02)` (<https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-errata-20220621.html#authenticatorGetAssertion>, <https://www.w3.org/TR/webauthn-2/#sctn-op-get-assertion>). Therefore, all the considerations, that were discussed in previous section ["FIDO U2F signature capabilities"](#fido-u2f-signature-capabilities), also apply to CTAP2.

However, CTAP2 also has some extensions (<https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-errata-20220621.html#sctn-defined-extensions>), which we look into at next sections.

#### `credBlob` and `largeBlobKey` extensions

`credBlob` extension (<https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-errata-20220621.html#sctn-credBlob-extension>) allows some secret information (a blob array) to be stored inside FIDO2 token, alongside the RP-specific credential. Optionally, computer could request that FIDO2 token performs the user authorization (i.e., asks the user to press the physical button on the FIDO2 token) or performs the verification of the supplied PIN-code, when retrieving this array.

This blob could be used as a place to store the symmetric encryption/decryption key of the CDOC2 Container. Unfortunately, YubiKey 5 Series tokens only support (<https://docs.yubico.com/hardware/yubikey/yk-tech-manual/yk5-apps.html#supported-extensions>) `appID` extension (<https://www.w3.org/TR/webauthn-2/#sctn-appid-extension>).

It's not know, if any FIDO2 tokens on the market support these extensions. They are not listed as mandatory features (<https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-errata-20220621.html#mandatory-features>) of CTAP2 standard.

### `hmac-secret` extension

This extension is used by the computer to retrieve a symmetric secret from the authenticator when it needs to encrypt or decrypt data using that symmetric secret (<https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-errata-20220621.html#sctn-hmac-secret-extension>).

#### Using HMAC Secret from computer applications

In order to create such a FIDO2 credential, which can be used to derive a CDOC2 Container symmetric encryption key, following steps should be done:

1. Computer chooses user validation protocol (<https://fidoalliance.org/specs/fido-v2.1-ps-20210615/fido-client-to-authenticator-protocol-v2.1-ps-errata-20220621.html#authenticatorClientPIN>), which is based on user's PIN code, or on-device user verification method like fingerprint or input UI with secure communication.
2. Computer sends `authenticatorClientPIN (0x06)` command with parameters `pinUvAuthProtocol` and `getKeyAgreement(0x02)` and establishes a shared secret with the authenticator.
3. Computer sends `authenticatorMakeCredential (0x01)` command with parameters `"hmac-secret": true`
4. Authenticator generates two random 32-byte values (called `CredRandomWithUV` and `CredRandomWithoutUV`) and associates them with the freshly created FIDO2 credential and sends back to the computer the key handle, with parameters `"hmac-secret": true`.
5. Computer should store the handle to FIDO2 credential and other required parameters.

In order to retrieve the key material for symmetric encryption key, the computer should do following steps:

1. Computer sends `authenticatorClientPIN (0x06)` command with parameters `pinUvAuthProtocol` and `getKeyAgreement(0x02)` and establishes a shared secret with the authenticator.
2. Computer sends `authenticatorGetAssertion (0x02)` command with extension map `hmac-secret` and parameters `salt1`, protecting the arguments with the shared secret established in the previous step.
3. Authenticator verifies the command parameters, chooses `CredRandom=CredRandomWithUV` and responds with `output1=HMAC-SHA-256(CredRandomWithUV, salt1)` and returns `output1`, protecting the data with shared secret established in the previous step.
4. Computer can use `output1` or `output2` as the key material for CDOC2 encryption scheme SC05.

An example of some open-source implementations, who are using this feature, could be found at

* <https://github.com/FiloSottile/age/discussions/390> and <https://github.com/olastor/age-plugin-fido2-hmac/blob/main/SPEC.md>
* <https://github.com/keepassxreboot/keepassxc/issues/3560>

#### PRF feature in WebAuthn3

The usage of HMAC Secret Extension is further improved in the upcoming WebAuthn version 3 standard (<https://w3c.github.io/webauthn/#prf-extension>). This allows websites to request PRF (pseudo-random function) outputs, that could be used as symmetric keys to encrypt user data. Internally, the browser would be talking to FIDO2 authenticator and would be using the same HMAC Secret Extension to obtain symmetric keys.

This should indicate that CTAP2 protocol extension `hmac-secret` is probably not going away.

Some further information is provided in:

* <https://forums.developer.apple.com/forums/thread/733413>
* <https://bitwarden.com/blog/prf-webauthn-and-its-role-in-passkeys>
* <https://github.com/w3c/webauthn/wiki/Explainer:-PRF-extension>

#### Passkeys

It's not clear, if browsers and operating systems, which have built-in support for passkeys (which are kind of FIDO2 authenticators) also support such extensions. Some information available at <https://github.com/w3c/webauthn/issues/1830> and <https://chromestatus.com/feature/5138422207348736> seem to hint that Android 13 and Chrome Canary might support this already.

### OATH credentials

OATH API feature is compatible with YubiKey 5 series security tokens and not compatible with YubiKey Security Key and YubiKey Bio series.

OATH is a consortium (<https://openauthentication.org/about-oath/>), which is standardizing authenticators and also one-time-password methods, such as time-based one-time password (TOTP) and HMAC-based one-time password (HOTP).

It turns out that it is possible to use HOTP, also published as <https://www.rfc-editor.org/rfc/rfc4226.html>, as a decryption key provider. This has been described in <https://support.yubico.com/hc/en-us/articles/360013779759-Using-Your-YubiKey-with-KeePass> and (experimentally) implemented in KeepPassXC plugin KeeChallenge (<https://brush701.github.io/keechallenge/>).

Since this seems to be a non-standard way of using an authentication protocol for encryption/decryption. It's not clear, what kind of vulnerabilities or risks this method may have. We do not recommend to further analyze this feature.

### Smart-card API

Smart-card API feature is compatible with YubiKey 5 series security tokens and not compatible with YubiKey Security Key and YubiKey Bio series.

Smart-card API allows to perform RSA or ECC sign/decrypt operations using a private key stored on YubiKey tokens. RSA 1024, RSA 2048, or ECC secp256r1 keys are supported. YubiKey 5 can hold up to 24 key pairs and certificates.

In a sense, with this API, YubiKey security token becomes a regular smart-card, comparable to ID-card, but YubiKey is directly usable over USB interfaces and also over contact-less interfaces. From a cryptography viewpoint, such tokens could be used to in CDOC2 encryption schemes SC01, SC02, SCO3, SC04. However, because YubiKey tokens are not integrated with identity management function of ID-card eID scheme, there's no easy way for Senders to find out, what are the correct key pairs of intended Recipients.

Another possibility is to use YubiKey hosted EC key pair for ECDH shared key establishment and to use this derived key as encryption/decryption key for the local storage of CDOC2 Container. Perhaps it could be done in a similar way as NIST SP 800-73-4 Part 2, Section 4.2 is establishing (<https://csrc.nist.gov/files/pubs/sp/800/73/4/final/docs/sp800_73-4_pt2_revised_draft.pdf>) secrets for secure messaging, or in a similar way as ECIES scheme is establishing secrets for encryption/decryption (<https://en.wikipedia.org/wiki/Integrated_Encryption_Scheme>). CDOC2 currently doesn't have such a crypto scheme defined, it would need to be an addition to existing storage-crypto schemes SC05 and SC06.

<!-- YubiKey CLI application `yubico-piv-tool` (<https://developers.yubico.com/yubico-piv-tool/Manuals/yubico-piv-tool.1.html>) provides command `test-decryption`, which shows an example, how to do ECDH key agreement. -->

### OpenPGP Smart Card API

Not analyzed currently. Assuming this is similar to NIST PIV-compliant smart-card API.

## Security aspects

### Identity management

In case FIDO token is used as simple authenticator, CDOC2 system has to maintain associations between national identity codes and FIDO public key pairs. This database and self-service management portal then becomes a lucrative single point for attacks and has to be protected as a trusted system component, because if attacker is able to add their own FIDO public key to the user's account, they are able to authenticate to Capsule Servers and retrieve the key material for decrypting the CDOC2 Container on behalf of the user.

In that sense, the identity proofing and identity management functions of those eID schemes, which are supported by CDOC2 System, are really critical.

### Encryption key inside application memory

In case FIDO token is used as symmetric encryption key provider, the encryption key is transferred to CDOC2 Client Application process memory and is processed on the computer CPU. The presents an opportunity to leak the key and this may feel risky, when compared to the usual practices of using HSM-bound crypto material.

It might be interesting to compare the security level of YubiKey hosted encryption key and ordinary USB memory stick, which hosts wrapped encryption key, protected with user's PIN or password. In both cases, the encryption key is transferred to the application memory and processed there, in the clear text. However, YubiKey provides better protection against offline brute-force attacks, in case the PIN-code or password, which is used to derive the unwrapping key, is rather short. For example, if we use a very expensive key derivation function, which takes 5 minutes to derive unwrapping key, the attacker could still simply try all 4-digit PIN-codes in about a month time and successfully retrieve the unwrapping key.

## Summary

There are multiple ways to continue:

1. Use YubiKey security token (or any other compliant security token) as authenticator for accessing CDOC2 Capsule Servers. This could be achieved by using FIDO U2F compliant interface or by using smart-card compatible interface.
2. Use YubiKey security token (or any other FIDO2 compatible token, including passkey implementations, which supports `hmac-secret` extension) as symmetric encryption/decryption key provider for long-term storage crypto. This could complement password-based encryption schemes in CDOC2 System.
3. Use YubiKey security token (or any other smart-card compatible token) as a symmetric encryption key provider, based on EC key pair and ECDH key establishment protocols, for long-term storage crypto. This could add to password-based encryption schemes in CDOC2 System.

Current recommendation is to further study the options 2 and 3 and to work out approximate estimates for integration and development efforts. As option 2 is also supported by Security Key Series, which are somewhat cheaper than YubiKey 5 series (<https://www.yubico.com/ee/store/compare/>), the priority should be on option 2.
