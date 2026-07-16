# Fix Workflow — improving-prompt-artifacts

Interactive workflow for applying audit recommendations to a prompting artifact.
Consumes a prior audit report. Proposes fixes per violation. Awaits per-violation approval. Applies approved fixes via the `Edit` tool. Updates the artifact's canonical version block and reports revision provenance in the fix summary.

---

<execution-rules>
Do not propose fixes for criteria not in the supplied audit report.
Do not apply any fix without explicit user approval for that specific fix.
Use `Edit` for targeted text replacements. Use `Write` only for full-file structural rewrites with explicit user approval.
`Edit` and `Write` calls during this run target `target-artifact` only. If a fix appears to require modifying a different file, halt and report — do not write. Reason: the audit report scopes the fix run; writing outside the scoped artifact is a silent regression on an unrelated file.
Surface every iteration of each fix proposal in chat along with its self-challenge notes — iter-1, iter-2, iter-3, and any further iterations triggered by a Drifting verdict. The `y/n` prompt appears only after the trajectory verdict is surfaced. Reason: user visibility into the refinement steps lets the reviewer verify the self-challenge actually happened — without it, the iteration loop becomes internal handwaving the user cannot audit.
After all approved fixes are applied, update the artifact's canonical version block and record revision provenance in the fix summary (criterion VER-2).
Do not re-run the audit at the end of the fix workflow — that is a separate invocation.
</execution-rules>

---

## Inputs

| Input | Required | Source |
|:------|:---------|:-------|
| Artifact path | yes | user prompt |
| Audit report | yes | user prompt (path) or paste (inline content) |
| Target Model declaration | yes | inferred from artifact metadata or asked |
| Target Environment declaration | yes | inferred from artifact metadata or asked |

If audit report is absent: halt. Report: "Fix workflow requires a prior audit report. Run `audit <artifact>` first, then re-invoke with the report path."

If Target Model or Target Environment cannot be inferred and is not in the audit report: ask the user once. Block on the answer.

---

## Workflow steps

1. **Read inputs.** Read the artifact (`Read` tool) and the audit report. Confirm both are parseable. Extract the `Artifact:` path from the audit report header and bind it as `target-artifact` for the whole run. Every `Edit` and `Write` call during this fix run must target `target-artifact` verbatim. If the user-supplied artifact path differs from the report's `Artifact:` line, halt and surface the mismatch — do not proceed.

2. **Filter violations.** Build a fix queue containing only Blocking and Major violations from the report. Surface Minor violations to the user as "skipped — re-run audit and request inclusion if you want these fixed."

3. **For each violation in the queue:**
   1. Display the violation block verbatim from the audit report — the full block exactly as it appears in the report file (criterion ID, Severity, Finding, Location, Citation, Fix). Do not paraphrase, summarize, or restate. Reason: paraphrase drifts wording across runs; the report file is the canonical text the user reviewed.
   2. **Iteration 1 — draft.** Propose a first concrete replacement (the exact text that would land in `target-artifact`, plus insertion location).
   3. **Self-challenge — iteration 1.** Audit the iter-1 proposal on two axes:
      - **Fix-intent** — does it address exactly the violation's `Fix:` line, no more no less? Flag scope creep (extra edge cases, unrelated rules, prose expansion).
      - **Predictability-intent** — does it reduce run-to-run variance in `target-artifact`'s runtime behaviour? See `## Predictability intent` below for the surfaces to test against.
   4. **Iteration 2 — revise.** Propose a second concrete replacement that addresses the challenges from step 3. Show the iter-2 text in full.
   5. **Self-challenge — iteration 2.** Re-audit on the same two axes. Flag any remaining drift on either axis.
   6. **Iteration 3 — revise.** Propose a third concrete replacement that addresses the challenges from step 5. Show the iter-3 text in full.
   7. **Self-challenge — iteration 3.** Audit on the same two axes. Iter-3 is not exempt from challenge.
   8. **Trajectory analysis.** Analyse the three drafts as a set and assign one of three verdicts. Surface the verdict explicitly before any user prompt.
      - **Stable** — iter-3 self-challenge passes both axes AND iter-2 and iter-3 share the same insertion location, the same structural shape, and the same set of named surfaces being added. Differences are wording polish only.
      - **Drifting** — iter-3 self-challenge fails on at least one axis, but the trajectory iter-1 → iter-2 → iter-3 shows convergence (each iteration removes prior failures or stabilises at least one of: insertion location, structural shape, named surfaces).
      - **Divergent** — the three structural attributes (insertion location, structural shape, set of named surfaces) do not stabilise across iter-2/iter-3, OR each iteration introduces a new variance surface its predecessor did not.
   9. **Branch on verdict.**
      - **Stable** → surface iter-3 + the trajectory verdict and ask: `Proceed (y/n)?`. On `y`, apply iter-3 text via `Edit` (or `Write` per the structural-rewrite rule in `<execution-rules>`), targeting `target-artifact`. On `n`, skip this fix; mark as deferred.
      - **Drifting** → run iter-N+1, self-challenge it, re-analyse the trajectory across all iterations to date. Cap at iter-5. If iter-5 still drifts, fall through to **Divergent**.
      - **Divergent** → surface every iteration produced + a one-sentence divergence diagnosis (which structural attribute did not stabilise, or which new variance surface each iteration introduced) + the recommendation "no change to `target-artifact` for this violation; the fix may be ill-posed for this artifact." Ask: `Proceed with no-change (y/n)?`. On `y`, skip this fix; mark as deferred-by-divergence. On `n`, halt this violation and surface: "Provide a steer for the next iteration." The user's steer becomes input to iter-N+1, which restarts the loop with the steer recorded.
   10. Do not ask any `y/n` before the verdict is reached. The user approves only the convergence outcome, not an individual draft. Reason: surfaced iterations that invite approval invite premature commitment; the loop exists to push past the first plausible draft, and the verdict is the user's signal that the loop converged.
   11. Do not batch approvals across multiple violations. One `y/n` per fix.

