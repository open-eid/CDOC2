## Components

![SID/MID](img/SID_MID_full.png)



### CDOC2 client

Software running on user (sender or receiver) that can create/decrypt documents in CDOC2 format. 

For encryption generates encryption/decryption key material and distributes it between CDOC2 multi-server 
instances. 

For decryption creates auth-ticket for key material download from multi-server instances. Uses 
Smart-ID/Mobile-ID `/authentication` endpoint to sign auth-ticket.  


### CDOC2 multi-server

Stores encryption/decryption key material. Provides endpoints for auth-ticket creation and 
key material upload/download. For SID/MID use cases key material is distributed
between CDOC2 multi-servers, so that compromising 1 doesn't expose key material. Instances run on 
independent premises.

### Smart-ID app

Enables to authenticate and sign using Smart-ID. Installed on user smartphone.


### portal.cdoc2.ee

Web service to generate CDOC2 server and RIA proxy authentication long-term tickets. Used to access
API only (Bearer-Auth HTTP header), not used for key-material retrieval. Uses TARA to authenticate
using E-ID.

### RIA SID/MID proxy

Usually SID/MID RP API is used from server side and requires authentication. 

RIA SID/MID proxy provides access to SID/MID API from authentication.