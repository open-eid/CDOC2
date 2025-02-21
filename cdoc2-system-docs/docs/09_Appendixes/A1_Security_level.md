---
title: Appendix 1 - CDOC2 security level
---

# Appendix 1 - Security level of password-based encryption/decryption in CDOC2

## General regulatory requirements

Government-issued documents contain some guidance about the required security level. For example, NIST SP 800-57 Part 1, Revision 5 recommends that systems should use at least 128-bit security level and this is adequate for 2031 and beyond (NIST SP 800-57 Part 1, page 59, Table 4). This is applicable, when choosing encryption/decryption algorithms and protocols and in CDOC2 system, AES-128 and similar algorithms are in use.

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

Taking into account the NIST recommendation and based on tests on general purpose CPU (Apple M2 3.49 GHz), it takes around 1-2 seconds to run PBKDF2 algorithm with 10,000,000 ($1 \cdot 10^7$) iterations. This seems to be a reasonable performance tradeoff.

## Modeling attacker capabilities

When we consider brute-force exhaustive password search attack against CDOC2 Container, we have to somehow model the capabilities of the attacker. It is especially difficult, because we have to consider a long crypto-period. Attacker may store the captured CDOC2 Container and launch the attack after powerful computers have emerged, or execute the attack for a very long period of time, perhaps over multiple years.

"Bovine RC5 effort" (<https://www.distributed.net/RC5>) is one of examples of highly parallel exhaustive key searches performed in 2002. They were able to find 64-bit encryption key for RC5 ciphertext within 1,757 days, by using computers of 331,252 individuals. Massive parallel exhaustive search is therefore certainly within capabilities of attackers as well.

There are no guidelines for estimating, how many CPU cores an attacker might be able to use. We could use an estimate for an upper bound, by considering number of CPU cores in the world. ARM company has estimated that all their partners combined, have shipped more than 25 billion ($\approx 2.5 \cdot 10^{10}$) chips in year 2020 (<https://newsroom.arm.com/news/arm-partners-are-shipping-more-than-900-arm-based-chips-per-second-based-on-latest-results>). We could assume that all of those chips are controlled by a single attacker and all of those chips are capable of doing a PBKDF2 operation with $1 \cdot 10^7$ iterations in one second. Then we could have our upper bound for a very powerful attacker, which is $\approx 7.8 \cdot 10^{17}$ password tries per year.

Another option is to use estimation of Bitcoin Hash Rate. At September 2024, it is estimated that performance of the whole Bitcoin mining network is about 700 exahash per second ($\approx 7 \cdot 10^{18}$) (<https://www.bitcoinmagazinepro.com/blog/what-is-bitcoin-hash-rate-a-complete-guide-to-mining-power/>). Assuming that whole network is controlled by a single very powerful attacker, then this attacker may be able to do $\approx 2.2 \cdot 10^{19}$ PBKDF2 password tries per year.

## CDOC2 password length requirements

One example of practical passwords, which are considered secure, are Apple's "Automatic strong passwords" (<https://support.apple.com/en-gb/guide/security/secc84c811c4/web>). They are 20 characters long, contain one digit, one uppercase, two hyphens and 16 lowercase characters. Such generated passwords contain 71 bits of entropy.

If CDOC2 system would enforce using similar passwords and would use PBKDF2 with $1 \cdot 10^7$ iterations, it would mean that a hypothetical attacker possessing every ARM processor manufactured, could try out all password combinations ( $2^{71} \approx 2.3 \cdot 10^{21}$ ) within

$$ \frac{2.3 \cdot 10^{21}}{7.8 \cdot 10^{17}} \approx 3000 $$ years.

Another hypothetical attacker controlling the whole Bitcoin mining network, could try out all password combinations within

$$ \frac{2.3 \cdot 10^{21}}{2.2 \cdot 10^{19}} \approx 104 $$ years.

Taking into account that we modeled our upper bound for our attacker, these kinds of 71-bit entropy passwords should provide us multiple orders of magnitude for a security margin.
