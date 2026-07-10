---
name: aiwf-security-guardrails
description: Use as the security threat-triage and evidence guardrail for code, services, devices, data, dependencies, AI artifacts, incidents, and deployments. Select the smallest focused security skill after identifying assets, actors, trust boundaries, authorization, impact, and required approval gates.
---

# AIWF Security Guardrails

Use this skill to classify security work, establish authorization and evidence quality, and select focused owners. It is not a penetration-test authorization or a claim that a system is secure.

## Workflow

1. Define authorized scope, owner, assets, actors, trust boundaries, data flows, realistic harm, and whether the task is review, hardening, testing, or incident response.
2. Separate observed evidence, sourced facts, assumptions, and unknowns. Do not invent exploitability, severity, compliance, or a CVSS score.
3. Select no more than two focused security skills so a repository or domain owner still fits under the four-skill route cap.
4. Identify approval gates before scanning, publishing exposure, changing access/security controls, rotating credentials, deleting/quarantining files, or containing an incident.
5. Patch narrowly, preserve recovery, run negative and regression checks, and record residual risk.

Read `references/security-checklist.md` for the common control pass and `references/source-register.json` for framework status. Create a structured assessment with `python scripts/create_security_assessment.py --output <assessment.json> --title <title> --owner <owner> --scope <scope>`.

## Focused Owners

- `aiwf-application-api-security`: application, API, browser, auth, input, webhook, and LLM-tool boundaries.
- `aiwf-online-infrastructure-security`: internet exposure, DNS/TLS, IAM, cloud/VPS, containers, ports, and monitoring.
- `aiwf-local-device-security`: Windows/device controls, credentials, encryption, services, removable media, and local files.
- `aiwf-data-privacy-protection`: data inventories, minimization, access, retention, deletion, vendors, and audit evidence.
- `aiwf-software-ai-supply-chain-security`: dependencies, builds, releases, models, datasets, binaries, SBOMs, and provenance.
- `aiwf-incident-response-recovery`: suspected compromise, evidence, containment, recovery, and notification gates.

## Hard Stops

Stop and ask before:

- scanning a network or account without exact authorized targets
- exposing a service beyond localhost
- weakening auth, permissions, TLS, CORS, CSRF, or origin checks
- printing or moving secrets
- accepting unsigned or untrusted model, dataset, extension, or script downloads
- adding `shell=True`, `eval`, `exec`, unsafe `yaml.load`, or untrusted `pickle.load`
- changing firewall, credential, CI secret, production DB, device, or deployment permissions
- isolating a host, quarantining/deleting evidence, restoring a backup, or issuing breach notifications

## Required Checks

For security work, report:

- boundary checked
- risky inputs or outputs
- auth/permission impact
- secret handling impact
- validation run or not run
- evidence and confidence
- focused owner selected
- remaining risk and recheck date

For AI model and dataset work, include source trust, license or provenance signal when available, hash or immutable revision when practical, and whether the artifact is executed, loaded, or only stored.
