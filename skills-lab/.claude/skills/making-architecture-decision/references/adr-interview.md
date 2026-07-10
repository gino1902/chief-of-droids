# ADR Interview

Loaded by `SKILL.md` at the start of Phase 1, and revisited per-section when a supersession re-runs the interview. Every section below maps to a section in `adr-template.md`.

For each section: ask the opening question, evaluate the answer against the quality bar, push back when it falls into a named anti-pattern, and capture the final answer in the user's own language.

Scope: this skill captures architecture decisions, functional or technical, in software design or business process design. Examples below span both. A decision here is a choice among real options that shapes structure, not a requirement, a task, or a preference.

## Overall Rules

1. **Ask, don't prescribe.** Do not offer menu options for open answers (context, decision, consequences). Use free-form responses. Reserve multi-select for routing decisions.
2. **Push back once, maybe twice.** If the first answer is weak, name the specific issue and ask a sharper question. If the second is still weak, capture what the user has given, note the section is worth revisiting, and leave the record at Draft. Do not let the interview spiral.
3. **Quote the user back at them.** When challenging an answer, use the user's own words verbatim. Paraphrasing softens the challenge.
4. **Keep each answer to 1-3 sentences.** Longer answers usually hide something vague. If the user writes a paragraph, ask them to pick the sentence that matters most.
5. **Don't leak the anti-pattern names.** The user does not need to hear "that's a strawman option" - just ask the sharper question that follows.
6. **Stay in scope.** If the topic is not a decision (a requirement, a task, a personal preference, or a done deal with no alternatives), say so and stop. An ADR records a choice among options.

---

## 1. Context and forcing function

**Opening question:** "What decision has to be made, and what is forcing it now?"

Strong answers state the decision as an open question rather than a foregone answer, name the forcing function (why now, what breaks or blocks while it stays open), and name the constraints that bound it.

**Anti-patterns and pushback:**

- **Decision stated as the solution** ("the decision is to use Kafka" / "the decision is to centralise approvals in finance") -> "That's the answer. What was the open question, and what were the alternatives? An ADR records a choice among options, not a done deal."
- **No forcing function** ("we might want to rethink our messaging someday") -> "If nothing forces it, it isn't a decision yet. What breaks, blocks, or gets more expensive if this stays open?"
- **Requirement, not a decision** ("the system must handle 10k orders an hour" / "invoices must be approved within 48 hours") -> "That's a requirement, not a decision. What architectural choice does meeting it force? Capture that choice."
- **Unbounded scope** ("decide the whole platform architecture") -> "That's many decisions. Which single one are we recording here? The others each get their own ADR."

**Capture:** 1-2 sentences naming the open question, the forcing function, and the binding constraints. No answer yet.

---

## 2. Options considered

**Opening question:** "What are the real options on the table, 2 to 4 of them, and what is each in one line?"

Strong answers give 2-4 genuine options at the same altitude, each viable enough that a reasonable colleague would defend it, and name any option that was deliberately rejected early with the reason.

**Anti-patterns and pushback:**

- **Only one option** ("there's really only one way to do this") -> "With one option there is no decision to record. If it is truly forced, this is a spec, not an ADR. If not, what is the alternative you are rejecting, and why?"
- **Strawman alternatives** (one real option beside obviously bad foils) -> "Those are foils, not options. Give me the alternatives a reasonable colleague would actually argue for."
- **Options at different altitudes** ("option A: move to Postgres; option B: improve data quality") -> "Those aren't comparable choices. Put the options at the same level so the decision is real."
- **False binary** ("build it or buy it") -> "Is it really only those two? Adopt-and-extend, partial build, defer, or do-nothing, are any of those live options?"

Cross-domain examples of a clean option set: synchronous versus asynchronous integration; monorepo versus polyrepo; centralised versus federated process ownership; manual review versus an automated gate versus sampling.

**Capture:** 2-4 named options, one line each, plus any option not pursued and the reason.

---

## 3. Decision drivers

**Opening question:** "What criteria actually decide this, the few a reasonable person would weigh?"

Strong answers give a short set of criteria that genuinely discriminate between the options, named before the choice rather than reverse-engineered from it.

