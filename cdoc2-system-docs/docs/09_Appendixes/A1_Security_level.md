---
title: A1 - CDOC2 security level
---

# Security level of password-based encryption/decryption in CDOC2

## General regulatory requirements

Government-issued documents contain some guidance about the required security level. For example, NIST SP 800-57 Part 1, Revision 5 recommends that systems should use at least 128-bit security level and this is adequate for 2030 and beyond (TODO: exact reference). This is applicable, when choosing encryption/decryption algorithms and protocols and in CDOC2 system, AES-128 and similar algorithms are in use.

However, when it comes to password-based encryption/decryption, guidelines are not very good. For example, Section 8.1.5.3.8 of NIST SP 800-57 suggests that passwords should provide 128 bits of protection as well. If we would apply this, this would mean that users should use at least 21-character random passwords providing 128 bits of entropy. Also, NIST SP 800-57 doesn't take into account that trying out one password and trying out one AES key takes different amount of time.

German BSI document TR-02102-1 (<https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TG02102/BSI-TR-02102-1.pdf?__blob=publicationFile>) also gives similar guidance:

1. Section 6.3.1, Remark 6.4 (iii) - "In other situations where these conditions are not met (for example, when a cryptographic secret is directly derived from the password that provides access to sensitive information), it is recommended to choose passwords via a method that offers at least 120 bits of entropy"

There's another document SP 800-131 Part 1 - "Recommendation for Password-Based Key Derivation Part 1: Storage Applications", which applies specifically to our situation, but the recommendations are not very conclusive:

1. Annex A.1 - "For the security of electronically stored data, passwords should be strong enough so that it is infeasible for attackers to gain access by guessing the password"
2. Annex A.1 - "Passwords shorter than 10 characters are usually considered to be weak"
3. Annex A.1 - "Passphrases shorter than 20 characters are usually considered weak"

## PBKDF2 regulatory requirements

NIST SP 800-131 Part 1 gives following recommendation:

1. Annex A.2.2 - "The number of iterations should be set as high as can be tolerated for the environment, while maintaining acceptable performance."

German TR-02102-1 gives following recommendation (while suggesting to use Argon2id in place of PBKDF2)

1. Section B.1.3 - "The security parameters of Argon2id and the requirements for the passwords depend on the application scenario and should be discussed with an expert"

Taking into account the NIST recommendation and based on tests on general purpose CPU (Apple M2 3.49 GHz), it takes around 1-2 seconds to run PBKDF2 algorithm with 10,000,000 ($1 \cdot 10^7$) iterations. This seems to be reasonable performance tradeoff.

## Modeling attacker capabilities

When we consider brute-force exhaustive password search attack against CDOC2 Container, we have to somehow model the capabilities of the attacker. It is especially difficult, because we have to consider a long crypto-period. Attacker may store the captured CDOC2 Container and launch the attack after powerful computers have emerged, or execute the attack for longer period of time, like multiple years.

