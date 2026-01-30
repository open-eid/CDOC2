# Appendix C: Key Capsules API, version 2.1.0 of cdoc2services API

    openapi: 3.0.3
    info:
      contact:
        url: http://ria.ee
      title: cdoc2-key-capsules
      version: 3.0.1
      description: API for exchanging CDOC2 ephemeral key material in key capsules
    servers:
      - url: 'https://cdoc2.id.ee:8443'
        description: no auth (for creating key capsules). Regular TLS (no mutual TLS required).
      - url: 'https://cdoc2.id.ee:8444'
        description: mutual TLS authentication (for retrieving key capsules)

    paths:
      '/key-capsules/{transactionId}':
        get:
          summary: Get key capsule for transactionId
          description: Get key capsule for transactionId
          tags:
            - cdoc2-key-capsules
          parameters:
            - name: transactionId
              in: path
              schema:
                type: string
                minLength: 18
                maxLength: 34
              required: true
              description: transaction id from recipients.KeyServerCapsule.transaction_id (fbs)
          responses:
            '200':
              description: OK
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/Capsule'
              headers:
                x-expiry-time:
                  schema:
                    type: string
                    format: date-time
                  description: Key capsule may be deleted by server after expiry time. Format rfc3339#section-5.6
            '400':
              description: 'Bad request. Client error.'
            '401':
              description: 'Unauthorized. Client certificate was not presented with the request.'
            '404':
              description: 'Not Found. 404 is also returned, when recipient id in record does not match with public key in client certificate.'
          operationId: getCapsuleByTransactionId
          security:
            - mutualTLS: []

      /key-capsules:
        post:
          summary: Add Key Capsule
          description: Save Capsule and generate transaction id using secure random. Generated transactionId is returned in Location header
          operationId: createCapsule
          parameters:
            - schema:
                type: string
                format: date-time
              in: header
              name: x-expiry-time
              description: Expiry time requested (capsule may be deleted after expiry-time). Format rfc3339#section-5.6
              required: false
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Capsule'
          responses:
            '201':
              description: Created
              headers:
                Location:
                  schema:
                    type: string
                    example: /key-capsules/KC0123456789ABCDEF
                  description: 'URI of created resource. TransactionId can be extracted from URI as it follows pattern /key-capsules/{transactionId}'
              x-expiry-time:
                description: >
                  Actual expiry time applied by the server. Format [RFC 3339 §5.6](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6)
                schema:
                  type: string
                  format: date-time
                  example: '2025-12-31T23:59:59Z'
              x-expiry-time-adjusted:
                description: >
                  Optional. Indicates whether the requested expiry time was adjusted to match the server's maximum limit.  
                  `true` means the server applied a shorter expiry than requested.
                schema:
                  type: boolean
                  example: true
            '400':
              description: Bad request. Client error.
          security: []
          tags:
            - cdoc2-key-capsules

    components:
      schemas:
        Capsule:
          title: Capsule
          type: object
          properties:
            recipient_id:
              type: string
              format: byte
              minLength: 65 # EC public key
              maxLength: 2100 # 16 K RSA public key = 2086 bytes
              description: 'Binary format is defined by capsule_type'
            ephemeral_key_material:
              type: string
              format: byte
              maxLength: 2100
              description: 'Binary format is defined by capsule_type'
            capsule_type:
              type: string
              enum:
                - ecc_secp384r1
                - ecc_secp256r1
                - rsa
              description: |
                Depending on capsule type, Capsule fields have the following contents:
                 - ecc_secp384r1:
                      * recipient_id is EC pub key with secp384r1 curve in TLS format (0x04 + X coord 48 bytes + Y coord 48 bytes) (https://www.rfc-editor.org/rfc/rfc8446#section-4.2.8.2)
                      * ephemeral_key_material contains sender public EC key (generated) in TLS format.
                - ecc_secp256r1:
                      * recipient_id is EC pub key with secp256r1 curve in TLS format (0x04 + X coord 32 bytes + Y coord 32 bytes) (https://www.rfc-editor.org/rfc/rfc8446#section-4.2.8.2)
                      * ephemeral_key_material contains sender public EC key (generated) in TLS format.
                 - rsa:
                      * recipient_id is DER encoded RSA recipient public key - RsaPublicKey encoding [RFC8017 RSA Public Key Syntax A.1.1](https://www.rfc-editor.org/rfc/rfc8017#page-54)
                      * ephemeral_key_material contains KEK encrypted with recipient public RSA key
            
                This is a extensible enum — servers may add values. Clients MUST tolerate unknown values.
              x-extensible-enum: true
          required:
            - recipient_id
            - ephemeral_key_material
            - capsule_type
      securitySchemes:
        mutualTLS:
          # since mutualTLS is not supported by OAS 3.0.x, then define it as http basic auth. MutualTLS must be implemented
          # manually anyway
          #type: mutualTLS
          type: http
          scheme: basic
    tags:
      - name: cdoc2-key-capsules