**Surface format for each iteration** — show the iteration in this shape:

```
**Iteration <N>**
Proposed replacement text:
  <verbatim text that would be inserted/edited in target-artifact>

Insertion location:
  <quoted anchor from target-artifact, ≤30 words, or "new block at end of <section>">

Self-challenge:
  Fix-intent: <pass | fail — reason>
  Predictability-intent: <pass | fail — reason>
```

After the last iteration, surface the trajectory verdict in this shape:

```
**Trajectory verdict: <Stable | Drifting | Divergent>**
Insertion location stabilised: <yes | no — detail>
Structural shape stabilised: <yes | no — detail>
Named surfaces stabilised: <yes | no — detail>
New variance surfaces introduced by latest iteration: <none | list>
```

Then prompt per the branch rules in sub-step 9.

4. **Apply each approved fix.** Use `Edit` per fix. Preserve the rest of the file. If a fix requires structural rewrite (e.g. STR-1 section split, STR-2 XML restructure), surface this explicitly and request `Write` approval before applying.

5. **Update the version block (VER-2).** After all fixes are applied, ensure `target-artifact` ends with the canonical workspace version block, bumping `Version` and setting `Last Updated` to today:

   ```markdown
   | Field        | Value      |
   |--------------|------------|
   | Version      | [bumped]   |
   | Last Updated | [today]    |
   | Status       | [Draft | Review | Final] |
   ```

   Do not inject a separate provenance or metadata block into the artifact. The revision provenance (Target Model, Target Environment, Best-Practices Ref, Revision Source) is recorded in the fix summary below, not in the artifact.

6. **Produce fix summary.**

   ```
   FIX SUMMARY
   Artifact: [path]
   Audit report consumed: [path or "inline"]
   Target Environment: [value]
   Target Model: [value]
   Best-Practices Ref: [date]
   Revision Source: improving-prompt-artifacts skill
   Last Revised: [today's date]

   Fixes applied: [n]
   Fixes deferred: [n] — criterion IDs: [list]
   Fixes user-edited: [n] — criterion IDs: [list]
   Minor violations skipped: [n] — re-run audit to include

   Version block: [bumped to <version> | added]
   ```

---

## Predictability intent

A fix proposal passes the predictability-intent check when it does not introduce, and where possible removes, the following variance surfaces in `target-artifact`:

| Surface | Failure shape |
|:--------|:--------------|
| Modal verbs in hard rules | `should`, `may`, `might`, `could`, `would` used where the rule must execute deterministically. Imperative or `must` required. |
| Hedging qualifiers | `usually`, `typically`, `generally`, `often`, `normally`, `in most cases` in a hard rule. |
| Ambiguous fallback | A branch without an explicit catch-all, or a fallback whose target output is not pinned. |
| Unbounded output | Length, item count, or section count left open where a bound is needed to constrain variance. |
| Missing Reason clause | A non-obvious rule without a Reason clause that encodes intent (not restatement). |
| Counterfactual Reason clause | A Reason clause whose stated principle, causal claim, or named consequence is contradicted by the artifact's own documented behaviour (failure-scenario tables, phase outputs, configuration in referenced files, or workspace conventions the artifact inherits). Failure-mode example: the Reason asserts atomicity but the artifact's own failure table permits a partial-write outcome. Test: pick the most specific claim in the Reason; can you find a sentence elsewhere in `target-artifact` that contradicts it? |
| Synonym drift | Two terms used interchangeably for the same concept inside `target-artifact`. |
| Implied scope | Effort, depth, or completeness left to the model to infer. |
| Negative framing where positive form is unambiguous | `do not return X` where `return only Y` would have been clearer. |
| Dangling reference | "standard format", "usual approach", or any pointer to behavior not defined inline or in a resolvable reference. |

A proposal that adds one of these surfaces fails the predictability check even if it satisfies the fix-intent. A proposal that removes a surface that was not in the audit report's `Fix:` line still passes — incidental predictability gains are welcome; incidental scope creep on fix-intent is not.

---

## Tool selection

| Operation | Tool | Notes |
|:----------|:-----|:------|
| Read artifact | `Read` | Use `offset` / `limit` for files >2000 lines |
| Read audit report | `Read` | Same |
| Apply single-line or local fix | `Edit` | One Edit call per fix; preserves surrounding content |
| Rename a term across the artifact | `Edit` with `replace_all: true` | Use when STR-3 fix collapses synonym drift |
| Restructure file (XML wrapping, section split) | `Write` | Requires explicit "approve structural rewrite" from user before invocation |

---

## Error handling

| Condition | Action |
|:----------|:-------|
| `Edit` fails (old_string not unique) | Surface the failure; ask user whether to apply with more surrounding context or skip this fix |
| `Edit` fails (old_string not found) | The artifact has changed since audit; halt and recommend re-audit |
| Audit report references criterion IDs not in audit-criteria.md | Surface as "stale report — re-run audit before applying fixes" |
| User provides ambiguous response to a fix proposal | Re-ask: "Respond `y` or `n`. No other response is processed." |

---

## Cross-run behaviour

Fix runs are independent. A fix workflow consumes one audit report and produces one revised artifact. Do not chain fix workflows without re-auditing in between — the revised artifact's violation profile changes after edits, and a fresh audit is the only reliable evidence of the new state.

---

| Field        | Value      |
|--------------|------------|
| Version      | 1.3        |
| Last Updated | 2026-07-16 |
| Status       | Draft      |
