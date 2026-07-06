# Security Checklist

Use this checklist when code touches trust boundaries.

## Inputs

- Validate user-controlled strings, paths, filenames, URLs, JSON, YAML, archives, and uploaded files.
- Normalize and bound paths before file reads, writes, extraction, or deletion.
- Set size and type limits for uploads and generated artifacts.
- Treat model, dataset, LoRA, extension, and script downloads as untrusted until provenance is checked.

## Execution

- Avoid `eval`, `exec`, untrusted `pickle.load`, unsafe `yaml.load`, and dynamic imports from user-controlled paths.
- Prefer subprocess argument arrays over shell strings.
- Avoid `shell=True` unless the command is fixed, local, and justified.
- Keep install scripts and post-install hooks out of automatic flows unless explicitly requested.

## Web/API

- Keep auth and authorization checks server-side.
- Do not rely on frontend gating for real permissions.
- Do not broaden CORS for production without a specific origin plan.
- Keep error responses useful but not secret-revealing.
- Check SSRF risk before fetching user-provided URLs.
- Check CSRF/session implications when adding browser-authenticated mutation routes.

## Secrets

- Do not log API keys, tokens, cookies, Authorization headers, private paths, or signed URLs.
- Do not put secrets into frontend bundles, committed config, receipts, screenshots, or public docs.
- Prefer env vars or the repo's existing secret manager pattern.

## Dependencies And Artifacts

- Prefer pinned versions, lockfiles, hashes, or immutable revisions where practical.
- Check license/provenance for models and datasets when the artifact may be redistributed.
- Do not silently replace lockfiles or dependency managers.
- Record any skipped security validation as a residual risk.
