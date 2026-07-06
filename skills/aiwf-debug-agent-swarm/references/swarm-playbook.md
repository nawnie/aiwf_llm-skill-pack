# Swarm Playbook

Use this reference to turn a broad debugging request into a high-fanout but controlled set of subagent tasks.

## Lane Matrix

Start with the smallest set that covers the repo, then add lanes until every independent risk area has an owner.

| Lane | Agent | Scope | Output |
| --- | --- | --- | --- |
| Repro and symptom | explorer | Error text, logs, failing command, user-reported behavior | Minimal repro, suspected entry points, first failing boundary |
| Build and tests | explorer | Manifests, lockfiles, CI, test configs | Exact commands, broken scripts, likely dependency/config problems |
| Architecture map | explorer | App entry points, routing, service boundaries | Component map and high-risk integration points |
| Module crawl | explorer | One top-level directory or package per agent | Findings with file/line refs and local test ideas |
| State and config | explorer | Env loading, config files, persistence, caches | Missing defaults, bad paths, unsafe assumptions |
| Error handling | explorer | Exceptions, logging, retries, async boundaries | Unhandled failures, swallowed errors, bad user feedback |
| Data/model pipeline | explorer | Dataset loading, model calls, GPU/runtime paths | Shape/device/path failures, fallback gaps, heavy-run risks |
| UI workflow | explorer | Frontend state, routes, forms, loading/error states | User-visible regressions and repro steps |
| Test gap | explorer | Existing tests for touched modules | Missing coverage for likely bug classes |

For very large repos, create one module-crawl lane for each important top-level directory plus the cross-cutting lanes above. If the tool reaches a concurrency limit, keep the remaining lanes queued and spawn them after closing completed agents.

## Explorer Prompt Template

```text
You are one of many parallel debugging agents crawling this project. Do not modify files.

Project root: <absolute path>
Lane: <specific lane name>
Scope: <directories/files/questions>
Shared context: <bug report, failing command, inventory path, constraints>
Debug pass folder: <absolute path>

Find concrete debugging evidence in your lane only. Write your Markdown report to the debug pass folder. Include:
1. Top findings, ordered by severity, with file/line references.
2. Evidence, user-visible impact, and repro or verification commands if any.
3. Likely root cause hypotheses and confidence.
4. Research used, or why local evidence is at least 90/100 confidence.
5. What you did not inspect.

Avoid broad summaries. Do not duplicate other lanes. Do not explain the fix. Do not make changes unless the entire repair is a syntax fix of three changed lines or fewer, and record exact lines changed.
```

## Syntax Fix Prompt Add-On

```text
You may apply a simple syntax fix only if it changes three lines or fewer.
If you do, write the exact file, line numbers, and validation command in your debug-pass report.
Do not make broader behavioral changes.
```

## Parent Coordination Loop

1. Create a lane table before spawning:

```text
lane | agent type | scope | agent id | status | expected result
```

2. Spawn the first wave in parallel. Prefer broad read-only explorers; the parent agent implements repairs after reading reports.
3. While agents run, reproduce the issue locally or inspect a non-overlapping area.
4. Wait only when the next integration step needs results.
5. When a result arrives, update the lane table, extract actionable findings, and close the agent.
6. Spawn follow-up agents only for genuinely new questions or queued lanes.
7. Before editing, read every report, choose one fix plan, and check for file conflicts.
8. After parent edits, run the narrowest useful tests, then broaden tests if risk warrants.

## Finding Format

Use this format when merging results:

```text
[severity] title
file:line
Evidence:
Impact:
Fix detail omitted:
Verified by:
Source lane:
```

Severity order:

- Critical: data loss, security exposure, destructive action, production outage.
- High: crash, build break, common workflow unusable.
- Medium: incorrect behavior with workaround or limited scope.
- Low: maintainability, test gap, weak diagnostics.

## Good Swarm Shapes

- Many explorers, one parent integrator, then parent-owned fixes.
- One explorer per top-level module when the bug location is unknown.
- A final verifier explorer after patches, focused on changed files and regression risk.

## Bad Swarm Shapes

- Multiple agents asked to "debug the whole repo".
- Multiple agents editing the same files.
- Agents writing full patch recipes instead of issue evidence.
- Agents that only summarize README content.
- Follow-up agents spawned before existing results are read.
- Heavy test/model runs delegated without clear runtime limits or user approval.
