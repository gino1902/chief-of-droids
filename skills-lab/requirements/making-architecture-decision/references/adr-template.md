# ADR Template

Loaded by `SKILL.md` after the interview is complete. Fill it in using the captured answers and write to `ADR-<NNN>-<slug>.md`.

## Rules for filling in

- Use the user's own language where possible. Do not paraphrase into generic architecture-speak.
- One decision per record. If the interview surfaced more than one, split into separate ADRs.
- Section order is locked. Do not add new top-level sections.
- The rationale table's columns are the decision drivers captured in interview section 3. One column per option, one row per driver.
- The basis line under the decision and the Sources section must agree. Cite only sources that drove the choice, each with its section. Where no authority mandates the choice, state that in the basis line rather than padding Sources.
- Consequences must include at least one downside or thing given up.
- Validation must name an observable check, not a restatement of intent.
- Status is `Draft` unless the user promotes it. A decided ADR is immutable; changes go through supersession.
- Set the title to state the decision and the chosen option.

## Numbering and location

- Filename: `ADR-<NNN>-<slug>.md`, where `<NNN>` is the next number in the decisions log (zero-padded, matching the log's existing width) and `<slug>` is a short kebab-case topic.
- Location: the decisions log for the target repo (`decisions/` or `docs/adr/`). Confirm with the user if ambiguous.
- The log numbers its own ADRs from 001, independent of any other decision log in the wider repository.

## Template

The block below is the literal file to write (minus this line and the fences). Replace every `{{placeholder}}` with the captured answer.

~~~markdown
# ADR-{{NNN}} - {{decision title, ending with (Option X) for the chosen option}}

| Field | Value |
|:------|:------|
| Date | {{YYYY-MM-DD}} |
| Status | {{Draft / Accepted / Superseded by ADR-NNN}} |
| Task | {{ticket id or TBD}} |
| Decision-makers | {{named person or role}} |
| Consulted | {{parties consulted}} |
| Informed | {{audience informed}} |

---

## Context

{{1-2 short paragraphs: the open question, the forcing function (why now), and the constraints that bound it. State the failure mode the decision guards against if there is one. No answer yet.}}

---

## Options evaluated

**Option A - {{name}}**
{{one line}}

**Option B - {{name}}**
{{one line}}

**Option C - {{name}}**
{{one line, optional}}

**Options not pursued**
- {{option and the reason it was rejected early, optional}}

---

## Decision

**{{chosen option, stated as a commitment, with any mandatory mitigation named here}}**

### Rationale

| Criterion | Option A | Option B | Option C |
|:----------|:---------|:---------|:---------|
| {{driver 1}} | | | |
| {{driver 2}} | | | |
| {{driver 3}} | | | |

{{one short paragraph: why the chosen option wins on the drivers that matter.}}

Basis: {{the specific source and section, benchmark, or constraint that drove the choice. If no authority mandates it, say so explicitly here.}}

---

## Validation

{{how compliance with the decision is observed (a review gate, test, config invariant, or process control), and the condition that would reopen it.}}

---

## Consequences

- {{consequence, positive}}
- {{consequence, negative or thing given up}}
- {{further consequences as needed}}

---

## Sources

- {{source title, section "<section>" - URL}}

<!-- Only sources that drove the decision. Omit this section's URLs if the basis is an internal judgement with no external authority; keep the note in the Basis line instead. -->

---

| Field | Value |
|:------|:------|
| Version | 0.1 (draft) |
| Last Updated | {{YYYY-MM-DD}} |
~~~

## Post-write checklist

Before confirming the write, scan the draft for:

- [ ] Metadata table present with Date, Status, Task, Decision-makers, Consulted, Informed.
- [ ] Title states the decision and the chosen option.
- [ ] `Options evaluated` lists 2-4 genuine options, plus any option not pursued with its reason.
- [ ] The rationale table's rows are the decision drivers, and the chosen option wins on them (the decision follows from the drivers).
- [ ] The Basis line names a specific source and section, a benchmark, or a constraint, or explicitly states that no authority mandates the choice.
- [ ] Sources contains only sources that drove the decision, each with its section, and agrees with the Basis line.
- [ ] Consequences include at least one downside or thing given up.
- [ ] Validation names an observable check, not a restatement of intent.
- [ ] Status is `Draft` unless the user promoted it.
- [ ] No placeholders remain (`{{...}}`).
- [ ] Filename is `ADR-<NNN>-<slug>.md` with `<NNN>` the next number in the log.
