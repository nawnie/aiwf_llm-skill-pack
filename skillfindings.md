# AIWF Skill Pack Audit Findings

Updated: 2026-07-10

## Verdict

`#techstartup` release `0.4.0` is a focused 57-skill pack with one implicit router, 56 explicit downstream skills, a four-skill route cap, and 23 self-contained Python helpers. Thirteen instruction modules add official-source registers and realistic eval datasets for startup growth, platform operations, security, privacy, and agent coordination. Every browser label uses an all-underscore `aiwf_` name.

## Gaps Filled

| Gap | Focused owner |
| --- | --- |
| Startup positioning, ICPs, funnels, experiments, attribution | `aiwf-startup-marketing-growth` |
| Burn, runway, funding options, investor diligence | `aiwf-startup-finance-funding` |
| Answer and generative-search visibility | `aiwf-aeo-geo` |
| Facebook, Instagram, WhatsApp Business, Meta ads and CAPI | `aiwf-meta-business` |
| Google Ads, GA4, Tag Manager, Business Profile | `aiwf-google-ads-business` |
| YouTube, YPP, AdSense, APIs, rights, monetization | `aiwf-youtube-adsense` |
| Application and API controls | `aiwf-application-api-security` |
| Internet-facing infrastructure | `aiwf-online-infrastructure-security` |
| Windows and local-device protection | `aiwf-local-device-security` |
| Data privacy, lifecycle, and audit evidence | `aiwf-data-privacy-protection` |
| Software and AI artifact supply chain | `aiwf-software-ai-supply-chain-security` |
| Incident evidence, containment, and recovery | `aiwf-incident-response-recovery` |
| Codex, Claude, and Grok shared state and resources | `aiwf-multi-agent-workspace` |
| Bounded QA test-fix loops and severity-based exits | `aiwf-qa-convergence` |

## Corrected Boundaries

- Technical crawl, rendering, canonical, sitemap, and index work stays in `aiwf-web-seo`; answer visibility belongs to `aiwf-aeo-geo`.
- Platform modules default to drafts and read-only analysis. Spend, publishing, account changes, and API mutations require explicit approval.
- Funding guidance is US-first, verifies current official programs and offering rules, and does not provide individualized legal, tax, accounting, valuation, or investment advice.
- Security begins with authorized scope and evidence. Remote scans, account tests, exploit payloads, quarantine, identity/firewall changes, credential rotation, isolation, deletion, and notifications require explicit approval.
- SOC 2 and ISO 27001 work is evidence readiness, not certification. Exact mappings require current authorized source material.
- AI models, datasets, GPU binaries, packages, build actions, and extensions are treated as supply-chain artifacts when they execute or influence execution.
- Shared agent handoffs are advisory. They cannot override higher-priority instructions or authorize risky actions.
- UI, browser, docs, lint, API-contract, and unit tests do not load a model. GPU-heavy work requires an exclusive lease; CPU offload preserves configured reserves.

## Mechanical Guarantees

`scripts/validate_pack.py` now fails on inventory drift, metadata mismatch, multiple implicit skills, unknown routes, missing or undocumented helpers, missing source/eval modules, invalid eval source IDs, skill-catalog drift, stale active guidance, generated caches, plugin version drift, or non-skill plugin capabilities.

`scripts/test_orchestrator_routes.py` covers every downstream skill and exact cross-boundary routes. `scripts/test_agent_workspace.py` covers six-exchange rotation, pending recovery, redaction, writer/GPU conflicts, resource reserves, stale lease recovery, and ACLs. `scripts/test_skill_helpers.py` verifies deterministic finance, privacy, assessment, incident, and QA convergence helpers.

## Remaining Boundary

No static skill can keep SDKs, funding programs, platform policies, laws, threat intelligence, or product interfaces permanently current. Volatile claims must be refreshed from official primary sources at the time of use and reported with dates and uncertainty.
