# Memory And Context Patterns

Use this reference when durable project knowledge, previous plan state, cached summaries, or memory tools are available.

## Memory First, But Verify Staleness

Before rediscovering known project facts, check available memory or durable context.

Use memory directly only when:

- it is relevant to the current request
- it has a confidence or provenance signal
- it is recent enough for the type of fact
- using it will not hide an important current-state change

Verify memory against live files or tools when:

- the fact is time-sensitive
- the outcome controls a risky action
- the memory is old or low confidence
- the user reports a contradiction
- the memory affects deployment, training, eval, budgets, or safety gates

## Memory Write Rules

Write or update durable memory only for facts that should affect future tasks.

Good memory candidates:

- explicit user preferences
- project decisions
- known environment constraints
- stable paths and commands
- acceptance gates
- recurring failure modes
- verified latest status snapshots

Avoid writing:

- transient tool noise
- guesses
- stale partial plans
- facts without source or confidence

## Memory Shape

Store memory in a form future work can act on:

```text
Key: project.area.fact
Value: concise fact plus implication
Confidence: source-backed confidence
Source: file, command, user decision, or run ID
Written/verified date: date
Tags: project, subsystem, topic
```

When replacing old information, mark the old fact as superseded instead of leaving contradictory memories active.

## Apply User Preferences

If memory includes user preferences, apply them to the response and work style.

Examples:

- concise output
- no unnecessary headers
- verify before acting
- do not ask again for a stored limit

## Budget And Gate Memories

Treat remembered budgets and gates as active constraints.

Examples:

- VRAM ceilings
- trace-count gates
- eval acceptance thresholds
- required approval language
- deployment preconditions

If a requested action violates a remembered gate, stop and explain the gate rather than continuing.
