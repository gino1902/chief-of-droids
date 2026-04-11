# Prompt Maintenance — Methodology

> Reusable four-step pattern for auditing and trimming Claude system prompts.
> Cross-reference: per-project audit logs live in `<repo>/doc/system-prompt-token-audit.md`.

---

## Why This Matters

The project instruction prompt loads on every session. Every token consumes part of the model's attention budget before any task begins. Anthropic's context engineering guidance is explicit: treat context as a finite resource with diminishing marginal returns — keep it informative, yet tight.

Token audits should be run periodically as the prompt grows through iterative development. Without a discipline for cutting, prompts accumulate redundancy, stale rules, and over-specification over time.

---

## The Four-Step Pattern

### Step 1 — Challenge the prompt as a whole

Do not optimise line by line. First ask: what is the purpose of each section, and is it earning its tokens?

For each section or rule, ask:
- Is this enforced elsewhere (workflow, CONSTITUTION, CLAUDE.md)?
- Does it fire at the right activation scope (every task vs. triggered tasks only)?
- Is it platform-specific content that belongs in CONSTITUTION, not the system prompt?
- Is it documentation for humans rather than instructions for Claude?

This step produces candidate cuts with rough justifications. Do not write anything yet.

---

### Step 2 — Measure token counts per section

Never state token counts from intuition — measure with code.

**Recommended method:**
- tiktoken (cl100k_base) if network allows — closest available proxy for Claude's tokenizer
- Fallback: character count ÷ 3.8 chars/token approximation
- 3.8 chars/token is a reasonable midpoint for structured technical prose with symbols
- Real variance: ±10–15% — treat as directional, not exact

**Known failure mode:** intuitive estimates undercount by 2x or more for structured prompts with XML tags and repeated keywords. Always measure before claiming savings.

---

### Step 3 — Verify behavioural arguments

This is the critical gate. A rule that "feels redundant" is only safe to cut if the behaviour it enforces is covered elsewhere **at the same activation scope**.

**Key distinction:**

Rules in `<rules>` fire on **every task**. Workflow steps only fire when that workflow is **explicitly triggered**. These are not the same activation scope. A rule that duplicates a workflow step is not fully redundant — it provides a catch for sessions where the workflow is never triggered.

**Applied pattern:** consolidate rather than delete when scope differs. 3 lines → 1 line covering the same guard is a valid outcome.

---

### Step 4 — Verify against official Anthropic documentation

Behavioural arguments must be grounded in Anthropic's published guidance, not in Claude's self-assessment.

**Source to fetch:** `https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents`

**Claims to verify:**

| Claim | Expected verdict |
|---|---|
| Keep context minimal — every token depletes attention budget | Confirm |
| Avoid hardcoding platform-specific brittle rules | Confirm |
| Redundant rules in `<rules>` can be cut if workflow covers them | Verify scope carefully |
| Task steps are self-evident and can be trimmed aggressively | Verify — vague guidance assumption |
| Empty tags are dead weight | Confirm |
| Namespace block redundant if it lives in runtime files | Confirm via just-in-time strategy |

**Lesson:** behavioural arguments that seem sound often require revision once official docs are consulted. Never skip this step.

---

## Trigger Conditions for a New Audit

Run an audit when any of the following occur:
- A new workflow is added to the system prompt
- A new rule is added to `<rules>`
- A new repo is added to the routing table
- A use-case-specific term or URL is found in the system prompt
- The prompt has grown by more than 200 tokens since the last audit
- A session challenge reveals potential redundancy

---

*Cross-reference: `configuration-layer-guide.md` for the multi-project architecture. Per-project audit logs live in `<repo>/doc/system-prompt-token-audit.md`.*
