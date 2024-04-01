---
title: Introduction
---

# Introduction

## Goal

TO-TRANSLATE "CDOC2 kasutusmallimudel", Section 1.1 "Eesmärk"

This documentation aims to describe the CDOC2 system.

## Document scope

TO-TRANSLATE "CDOC2 kasutusmallimudel", Section 1.2 "Käsitlusala"

## Terms and acronyms

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

## Short overview

TO-TRANSLATE "CDOC2 kasutusmallimudel", Section 1.5 "Ülevaade"
