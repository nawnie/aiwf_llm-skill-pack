# Verification Checklist

Use this checklist when a plan or route needs a stricter review.

Default review policy:

- Run 4 passes by default for non-trivial work.
- After pass 4, continue only if the most recent pass found a material issue.
- Focus extra passes on the affected lane or cards.

## Task Fit

- Is the active route solving the user's actual request rather than an inferred substitute?
- Are constraints from the user, repository, and environment reflected in the relevant lanes and cards?
- Are any important assumptions still unstated?

## Evidence

- Has each active card's file path, dependency, tool, endpoint, or environment fact been checked?
- Are time-sensitive facts verified from current sources when required?
- Are decisions tied to concrete evidence instead of memory or habit?
- Has each tool result been interpreted before it is used as evidence?

## Tool Use

- Does the next tool call answer a real question in the active route?
- Can independent checks be run in parallel?
- Did a failed tool call trigger a fallback route instead of a dead end?
- Is state from tool output carried forward accurately?
- Are irreversible actions gated by confirmation or an explicit prior instruction?

## Project Fit

- Which files, modules, configs, tests, or interfaces does this route affect?
- Do those files reveal related changes that must happen together?
- Has every new variable, prop, type, schema field, env var, or config key been added everywhere it must exist?
- Are imports, exports, registrations, tests, and docs still consistent?
- Could the change break consumers outside the edited file?

## Safety

- Does the sequence avoid destructive actions until prerequisites are confirmed?
- Is there a rollback, backup, or bounded-blast-radius approach when relevant?
- Are unrelated user changes protected from accidental overwrite?

## Correctness

- Does each active card have a visible success condition?
- Is there a validation step after every meaningful edit or command?
- Would the route still work if the first hypothesis is wrong?
- Does the project still fit together after the proposed edits, not just the touched file?

## Efficiency

- Can the task be solved with fewer steps or less risk?
- Can uncertain steps be converted into quick inspections or experiments?
- Is the map proportional to the size of the task?
- Are unchanged lanes being left alone instead of rewritten?
- Is only the relevant slice of `plan.md` being updated or reread?

## Stop Rule

The plan is solid enough to execute when:

- no critical assumption remains unchecked
- the remaining uncertainty is explicit and acceptable
- the next action is safe and testable
- another review pass is unlikely to change the approach materially
- at least 4 passes have completed unless the task was genuinely trivial
- tool results have been validated and any acceptance gates have passed