"Bovine RC5 effort" (<https://www.distributed.net/RC5>) is one of the examples of highly parallel exhaustive key searches performed in 2002. They were able to find 64-bit encryption key for RC5 ciphertext within 1,757 days, by using computers of 331,252 individuals. Massive parallel exhaustive search is therefore certainly within capabilities of attackers.

There are no guidelines for estimating, how many CPU cores an attacker might be able to use. We could use an estimate for the upper bound, by taking the number of CPU cores in the world. ARM company has estimated that all their partners combined, have shipped more than 25 billion ($\approx 2.5 \cdot 10^{10}$) chips in year 2020 (<https://newsroom.arm.com/news/arm-partners-are-shipping-more-than-900-arm-based-chips-per-second-based-on-latest-results>). We could assume that all of those chips are controlled by single attacker and all of those chips are capable of doing a PBKDF2 operation with $1 \cdot 10^7$ iterations in one second. Then we could have our upper bound for a very powerful attacker, which is $\approx 7.8 \cdot 10^{17}$ password tries per year.

TODO: Another way to validate this upper bound, is to compare this with bitcoin mining performance, because PBKDF2() operation is essentially doing SHA-256 hash computations. We could assume that attacker is controlling the whole bitcoin mining infrastructure and could arrive another upper bound.

## CDOC2 password length requirements

One example of practical passwords, which are considered secure, are Apple's "Automatic strong passwords" (<https://support.apple.com/en-gb/guide/security/secc84c811c4/web>). They are 20 characters long, contain one digit, one uppercase, two hyphens and 16 lowercase characters. Such generated passwords contain 71 bits of entropy.

If CDOC2 system would enforce using similar passwords and would use PBKDF2 with $1 \cdot 10^7$ iterations, it would mean that our hypothetical attacker could try out all combinations ( $2^{71} \approx 2.3 \cdot 10^{21}$ ) within

$$ \frac{2.3 \cdot 10^{21}}{7.8 \cdot 10^{17}} \approx 3000 $$

years. Taking into account that we modeled our upper bound for our attacker, these kinds of 71-bit entropy passwords should provide us multiple orders of magnitude for a security margin.

-------------------------------

# Notes down below

# CDOC2 security level

Plan:

1. There are no strict requirements for password length, when PBKDF2 is used for AES128 encryption keys.
2. But there are some heuristics-based guidelines.
   1. "In 2023, OWASP recommended to use 600,000 iterations for PBKDF2-HMAC-SHA256 and 210,000 for PBKDF2-HMAC-SHA512.[6]"
3. Also, when we use maximal reasonable iteration count, then we allow the attacker to have about 1 PBKDF2 try per second.
   1. Assuming that SHA-256 is safe
   2. Assuming in safety margin. 10 fold? million fold?
   3. Then we can let users use X-character passwords

Safety margin: 

https://crypto.stackexchange.com/questions/68672/origin-of-values-for-security-margin
https://eprint.iacr.org/2017/560.pdf
https://www.cryptopp.com/wiki/Security_Level

distributed.net was able to find RC5-64 key within 1,757 days. So, they broke 64-bit entropy password. They were able to do 2^64 = 18446744073709551616 = 10^19 tries.

10^19/(1757*24*60*60) = 10^10 tries per second

They used 331 000 individuals. Assuming that attackers nowadays are able to utilise every computer in the world. (https://newsroom.arm.com/news/arm-partners-are-shipping-more-than-900-arm-based-chips-per-second-based-on-latest-results)

70 million chips a day -> 2*10^10 chips per year.

Assuming that attacker is able to use all of such chips and is able to parallelise PBKDF computations.






## Password length

CDOC2 system security model is based on 128-bit security level (<https://en.wikipedia.org/wiki/Security_level>). For example, AES encryption implemented inside CDOC2 system uses 128-bit keys, which translates to 128-bit security level. There are lot of assumptions and estimations and safety margins included here, but the general consensus is that 128-bit security level provides adequate protection beyond 2030.

<https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf>

"SP 800-57, Part 1 also provides guidance about protecting information past 2030. Section 5.6.4 of that document advises selecting algorithms and key sizes that are expected to be secure for the entire security life of the protected data. This is particularly important when nearing algorithm transition dates. For example, if the data to be encrypted has a security life of 15 years, then protection at a security strength of 112 bits will not be sufficient, since the 15-year period extends beyond 2030."

Password length recommendations are based on the same assumption, that it shouldn't be easier to brute-force passwords used in the password-based encryption/decryption scheme (TODO: link to scheme).

TODO: However, brute-forcing a 128-bit AES key would take more energy and more time than lifetime of multiple universes (TODO: link) So, does it make sense to have this high bar?

Brute-forcing passwords is possible when attacker tries all possible password combinations.

Example: We know that user have to use a 20 character password, from the set of case sensitive alphanumeric (a–z, A–Z, 0–9) characters. This translates to roughly 5.9 bits per character. Times 20, gives 118 bits of entropy.

That means that attacker has to try out $2^118$ combinations. Which is too much anyway.

Is it ok, if we lower the bar to 100 years?

<https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-132.pdf>

"Passphrases shorter than 20 characters are usually considered weak."
"Passwords shorter than 10 characters are usually considered to be weak."

"iteration count of 10,000,000 may be appropriate."
"The number of iterations should be set as high as can be tolerated for the environment, while maintaining acceptable performance."

1 second for generation?

10 characters, capital, numbers, 5.9 bits of entropy per character.

$10*5.9 = 59$

$2^59 = 576460752303423488 = 5*10^17$

Age of universe is 13 billion years = 13 * 10^9 years * 365*24*60*60 =  4*10^17 seconds

$ (5*10^17) / (2*10^10) = 2.5*10^7 seconds

3.1*10^7 seconds in a year

So .. 10 character password with ~60 bits of entropy, with 1 second PBKDF iterations, could be found by utilising all ARM cores shipped within one year in a whole world, by running all of them for 1 year.

Fine, let's do 20 characters, like Apple offers, and lets use 71 bits of entropy.

$2^71 = 2361183241434822606848 = 2.3 * 10^21$

20 character password, with ~71 bits of entropy, could be found by utilising all ARM cores shipped within one year in a whole world, by running all of them for 3700 years.

$ (2.3 * 10^21) / (2*10^10) / (3.1*10^7) = 3700$ years.

This should be good, we have safety margin of 1000 times. Even if the attacker is able to do PBKDF thousand times quicker, it still takes them all the ARM cores and a year.

BSI Technical Guideline – Cryptographic Algorithms and Key Lengths

"In other situations where these conditions are not met (for example, when a cryptographic secret is directly derived from the password that provides access to sensitive information), it is recommended to choose passwords via a method that offers at least 120 bits of entropy."


https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TG02102/BSI-TR-02102-1.pdf?__blob=publicationFile

"9. SecretSharing"


https://www.theregister.com/2009/08/03/new_crypto_attack/


https://www.cyber.gov.au/resources-business-and-government/essential-cyber-security/ism/cyber-security-guidelines/guidelines-cryptography

