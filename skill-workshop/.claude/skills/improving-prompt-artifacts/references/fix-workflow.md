# Fix Workflow — improving-prompt-artifacts

Interactive workflow for applying audit recommendations to a prompting artifact.
Consumes a prior audit report. Proposes fixes per violation. Awaits per-violation approval. Applies approved fixes via the `Edit` tool. Emits revision metadata.

---

<execution-rules>
Do not propose fixes for criteria not in the supplied audit report.
Do not apply any fix without explicit user approval for that specific fix.
Use `Edit` for targeted text replacements. Use `Write` only for full-file structural rewrites with explicit user approval.
After all approved fixes are applied, append or update the revision metadata block (criterion VER-2).
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

1. **Read inputs.** Read the artifact (`Read` tool) and the audit report. Confirm both are parseable.

2. **Filter violations.** Build a fix queue containing only Blocking and Major violations from the report. Surface Minor violations to the user as "skipped — re-run audit and request inclusion if you want these fixed."

3. **For each violation in the queue:**
   1. State the criterion ID, severity, and finding.
   2. Quote the current text (≤20 words).
   3. State the exact proposed replacement.
   4. Cite the best-practices section that supports the fix, or "in-house" if criterion is in-house.
   5. Await one of three explicit user responses:
      - `approve` — proceed with this fix
      - `reject` — skip this fix; mark as deferred
      - `edit <new text>` — accept a user-supplied replacement instead of the proposal
   6. Do not batch approvals across multiple violations. One approval per fix.

4. **Apply each approved fix.** Use `Edit` per fix. Preserve the rest of the file. If a fix requires structural rewrite (e.g. STR-1 section split, STR-2 XML restructure), surface this explicitly and request `Write` approval before applying.

5. **Emit revision metadata (VER-2).** After all fixes are applied, append or update the metadata block at the bottom of the artifact:

   ```markdown
   | Field                | Value                                |
   |----------------------|--------------------------------------|
   | Target Model         | [model id]                           |
   | Target Environment   | [claude-code | claude-desktop | both]|
   | Best-Practices Ref   | [YYYY-MM-DD snapshot]                |
   | Last Revised         | [today's date]                       |
   | Revision Source      | improving-prompt-artifacts skill     |
   ```

   If a version block already exists at the bottom (per workspace convention), keep it and add the revision metadata above it, or merge the two blocks if the artifact's authoring convention permits.

6. **Produce fix summary.**

   ```
   FIX SUMMARY
   Artifact: [path]
   Audit report consumed: [path or "inline"]
   Target Environment: [value]
   Target Model: [value]
   Best-Practices Ref: [date]

   Fixes applied: [n]
   Fixes deferred: [n] — criterion IDs: [list]
   Fixes user-edited: [n] — criterion IDs: [list]
   Minor violations skipped: [n] — re-run audit to include

   Revised metadata block: [appended | updated | merged with existing version block]
   ```

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
| User provides ambiguous response to a fix proposal | Re-ask: "Respond `approve`, `reject`, or `edit <text>`. No other response is processed." |

---

## Cross-run behaviour

Fix runs are independent. A fix workflow consumes one audit report and produces one revised artifact. Do not chain fix workflows without re-auditing in between — the revised artifact's violation profile changes after edits, and a fresh audit is the only reliable evidence of the new state.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-05-17 |
| Status       | Draft      |
