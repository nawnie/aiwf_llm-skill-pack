# UI Routing

Use this reference when the user asks for Gradio, React, frontend, tabs, controls, defaults, API-visible UI behavior, or UX research that may feed UI/product decisions.

## Stock Skills

- `hugging-face:huggingface-gradio`: Gradio tab/callback/component work.
- `build-web-apps:react-best-practices`: React/TypeScript frontend work.
- `aiwf-avoid-ai-design`: AI-looking design cleanup for Gradio, React/web, dashboards, PDFs, and document layouts, including teal-everywhere and generic generated-layout complaints.
- `product-design:research`: current user pain, UX friction, onboarding, docs/help, support pain, or product complaints for a named product.
- `local-ai-dev`: backend API and local app integration.
- `avoid-ai-writing`: required for UI copy written to non-gitignored files.

## AIWF UI Split

- Gradio/Python UI lives under `aiwf/web/`.
- React frontend lives under `frontend/`.
- Do not add to React when the user says pipeline/engine-only or "no React."
- It is acceptable to update Gradio defaults when the backend default would otherwise point at missing or unsafe model assets.
- Product research needs a named product, audience or likely audience, time horizon, and source scope. If those are missing, ask before scanning.

## AIWF Files To Inspect First

- `aiwf/web/tabs/`
- `aiwf/web/app.py`
- `aiwf/web/pro_api.py`
- `frontend/src/`

## Guardrails

- Keep defaults aligned with validated pipeline/service defaults.
- Use `aiwf-avoid-ai-design` when the UI or document complaint is about visual AI tells, default themes, teal-heavy styling, generic cards, or generated-looking layout.
- Audit new UI copy, labels, empty states, helper text, and docs with `avoid-ai-writing` when written to non-gitignored files.
- Avoid UI expansion before engine and no-GUI smoke validation.
- Prefer page-level obvious controls for persistent settings.
