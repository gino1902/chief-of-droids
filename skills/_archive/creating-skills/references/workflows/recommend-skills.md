<!-- version: 0.2 | author: chief-of-droids workspace | last_updated: 2026-03-30 -->

# Workflow: recommend skills

Trigger: `recommend skills` | "what skills should I add" | "skill gaps from sessions"
| "what am I missing as skills"

Analyses the most recent `managing-sessions` findings file to surface skill gaps —
patterns, workflows, or domain knowledge the user is performing manually or ad-hoc
that a skill could formalise. Matches gaps against the source catalog in
`references/skill-sources.md`. Produces a structured recommendation file.

**Confidence model:** Recommendations are only as good as the findings file they
consume. This workflow runs three confidence checks before producing output.
Confidence level is surfaced explicitly — never presented as uniform.

---

## Step 0 — Locate and gate on findings file

1. List `.tasks/sessions-findings/` via Filesystem tool
   — If directory absent or empty: halt
     `⚠️ No findings file found at .tasks/sessions-findings/ — run managing-sessions first, then retry.`
2. Identify the most recent findings file by filename date (YYYY-MM-DD prefix)
3. Surface to user before proceeding:
   ```
   Most recent findings file: <filename>
   Last modified: YYYY-MM-DD
   Proceed with this file? (yes / no)
   ```
   — Wait for explicit confirmation. Do not proceed without it.
   — If user says no: ask which file to use; accept explicit path override
4. Read the confirmed findings file via Filesystem tool
   — If unreadable: halt
     `⚠️ Findings file unreadable — cannot proceed.`

---

## Step 1 — Read source catalog

5. Read `references/skill-sources.md` via Filesystem tool
   — If unreadable: halt
     `⚠️ skill-sources.md unreadable — cannot match gaps against sources; workflow halted.`
6. Note which sources have a Guide available (✅ in Guide column) — these are
   match-eligible for concrete skill patterns; sources without a Guide can
   suggest domain coverage only

---

## Step 2 — Read current skill coverage

7. List `skills/` directory via Filesystem tool — do not enumerate from memory
8. For each skill directory found: read SKILL.md `description` field only
   (frontmatter block — first 10 lines sufficient)
   — Build a coverage map: skill name → domain summary
   — This is the baseline against which gaps are measured

---

## Step 3 — Extract gap signals from findings file

9. Scan the findings file for gap signals across four signal types:

   | Signal type | Where to look in findings file | What it indicates |
   |:------------|:-------------------------------|:------------------|
   | Manual workaround | Net-New Content, Known Gaps table | User doing by hand what a skill could automate |
   | Repeated correction | Extracted Findings — category "Correction" | A recurring error that a skill constraint could prevent |
   | Untracked domain | Extracted Findings — category "Architecture decision" or "ADR" | Domain knowledge not covered by any existing skill |
   | Open item cluster | Known Gaps table — High priority items | Concentration of unresolved work in one area |

