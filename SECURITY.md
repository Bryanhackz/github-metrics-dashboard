# Security Policy

## Supported Versions
Currently, only the latest `main` branch is supported.

## Scope
This application acts as a proxy to the GitHub API. The primary security focus is on preventing Server-Side Request Forgery (SSRF) by validating the requested repository format, protecting API tokens, and mitigating rate-limit exhaustion via SQLite caching.

## Reporting a Vulnerability
Please do not report security vulnerabilities through public GitHub issues. Send an email to **br4yangil006@gmail.com**. You should receive a response within 48 hours.

Please include:
- Type of issue (e.g., SSRF, token leakage, cache poisoning)
- Full paths of source file(s) related to the issue
- Step-by-step instructions to reproduce the issue
- Impact of the issue
