---
title: 2.1. System Context -  Hardware Token/Capsule Server
---
# System Context -  Hardware Token/Capsule Server

The CDOC2 system operates in two distinct deployment contexts. This page describes the Hardware Token/Capsule Server context; for the Smart-ID/Mobile-ID context, see [SID/MID](ch001_system_context_sid_mid.md). Both contexts share the CDOC2 reference library and CDOC2 CLI client as common components.

> **Note:** DigiDoc4 is the primary end-user client application through which
> most users interact with CDOC2. However, DigiDoc4 is not part of the CDOC2
> system scope defined here, as its architecture and documentation are
> maintained separately.

## Overview

![CDOC2 component diagram](../img/CDOC2_system_context_1.7.png)

In the Hardware Token context, encryption and decryption flows rely on the Recipient holding a hardware security token (e.g. an Estonian ID-card). Key material is stored as a Server Capsule and mediated via a CDOC2 Capsule Server. Unlike the SID/MID context, no additional authentication servers or key share distribution are involved - the Recipient's hardware token provides the cryptographic identity directly.

## Primary Components

1. CDOC2 Capsule Server (CCS): Stores Server Capsules and mediates them between Sender and Recipient, used by CDOC2 clients such as the reference CLI client and DigiDoc4. Every CDOC2 Capsule Server uses a local database component as well.

## Shared Libraries

2. CDOC2 Reference Library: used by CDOC2 servers and the CLI client.
3. CDOC2 CLI Client: a command-line Java application that implements all CDOC2 end-user use cases, but without a graphical user interface.

## External Systems

The CDOC2 system depends on the following external components and services.

1. OCSP servers (SK ID Solutions, Zetes): Provide certificate validity checking for ID-card certificates.
2. LDAP servers (SK ID Solutions, Zetes): Used by CDOC2 client applications to search for Recipient certificates prior to encryption.