**Anti-patterns and pushback:**

- **Criteria reverse-engineered to fit a chosen option** -> "Were these the criteria before you picked, or after? Name the ones that could have changed your mind."
- **Everything matters equally** ("all of these are critical") -> "If every criterion is critical, none of them discriminates. Which two or three actually separate the options?"
- **Vanity criteria** ("it's more modern" / "it's industry best practice") -> "Modern or best practice for what outcome? Name the concrete property that matters here, not the label."

**Capture:** 3-6 criteria that discriminate between the options. These become the columns of the rationale table.

---

## 4. Decision and basis

**Opening question:** "Which option, and what makes it the right one given the drivers, and what is it based on?"

Strong answers name the chosen option, show it follows from the stated drivers, and cite the specific basis, an authoritative source and section, a benchmark, or a binding constraint. Where no authority mandates the choice, they say so.

**Anti-patterns and pushback:**

- **Decision doesn't follow from the drivers** -> "Your drivers point at option B, but you chose A. What driver did I miss, or is the real reason unstated?"
- **Decision with no basis** ("it just feels right") -> "On what basis? A source, a benchmark, or a constraint. If it is judgement with no external backing, say that plainly rather than dressing it up."
- **Basis cites an uninvolved authority** (a blog or vendor page that did not drive the choice) -> "Did that actually drive the decision, or is it decoration? Cite only what you used."
- **Cargo-culted authority** ("a big tech company does it this way") -> "Their constraints aren't yours. What in your context makes this the right call?"

**Capture:** the chosen option, the rationale tied to the drivers, and the specific basis with its section, or an explicit note that no authority mandates it.

---

## 5. Consequences

**Opening question:** "What follows from this, the good and the bad, and what are you giving up?"

Strong answers name positive and negative consequences and the thing traded away.

**Anti-patterns and pushback:**

- **Only upsides** ("nothing but benefits") -> "Every real decision costs something. What gets harder, slower, or riskier because of this?"
- **Consequence restated as the decision** ("the consequence is we use Kafka") -> "That's the decision again. What changes downstream because of it, for the team, the system, or the process?"

**Capture:** a short list, both signs, including what was given up.

---

## 6. Validation

**Opening question:** "How will you know this decision is being followed, and that it still holds?"

Strong answers name a checkable signal that the decision is in force (a review gate, a test, a config invariant, a process control) and a condition that would trigger revisiting it.

**Anti-patterns and pushback:**

- **No way to check** ("we'll just follow it") -> "How would a reviewer catch a violation? With no check, the ADR drifts from reality. Name the gate."
- **Validation restates the intent** -> "That's the intent again. What is the observable that proves compliance?"

**Capture:** how compliance is observed, plus the condition that reopens the decision.

---

## 7. Sources

**Opening question:** "What authoritative sources ground this decision, and which section of each?"

Strong answers list only sources actually used, each with the specific section behind the decision.

**Anti-patterns and pushback:**

- **Sources not used** ("here's a reading list") -> "Did each of these drive the decision? Drop the ones that didn't. A source that was not used is false authority."
- **Missing grounding where it exists** ("no sources, just us") when authoritative guidance is available -> "Is there official guidance on this? If so, it should either back the choice or be argued against. If there genuinely is none, note that plainly."

**Capture:** the sources used, each with its section, matching the basis captured in section 4.

---

## 8. Governance

**Opening question:** "Who owns this decision, who was consulted, and who needs to be informed?"

Strong answers name a decision-maker (a person or role), the consulted parties, and the informed audience.

**Anti-patterns and pushback:**

- **Everyone or the team** ("the team decides") -> "Who specifically owns the call? Consulted and informed can be groups, but the decision-maker is a named person or role."

**Capture:** decision-makers, consulted, informed.

---

## After the Interview

Confirm this is a single decision. If two surfaced, offer to split into separate ADRs. Determine the next ADR number in the log. Then read `adr-template.md`, fill it in from the captured answers, run its post-write checklist, present the draft in chat, offer one edit round, and write to `ADR-<NNN>-<slug>.md`.
