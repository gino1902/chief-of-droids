<!-- version: 1.5 | author: chief-of-droids workspace | last_updated: 2026-04-03 -->

# Assessment Checklist

Run against any SKILL.md during critique or assess workflows.
Always fetch official sources before running — this checklist supplements
live docs, does not replace them.

**Scope:** This checklist is the *correctness instrument* — it answers whether a skill
conforms to the Anthropic standard. It does not assess pattern completeness against
comparable skills; that is the role of `skill-sources.md` via the `enrich skill` workflow.

---

## Frontmatter

- [ ] `name` present — lowercase, hyphens only, max 64 chars
- [ ] `description` present — third person, max 1024 chars (official spec)
- [ ] `description` is trigger-inclusive — states both what it does AND when to use it
- [ ] `description` is "pushy" — proactively tells Claude when to invoke
- [ ] No XML tags in `name` or `description`
- [ ] No reserved words ("anthropic", "claude") in `name`

## Structure

- [ ] SKILL.md acts as table of contents — no bulk content inline
- [ ] SKILL.md body under 500 lines (official limit for optimal performance)
- [ ] Reference files declared explicitly with guidance on when to read them
- [ ] Large reference files (>100 lines) have a table of contents
- [ ] Multi-domain skills organise references by domain variant
- [ ] References are one level deep from SKILL.md — no nested chains
- [ ] No content Claude already knows — every line justified by token cost

## Instructions

- [ ] Imperative form used throughout ("Read...", "Fetch...", "Output...")
- [ ] Enforcement-critical rules use unambiguous directive language
  ("Always...", "Never...") — reserved for rules where deviation causes
  silent failure or incorrect output; not used for general guidance
- [ ] Specificity matched to task fragility: high / medium / low freedom explicit
- [ ] No heavy-handed MUSTs where explanation of why would work better
- [ ] Trigger examples are realistic — reflect actual user phrases
- [ ] Instructions generalise — not overfit to narrow examples
- [ ] Workflows have clear sequential steps with feedback loops where relevant
- [ ] Failure handling defined — skill does not silently proceed on missing files

## Workflow-Class Skills

Apply this section only when the skill implements a multi-step execution
workflow with classification logic, conditional branching, or stateful
output across multiple files or passes. Skip for reference-and-apply skills
(e.g. document formatters, domain advisors).

**Trigger signal:** skill has >3 sequential workflow steps, produces
output files, or classifies inputs into categories.

- [ ] Classification criteria are explicit and exhaustive — no implicit
  "otherwise" defaults; every possible input state maps to a named outcome
- [ ] All conditional branches are defined — if a step fires only under
  certain conditions, those conditions are stated; no branch is left implicit
- [ ] Pass/stage outputs are explicitly consumed by the next pass —
  it is clear what data flows forward and in what form
- [ ] Workflow stages are explicitly labelled — each stage has a name
  or number; outputs produced by a stage are identified by that label
  when referenced downstream
- [ ] Data-producing stages declare output persistence — if a stage
  produces data consumed in a later stage or surfaced to the user,
  the skill states whether that data is held in context or written
  to a file; implicit context-only storage is a silent failure risk
  on long workflows
- [ ] "Done" is defined — the workflow has an explicit completion condition,
  not just a list of steps that ends
- [ ] Failure handling covers runtime conditions, not just missing files —
  what happens when a tool returns unexpected output, an empty result, or
  a partial result mid-workflow?
- [ ] External tool behaviour assumptions are stated — if the workflow
  depends on a tool (e.g. `recent_chats`, `conversation_search`,
  `filesystem:read_text_file`) behaving in a specific way, that assumption
  is documented; known failure modes of that tool are in the failure table
- [ ] Cross-run state is addressed — if the skill writes output files that
  accumulate across runs, the skill defines how later runs interact with
  earlier output (append / overwrite / deduplicate)
- [ ] Confidence or quality level is surfaced to the user — if the workflow
  can produce output of varying completeness depending on tool availability
  or data quality, the skill reports that level explicitly rather than
  presenting all output as equally reliable

## Source Catalog Workflows (add source)

Apply this section when the skill includes a workflow that evaluates external
sources and writes to a scored catalog file (e.g. `add source` workflow).

- [ ] Three qualification criteria evaluated in order before any write:
  (1) URL fetchable and returns content, (2) individually addressable SKILL.md
  files present with explicit trigger/scope, (3) score ≥ 3.00 threshold applied
- [ ] Partial fetch handling defined — workflow states what to do when URL loads
  but SKILL.md content is not directly accessible (sub-path attempts, confidence flag)
- [ ] Scoring rubric present — five criteria with weights, 1–5 scale, worst-case
  security rule stated
- [ ] Exclusion Log write defined — rejected sources recorded with criterion and reason
- [ ] Catalog row insertion order stated (Score desc, Stars desc within ties)
- [ ] Write gate present — no write to skill-sources.md without explicit user approval
- [ ] Read-back after write — workflow confirms write succeeded via filesystem read

## Composition

- [ ] Compose declarations present if skill combines with others
- [ ] No capability overlap with existing skills without explicit delegation pattern

## Security

- [ ] No hardcoded credentials, API keys, or sensitive data
- [ ] No unexpected network calls or file access patterns
- [ ] Skill contents match stated purpose — no surprises

---

## Severity Definitions

- Blocking — prevents correct discovery or execution; must fix before use
- Major — degrades output quality or trigger accuracy; fix before production
- Minor — style or optimisation issue; fix opportunistically

## Overall Rating

- Pass — no Blocking or Major issues
- Partial — one or more Major issues, no Blocking
- Fail — one or more Blocking issues

---

## Checklist Scope Note

The Frontmatter, Structure, Instructions, Composition, and Security sections
cover all skill classes and are reliable for structural compliance assessment.

The Workflow-Class Skills section covers correctness of execution logic —
it is the only section that can surface classification errors, branching
gaps, and state management issues. A skill passing all other sections but
failing Workflow-Class checks should be rated Partial or Fail, not Pass.

The Source Catalog Workflows section covers correctness of catalog management
logic — applies only to skills with a source evaluation and write workflow.
A skill with an add-source workflow that fails this section should be rated
Partial or Fail even if all other sections pass.

A Pass rating on this checklist does not validate extraction accuracy,
tool query effectiveness, or real-data behaviour. Those require a live run.
