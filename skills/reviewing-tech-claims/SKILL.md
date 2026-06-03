---
name: reviewing-tech-claims
description: >
  Verifies technical claims against official documentation and produces
  inline verification markers (✅ Verified or ⚠️ Unverified) on every claim.
  Load when prompt includes a verification qualifier, or proactively when
  composing with architecting-data-platforms or editing-docs on version-sensitive
  technical claims such as package names, CLI commands, API signatures,
  config syntax, install steps, or UI paths. Composes with:
  architecting-data-platforms, editing-docs.
---
<!-- version: 1.8 | author: chief-of-droids workspace | last_updated: 2026-06-03 -->

# Reviewing Tech Claims Skill

## Usage

Trigger by including one of the following phrases in the prompt:

- `technically verified`
- `verify against official docs`
- `tech-checked`
- `source-verified`
- `confirmed against official source`
- `update comparison guide`
- `tech verify comparison guide`
- `verify and update claude-code-vs-claudeai`
- `refresh comparison guide`
- `check comparison guide against official docs`

Also load proactively when composing with `architecting-data-platforms` or
`editing-docs` and the planned output contains version-sensitive technical claims
(package names, CLI commands, API signatures, config syntax, install steps, UI
paths). Do not wait for an explicit qualifier in that context.

---

## Rule

**Never write technical claims from memory. Always verify against the publisher's current official documentation first.**

---

## Reference Files

- `references/verification-workflow.md` — use filesystem tool to read before any verification task;
  contains the Official Sources table and the 4-step verification procedure
- `references/workflows/update-comparison-guide.md` — step-by-step workflow for verifying,
  correcting, and gap-filling `my-claude-fmk/claude-desktop/claude-code-vs-claudeai.md`;
  load when any trigger phrase for that workflow is detected

---

## Failure Handling

If `references/verification-workflow.md` cannot be read via filesystem tool, halt immediately.
Do not proceed from memory. Surface the failure:
`⚠️ verification-workflow.md unreadable — cannot verify claims. Resolve before continuing.`

---

## Composes With

| Skill | When |
| :--- | :--- |
| `architecting-data-platforms` | Any output containing Databricks, Azure, MLflow, or Prophet version-sensitive claims |
| `editing-docs` | Any structured document (`.md`, `.docx`, runbook, ADR) containing technical install or config steps |
