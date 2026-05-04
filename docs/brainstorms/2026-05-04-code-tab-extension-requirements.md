# Code Tab Extension — Brainstorm State (2026-05-04)

> Snapshot of the Code Tab Extension design discussion at session end on 2026-05-04.
> Captures what is settled, what is open, and where to resume. Supersedes the
> "dual-environment-handoff migration" FRAMING.md draft that opened the session —
> that framing was substantially wrong (cross-repo scope, migration semantics)
> and was challenged out during the session.

---

## Context

The chief-of-droids framework today operates entirely from the Claude Desktop
Chat tab. Knowledge work — discovery, framing, skill authoring, document
authoring — runs cleanly there via Filesystem MCP and the explicit routing in
HOW-TO-TRIGGER.md. Code work does not: the Chat tab has no inner dev loop
(no subprocess execution, no iterative test cycle, no agentic permission
modes), so tasks like TASK-051 (SQLite migration), TASK-080 (.docx generator
update), and TASK-018 (skill testing harness) cannot run efficiently in Chat.

This work proposes adding a **Code dimension** to chief-of-droids — Claude
Code sessions running against the same single repo — with a structured
handoff between Chat (intent + observation) and Code (iterative execution).

---

## Scope

Single repo: `chief-of-droids/`. The Code dimension is internal to this repo;
it adds a Code-tab execution surface for code-shaped work that originates
from and returns to the Chat-tab governance layer.

**Out of scope:**

- Sibling repos (e.g. `sqli-ai-taskforce/`). Inventory at session start
  confirmed sibling repos exist under `Workspace/` and are independently
  governed; chief-of-droids does not extend to govern them.
- Cross-repo orchestration. The original cross-repo migration framing was
  rejected after the inventory.
- Multi-user write coordination. Operator scope is "personal now,
  multi-user-ready later — don't preclude, don't design for."

---

## Boundary rule (loose reading)

> Iterative implementation work happens only in the target tree. Chief-of-droids
> initiates intent and observes results. Each side writes its own surface.
> Reads-across are allowed; commits-across are not.

Concretely:

| | Chat (governance layer) | Code (target work area) |
| :--- | :--- | :--- |
| Writes | governance files (CLAUDE.md, skills/, .tasks/, handoff envelopes) | implementation files + result envelopes |
| Reads | result envelopes, branch diffs, monitoring logs | handoff envelope from chief-of-droids |
| Commits | governance-layer files only | implementation files only |
| Owns | intent, ledger, skills inventory | implementation, test results, code commits |

The actual restriction is **commit reach**, not exec reach. Chat may read
anywhere and may exec to fire Code sessions; Chat may not write or commit
in any tree it does not own. This was challenged from a stricter reading
("zero exec reach") and resolved to loose because strict adds no real safety
property — the same actor can already write its own files; refusing exec
while permitting filesystem writes is theatre.

---

## Decisions made this session

1. **Project rename.** "Dual-environment-handoff migration" → "Code tab
   extension." Migration implies A→B replacement; this is composition (Chat
   stays, Code is added beside it). Drop the Sandcrawler / Landspeeder
   metaphor — internal nicknames added noise, not signal. Note: TASK-083
   still references the legacy names; treat as legacy only, do not propagate.

2. **Topology is single-repo.** Earlier brainstorm rounds debated child vs
   sibling vs hybrid topologies. Inventory showed `chief-of-droids/` already
   has zero sub-repos (former `datawan/` and `slide-gen/` were deprecated
   2026-05-03). The topology question was answered by removal. No registry,
   no walk-up isolation problem, no skills sync question.

3. **Operator scope: personal now, multi-user-ready later.** Don't preclude
   future multi-user, don't design for it. Worktree-based design (TASK-071)
   keeps multi-user open at no design cost.

4. **claude-proxy.py removed.** A 200-line REPL using the public anthropic
   SDK to count tokens; not a proxy, not a launcher, not referenced anywhere
   in the workspace. Its presence misled the launch-mechanism brainstorm by
   suggesting a partial launcher when it has no orchestration code. Removed
   under TASK-086 (TASKS.md committed; manual `rm` to follow). Token
   measurement capability deferred to TASK-085.

5. **Launch mechanisms inventoried.** Four candidates:
   - **A** — operator opens Claude Code manually, no Chat-side prep
   - **B** — Chat composes the `claude --print --cwd <target> ...` command,
     operator pastes/runs (zero infra, real Code session)
   - **C** — Chat fires `claude --print` via a bash MCP scoped for exec
     reach (target state, automated trigger)
   - **D** — API agent loop rebuilding Code-tab behaviour from scratch
     (TASK-070 territory; wrong shape for this use case)

   No final pick yet — see Open forks. Working recommendation: B now, C
   later. D is for the parallel-fan-out use case (TASK-070), not this one.

