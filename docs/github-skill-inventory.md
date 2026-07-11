# Public Skill Inventory Review

Updated: 2026-07-10

The public package vendors only Shawn-owned `aiwf-` skills. External GitHub skills may inform implementation when their license and provenance are verified, but their files, branding, and licenses are not copied into this pack.

## Current Result

- 57 source skills match `manifest.json` exactly.
- One implicit router selects up to four focused downstream skills.
- Every Shawn-authored browser label begins with `aiwf_`; canonical Agent Skills IDs remain valid `aiwf-` hyphen-case.
- Thirteen `#techstartup` instruction modules cover growth, funding, platforms, security, privacy, incidents, and multi-agent coordination.
- All skill-owned Python helpers are bundled and path-portable.
- Overlapping umbrella instructions were consolidated into focused owners.
- The README four-column catalog lists every skill exactly once and is validator-enforced.

## Reuse Rule

Before borrowing from a public skill:

1. Verify the repository, current commit, license, and relevant source file.
2. Prefer a link or attribution over vendoring.
3. Reimplement only the small behavior needed for Shawn's projects.
4. Keep third-party names out of Shawn-owned frontmatter and plugin branding.
5. Run `python .\scripts\validate_pack.py` before export.

The canonical current inventory is `manifest.json`; this note is not a second manifest.
