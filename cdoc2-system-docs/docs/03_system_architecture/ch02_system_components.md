---
title: 3. CDOC2 system components
---

# CDOC2 system components

## CDOC2 reference Java library

Implements client side functionality for CDOC2 system.

## CDOC2 Capsule Server (CCS)

Stores encryption/decryption key material. Provides endpoints for auth-ticket creation and key material upload/download.

## CDOC2 CLI user application

Command line utility to create/process CDOC2 files. Provides CLI interface to CDOC2 reference Java library.

# Interfaces between system components

## CDOC2 Capsule Server (CCS) interface

* `/key-capsules` - Add a server capsule and receive a transaction indentifier.
* `/key-capsules/{transactionId}`- Retrieve a server capsule by prividing a transaction identifier.
