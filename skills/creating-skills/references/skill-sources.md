<!-- version: 2.1 | author: chief-of-droids workspace | last_updated: 2026-03-30 -->

# Skill Sources

Reference catalog used by the `enrich skill` and `recommend skills` workflows.

**Consumed by:**
- `enrich skill` workflow (E2–E3) — pattern extraction: identifies authoring patterns
  present in catalog sources that are absent from the skill under review
- `references/workflows/recommend-skills.md` (Step 1 and Step 5) — coverage matching:
  checks whether a gap identified in session findings already has a source catalog entry,
  and states the coverage delta vs. the gap

**Role:** Completeness instrument — surfaces patterns present in comparable skills
that may be absent from the skill under review, and matches session-identified gaps
against known sources. Not a correctness standard; use `assessment-checklist.md`
for conformance assessment.

**Updated by:** `add source` workflow in `creating-skills` — evaluates, scores, and writes on approval

---

## Qualification Rules

A source is added to this catalog only when:
1. It has been fetched and verified to be reachable (not a 404 or auth wall)
2. It contains individually addressable SKILL.md files with explicit trigger/scope definition
3. It has been assessed against the five scoring criteria; sources scoring below 3.00 are excluded

Sources that fail fetch, are link aggregators, or do not meet criterion 2 are excluded regardless of score.

See `references/workflows/add-source.md` for the full qualification protocol.

---

## Catalog

*Stars fetched 2026-03-30. ~ = from search snippet, not direct repo page.*

| Name | Address | Repo | Reusability (25%) | Context-awareness (20%) | Tool integration (20%) | Determinism (15%) | Security (20%) | Score | Stars | Engineer signal |
|:-----|:--------|:-----|:------------------|:------------------------|:-----------------------|:------------------|:---------------|:------|:------|:----------------|
| Workspace Skills | /home/gino/workspace/skills/ | n/a | 4 | 5 | 5 | 5 | 5 | 4.85 | n/a | n/a — internal |
| Anthropic Skills GitHub Repo | https://github.com/anthropics/skills/ | anthropics/skills | n/a | n/a | n/a | n/a | n/a | 5.00 | 102,000 | Strong — official Anthropic repo; cited in all major platform docs |
| OpenAI Skills | https://github.com/openai/skills | openai/skills | 4 | 4 | 5 | 4 | 4 | 4.20 | 15,700 | Strong — OpenAI Agents SDK team engineering blog; cited in VS Code and Codex official docs |
| obra/superpowers | https://github.com/obra/superpowers | obra/superpowers | 3 | 5 | 4 | 5 | 4 | 4.10 | ~2,000 | Strong — Jesse Vincent (Prime Radiant); blog.fsck.com writeup; Simon Willison citation |
| EveryInc/compound-engineering-plugin | https://github.com/EveryInc/compound-engineering-plugin | EveryInc/compound-engineering-plugin | 3 | 4 | 4 | 4 | 3 | 3.55 | ~10,100 | Strong — Every.to published case study; named engineering team; 10k+ stars with active release cadence (v2.53.0 2026-03-25) |

---

## Column Definitions

| Column | Meaning |
|:-------|:--------|
| Name | Human-readable source label |
| Address | Full URL or absolute filesystem path |
| Repo | GitHub repo identifier (owner/repo); n/a for internal sources |
| Reusability (25%) | 1–5: no project-context or sibling-skill dependencies; n/a for primary sources not sampled against criteria |
| Context-awareness (20%) | 1–5: skill adapts gracefully across trigger variants without breaking; n/a for primary sources |
| Tool integration (20%) | 1–5: skill explicitly states when, why, and how to invoke each tool; n/a for primary sources |
| Determinism (15%) | 1–5: output structure consistent across runs; n/a for primary sources |
| Security (20%) | 1–5: rated on worst-case sampled skill — scoped calls, no blind exec, no unconstrained external fetch; n/a for primary sources |
| Score | Weighted decimal: Σ(rating × weight). Anthropic GitHub Repo: editorial 5.00 — correctness standard, not a pattern-extraction source |
| Stars | GitHub stars at fetch date; ~ = from search snippet not direct repo page; n/a for internal |
| Engineer signal | Strong / Weak / None + one-line evidence. Strong = named practitioner citation. Weak = roundup/vendor only. None = no evidence found |

---

## Exclusion Log

Sources evaluated and excluded from this catalog:

| Source | Reason | Criterion failed |
|:-------|:-------|:----------------|
| skillmatic-ai/awesome-agent-skills | Primary artifact is curated links; no own SKILL.md files | Criterion 2 |
| affaan-m/everything-claude-code | Skills embedded in config harness; not independently addressable | Criterion 2 |
| abubakarsiddik31/claude-skills-collection | Link aggregator | Criterion 2 |
| travisvn/awesome-claude-skills | Link aggregator | Criterion 2 |
| ComposioHQ/awesome-claude-skills | Aggregator with 1 embedded skill; insufficient catalog | Criterion 2 |
| agentskills.io / Microsoft Agent Framework | Specification and SDK sources only; no SKILL.md catalog | Criterion 2 |
| cloudflare/skills | Direct SKILL.md fetch blocked; confidence penalty applied; excluded pending verification | Criterion 1 |
| sickn33/antigravity-awesome-skills | Score 2.65 — below 3.00 threshold; security findings (33 triage items); uneven community quality | Criterion 3 |
| Anthropic Skills Best Practices | Spec/guide source; no SKILL.md catalog to sample | Criterion 2 |
| AgentSkills Specification | Spec source; no SKILL.md catalog to sample | Criterion 2 |
