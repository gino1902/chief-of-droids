<!-- version: 1.1 | author: chief-of-droids workspace | last_updated: 2026-05-05 -->

# Challenge Rules

Best-practice checks applied against interview answers before artefact generation.
Run every rule against the parsed answers. Report issues as Major or Minor.

Cross-reference: verified against `platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`
and `code.claude.com/docs/en/best-practices` (2026-03-19).

---

## Contents

- CLAUDE.md Rules
- System Prompt Rules
- Severity Definitions

---

## CLAUDE.md Rules

### R01 — Minimum-necessary discipline (Major)

**Check:** S4Q14 (minimum-necessary rule) must answer "what must Claude know every
session to avoid mistakes" — not a wishlist.

**Fail condition:** Answer lists preferences, formatting rules, or things Claude
already knows from the domain (e.g. "always be professional", "follow best practices").

**Recommendation:** Strip to facts Claude cannot infer. If Claude would do the right
thing without being told, cut it.

**Source:** Official best-practices — "For each line ask: would removing this cause
Claude to make mistakes? If not, cut it."

---

### R02 — CLAUDE.md is not a Claude Code CLAUDE.md (Major)

**Check:** S4Q13 (format defaults) and S4Q14 (minimum-necessary) must not contain
build commands, lint rules, test runners, or code style guidelines.

**Fail condition:** Answer includes any of: `npm`, `pytest`, `eslint`, `ruff`,
`make`, `docker`, language-specific coding conventions.

**Recommendation:** Move code tooling to a Claude Code CLAUDE.md if this project
has a code component. The Claude Desktop CLAUDE.md governs output defaults only.

---

### R03 — Gotchas section will be populated (Minor)

**Check:** S6Q19 (gotchas) must not be empty or "none".

**Fail condition:** Empty or "none" — the gotchas section is the highest-signal
content in CLAUDE.md according to official best practices.

**Recommendation:** Think of one thing Claude typically gets wrong in this domain
(e.g. over-engineers, misses audience, invents specifics, ignores constraints).
Even one gotcha is better than none.

**Source:** Community-verified pattern — "Gotchas section in every skill/CLAUDE.md
is highest-signal content."

---

## System Prompt Rules

### R04 — Role is one sentence (Minor)

**Check:** S2Q7 (solution) should map to a one-sentence `<role>` block.

**Fail condition:** Solution is vague ("help with things"), generic ("AI assistant"),
or a job title without a deliverable ("Data Engineer").

**Recommendation:** Structure as: "You are a [role] that [produces/enables] [specific output]
for [audience/context]."

---

### R05 — Hard rules are hard (Major)

**Check:** S6Q17 (hard rules) must contain only non-negotiable constraints —
not soft preferences or defaults.

**Fail condition:** Rules contain words like "try to", "prefer", "usually",
"when possible" — these are defaults, not rules.

**Recommendation:** Move soft preferences to `<defaults>`. Keep `<rules>` for
things that must never happen without explicit confirmation.

---

### R06 — Workflows are scoped (Minor)

**Check:** S6Q20 (workflows) — if non-empty, each workflow must have a distinct
trigger phrase and ≤5 steps.

**Fail condition:** Workflow description is vague ("do the usual thing"),
has no trigger phrase, or describes >5 steps.

**Recommendation:** Name the trigger explicitly. If steps exceed 5, note that
this workflow should move to API orchestration.

**Source:** Official guidance — "Keep workflows to ≤5 steps in the system prompt.
Beyond that, Claude's execution becomes unreliable."

---

### R07 — Skills selection is intentional (Minor)

**Check:** S5Q16 (skills) — if "all" is selected, challenge whether all skills
are genuinely relevant.

**Fail condition:** "all" selected for a project where domain-specific skills
(e.g. `architecting-data-platforms`) clearly do not apply.

**Recommendation:** List only skills that match the domain. Irrelevant skill
descriptions load into every session and consume context.

**Source:** Official best-practices — "CLAUDE.md is loaded every session, so only
include things that apply broadly."

---

## Severity Definitions

| Severity | Meaning | Action |
| :--- | :--- | :--- |
| Major | Will produce a flawed or misleading artefact | Propose fix, wait for user response |
| Minor | Will produce a suboptimal artefact | Surface recommendation, proceed if user says skip |
