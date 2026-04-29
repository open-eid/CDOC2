# Appendix E: Key Shares API, version 1.0.1-draft of cdoc2-key-shares API

    openapi: 3.0.3
    info:
      contact:
        url: http://ria.ee
      title: cdoc2-key-shares
      version: 1.2.1-draft
      description: |
        API for exchanging CDOC2 key material shares.
        
        `KeyShare` objects defined here are created by splitting cryptographic material required for 
        encrypting/decrypting CDOC2 document. `KeyShare` objects required for combining original cryptographic material 
        are stored in CDOC2 header `KeySharesCapsule` [FBS](https://github.com/open-eid/cdoc2-java-ref-impl/blob/master/cdoc2-schema/src/main/fbs/recipients.fbs) object.
        
        To access `KeyShare` objects, recipient must authenticate himself by including `x-cdoc2-auth-token` 
        and `x-cdoc2-auth-x5c` headers for `getKeyShareByShareId` operation.
        
        * `x-cdoc2-auth-token` is sd-jwt defined in WIP https://open-eid.github.io/CDOC2/2.0/ . 
          Java implementation for `x-cdoc2-auth-token` can be found WIP https://github.com/open-eid/cdoc2-auth
          `x-cdoc2-auth-token` is signed by Smart-ID [authentication](https://github.com/SK-EID/smart-id-documentation?tab=readme-ov-file#2310-authentication-session) 
          certificate or [Mobile-ID authentication](https://github.com/SK-EID/MID?tab=readme-ov-file#32-initiating-signing-and-authentication) certificate.
        * `x-cdoc2-auth-x5c` is PEM encoded X509 certificate (without newlines) that was used to sign x-cdoc2-auth-token. 
          Certificate holders identify is specified in Subject "serialnumber" field. Example certificate subject: 
          'serialNumber = PNOEE-30303039914, GN = OK, SN = TESTNUMBER, CN = "TESTNUMBER,OK", C = EE'
          Certificate full structure is defined in 
          [Certificate and OCSP Profile for Smart-ID](https://www.skidsolutions.eu/wp-content/uploads/2024/10/SK-CPR-SMART-ID-EN-v4_7-20241127.pdf)
    
    servers:
      - url: 'https://localhost:8443'
        description: Regular TLS (no mutual TLS required).
    
    paths:
      '/key-shares/{shareId}':
        get:
          summary: Get key share for shareId
          description: Get key share for shareId
          tags:
            - cdoc2-key-shares
          operationId: getKeyShareByShareId
          parameters:
            - name: shareId
              in: path
              schema:
                type: string
                minLength: 18
                maxLength: 34
              required: true
            - name: x-cdoc2-auth-token
              in: header
              schema:
                type: string
              required: true
              description: |
                SDJWT [Auth token WIP](https://github
                .com/open-eid/CDOC2/blob/master/cdoc2-system-docs/docs/03_system_architecture/ch06_ID_authentication_protocol.md?ref_type=heads#verifying-sd-jwt-verifying-authentication-ticket)
            - name: x-cdoc2-auth-x5c
              in: header
              schema:
                type: string
              required: true
              description: |
                PEM encoded X509 certificate (without newlines) that was used to sign x-cdoc2-auth-token. 
                Certificate holders identify is specified in Subject "serialnumber" field. Example certificate subject: 
                'serialNumber = PNOEE-30303039914, GN = OK, SN = TESTNUMBER, CN = "TESTNUMBER,OK", C = EE'
                Certificate full structure is defined in 
                [Certificate and OCSP Profile for Smart-ID](https://www.skidsolutions.eu/wp-content/uploads/2024/10/SK-CPR-SMART-ID-EN-v4_7-20241127.pdf)
            - $ref: '#/components/parameters/SessionTokenHeader'
            - $ref: '#/components/parameters/SessionX5cHeader'
            - $ref: '#/components/parameters/SidRpV3SignatureParams'
          responses:
            '200':
              description: OK
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/KeyShare'
            '400':
              description: 'Bad request. Client error.'
            '401':
              description: 'Unauthorized. No correct auth headers'
            '404':
              description: 'Not Found. 404 is also returned, when recipient id in record does not match user id in auth-ticket'
    
      '/key-shares':
        post:
          summary: Add Key Share
          description: Save a key share and generate share id using secure random. Generated share is returned in Location header
          operationId: createKeyShare
          responses:
            '201':
              description: Created
              headers:
                Location:
                  schema:
                    type: string
                    example: /key-shares/9a7c3717d21f5cf19d18fa4fa5adee21
                  description: 'URI of created resource. ShareId can be extracted from URI as it follows pattern /key-shares/{shareId}'
            '400':
              description: 'Bad request. Client error.'
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/KeyShare'
          tags:
            - cdoc2-key-shares
    
      '/key-shares/{shareId}/nonce':
        post:
          description: |
            Create server nonce for authentication signature.
          operationId: createNonce
          parameters:
            - name: shareId
              in: path
              schema:
                type: string
                minLength: 18
                maxLength: 34
              required: true
            - $ref: '#/components/parameters/SessionTokenHeader'
            - $ref: '#/components/parameters/SessionX5cHeader'
          responses:
            '200':
              description: Created
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/NonceResponse'
            '400':
              description: 'Bad request. Client error.'
            '403':
              description: 'Authentication failed'
            '404':
              description: 'Not Found. (shareId)'
          requestBody:
            required: false
            description: Always empty (OAS doesn't allow post without body, so optional body is defined here)
            content:
              application/json:
                schema: #empty request body
                  type: object
                  nullable: true
          tags:
            - cdoc2-key-shares
    
      '/session_nonce':
        post:
          summary: Generates session nonce
          description: |
            Returns a randomly generated nonce value and stores this value in the database for 24 hours
          tags:
            - cdoc2-key-shares
          operationId: generateSessionNonce
          responses:
            '200':
              description: Created
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/NonceResponse'
            '400':
              description: 'Bad request. Client error.'
            '403':
              description: 'Authentication failed'
          requestBody:
            required: false
            description: Always empty (OAS doesn't allow post without body, so optional body is defined here)
            content:
              application/json:
                schema: #empty request body
                  type: object
                  nullable: true
    
    components:
      schemas:
        KeyShare:
          title: Key Share
          type: object
          properties:
            share:
              type: string
              format: byte
              minLength: 32
              maxLength: 128
              description: |
                Base64 encoded Key Share. Binary format. 
    
            recipient:
              type: string
              minLength: 12
              maxLength: 32
              description: |
                Recipient who can download this share. ETSI319412-1. Example "etsi/PNOEE-48010010101". 
                Must match certificate subject serialnumber field (without "etsi/" prefix).
                In future might support other formats 
                [etsi/:semantics-identifier](https://github.com/SK-EID/smart-id-documentation/blob/v2/README.md#2322-etsisemantics-identifier)
          required:
            - share
            - recipient
    
        NonceResponse:
          title: Nonce response
          type: object
          properties:
            nonce:
              type: string
              minLength: 12
              maxLength: 16
              description: 'server nonce for subsequent authentication'
          required:
            - nonce
    
      parameters:
        SessionTokenHeader:
          name: x-cdoc2-session-token
          in: header
          required: true
          schema:
            type: string
          description: |
            SDJWT [Session token WIP](). Signed by cdoc2-auth-server using key identified by 
            'kid' in JWT header. Contains a MID/SID signature as part of the payload. 'aud' claim
            contains selectively-disclosed array element identifying a session nonce that is 
            checked by the server x-cdoc2-session-token is presented to.
    
        SessionX5cHeader:
          name: x-cdoc2-session-x5c
          in: header
          required: true
          schema:
            type: string
          description: |
            PEM encoded X509 certificate (without newlines) that was used to 
            generate the MID/SID signature in x-cdoc2-session-token payload. 
            Certificate holder's identity is specified in Subject "serialnumber" field. Example certificate subject: 
            'serialNumber = PNOEE-30303039914, GN = OK, SN = TESTNUMBER, CN = "TESTNUMBER,OK", C = EE'
            Certificate full structure is defined in 
            [Certificate and OCSP Profile for Smart-ID](https://www.skidsolutions.eu/wp-content/uploads/2024/10/SK-CPR-SMART-ID-EN-v4_7-20241127.pdf)
    
        SidRpV3SignatureParams:
          name: x-cdoc2-sid-rpv3-signature-parameters
          in: header
          required: false
          schema:
            type: string
          description: |
            Base64Url-encoded JSON structure containing additional parameters necessary to verify the
            signature of an auth token (x-cdoc2-auth-token). Required when the auth token is signed 
            with SID RPv3, omitted otherwise.
          example: '{
      "interactionsDigest": "olJN7OXUvfy1bUPNu712X3A7MOm1BXiWtlAmv+ubIz0=",
      "interactionTypeUsed": "confirmationMessageAndVerificationCodeChoice",
      "signature": {
        "serverRandom": "sV9wlKtZe5tr0gN9ietPSJ/T",
        "userChallenge": "fykZLrfSkl1on1pHNPkdAYQ-izGt7VFyczyCC3lxrik",
        "flowType": "Notification",
        "signatureAlgorithm": "rsassa-pss",
        "signatureAlgorithmParameters": {
          "hashAlgorithm": "SHA-256",
          "maskGenAlgorithm": {
            "algorithm": "id-mgf1",
            "parameters": {
              "hashAlgorithm": "SHA-256"
            }
          },
          "saltLength": 32,
          "trailerField": "0xbc"
        }
      }
    }'
    
      securitySchemes:
        bearerAuth: # for /key-shares endpoints, long-term token
          type: http
          scheme: bearer
        basicAuth: # temporary solution for initial functionality of /key-shares endpoints
          type: http
          scheme: basic
    
    tags:
      - name: cdoc2-key-shares
