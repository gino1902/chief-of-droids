# Verification Workflow

Read this file before any verification task.

---

## Official Sources

Use this table as the first lookup for any topic.

**For Databricks, Delta Lake, MLflow, Azure, and Prophet sources, defer to
`data-platform-architect/SKILL.md` — Official Sources table. Do not duplicate
those rows here.**

| Topic | Official Source |
| :--- | :--- |
| Anthropic — Claude API, models, general docs | `docs.anthropic.com` |
| Anthropic — Claude Code docs (settings, memory, skills, subagents, hooks, permissions, surfaces) | `code.claude.com` |
| Anthropic — support, plans, billing, release notes | `support.claude.com` |
| MCP protocol spec | `modelcontextprotocol.io` |
| npm packages | `npmjs.com` — confirm exact package name exists and is not deprecated |
| Node.js | `nodejs.org/en/docs` |
| Python | `docs.python.org/3` |
| Python packages (PyPI) | `pypi.org/project/{package-name}` |
| GitHub Actions | `docs.github.com/en/actions` |
| Docker | `docs.docker.com` |
| Any other tool or SaaS | The publisher's official developer docs — no community sources |

**Priority rule:** Official docs > official GitHub repo README > nothing.
Community blogs, Medium, Stack Overflow, and tutorials are never ground truth.

---

## Verification Steps

1. **Identify** every technical claim in the planned output — package names, CLI
   commands, UI paths, config syntax, API endpoints, auth methods, versions,
   install steps, and any similar detail.

2. **Find the official source** for each claim using the Official Sources table
   above. Always target the **latest version** of the documentation. If the
   source has version selectors, confirm you are on the current release.

3. **Check document freshness.** For every fetched source, look for a
   last-updated or published date.

   - **No date found:** treat as outdated — flag it, require user approval
     before citing.
   - **Date found, older than 12 months:** flag it.
     `⚠️ Source outdated (last updated: YYYY-MM) — verify before use.`
   - **Date found, under 12 months:** cite freely; note the date inline when
     version matters.

   If flagged as stale and the source is an official versioned doc, attempt one
   re-fetch targeting the same domain before excluding. If no fresher version is
   found, flag and stop — do not fall back to community or blog sources.

4. **Write only after confirmation.** If no official source is findable, flag
   the claim:

   ```
   ⚠️ Unverified — confirm against official docs before using
   ```
