# Olemasoleva TARA/GovSSO lahenduse kasutamine süsteemis CDOC2

## Küsimus

Tõnis Reimo edastas järgmise küsimuse:

>kas keegi tuletaks mulle meelde:
>miks on idee teha eraldi autentimisprotokoll Smart-ID/Mobiil-ID krüpteerimislahendusele parem, kui kasutada juba olemasolevat TARA/GovSSO lahendust?

CDOC2-kliendi ja CDOC2-serverite vahele on vaja eraldi autentimisprotokolli, et oleks võimalik ühe autentimisega (ühe PIN sisestamisega) autentida mitme võtmeedastusserveri vastu. Samas on vaja takistada "replay-attack"-tüüpi rünnakut, kus kompromiteerinud CDOC2-serveril ei oleks võimalik saada ligipääsu teistesse CDOC2-serveritesse. Serverid jagavad konteineri dekrüpteerimise võtmematerjali.

Aga Sinu küsimus pani mõtlema ja tegelikult saaks krüpteerimissüsteemis CDOC2 lahendada MID/SID autentimisvahendite kasutamise kasutades ka autentimisteenust TARA.

Mustandkujul võiks see toimuda järgmiselt:

1. CDOC2 klient hangib CDOC2 serveritest allkirjastatavad serverite nonsside väärtused (`nonce1`, `nonce2`, `nonce3`), koostab allkirjastamisele mineva autentimisstruktuuri ja arvutab sellest räsi `hash(autentimisstruktuur)`.

```json
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

2. CDOC2 klient avab kasutaja arvutis brauseri koos TARA autentimislehega ning saadab sinna OIDC authorize päringu (vt [GovSSO authentication process][1] ja [TARA autentimispäring][2]). OIDC authorize päringu parameetri `nonce` väärtuseks on `hash(autentimisstruktuur)`.
3. Kasutaja viib TARA veebilehel autentimise läbi (ükskõik, millise autentimisvahendiga).
4. TARA tagastav autentimiskinnituse koos allkirjastatud identsustõendi `id_token` väärtusega, kuhu on lisatud kliendi poolt antud `nonce` väärtus. (vt [TARA identsustõend][3])
5. CDOC2 klient koostab igale CDOC2 serverile autentimispiletid (välja `authentication_signature_value` väärtusena kasutatakse TARA identsustõendit (vt [TARA identsustõend][3]):

```json
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

6. Senini kontrollis CDOC2 server kasutaja avaliku võtme vastavust võtmekapslis olevale avalikule võtmele, siis nüüd peab võtmekapslis olema kirjas selle saaja  isikukood ning CDOC2 server peab kontrollima struktuuris `id_token` oleva isikukoodi vastavust.

## Puudused

* Praeguses protokolli versioonis allkirjastab identsustõendi `id_token` TARA ise. Seega, kui TARA on ründaja poolt üle võetud, siis ründaja saab suvalise inimese nimel võtmeedastusserveritesse autentida ning kõik võtmekapslid alla laadida. Intuitiivselt tundub, et sellise lahenduse turvatase on madalam, võrreldes olukorraga, kus võtmekapsli laadimiseks on rangelt vajalik kasutaja autentimisvahendi moodustatud signatuur. Turvalisust saaks tõsta, kui TARA tagastaks _identsustõendis_ `id_token` ka välja `dts`. See võimalus on välja pakutud projekti SPOF2.1 aruande jaotises 5.1.8 ("Autentimisvahendi poolt moodustatud autentimissignatuur eraldatud signatuuriga JWS-vormingus").
* OIDC protokoll ning TARA autentimisleht on disainitud töötama brauseris. CDOC2 klientide (DigiDoc4, MOPP, cdoc2-ref-impl) ja brauseri suhtlemine võib olla tehniliselt keerukas. Loodame praegu, et seda on võimalik lahendada, nt kui kasutada standardis "OAuth 2.0 Device Authorization Grant" (RFC8628) kirjeldatud mustreid.
* Kui TARA ei tööta (näiteks teenusetõkestusründe tõttu), siis ei saa ka CDOC2 dokumente dekrüpteerida.

## Eelised

* Autentimisvahendite kasutamise tehnilised detailid (ID-kaardiga suhtlemine, Smart-ID RP-API kasutamine, vms) on kõik TARA poolt juba lahendatud ning seeläbi saab CDOC2 klient olla tehniliselt lihtsam, odavam ning tulevikukindlam.'
* Pole vaja SID/MID proksit täiendada, ega kasutada.
* Saaja (dekrüpteerija) sertifikaadi kehtivuse kontroll on juba TARAs tehtud, CDOC2 serverid ei pea seda uuesti tegema.
* CDOC2 dekrüpteerimisvõimekuse saab üsna lihtsalt lisada kõigile TARA poolt toetatud autentimisvahenditele (EU eID)

## Küsimused

* Kas RIA-le sobib kirjeldatud plaani kohaselt krüpteerimissüsteemis CDOC2 autentimisteenuse TARA kasutamine, kus TARA muutuks väga kriitiliseks komponendiks, mida tuleb täiel määral usaldada?
* Kas RIA plaanib autentimisteenust TARA täiendada, et lisada autentimissignatuuri edastamine ning seeläbi vähendada usaldusvajadust?

## Viited

* [1]: <https://e-gov.github.io/GOVSSO/ArchivedPocTechnicalSpecification#authentication-process> GovSSO authentication process
* [2]: <https://e-gov.github.io/TARA-Doku/TehnilineKirjeldus#41-autentimisp%C3%A4ring> TARA autentimispäring
* [3]: <https://e-gov.github.io/TARA-Doku/TehnilineKirjeldus#431-identsust%C3%B5end> TARA identsustõend
* [4]: <https://gitlab.cyber.ee/id/ee-ria/ria_tender_test_assignment_2023/-/blob/master/exercise-2.3-authentication-multi-server/multi-server-auth-protocol.md?ref_type=heads#autentimispiletite-kontrollimise-algoritm> multiserver auth protocol
* [5]: SPOF2.1 projekti aruanne versiooni 1.1
