---
name: aiwf-security-guardrails
description: AIWF security guardrail skill for code, model, dataset, dependency, service, and deployment work. Use when prompts mention security, auth, authorization, CORS, secrets, tokens, API keys, injection, unsafe deserialization, path traversal, uploads, SSRF, shell commands, dependency supply chain, model download trust, public network exposure, or vulnerability review.
---

# AIWF Security Guardrails

Use this skill to keep AIWF and local-AI code changes from creating avoidable security risk. It is a guardrail lane, not a replacement for a full penetration test.

## Workflow

1. Identify the security boundary before editing:
   - user input
   - file upload or archive extraction
   - model or dataset download
   - subprocess or shell call
   - API auth or permission check
   - local service bind address
   - frontend secret exposure
2. Inspect the repo-native pattern for auth, config, logging, validation, and error handling.
3. Block unsafe shortcuts unless Shawn explicitly accepts the risk.
4. Patch narrowly and preserve existing security architecture.
5. Validate with the narrowest relevant checks and record residual risk.

Read `references/security-checklist.md` when the task touches a security boundary or when the repo pattern is unclear.

## Hard Stops

Stop and ask before:

- exposing a service beyond localhost
- weakening auth, permissions, TLS, CORS, CSRF, or origin checks
- printing or moving secrets
- accepting unsigned or untrusted model, dataset, extension, or script downloads
- adding `shell=True`, `eval`, `exec`, unsafe `yaml.load`, or untrusted `pickle.load`
- changing firewall, credential, CI secret, production DB, or deployment permissions

## Required Checks

For security-related code changes, report:

- boundary checked
- risky inputs or outputs
- auth/permission impact
- secret handling impact
- validation run or not run
- remaining risk

For AI model and dataset work, include source trust, license or provenance signal when available, hash or revision pinning when practical, and whether the artifact is executed, loaded, or only stored.
