<!--- This file contains acronyms, which will be highlighted and provided with a tooltip in the built HTML -->

*[CDOC2 System]: IT system, which allows users to send encrypted files to each other with the help of CDOC2 Client Applications and CDOC2 Capsule Transmission Servers
*[CTS]: CDOC2 Capsule Transmission Server
*[hardware security token]: Smart-card (for example Estonian eID ID-card) or FIDO authenticator with asymmetric cryptographic keys

*[ECDH]: Elliptic-curve Diffie–Hellman. Key-agreement protocol that allows two parties, each having an elliptic-curve public–private key pair, to establish a shared secret over an insecure channel. (<https://en.wikipedia.org/wiki/Elliptic-curve_Diffie–Hellman>)

<!--- acronyms about various keys -->

*[CEK]: Content Encryption Key. Symmetric key used to encrypt the payload of CDOC2 Container.
*[KEK]: Key Encryption Key. Symmetric key used to encrypt (wrap) the CEK, so that CEK could be transmitted inside CKC.
*[FMK]: File Master Key. Cryptographic key material for deriving the CEK.
*[CKC]: CDOC2 Key Capsule. Data structure inside CDOC2 Container. CKC contains information for decrypting the payload of CDOC2 Container. <br/> That information could be a symmetric cryptographic key, a share of symmetric cryptographic key, <br/> or necessary data for establishing such key with key derivation algorithm or key-agreement protocol, for example, with ECDH.