10. For each signal found:
    - Classify signal type (from table above)
    - Note source session title and date
    - Map against coverage baseline from Step 2 — is this domain already covered?
    - If covered: is the gap a trigger gap (skill exists but doesn't fire) or a
      content gap (skill fires but lacks the knowledge)?
    - If not covered: this is a candidate for a new skill

11. Discard signals where:
    - The finding is already `on-disk` in an existing skill's reference files
    - The domain is standard Claude knowledge (no skill token value)
    - The finding appears only once and shows no recurrence pattern
      **Exception:** a single-occurrence finding corroborated by a Known Gap
      entry in the same findings file is NOT discarded — Known Gap classification
      is an explicit editorial signal that the finding is structurally significant,
      regardless of session count. Treat it as equivalent to a two-session recurrence
      for discard-rule purposes.

    > Rationale: single-occurrence findings may be session noise. Recurrence
    > across multiple sessions is the primary confidence signal. Known Gap
    > corroboration is a deliberate override — it encodes editorial certainty
    > that the gap is real and recurring even if session evidence is thin.

---

## Step 4 — Confidence assessment per recommendation

12. For each candidate gap surviving Step 3, assign a confidence level:

    | Confidence | Criteria |
    |:-----------|:---------|
    | High | Signal appears in ≥2 sessions OR is classified High priority in Known Gaps table |
    | Medium | Signal appears in 1 session AND is corroborated by a correction or open item in the same findings file |
    | Low | Signal appears in 1 session only, no corroboration |

13. Discard Low confidence candidates unless the findings file confidence level
    (from its Summary header) is itself High — a High-confidence findings run
    elevates single-session signals to Medium; Low-confidence findings runs
    cannot produce High or Medium recommendations.

14. Surface confidence degradation explicitly if findings file confidence is
    Medium or Low:
    ```
    ⚠️ Findings file confidence: [Medium/Low] — recommendation confidence
    capped at [Medium/Low] regardless of signal recurrence.
    ```

---

## Step 5 — Match against source catalog

15. For each surviving candidate (High or Medium confidence):
    - Search `references/skill-sources.md` for a matching pattern or domain
    - Record: source name, address, Guide available (yes/no), Score
    - If a Guide is available (✅): this source can inform the skill structure
      directly — flag as "pattern available"
    - If no Guide: source provides domain coverage evidence only —
      flag as "domain reference only"
    - If no match in catalog: flag as "no external source — build from
      workspace patterns only"
    
    > Design note: absence of a catalog match does NOT reduce a recommendation's
    > confidence level. Confidence is determined entirely by session signal
    > recurrence (Step 4). The source catalog match affects implementation
    > guidance only — it tells you where to look when building the skill,
    > not whether the gap is real.

---

## Step 6 — Synthesise and confirm

16. Output recommendation table in chat before writing:

    | Candidate skill | Signal type | Sessions | Confidence | Source match | Pattern available |
    |:----------------|:------------|:---------|:-----------|:-------------|:------------------|
    | [name] | [type] | N | High/Med | [source] | Yes/No |

17. Surface findings file metadata as context:
    ```
    Source: <findings filename>
    Findings confidence: High/Medium/Low
    Sessions analysed: N
    Recommendation count: N (High: N, Medium: N, discarded: N)
    ```

18. Ask: "Confirm recommendations before I write the output file?"
    — Wait for explicit confirmation
    — If user requests changes: revise table, re-confirm before writing

---

## Step 7 — Write output file

19. Determine output path:
    `.tasks/skill-recommendations/YYYY-MM-DD-recommend-skills.md`
    — If directory absent: flag
      `⚠️ Directory .tasks/skill-recommendations/ does not exist — confirm creation before writing`
    — Wait for confirmation; create directory via Filesystem tool, then write
    — If file with this name already exists: append `-2`, `-3` — never overwrite

20. Build output file:

```markdown
# Skill Recommendations — YYYY-MM-DD

## Source

| Field | Value |
|:------|:------|
| Findings file | [filename] |
| Findings confidence | High / Medium / Low |
| Sessions analysed | N |
| Run date | YYYY-MM-DD |

---

## Recommendations

| Candidate skill | Signal type | Sessions | Confidence | Source match | Pattern available | Status |
|:----------------|:------------|:---------|:-----------|:-------------|:------------------|:-------|
| [name] | [type] | N | High/Med | [source] | Yes/No | Proposed |

---

## Discarded Signals

| Signal | Reason discarded |
|:-------|:-----------------|
| [description] | Single occurrence / Already on-disk / Standard knowledge |

---

## Next Steps

For each High confidence recommendation:
- Run `author skill <n>` to scaffold
- Use source match as reference input if pattern available

For each Medium confidence recommendation:
- Run `manage sessions` again to confirm recurrence before acting
```

21. Write file via Filesystem tool
22. Report path written

---

## Failure Handling

| Condition | Action |
|:----------|:-------|
| `.tasks/sessions-findings/` absent or empty | Halt — instruct user to run `managing-sessions` first |
| Findings file unreadable | Halt — report path and error |
| `skill-sources.md` unreadable | Halt — cannot match without catalog |
| `skills/` directory unreadable | Proceed without coverage map; flag: `⚠️ Cannot read skills/ — gap-vs-coverage check skipped; all signals treated as uncovered` |
| Findings file confidence is Low | Cap all recommendations at Low; flag degradation in output |
| Zero candidates survive Step 3 | Report: "No skill gaps identified in this findings file." — do not write output file |
| Zero candidates survive Step 4 | Report: "All signals below confidence threshold." — do not write output file |
| Output directory absent | Surface to user, await confirmation before creating |
| Output file already exists | Append `-2`, `-3` suffix — never overwrite |

---

## Output

Written to: `.tasks/skill-recommendations/YYYY-MM-DD-recommend-skills.md`
Not written if zero recommendations survive confidence filter.

---

## Known Limitations

- Signal extraction in Step 3 relies on findings file being well-formed.
  Malformed or partial findings files may produce false gaps.
- Recurrence check is within one findings file only — does not compare
  across multiple findings files from different runs.
- Source catalog match is keyword-based; no semantic matching.
  Gaps with unusual framing may not match even when a source exists.

| Field        | Value      |
|:-------------|:-----------|
| Version      | 0.2        |
| Last Updated | 2026-03-30 |
| Status       | Active     |
