# Skill Authoring Policy

Use this policy when creating or changing skills in this pack.

## Portable Core

- Keep `SKILL.md` as the provider-neutral contract: trigger metadata, core workflow, guardrails, and when to load references.
- Keep the body concise. Move long source rules, provider details, examples, and checklists into `references/`.
- Use bundled `scripts/` for deterministic validation, routing, receipts, or repeated file checks.
- Bundle every referenced helper inside the owning skill. Use `<this-skill>` or a relative path; never depend on a hard-coded global skill path.
- Mention every bundled helper from `SKILL.md` or a linked reference so its purpose is discoverable and validated.
- Require receipts for research, dataset, validation, and publish workflows when claims need proof.

## Provider Adapters

- Put OpenAI-facing display metadata in `agents/openai.yaml`.
- Set `allow_implicit_invocation: true` only for `aiwf-orchestrator`; every downstream skill is explicit.
- Put provider-specific usage notes in references or scripts, not in the core workflow unless they change behavior.
- Prefer MCP/tools when a provider exposes stable tools or resources. Keep the portable fallback clear.
- Do not include secrets, account-specific URLs, local API keys, or private credentials in skill files.

## Pack Boundary

- Vendor Shawn-owned `aiwf-` skills only.
- Do not bundle outside skill folders, outside license files, or external branding.
- If a local installed skill is useful during development, treat it as an optional working tool, not pack source.

## Validation

Run these before committing skill-pack changes:

```powershell
.\scripts\validate_skills.ps1
python .\scripts\validate_pack.py
python .\scripts\test_orchestrator_routes.py
python "C:\Users\Shawn\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" .
git diff --check
```

For public prose, run the scan in `aiwf-avoid-ai-pushes` and fix only newly edited prose unless Shawn asks for a broader rewrite.
