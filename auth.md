
## blah


Old protocol

JWT protocol

SD-JWT protocol

SD-JWT without holder binding?

Structure:

```json
{
    "iss": "etsi/PNOEE-48010010101",
    "capsule_access_data": [
        {   
            "serverURL": "https://cdoc.ria.ee:443/capsules",
            "capsuleID": "9EE90F2D-D946-4D54-9C3D-F4C68F7FFAE3",
            "serverNonce": "59b314d4815f21f73a0b9168cecbd5773cc694b6"
        },
        {
            "serverURL": "https://cdoc.smit.ee:443/capsules",
            "capsuleID": "5BAE4603-C33C-4425-B301-125F2ACF9B1E",
            "serverNonce": "9d23660840b427f405009d970d269770417bc769"
        }
    ]
}
```

This is the JWT, that is issued (signed) by user. Later, we will disclose only those elements of the `capsule_access_data` array to capsule servers, which are necessary.



