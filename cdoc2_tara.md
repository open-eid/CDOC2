Tõnis Reimo: 
>kas keegi tuletaks mulle meelde:
>miks on idee teha eraldi autentimisprotokoll smart-id/mobiil-id krüpteermislahendusele parem kui kasutada juba olemasolevat TARA/GovSSO lahendust?


Meil on vaja eraldi autentimisprotokolli, et oleks võimalik ühe autentimisega (ühe PIN sisestamise) autentida mitme võtmeedastusserveri vastu. Samas on vaja takistada "replay-attack" tüüpi rünnakut, kus kompromiteerinud (CDOC2) serveril ei oleks võimalik saada ligipääsu teistesse (CDOC2) serveritesse. Serverid jagavad krüpteerimise võtmematerjali.


Aga Sinu küsimus panin mõtlema ja tegelikult saaks SID/MID CDOC2 krüpteerimise toe lahendada ka kasutades TARA autentimislahendust. Sellisel juhul saadetaks kasutaja CDOC2 dekrüpteerimiseks läbi brauseri (TARA) SID/MID ennast autentima.

CDOC2 klient peab endiselt iga serveriga suhtlema, aga CDOC2 kliendi moodustatud autentimis struktuur räsi allkirjastatakse TARA poolt. Vt protokolli kirjeldust all pool.

TARAga autentimisel oleksid eelised ja puudused võrreldes otse SID/MID RP API kasutamisega.

Puudused:
* Praeguses TARA versioonis allkirjastab _identsustõendi_ ^3 TARA. Seega on turvalisus viletsam kui
otse SID/MID proxy kaudu autentimisvõtmega allkirjastamine. Turvalisus oleks parem, kui TARA tagastaks
  _identsustõendis_ "dts" välja (Autentimisvahendi poolt moodustatud autentimissignatuur
  eraldatud signatuuriga JWS-vormingus.). Vt ^5 SPOF2.1 #5.1.8 
* OIDC protokoll on disainitud töötama brauseris. CDOC2 klientides (DigiDoc4, Mopp, cdoc2-ref-impl) 
  võib brauseriga suhtlemine mõningaid tehnilisi keerukusi põhjustada. Peaks olema siiski võimalik 
  lahendada, nt saab kasutada  OAuth 2.0 Device Authorization Grant (rfc8628)
* Kui TARA maha tõmmata (DDOS), siis ei saa ka CDOC2 dokumente dekrüpteerida.

Eelised:
* Autentimisvahenditega (SID/MID) jahmerdamised on TARA juba ära lahendanud. 
  Pole vaja SID/MID proxit täiendada.
* Saaja (dekrüpteerija) sertifikaadi kontroll on juba TARAs tehtud, pole vaja CDOC2 serveris 
 sertifikaati kontrollida (peab vaatama identy tokeni väljastamisaega)
* Lisana saab väikeste täindustena CDOC2 krüpteerimisvõimekuse kõigile TARA poolt toetatud 
  autentimisvahenditele (EU eID)

Küsimused Reimole:
* Kas RIAle sobib TARA kasutamine CDOC2le Smart-ID/Mobiil-ID teostamiseks? (Kuna praguses SID/MID proxy ei toeta authentication APIt, siis TARA kasutamisel ei ole SID/MID proxy täiendusi teha)
* Võib teha esimese variandi TARAga ja hiljem lisada otse SID/MID proxyde toe.


## CDOC2 TARA (draft)

Lihtsustatult:

* CDOC2 klient küsib igalt CDOC2 võtmeserverilt nonss väärtuse (nonce1, nonce2, nonce3)
* CDOC2  loob autentimis struktuuri ja arvutab sellest räsi - _hash(autentimis struktuur)_. Autentimis struktuur:
```  
  {
  "type": "CDOC2 authentication signature v0.1",
  "nonces": [
  {
  "transactionID": "transactionID1",
  "masked_nonce": "SHA-256(nonce1)"
  },
  {
  "transactionID": "transactionID2",
  "masked_nonce": "SHA-256(nonce2)"
  },
  {
  "transactionID": "transactionID3",
  "masked_nonce": "SHA-256(nonce3)"
  }
  ]
  }
```

* CDOC2 alustab OIDC authorize päringu (vt ^1 ja ^2). OIDC authorize päringu  parameetri 'nonce' väärtuseks on hash(autentimis struktuur) - /authorize?nonce=hash(autentimis struktuur)&teised_parameetrid.
* Peale TARA autentimisvoo läbimist saab CDOC2 klient TARA allkirjastatud identsustõendi (^3)
* CDOC2 klient koostab ja saadab igale võtmeserverile autentimispileti (_authentication_signature_value_ välja väärtus on TARA identsustõendi ^3):
```
{
    "type": "CDOC2 authentication ticket v0.1",
    "transaction": {
            "transactionID": "transactionID1",
            "nonce": "nonce1"
    },
    "masked_transactions": [
        {
            "transactionID": "transactionID2",
            "masked_nonce": "SHA-256(nonce2)"
        },
        {
            "transactionID": "transactionID3",
            "masked_nonce": "SHA-256(nonce3)"
        }
    ],
    "authentication_signature_type": "OIDC",
    "authentication_signature_value": "OIDC JWT ticket",
}
```
* Võtmeserver kontrollib, et _transaction.nonce_ väärtus on tema genereeritud. 
* Võtmeserver kontrollib _authentication_signature_type_ väljas sisalduva TARA poolt allkirjastatud identsustõendi allkirja.
* Võtmeserver kontrollib, et identsustõendi _nonce_ väärtus on _hash(autentimis struktuur)_

(Võtmeserveri kontrollid kirjutasin peast, multi-server-auth-protocol.md ^4 on need paremini lahti kirjutatud)


^1 [GovSSO authentication process](https://e-gov.github.io/GOVSSO/ArchivedPocTechnicalSpecification#authentication-process)
^2 [TARA autentimistõend](https://e-gov.github.io/TARA-Doku/TehnilineKirjeldus#41-autentimisp%C3%A4ring)
^3 [TARA identsustõend](https://e-gov.github.io/TARA-Doku/TehnilineKirjeldus#431-identsust%C3%B5end)
^4 [multi-server-auth-protocol](https://gitlab.cyber.ee/id/ee-ria/ria_tender_test_assignment_2023/-/blob/master/exercise-2.3-authentication-multi-server/multi-server-auth-protocol.md?ref_type=heads#autentimispiletite-kontrollimise-algoritm)
^5 SPOF2.1 - SPOF2.1 - autentimisprotokollistikud ver1.1 
