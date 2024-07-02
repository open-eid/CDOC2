---
title: Appendix 2 - Integration with Password Managers
---

# Appendix 2 - Integration with Password Managers

## Intro

Users regularly use passwords managers, either embedded into the browsers or separate applications, to manage and protect passwords that they need to enter into various web pages or applications. When CDOC2 System implements password-based encryption schemes, it becomes interesting question, if and how passwords managers could be used to simplify some of tasks, such as password generation, storing, and password entering.

## Password managers

This analysis covers following types of password managers.

Operating system integrated password managers:

  1. Windows Credential Manager (<https://support.microsoft.com/en-us/windows/accessing-credential-manager-1b5c916a-6a16-889f-8581-fc16e8165ac0>)
  1. MacOS/IOS KeyChain with iCloud KeyCloud syncing and backup service (<https://support.apple.com/en-us/109016>)

Browser integrated password managers:

  1. Google Password Manager for Chrome (<https://passwords.google.com/>)
  1. Mozilla Password Manager for Firefox (<https://www.mozilla.org/en-US/firefox/features/password-manager/>)

Third party (commercial) applications and services:

1. Bitwarden (<https://bitwarden.com>)
2. 1Password (<https://1password.com>)
3. LastPass (<https://lastpass.com>)

Open-source password managers:

1. KeePassXC (<https://keepassxc.org>)

## No security assessment

Current analysis only looks at integration possibilities, from simply technical viewpoint, and doesn't assess the quality or trustworthiness of particular passwords managers in any other way. For example, there's no assessment, how specific password manager application stores passwords in a local database, whether they are encrypted with some sort of master password or not.

Also, whether user should trust a commercial cloud-based password manager or synchronization services or any other software, depends on the attack model and risk tolerance of the particular user.

## Overview of integration possibilities

### Manual copy-paste

The most basic level of integration possibility is that user does perform all tasks manually by using clipboard function for copy-pasting passwords between CDOC2 Client application and password manager. This has added benefit that password manager could be both native application or website. Downside is the additional work that user needs to do.

### Hot-key-based auto-fill

KeePassXC has interesting integration option called "Auto-Type" (<https://keepassxc.org/docs/KeePassXC_UserGuide#_auto_type>). It works this way that KeePassXC application listens for a unique hot-key combination and then depending on the title of the application in focus ("Notepad", "DigiDoc4 Client"), KeePassXC searches for a matching password entry and sends a configurable sequence (for example, "username", TAB, "password", ENTER) to that application. Optionally, user can preview and confirm this action, before KeePassXC actually sends passwords to other windows.

Actual usage of this feature is not so simple, because window titles tend to include the opened filename as well, and KeePassXC doesn't support regular expressions. However, this might be something to keep in mind.

### CLI-based programmatic integration

Some password managers also offer separate CLI application, which could be invoked from shell scripts and could be used to integrate password manager services into various places, for example, CI/CD actions.

#### List of CLI applications

| Password Manager           | CLI application name| References                           |
| -------------------------- | ------------------- | ------------------------------------ |
| Windows Credential Manager | `cmdkey.exe`<br>`vaultcmd.exe` | [Windows Server manual page for `cmdkey`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmdkey) <br> [Hacker recipes - Windows Credential Manager](https://www.thehacker.recipes/a-d/movement/credentials/dumping/windows-credential-manager)|
| MacOS/IOS KeyChain         | `security`          | [Blog post with examples](https://blog.koehntopp.info/2017/01/26/command-line-access-to-the-mac-keychain.html), <br>[man page for `security`](https://www.unix.com/man-page/osx/1/security/) |
| Google Password Manager    | no official options | |
| Mozilla Password Manager   | no official options | |
| Bitwarden                  | `bw`                | <https://bitwarden.com/help/cli/> |
| 1Password                  | `op`                | <https://developer.1password.com/docs/cli> |
| LastPass                   | `lastpass-cli`      | <https://github.com/lastpass/lastpass-cli> |
| KeePassXC                  | `keepassxc-cli`     | [Section in User Manual](https://keepassxc.org/docs/KeePassXC_UserGuide#_command_line_tool), <br>[man page for `keepassxc-cli`](https://github.com/keepassxreboot/keepassxc/blob/develop/docs/man/keepassxc-cli.1.adoc) |

#### CLI API methods

All CLI application offer adequate collection of methods for shell script integration, such as adding new password entries, searching, reading password entries, and deleting password entries.

#### Access authentication

When another application runs the CLI application and asks for an access to stored password entry inside password manager database, the access call must be somehow authenticated, to make sure that potentially malicious applications, which are running under the privileges of the same user, cannot have access to passwords.

There are following authentication options:

1. Password-based authentication, where you supply your username and password to CDOC2 Client application. Essentially, Client application gains the same privileges as the original user.
2. "API key"-style authentication, where you create an independent software token and supply this to CDOC2 Client application.
3. MacOS KeyChain supports application name-based authentication, where you specify the path to the application binary, which is requesting access.

#### Fine-grained authorization

In case user has other passwords in the password manager database, in addition to passwords of various CDOC2 Containers, the question of allowing access to only a subset of password becomes important. It could be solved with following options:

1. Only store passwords for CDOC2 Containers in that particular password manager, which is integrated with CDOC2 Client application.
2. Create a separate "vault" or "collection of passwords", in case password manager supports this, and only allow CDOC2 Client application access to this particular "vault".
3. Add fine-grained ACLs to each password entry.

### Programmatic or REST API integration

#### List of APIs

| Password Manager           | API references                           |
| -------------------------- | ---------------------------------------- |
| Windows Credential Manager | [Win32 API WinCred.h](https://learn.microsoft.com/en-us/windows/win32/api/wincred/) |
| MacOS/IOS KeyChain         | [KeyChain Services](https://developer.apple.com/documentation/security/keychain_services), [Keychain items](https://developer.apple.com/documentation/security/keychain_services/keychain_items), [TN3137: On Mac keychain APIs and implementations](https://developer.apple.com/documentation/technotes/tn3137-on-mac-keychains) |
| Bitwarden                  | [Vault Management REST API](https://bitwarden.com/help/vault-management-api/) |
| 1Password                  | [1Password Connect REST API](https://developer.1password.com/docs/connect) |
| KeePassXC                  | [Linux FreeDesktop Secret Service API](https://specifications.freedesktop.org/secret-service/latest/) |

## Summary

This analysis reviewed how popular password managers on MacOS and Microsoft Windows operating systems could be integrated with the CODC2 Client Application. There is not a clearly superior integration option suitable for all users. CLI-based integration options could be superior for organizations who integrate container encryption into their information systems or other workflows. However, access authorization and having the authorization be fine-grained become important decisions which probably each organization has to tackle individually as it depends on the choice of password managers and information security policies. The manual copy-paste solution is probably the most realistic option for individuals who use the Client Application less frequently and not as part of an information system workflow and should problably be the suggested method.
