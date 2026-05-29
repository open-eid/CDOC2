---
title: Introduction
---

# Introduction

This is the technical documentation for the CDOC2 System - a secure file encryption and transmission system built on top of the Estonian eID ecosystem. The document covers analysis, protocol and format specification, and architecture documentation.

CDOC2 is the successor to CDOC 1.0 (XML-ENC based formats).  It addresses limitations of CDOC 1.0 by introducing a modern cryptographic architecture, a clear distinction between transport and storage encryption, and support for mobile eID authentication methods (Smart-ID and Mobile-ID) in addition to hardware security tokens.


## Document scope

This documentation describes:

* Supported encryption schemes (hardware security tokens, Smart-ID, Mobile-ID);
* Abstract and serialized CDOC2 Container and Capsule data formats;
* Details of cryptographic operations (key derivation, ECDH, key wrapping, AEAD encryption);
* Use of a CDOC2 capsule server (CCS) for server-side key management;
* Use of the CDOC2 Shares Server (CSS) for threshold-based key share distribution.
* Client authentication protocol and session management;
* Implementation guidelines.


## Document structure

The documentation is divided into five parts:

* Use Cases: describes the functionality of the CDOC2 Client Application and the CDOC2 Capsule Server as use case models;
* Protocol and Data Formats: defines the CDOC2 protocol, container format, capsule structures, and cryptographic operations;
* System Architecture: defines system components, interfaces, and deployment structure;
* Testing Specification: describes the testing approach, test scenarios, and load testing methodology;
* User Guides: practical guides for end users and integrators, including password strength guidelines and container storage recommendations.

 > **Note:** This document combines documentation for the Capsule Server and the Smart-ID/Mobile-ID (SiD/MiD) use cases, including the Shares Server and client authentication protocol. Sections marked with [SiD/MiD] apply exclusively to Smart-ID and Mobile-ID use cases.



![Funding](img/cofunding_logo.jpg)
 