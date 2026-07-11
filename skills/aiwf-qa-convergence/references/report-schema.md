# QA Convergence Schemas

Keep the manifest stable during a qualifying streak. If coverage must change, update it and let the helper reset the streak.

## Manifest

Paths are relative to `root`. Declare source, tests, configuration, and dependency files whose changes invalidate prior passes. Do not include generated QA receipts or build output in `source_paths`.

```json
{
  "schema_version": 1,
  "target": "android-editor",
  "source_paths": [
    "app/src",
    "engine",
    "build.gradle.kts",
    "gradle/libs.versions.toml"
  ],
  "required_gates": [
    {"name": "unit", "command": ".\\gradlew.bat testDebugUnitTest"},
    {"name": "build", "command": ".\\gradlew.bat :app:assembleDebug"}
  ],
  "runtime_flows": [
    "fresh install and launch",
    "select, mask, erase, preview, and export"
  ],
  "evidence_root": "qa/evidence"
}
```

## Pass Report

`progress` means the pass produced a useful diff, new evidence, a newly passing gate, or a smaller blocking set. `attempted_fixes` lists issue fingerprints addressed since the prior pass.

```json
{
  "schema_version": 1,
  "lens": "device-runtime",
  "progress": true,
  "gates": [
    {"name": "unit", "passed": true, "evidence": "qa/evidence/pass-02-unit.txt"},
    {"name": "erase-smoke", "passed": true, "evidence": "qa/evidence/pass-02-erase.png"}
  ],
  "findings": [
    {
      "fingerprint": "git:line-ending:PreviewDecoder.kt",
      "severity": "info",
      "status": "accepted",
      "reason": "Repository line-ending policy does not affect the build or runtime."
    }
  ],
  "attempted_fixes": ["android:Bitmap.setPixels:erase-preview"],
  "blocked": false,
  "aborted": false,
  "note": "Fresh install exercised the repaired erase path."
}
```

Allowed finding severities are `critical`, `high`, `medium`, `low`, and `info`. Allowed finding states are `open`, `accepted`, and `fixed`. Only low or informational findings may be accepted, and each accepted finding needs a concrete reason.

Set `blocked` only for an external dependency or decision that prevents the manifest from running. Set `aborted` only when continuing would violate an authorization, safety, destructive-action, or data boundary.
