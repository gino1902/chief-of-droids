<!-- version: 1.1 | author: slide-gen workspace | last_updated: 2026-03-12 -->

# Assessment Checklist

Run against any SKILL.md during critique or assess workflows.
Always fetch official sources before running — this checklist supplements
live docs, does not replace them.

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
- [ ] Specificity matched to task fragility: high / medium / low freedom explicit
- [ ] No heavy-handed MUSTs where explanation of why would work better
- [ ] Trigger examples are realistic — reflect actual user phrases
- [ ] Instructions generalise — not overfit to narrow examples
- [ ] Workflows have clear sequential steps with feedback loops where relevant
- [ ] Failure handling defined — skill does not silently proceed on missing files

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
