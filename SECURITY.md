# Security Policy

## Supported versions

Only the latest minor release of `ccxt-pandas` receives security fixes.

## Reporting a vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Use [GitHub's private vulnerability reporting](https://github.com/sigma-quantiphi/ccxt-pandas/security/advisories/new) to submit a report. You should receive an acknowledgment within 72 hours.

Please include:

- A description of the vulnerability
- Steps to reproduce
- The affected version(s)
- Any suggested mitigation

## Disclosure

We follow coordinated disclosure: once a fix is available, we will publish a GitHub security advisory and cut a patch release. Credit will be given to the reporter unless anonymity is requested.

## A note on API keys

`ccxt-pandas` is a thin pandas wrapper around CCXT. It never stores or transmits your exchange API keys; they live in the CCXT `Exchange` instance you pass in. Treat any leaked key as compromised — rotate it on the exchange and audit recent activity.
