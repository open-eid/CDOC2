# Appendix B: recipients.fbs
    namespace Recipients;

    //for future proofing and data type
    union KeyDetailsUnion {
        EccKeyDetails, RsaKeyDetails
    }

    // Elliptic curve type enum for ECCPublicKey recipient
    enum EllipticCurve:byte {
        UNKNOWN,
        secp384r1
    }


    table RsaKeyDetails {
        //RSA pub key in DER
        recipient_public_key:   [ubyte] (required);
    }

    table EccKeyDetails {
        // Elliptic curve type enum
        curve:                 EllipticCurve = UNKNOWN;

        //EC pub key in TLS format 
        //for secp384r1 curve: 0x04 + X 48 coord bytes + Y coord 48 bytes)
        recipient_public_key:  [ubyte] (required);
    }

    // ECC public key recipient
    table ECCPublicKeyCapsule {
        curve:                 EllipticCurve = UNKNOWN;
        recipient_public_key:  [ubyte] (required);
        sender_public_key:     [ubyte] (required);
    }

    table RSAPublicKeyCapsule {
        recipient_public_key:  [ubyte] (required);
        encrypted_kek:         [ubyte] (required);
    }


    table KeyServerCapsule {
        recipient_key_details: KeyDetailsUnion;
        keyserver_id:          string (required);
        transaction_id:        string (required);
    }


    // symmetric long term crypto
    table SymmetricKeyCapsule {
        salt:                 [ubyte] (required);
    }