> ⚠️ Unverified — `claude --print` non-interactive flag named from prior
> training context; verify against current Claude Code CLI docs before
> committing to launch mechanism B or C.

---

## Backlog cross-references

| Task | Relationship to this work |
| :--- | :--- |
| TASK-070 | Parallel-agent orchestrator artifact — D-shaped (constrained API agent, parallel fan-out). Different use case. Not a substitute for the Code tab extension; coexists. |
| TASK-071 | Multi-session worktree model — **co-design dependency.** Worktrees ARE the handoff payload (Code's branch = the work artifact). Resolve together with handoff substrate, not before. |
| TASK-083 | Per-environment audit methodology — touches the CLAUDE.md split decision (whether Code reads its own CLAUDE.md or the Chat one). |
| TASK-053 | Fetch-tool naming (`fetch` vs `web_fetch` per environment) — micro-instance of the same per-env tool-surface problem the Code tab extension faces at macro scale. Pattern to follow when resolved. |
| TASK-028 | Close-session "add completed tasks" step — affects how the commit gate composes with cross-environment work. |
| TASK-084 | HEAD-vs-working-tree drift check — same trust-the-read problem appears at the handoff boundary (does Code's read of the envelope match what Chat wrote?). |
| TASK-085 | Token consumption measurement decision — capability gap created by claude-proxy.py removal. |

---

## Open forks (resume here)

1. **Handoff substrate** — branch + envelope file? directory of envelopes?
   issue queue? Probably a branch (Code's branch IS the work), but
   pressure-test alternatives. Idempotency, drift detection, and state
   transitions (drafted / sent / executing / returned / closed) all hang
   off this choice.
2. **Envelope contents (Chat → Code)** — task ID, intent, target paths,
   acceptance criteria, branch name, skills/refs Code should load. Open:
   ledger pointer, idempotency key.
3. **Result envelope (Code → Chat)** — task ID echo, branch tip SHA,
   summary of what was done, test status. Open: written back in-place on
   the same envelope file, or to a separate file or branch.
4. **Worktree convention** — co-design with substrate. TASK-071 covers
   session init / merge-back / branch-aware commit gate / session identity.
5. **Launch mechanism (B vs C)** — orthogonal to envelope shape. Resolve
   after the envelope is defined.
6. **CLAUDE.md split for the Code dimension** — three candidates:
   - Single CLAUDE.md with env-conditional sections
     (sqli-ai-taskforce de-facto pattern)
   - CLAUDE.md (shared baseline) + AGENTS.md (Code-only delta,
     agentskills.io convention)
   - CLAUDE.md (Chat) + `.claude/CLAUDE.md` (Code, walked-up and
     concatenated)

   > ⚠️ Unverified — whether Claude Code reads `AGENTS.md` natively as
   > part of its session-start file set. Verify before deciding.

7. **Skill discovery for Code** — three candidates:
   - Code reads `chief-of-droids/skills/` via the HOW-TO-TRIGGER.md
     routing pattern (preserves the framework's "skills route via
     HOW-TO-TRIGGER" invariant across both environments)
   - Symlink under `.claude/skills/` pointing to `../skills/<name>`
     (cheap mechanical fix; gives Code-Claude native frontmatter
     discovery without duplication)
   - Selective copy/sync of Code-relevant skills only (worst — duplication
     plus drift risk)

8. **Ledger writer asymmetry** — three candidates:
   - Symmetric — both sides write, branch-isolated, merge resolves
   - Chat-owns — Code writes a result envelope, Chat closes the ledger
     entry (matches existing commit-gate discipline)
   - Append-only — any session appends, Chat compacts periodically

Recommended next-round order: substrate (1) → envelope contents (2) →
result envelope (3) → worktree (4 co-designed). Items 5–8 fall out
once 1–4 are settled.

---

## Resume hint

Open a new session in the Chief of Droids Claude Desktop project, then
prompt:

> Resume the Code Tab Extension brainstorm. Read
> `docs/brainstorms/2026-05-04-code-tab-extension-requirements.md`.
> Pick up at the next open fork (handoff substrate).
> Use brainstorming-ideas skill in resume mode.

The brainstorming-ideas skill Phase 0 resume check will find this file,
acknowledge the state, and continue from fork 1.

---

| Field | Value |
| :--- | :--- |
| Version | 1.0 |
| Last Updated | 2026-05-04 |
| Status | Draft |
