# skills-lab

Staging area where skills are designed, tested, and released. This repository is the producer of skills. Everywhere a skill is invoked to do real work is a consumer. The two have opposite needs, and keeping them apart is the point of the architecture below.

## Producer and consumer, and why they are separated

The producer wants churn. Half-finished skills, several versions side by side, deliberately broad trigger descriptions for testing, and the test harness all need to be discoverable while authoring.

A consumer wants stillness. Exactly one version of each skill, narrow triggers, and nothing half-built in context. That is what gives predictable, consistent behaviour from one run to the next.

When both live in the same tree the consumer inherits the producer's churn, which is the problem this layout removes.

## The tiers

```
skills-lab                          PRODUCER (isolated, all the churn)
        |  distributes ONE canonical copy per shared skill
        v
chief-of-droids/ root               MAIN consumer
   .claude/skills/                  holds the shared library, once
        |  inherited automatically, no copy
        v
wiki-data/, claude-code-digest/ …   END consumers
   .claude/skills/                  only skills unique to that area
```

skills-lab produces skills. The chief-of-droids root is the main consumer and holds the shared library, one canonical copy of each skill. Areas below the root, such as wiki-data, are end consumers. They inherit the shared library from the root and add only the skills that are unique to them.

## How Claude Code loading supports the tiers

The tiering is not enforced by convention alone. It follows from how Claude Code discovers skills.

Project skills load from `.claude/skills` in the directory a session starts in and from every parent directory up to the repository root. So a session started in an end consumer such as `wiki-data/` inherits the root's shared library with no copy and no symlink of its own. The root is the single distribution point, and each end consumer holds only what is local to it.

Claude Code also discovers skills on demand from nested `.claude/skills` directories below the starting point, the moment Claude reads or edits a file in one of them. This is the behaviour the architecture is designed around, because it is also what makes duplicate copies dangerous (see the next section).

## One skill, one tier

A skill lives at exactly one tier.

Shared skills live at the chief-of-droids root and nowhere below it. An end consumer holds a skill only when that skill is unique to the area and is never wanted elsewhere.

The reason is a name collision. If the root holds `wiki-audit` and `wiki-data/` also holds its own copy, both stay available. The unqualified name loads the root variant, and Claude Code appends the directory-qualified nested variant, `wiki-data:wiki-audit`, with an instruction to also invoke it when working on files in that directory. Which copy governs a run then depends on which files the session happened to touch, and any drift between the two copies diverges in silence. That is the run-to-run variance the whole layout exists to prevent.

## Distribution: link, do not copy

Vetted skills reach the root through one collision-proof channel, never by copying a `SKILL.md` into each consumer.

A plugin marketplace is the stronger option. Plugin skills use a `plugin-name:skill-name` namespace and cannot conflict with skills at other levels.

A symlink to the single canonical directory in this repository is the lighter option. Claude Code follows the symlink and loads the skill once, even when the same target is reachable from more than one location.

Copying is what creates the duplicates and the collisions described above, so it is not used for shared skills. The current `deploy.sh` flow copies skills into target projects. Migrating that flow to a link-based channel is the outstanding change this architecture calls for.

## Evidence behind the choice

The cost of not isolating is measured, not assumed.

Output quality falls as input length grows even when the added tokens are irrelevant, so a lab full of half-finished skills sitting inside a working repo taxes every unrelated session. See Chroma's context rot report.

Instruction-following accuracy falls as the number of instructions rises. Duplicated and colliding skills raise the effective instruction count and the chance of conflicting guidance. See the IFScale and ManyIFEval benchmarks.

Sources:

- Extend Claude with skills, Claude Code Docs. https://code.claude.com/docs/en/skills
- Context Rot: How Increasing Input Tokens Impacts LLM Performance, Chroma, 14 July 2025. https://www.trychroma.com/research/context-rot
- How Many Instructions Can LLMs Follow at Once? (IFScale), arXiv 2507.11538. https://arxiv.org/abs/2507.11538
- When Instructions Multiply (ManyIFEval), EMNLP 2025 Findings, arXiv 2509.21051. https://arxiv.org/abs/2509.21051

## Status of the migration

This document describes the target architecture. The move to a separate skills-lab repository, the reduction of each shared skill to one canonical copy, the removal of the wiki-data duplicates, and the switch from copy-based `deploy.sh` to a link-based channel are not yet done. They are the migration to be drafted next.

| Field        | Value      |
|--------------|------------|
| Version      | 1.0        |
| Last Updated | 2026-07-21 |
| Status       | Draft      |
