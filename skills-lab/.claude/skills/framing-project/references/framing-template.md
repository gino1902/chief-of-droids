# Framing Template

Loaded by `SKILL.md` after the interview is complete. Fill it in using the captured answers and write to `FRAMING.md`.

## Rules for filling in

- Use the user's own language where possible. Do not paraphrase into generic PM-speak.
- Each section stays compact. The whole doc should read in under 5 minutes.
- Section order is locked. Do not add new top-level sections.
- Keep both the Customer and Business dimension in "Who it's for" and "What success means". Do not collapse either into one.
- "Customer" and "user" mean the same person here. The customer is the user we are framing for. Use whichever word reads naturally.
- Set `last_updated` in the YAML frontmatter to today's ISO date (YYYY-MM-DD). Do not duplicate the date in prose.
- Set `name` in the frontmatter to the project or initiative name (the same value used in the H1 title).

## Template

The block below is the literal file to write (minus this line and the fences). Replace every `{{placeholder}}` with the captured answer.

~~~markdown
---
name: {{project_name}}
last_updated: {{YYYY-MM-DD}}
---

# {{project_name}} Framing

## Target problem

{{1-2 sentence diagnosis. Names the customer situation and the crux that makes it hard. No solution language.}}

## Our approach

{{1-2 sentences naming the goal (tied to the target problem) and the means chosen to reach it. The two must be consistent, the means clearly serving and sized to the goal.}}

## Who it's for

**Customer:** {{Who they are, by role or situation. Mark primary vs secondary if there is more than one. One line on the job they are hiring this to do.}}

**Business:** {{Whose business outcome this serves, the sponsor, team, or unit that carries the result, and why it matters to them.}}

## What success means

**For the customer:** {{The ability or change we cause, stated in the customer's own language. Specific and measurable.}}

- **{{customer measure}}** - {{how it is observed, and where}}

**For the business:** {{The business result that makes this worth doing, revenue, cost, risk, profit, or a capability, and over what time frame.}}

- **{{business measure}}** - {{definition, and where it is measured}}

<!-- 3-5 measures total across the two. Stop at 5. -->

## Tracks

### {{Track 1 name}}

{{One line: what this track is, the investment area, not a feature list.}}

_Why it serves the approach:_ {{one line}}

<!-- Duplicate the block above for 2-4 tracks total. If you can't keep it to 4, fold related tracks together. -->

## Not working on

- {{one line per item}}

<!-- Optional. Delete the section if unused. Use only for things the team keeps being tempted by. -->
~~~

## Post-write checklist

Before confirming the write, scan the draft for:

- [ ] Frontmatter present at the top with `name` and `last_updated` keys.
- [ ] `last_updated` carries today's date in ISO format (YYYY-MM-DD).
- [ ] No placeholders remain (`{{...}}`).
- [ ] "Who it's for" fills in both Customer and Business. Neither is empty.
- [ ] "What success means" fills in both a customer measure (in customer language, measurable) and a business measure (names a result and a time frame).
- [ ] "What success means" carries 3-5 measures total across the two dimensions, stopping at 5.
- [ ] Track count is between 2 and 4. Each track has a one-line purpose and a note on why it serves the approach.
- [ ] Target problem and Our approach are connected, one clearly responds to the other.
