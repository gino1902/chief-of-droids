# chief-of-droids

Workspace for building with Claude Code: authoring and releasing skills, the tools, docs, and knowledge base around them, and deploying them into new projects.

## Prerequisites

- Claude Code installed.
- Git.

## Repositories

The skills lab lives outside this tree, as the sibling repository `../skills-lab`. It is where skills are designed, tested, and released, and it must never be added to a chief-of-droids session, so its work-in-progress skills stay out of this repo's skill discovery.

| Repo | Purpose |
|------|---------|
| `skills/` | _(describe)_ |
| `tools/` | _(describe)_ |
| `docs/` | _(describe)_ |
| `shared/` | _(describe)_ |
| `wiki-data/` | _(describe)_ |
| `claude-code-digest/` | _(describe)_ |
| `desktop-chat/` | _(describe)_ |

## Creating a new project

Bootstrap the new repo, then deploy skills into it from the sibling lab with `bash ../skills-lab/deploy.sh <new-proj> <package-or-skills>`. See `../skills-lab/DEPLOYING.md` for details.
