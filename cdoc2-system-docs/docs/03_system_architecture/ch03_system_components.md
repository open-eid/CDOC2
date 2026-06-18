---
title: 3. CDOC2 system components -  Hardware Token/Capsule Server
---

# System Components - Hardware Token/Capsule Server

This page describes the system components relevant to the Hardware Token/Capsule Server context. For the Smart-ID/Mobile-ID context, see [SID/MID](ch04_system_components_sid_mid.md).

## Shared Components

### CDOC2 reference Java library

Implements client side functionality for CDOC2 system. Used by both the Hardware Token/Capsule Server and SID/MID contexts.

## Hardware Token/Capsule Server Components

### CDOC2 Capsule Server (CCS)

Stores encryption/decryption key material. Provides endpoints for auth-ticket creation and
key material upload/download.

### CDOC2 CLI user application

Command line utility to create/process CDOC2 files. Provides CLI interface to CDOC2 reference Java library.

## Interfaces between system components

### CDOC2 Capsule Server (CCS) interface

CSS interface provides the following endpoints:

* `/key-capsules/{transactionId}` Get Server Capsule based on the transaction identifier. Used by recipient to request a Server Capsule.
* `/key-capsules` Upload a Server Capsule to a CCS. Used by sender to upload Server Capsule to a CCS.

For full CCS OpenAPI specification, see [API References](../02_protocol_and_cryptography_spec/api_references.md).
