<!-- This file contains acronyms, which will be highlighted and provided with a tooltip in the built HTML -->
<!-- markdownlint-disable first-line-heading -->

*[CDOC]: Crypto Digidoc, encrypted file transmission format used in the Estonian eID ecosystem

*[CDOC 1.0]: Unofficial term for all (XML-ENC based) CDOC formats preceding this specification.

*[CDOC2 System]: IT system, which allows users to send encrypted files to each other with the help of CDOC2 Client Applications and CDOC2 Capsule Servers

*[CDOC2 Container]: File format for transmitting the encrypted payload and metadata information, <br/>including the capsule from Sender to Recipient

*[Capsule]: Data structure, which contains encryption scheme-specific information (encrypted symmetric keys, public keys, salt, server object references, ...)<br/>which Recipient can use to derive, establish or retrieve decryption keys for decrypting the CDOC2 Container. Capsule can either be a Server Capsule or a Container Capsule.

*[Server Capsule]: A Capsule that is mediated by a CDOC2 Capsule Server.

*[Container Capsule]: A Capsule that is created inside a CDOC2 container and is therefore not sent to a CDOC2 Capsule Server.

*[CCS]: CDOC2 Capsule Server

*[CSS]: CDOC2 Shares Server

*[KTS]: Key Transfer Server. Umbrella term used in use case IDs (UC.KTS.xx) covering both CCS and CSS, as both mediate transfer of key material between Sender and Recipient.

*[CDOC2 authentication server]: Web service to generate session tokens for CSS and Relying Party Servers

*[authentication ticket]: A server-specific presentation of the CDOC2 Authentication Token, created by selectively disclosing only the nonce relevant to one CSS server. One Authentication Token is signed once by the Recipient; a separate Authentication Ticket is derived and sent to each CSS.

*[SID/MID proxy]: Proxy provided by RIA to provide access to Smart-ID RP API and Mobile-ID REST API

*[hardware security token]: Smart-card with user key pairs, for example Estonian eID ID-card

*[ECDH]: Elliptic-curve Diffie–Hellman. Key-agreement protocol that allows two parties, each having an EC public–private key pair, to establish a shared secret over an insecure channel.

*[AEAD]: Authenticated Encryption with Additional Data

*[ECC]: Elliptic-Curve Cryptography

*[ECC DH]: Elliptic-Curve Cryptography Diffie Hellman key-establishment algorithm

*[ECC CDH]: Elliptic-Curve Cryptography Co-factor Diffie Hellman key-establishment algorithm

*[nonce]: A randomly generated, single-use value issued by a CSS server, used to prevent replay of authentication tickets.

*[HMAC]: Hash-Based Message Authentication Code. Protects integrity of CDOC Container.

<!--- acronyms about various keys -->

*[CEK]: Content Encryption Key. Symmetric key used to encrypt the payload of CDOC2 Container.

*[KEK]: Key Encryption Key. Symmetric key used to encrypt (wrap) the FMK, so that FMK could be transmitted inside CDOC2 Container to Recipient.

*[FMK]: File Master Key. Cryptographic key material for deriving other encryption and HMAC keys.

*[CC]: CDOC2 Capsule. Data structure inside CDOC2 Container. CC contains information for decrypting the payload of CDOC2 Container. <br/> That information could be a symmetric cryptographic key, a share of symmetric cryptographic key, <br/> or necessary data for establishing such key with key derivation algorithm or key-agreement protocol, for example, with ECDH.

*[HHK]: Header HMAC Key
