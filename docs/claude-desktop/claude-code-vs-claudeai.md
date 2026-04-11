# Claude Code vs Claude.ai vs Claude Desktop — Comparison Reference

> Doc-verified against Anthropic official docs (docs.claude.com, code.claude.com, support.claude.com) — April 2026.
> Ordered by project creation steps: from initial setup to agentic runtime.
> Corrections from conversation review are marked ✱
>
> **Claude Desktop** in this document refers to Anthropic's MCP-enabled chat client app (macOS/Windows),
> not the Claude Code Desktop app (a separate product that provides a GUI for Claude Code sessions).

---

## 1. Project Setup & Configuration

| Concept                        | Claude.ai                            | Claude Desktop                                                          | Claude Code                                                               |
|:------------------------------ |:------------------------------------ |:----------------------------------------------------------------------- |:------------------------------------------------------------------------- |
| Where does the project live?   | Anthropic's cloud (UI-managed)       | Anthropic's cloud (UI-managed); Cowork projects stored locally          | Your codebase (filesystem)                                                |
| Versioned with git?            | No                                   | No                                                                      | Yes — commit `CLAUDE.md` and `.claude/`                                   |
| Shared with team?              | No — per user (Team/Enterprise: sharable projects) | No — per user (Team/Enterprise: sharable chat projects) | Yes — committed to repo                                                   |
| Project-level config file      | Project Instructions (UI text field) | Project Instructions (UI text field)                                    | `CLAUDE.md` or `.claude/CLAUDE.md` at project root                        |
| User-level config file         | User preferences (UI)                | User preferences (UI)                                                   | `~/.claude/CLAUDE.md`                                                     |
| Personal project-level config  | N/A                                  | N/A                                                                     | `CLAUDE.local.md` at project root — gitignored, personal notes only ✱     |
| Org-wide config file           | N/A                                  | N/A                                                                     | Managed policy CLAUDE.md — deployed by IT to system path; cannot be excluded |
| Subdirectory-level config      | No                                   | No                                                                      | `CLAUDE.md` in any subdirectory — loaded on demand when Claude reads files there |
| Conditional rules by file type | No                                   | No                                                                      | `.claude/rules/*.md` — scoped via `paths:` frontmatter (glob patterns)    |
| Settings file                  | Not applicable                       | Not applicable                                                          | `~/.claude/settings.json` (user) / `.claude/settings.json` (project)      |
| Settings precedence            | N/A                                  | N/A                                                                     | Managed > CLI args > Local > Project > User (Managed highest, User lowest) ✱ |
| Personal settings (gitignored) | N/A                                  | N/A                                                                     | `.claude/settings.local.json` — git-ignored automatically when created     |

> ✱ **`CLAUDE.local.md`** is a first-class documented file (not a workaround). It lives at `./CLAUDE.local.md`, is personal and project-specific, loads alongside `CLAUDE.md`, and should be added to `.gitignore`. Running `/init` with the personal option does this automatically. Verified: code.claude.com/docs/en/memory, 2026-04-06.

> ✱ **Settings precedence** — full order: Managed (highest) → Command line arguments → Local (`.claude/settings.local.json`) → Project (`.claude/settings.json`) → User (`~/.claude/settings.json`) (lowest). Local outranks Project. CLI args are a temporary session override below Managed. Verified: code.claude.com/docs/en/settings §Settings precedence, 2026-04-06.

---

## 2. System Prompt

| Concept                         | Claude.ai                                                        | Claude Desktop                                                                   | Claude Code                                                                         |
|:------------------------------- |:---------------------------------------------------------------- |:-------------------------------------------------------------------------------- |:----------------------------------------------------------------------------------- |
| System prompt visible?          | Yes — editable in Project Instructions                           | No — internal, not published; Project Instructions ≠ system prompt               | No — internal, not published                                                        |
| Can you replace it?             | Yes — fully editable                                             | No                                                                               | No — append only via flag; `--system-prompt` replaces it entirely for one session ✱ |
| How to customize it             | Edit Project Instructions directly                               | Custom Instructions (UI) — appended to system prompt, not replacing it           | `--append-system-prompt` flag (append) / `--system-prompt` flag (replace)           |
| What it configures              | Who Claude is: tone, persona, response style, context about you  | Who Claude is: tone and style via Custom Instructions                            | Who Claude is as an agent: tools available, coding style, safety rules, file access |
| Configures project knowledge?   | Yes — Project Instructions carries both role AND project context | Partially — Project Instructions and knowledge base are separate from sys prompt | No ✱ — project knowledge lives in `CLAUDE.md`, not the system prompt                |
| CLAUDE.md delivery mechanism    | N/A                                                              | N/A                                                                              | Delivered as a **user message** after the system prompt — not injected into it ✱    |
| Internal system prompt contents | N/A                                                              | Not published                                                                    | Not published                                                                       |
| Analogy                         | Employment contract + project brief combined                     | Employment contract + appended preferences                                       | Employment contract only — project brief is separate (`CLAUDE.md`)                  |

> ✱ **`--system-prompt` vs `--append-system-prompt`:** `--append-system-prompt` adds text to the end of the internal system prompt for the session. `--system-prompt` replaces the system prompt entirely. Most use cases should use `--append-system-prompt`. Verified: code.claude.com/docs/en/sub-agents §Invoke subagents explicitly, 2026-04-06.
>
> ✱ **CLAUDE.md is not system-prompt injection:** CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. Claude reads it and tries to follow it, but there is no guarantee of strict compliance — especially for vague or conflicting instructions. For system-prompt-level enforcement, use `--append-system-prompt` (must be passed every invocation). Verified: code.claude.com/docs/en/memory §Troubleshoot, 2026-04-06.

---

## 3. Memory & Persistent Context

| Concept                     | Claude.ai                                                      | Claude Desktop                                                    | Claude Code                                                                             |
|:--------------------------- |:-------------------------------------------------------------- |:----------------------------------------------------------------- |:--------------------------------------------------------------------------------------- |
| Mechanism name              | Memory system                                                  | Memory system (same as claude.ai — shared account)                | Two systems: `CLAUDE.md` + Auto memory                                                  |
| Who writes it?              | Anthropic auto-generates from conversations                    | Anthropic auto-generates from conversations                       | `CLAUDE.md`: you write it. `MEMORY.md`: Claude writes it automatically                  |
| Stored where?               | Anthropic's cloud (per user)                                   | Anthropic's cloud (per user) — same memory, same account          | `CLAUDE.md` on disk (git-tracked) + `~/.claude/projects/<project>/memory/` (local only) |
| Loaded at session start?    | Yes — injected at runtime                                      | Yes — injected at runtime                                         | Yes — both `CLAUDE.md` and first 200 lines / 25KB of `MEMORY.md` loaded at start ✱      |
| User can edit it?           | Via memory edits tool                                          | Via memory edits tool (Settings > Capabilities)                   | Directly — edit the markdown file, or `/memory` command                                 |
| Memory import / export?     | Yes — Settings > Capabilities > Import/export ✱                | Yes — same as claude.ai ✱                                         | N/A                                                                                     |
| Incognito / private mode?   | Yes — incognito chats excluded from memory synthesis ✱         | Yes — same incognito toggle as claude.ai ✱                        | N/A — no incognito concept; sessions are always local                                   |
| Past-chat search?           | Yes — paid plans (Pro/Max/Team/Enterprise); RAG over history ✱ | Yes — same as claude.ai ✱                                         | N/A                                                                                     |
| Gitignore recommended?      | N/A                                                            | N/A                                                               | `MEMORY.md` and `settings.local.json` — yes. `CLAUDE.md` — no, commit it                |
| Auto-learned from sessions? | Yes                                                            | Yes — same memory system as claude.ai                             | Yes — Auto memory (`MEMORY.md`): build commands, debugging insights, preferences        |
| Key distinction             | Memory = who you are to Claude                                 | Memory = who you are to Claude (identical to claude.ai)           | `CLAUDE.md` = rules you impose. `MEMORY.md` = what Claude has learned                   |
| Per-project memory?         | Yes — each project has its own memory summary                  | Yes — each project has its own memory summary                     | Yes — per working tree under `~/.claude/projects/<project>/memory/`                     |

> ✱ Auto memory has a dual limit: first 200 lines **or** first 25KB of `MEMORY.md`, whichever comes first. Topic files (`debugging.md`, etc.) are not loaded at startup — read on demand. Verified: code.claude.com/docs/en/memory §How it works, 2026-04-06.
>
> ✱ **Memory import/export (claude.ai / Desktop):** Users can export their memory and import from other AI providers via Settings > Capabilities. Verified: support.claude.com/en/articles/12123587, 2026-04-06.
>
> ✱ **Incognito chats (claude.ai / Desktop):** Incognito chats are not saved to chat history and not included in memory synthesis. Verified: support.claude.com §Using incognito chats, 2026-04-06.
>
> ✱ **Past-chat search (claude.ai / Desktop):** Users on paid plans can prompt Claude to search across previous conversations using RAG. Separate from memory synthesis. Verified: support.claude.com/en/articles/11817273, 2026-04-06.

---

## 4. Skills

| Concept                           | Claude.ai                                                          | Claude Desktop                                                              | Claude Code                                                                |
|:--------------------------------- |:------------------------------------------------------------------ |:--------------------------------------------------------------------------- |:-------------------------------------------------------------------------- |
| Feature exists?                   | Yes (since Oct 2025)                                               | Yes — same feature, same Customize > Skills UI                              | Yes                                                                        |
| Pre-built skills available?       | Yes — `docx`, `xlsx`, `pptx`, `pdf` (Anthropic-managed)            | Yes — same Anthropic-managed skills; also available in Cowork               | Bundled skills ship with CLI: `/batch`, `/simplify`, `/debug`, `/loop` etc |
| Custom skills?                    | Yes — upload zip via Customize > Skills                            | Yes — same upload flow via Customize > Skills                               | Yes — filesystem at `.claude/skills/<skill-name>/SKILL.md`                 |
| Same SKILL.md format?             | Yes — open Agent Skills standard                                   | Yes — open Agent Skills standard                                            | Yes                                                                        |
| Auto-invoked by Claude?           | Yes — based on description match (200-char cap on description)     | Yes — same mechanism as claude.ai                                           | Yes — description-match; 250-char description cap in skill listing ✱       |
| Manually invoked?                 | No slash commands in chat UI                                       | No slash commands in chat UI                                                | Yes — `/skill-name` in CLI                                                 |
| Versioned in git?                 | No — per user account                                              | No — per user account                                                       | Yes — `.claude/skills/` committed to repo                                  |
| Org-wide distribution?            | Yes — Team/Enterprise owners provision via Organization settings   | Yes — same org provisioning as claude.ai                                    | Yes — via plugins or committed to repo; managed settings for org-wide      |
| Plugin marketplace distribution?  | N/A                                                                | N/A                                                                         | Yes — skills bundled inside plugins; official Anthropic marketplace exists ✱ |
| Require code execution enabled?   | Yes — skills run in a VM sandbox                                   | Yes — skills run in a VM sandbox                                            | No — filesystem-based, no sandbox needed for SKILL.md reads                |
| Skills in Office add-ins?         | N/A                                                                | Yes — Excel and PowerPoint add-ins support skills (March 2026) ✱            | N/A                                                                        |
| Max skills per API request        | Up to 8 (via `container` parameter in Messages API)                | N/A (UI, not API)                                                           | N/A — filesystem, no enforced limit                                        |
| How Claude accesses skill content | VM filesystem — reads SKILL.md via bash when triggered             | VM filesystem — reads SKILL.md via bash when triggered                      | Local filesystem — reads SKILL.md via bash when triggered                  |
| Plan availability                 | Free, Pro, Max, Team, Enterprise ✱                                 | Free, Pro, Max, Team, Enterprise ✱                                          | Available to Claude Code users                                             |

> ✱ **Plan availability (claude.ai / Desktop):** Custom skills (upload your own) are available on all plans including free. Verified: support.claude.com, 2026-03-26.
>
> ✱ **Skill description cap (Claude Code):** Descriptions longer than 250 characters are truncated in the skill listing to reduce context usage. The budget scales dynamically at 1% of context window with an 8,000-character fallback. Front-load key use cases. Verified: code.claude.com/docs/en/skills, 2026-04-06.
>
> ✱ **Plugin marketplace (Claude Code):** Skills can be bundled inside plugins and distributed via the official Anthropic marketplace or custom org marketplaces. `/plugin` command browses and installs from marketplace. Verified: code.claude.com/docs/en/plugins, 2026-04-06.
>
> ✱ **Skills in Office add-ins (Claude Desktop):** The Excel and PowerPoint Claude add-ins added skills support in March 2026. Skills authored in Customize > Skills are available within these add-ins. Verified: support.claude.com release notes March 11 2026.

---

## 5. Skill Invocation Control (Claude Code only)

| Frontmatter field                | Effect                                                              | Use case                                                        |
|:-------------------------------- |:------------------------------------------------------------------- |:--------------------------------------------------------------- |
| *(none — default)*               | Both user and Claude can invoke; description in context always      | General-purpose reference or task skills                        |
| `disable-model-invocation: true` | Only user can invoke via `/skill-name`; description removed from context | Side-effect workflows: `/deploy`, `/commit`, `/send-slack-message` |
| `user-invocable: false`          | Only Claude can invoke; hidden from `/` menu                        | Background knowledge; not meaningful as a user action           |
| `context: fork`                  | Runs in isolated subagent; results returned to main session         | Long autonomous tasks needing isolated context                  |
| `agent: <n>`                     | Companion to `context: fork` — specifies subagent type: `Explore`, `Plan`, `general-purpose`, or any custom agent ✱ | Codebase research (`Explore`), planning, or custom agents |
| `paths: <glob>`                  | Auto-activates only when Claude works with files matching the glob  | Scoping a skill to specific file types or directories           |
| `allowed-tools: <tools>`         | Restricts which tools Claude can use while this skill is active     | Read-only skills: `allowed-tools: Read Grep Glob`               |
| `model: <alias>`                 | Overrides the model used when this skill runs                       | Route heavy skills to `opus`, lightweight to `haiku`            |
| `effort: <level>`                | Overrides effort level for this skill (`low`/`medium`/`high`/`max`) | Force extended thinking for a specific skill                    |
| `hooks:`                         | Lifecycle hooks scoped to this skill only                           | Run linter after every edit made by this skill                  |
| Shell injection `` !`cmd` ``     | Runs shell command before skill content is sent to Claude; output replaces the placeholder ✱ | Inject live PR diff, env state, or test results into skill prompt |

> ✱ `agent:` is a companion field to `context: fork`, not standalone. If `context: fork` is omitted, `agent:` has no effect. Verified: code.claude.com/docs/en/skills §Frontmatter reference, 2026-04-06.
>
> ✱ **Shell injection in skills:** The `` !`command` `` syntax in skill content executes a shell command before the skill is sent to Claude. Output replaces the placeholder — Claude sees the result, not the command. For multi-line commands, use a fenced ` ```! ` block. Disable with `disableSkillShellExecution: true` in managed settings. Verified: code.claude.com/docs/en/skills §Inject dynamic context, 2026-04-06.
>
> Note: Claude Desktop uses Anthropic's VM-based skills mechanism. The frontmatter fields in this table are Claude Code-specific — they are not applicable to claude.ai / Desktop skills uploaded via zip.

---

## 6. Commands (Claude Code)

| Aspect                     | Slash Commands (legacy)                          | Skills (current)                                       |
|:-------------------------- |:------------------------------------------------ |:------------------------------------------------------ |
| Location                   | `.claude/commands/*.md`                          | `.claude/skills/<n>/SKILL.md` ✱                        |
| Invocation                 | Manual only — you type `/command-name`           | Auto (Claude decides) + manual `/skill-name`           |
| Supports bundled files?    | No — single markdown file                        | Yes — `scripts/`, `examples/`, reference files         |
| Status                     | Merged into skills system — still fully supported | Recommended going forward                             |
| Same frontmatter support?  | Yes — same fields apply ✱                        | Yes                                                    |
| Name conflict resolution   | N/A                                              | Skill wins over command of same name ✱                 |

> ✱ "Custom commands have been merged into skills." A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. If a skill and command share a name, the skill takes precedence. Verified: code.claude.com/docs/en/skills, 2026-04-06.

---

## 7. Agents & Agentic Loop

| Concept                           | Claude.ai                                    | Claude Desktop                                                                      | Claude Code                                                                  |
|:--------------------------------- |:-------------------------------------------- |:----------------------------------------------------------------------------------- |:---------------------------------------------------------------------------- |
| Agentic by default?               | No — conversational (single turn)            | No for chat. Cowork (research preview) adds agentic capability for knowledge work ✱ | Yes — autonomous developer agent                                             |
| Has an agent loop?                | No                                           | Cowork only: perceive → act → observe → repeat in local VM                          | Yes — perceive → act → observe → repeat                                      |
| Decides next action autonomously? | No                                           | Cowork only: yes, within task scope                                                 | Yes                                                                          |
| Number of API calls per task      | 1                                            | 1 (chat) / N for Cowork tasks                                                       | N — unknown upfront, goal-directed                                           |
| Stops when?                       | After one response                           | Chat: after one response. Cowork: when task is complete                             | When Claude decides the goal is achieved (`end_turn`)                        |
| Tool results fed back into loop?  | No                                           | Cowork only: yes                                                                    | Yes — tool results re-enter conversation history each turn                   |
| Permission modes                  | N/A                                          | N/A                                                                                 | `default`, `acceptEdits`, `plan`, `auto`, `bypassPermissions`, `dontAsk` ✱   |
| Plan mode                         | N/A                                          | N/A                                                                                 | Yes — Claude presents plan for approval before acting; read-only exploration ✱ |
| Hooks system                      | N/A                                          | N/A                                                                                 | Yes — shell commands fired at lifecycle events in the agent loop ✱           |
| Agent teams                       | N/A                                          | N/A                                                                                 | Yes — experimental; multiple sessions with peer-to-peer messaging ✱          |
| Computer use                      | N/A                                          | Yes — Cowork computer use (research preview, Pro/Max) ✱                             | Yes — Claude Code Desktop app, research preview, Pro/Max ✱                   |
| Context management across turns?  | N/A                                          | Cowork: automatic within task; no `/compact` equivalent                             | Automatic compaction at ~95% capacity; `/compact` manual trigger             |
| Built-in subagent types           | None                                         | None in chat. Cowork spawns subtasks internally                                     | `Explore` (read-only), `Plan`, `general-purpose`, custom agents              |
| Execution environment             | Anthropic's cloud                            | Chat: cloud. Cowork: local VM on user's machine ✱                                   | User's machine (or cloud session via Claude Code web/Desktop app)            |

> ✱ **Cowork** is a research preview feature in Claude Desktop that brings Claude Code-style agentic capabilities to knowledge work (documents, files, research). It runs in a local VM, supports MCP connectors, and requires a Pro, Max, Team, or Enterprise plan. It is distinct from Claude Code. Computer use in Cowork launched March 23 2026. Verified: support.claude.com/en/articles/13345190, 2026-04-06.
>
> ✱ **Permission modes (Claude Code):** Control how tool-use approvals are handled per session or per subagent. `default` = standard prompts. `acceptEdits` = auto-accept file edits. `plan` = read-only exploration before acting. `auto` = background classifier reviews commands. `bypassPermissions` = skip all prompts (dangerous; container/VM use only). `dontAsk` = auto-deny unapproved tools. Set via `defaultMode` in `settings.json` or `--permission-mode` CLI flag. Verified: code.claude.com/docs/en/permission-modes, 2026-04-06.
>
> ✱ **Hooks system (Claude Code):** Shell commands fired at specific agent loop events. Key events: `PreToolUse` (before a tool executes), `PostToolUse` (after), `Stop` (session end), `SubagentStart`, `SubagentStop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`. Exit code 2 blocks the triggering action and feeds feedback back to Claude. Configured in `settings.json` or skill/subagent frontmatter. Verified: code.claude.com/docs/en/settings §Hook configuration, 2026-04-06.
>
> ✱ **Agent teams (Claude Code):** Multiple independent Claude Code sessions with a lead agent coordinating work and teammates communicating peer-to-peer. Unlike subagents (single session), teammates run in separate context windows. Experimental — enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Verified: code.claude.com/docs/en/agent-teams, 2026-04-06.
>
> ✱ **Computer use (Claude Code Desktop):** Research preview on macOS and Windows. Requires Pro or Max plan. Not available on Team or Enterprise plans. Claude controls screen with Accessibility + Screen Recording permissions. Verified: code.claude.com/docs/en/desktop, 2026-04-06.

---

## 8. SDK & Programmatic Access

| Concept                           | Claude.ai     | Claude Desktop | Claude Agent SDK                                                                           |
|:--------------------------------- |:------------- |:-------------- |:------------------------------------------------------------------------------------------ |
| SDK package (Python)              | N/A (UI only) | N/A (UI only)  | `claude-agent-sdk` — `from claude_agent_sdk import query, ClaudeAgentOptions` ✱            |
| SDK package (TypeScript)          | N/A           | N/A            | `@anthropic-ai/claude-agent-sdk` — npm package; GitHub repo: `anthropics/claude-agent-sdk-typescript` ✱ |
| Former name                       | N/A           | N/A            | `@anthropic-ai/claude-code-sdk` — renamed; migration guide available ✱                     |
| Use Claude Code system prompt?    | No            | No             | Yes — handled automatically by SDK (no manual `preset` field) ✱                            |
| Append to system prompt?          | No            | No             | Via `ClaudeAgentOptions` — see SDK docs for current parameter names                        |
| Load `CLAUDE.md` from filesystem? | No            | No             | Yes — requires `setting_sources=["project"]` (Python) / `settingSources: ['project']` (TS) |
| Load skills from filesystem?      | No            | No             | Yes — requires `setting_sources=["project", "user"]` + `allowed_tools=["Skill"]`           |
| Agent loop managed by SDK?        | No            | No             | Yes — `query()` async generator; `ClaudeSDKClient` for bidirectional + custom tools ✱      |
| Custom tools and hooks in SDK?    | N/A           | N/A            | Yes — `ClaudeSDKClient` supports in-process MCP tool functions and hook callbacks ✱        |
| Third-party provider support?     | N/A           | N/A            | Yes — AWS Bedrock, Google Vertex AI, Microsoft Foundry via env vars ✱                      |
| Use pre-built API skills?         | N/A           | N/A            | Via Messages API (beta) — `container: {"skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]}` + `code_execution` tool ✱ |
| Context auto-managed?             | No            | No             | Yes — automatic compaction built into SDK                                                  |

> ✱ **SDK rename (April 2026):** The Claude Code SDK has been renamed to the **Claude Agent SDK**. Python package: `claude-agent-sdk` (`pip install claude-agent-sdk`); import as `from claude_agent_sdk import query, ClaudeAgentOptions`. TypeScript npm package: `@anthropic-ai/claude-agent-sdk` (`npm install @anthropic-ai/claude-agent-sdk`); GitHub repo: `anthropics/claude-agent-sdk-typescript`. The old `claude-code-sdk` (Python) is officially deprecated on PyPI with a redirect notice. The `systemPrompt: { preset: "claude_code" }` pattern from earlier doc versions is not part of the current SDK surface. Verified: pypi.org/project/claude-agent-sdk, npmjs.com/package/@anthropic-ai/claude-agent-sdk, platform.claude.com/docs/en/agent-sdk/overview, 2026-04-06.
>
> ✱ **`query()` vs `ClaudeSDKClient`:** `query()` is the simple async generator for fire-and-receive use. `ClaudeSDKClient` enables bidirectional interactive conversations, custom in-process MCP tool functions (decorated with `@tool`), and hook callbacks. Use `ClaudeSDKClient` when your agent needs to offer tools back to Claude or intercept lifecycle events. Verified: github.com/anthropics/claude-agent-sdk-python, 2026-04-06.
>
> ✱ **Third-party providers:** Set `CLAUDE_CODE_USE_BEDROCK=1` for AWS Bedrock, `CLAUDE_CODE_USE_VERTEX=1` for Google Vertex AI, `CLAUDE_CODE_USE_FOUNDRY=1` for Microsoft Foundry. Credentials must be configured separately for each provider. Verified: platform.claude.com/docs/en/agent-sdk/overview, 2026-04-06.
>
> ✱ **Skills via Messages API (beta):** Skills require three beta headers (`code-execution-2025-08-25`, `skills-2025-10-02`, and optionally `files-api-2025-04-14`), the `code_execution` tool in the request, and the `container` parameter. Full shape: `container={"skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]}`. Up to 8 skills per request. Must use `client.beta.messages.create`, not `client.messages.create`. Verified: platform.claude.com/docs/en/build-with-claude/skills-guide, 2026-04-06.

---

## 9. Subagents (Claude Code only)

| Concept                        | Detail                                                                                                                              |
|:------------------------------ |:----------------------------------------------------------------------------------------------------------------------------------- |
| Location                       | `~/.claude/agents/` (user) or `.claude/agents/` (project) — markdown files with YAML frontmatter                                   |
| Purpose                        | Independent Claude instance with its own tool scope and system prompt                                                               |
| Difference from skills         | Skills = portable expertise injected into current context. Subagents = separate Claude instances with isolated tool access          |
| Difference from agent teams    | Subagents run within one session and cannot spawn other subagents. Agent teams are separate sessions with peer-to-peer messaging ✱  |
| Execution mode                 | Foreground (blocking, passes permission prompts through) or background (concurrent, permissions pre-approved at spawn time) ✱       |
| Can use skills?                | Yes — preloaded via `skills:` frontmatter; full content injected at startup, not loaded on demand ✱                                 |
| Persistent memory?             | Yes — `memory: user|project|local` frontmatter gives subagent a cross-session memory directory ✱                                    |
| Isolated worktree support?     | Yes — `isolation: worktree` in frontmatter gives subagent an isolated git worktree copy                                             |
| Model override?                | Yes — `model: sonnet|opus|haiku|<full-id>` frontmatter; default is `inherit` from parent session                                    |
| Max turns?                     | Configurable — `maxTurns:` frontmatter caps agentic turns before subagent stops                                                     |
| Explicit invocation?           | `@agent-name` mention in prompt guarantees that subagent runs; `--agent <n>` runs entire session as that subagent ✱                 |
| Defined programmatically?      | Yes — via Agent SDK `ClaudeAgentOptions` / `--agents` CLI flag (JSON), or filesystem `.claude/agents/` ✱                           |

> ✱ **Agent teams vs subagents:** Subagents work within a single session and cannot spawn other subagents. Agent teams are independent Claude Code sessions coordinated by a lead, with peer-to-peer messaging between teammates. Use subagents for focused, isolated tasks; use agent teams when workers need to share findings and coordinate independently. Verified: code.claude.com/docs/en/sub-agents, code.claude.com/docs/en/agent-teams, 2026-04-06.
>
> ✱ **Background subagents:** Background subagents run concurrently. Claude Code prompts for any needed tool permissions before spawning; the subagent then runs without interruption. A background subagent that needs clarification auto-denies that tool call but continues. Press Ctrl+B to background a running task. Verified: code.claude.com/docs/en/sub-agents §Run subagents in foreground or background, 2026-04-06.
>
> ✱ **Subagent persistent memory:** `memory: user` stores to `~/.claude/agent-memory/<name>/`; `memory: project` to `.claude/agent-memory/<name>/`; `memory: local` to `.claude/agent-memory-local/<name>/`. First 200 lines / 25KB of `MEMORY.md` in that directory load at subagent startup. Verified: code.claude.com/docs/en/sub-agents §Enable persistent memory, 2026-04-06.
>
> ✱ **Subagents and skills:** A subagent can preload skills via a `skills:` list in its frontmatter — full skill content is injected at subagent startup rather than loaded on demand. Verified: code.claude.com/docs/en/sub-agents §Preload skills into subagents, 2026-04-06.
>
> ✱ **Explicit invocation and session-wide subagent:** `@agent-name` in the prompt (typeahead supported) guarantees that subagent runs for that task. `claude --agent <n>` runs the entire session under that subagent's system prompt, replacing the default Claude Code system prompt. Set `agent` in `.claude/settings.json` to make it the default for a project. Verified: code.claude.com/docs/en/sub-agents §Invoke subagents explicitly, 2026-04-06.
>
> ✱ **Subagents defined programmatically:** CLI flag `--agents` accepts JSON with the same frontmatter fields as file-based subagents. SDK callers use `ClaudeAgentOptions` with `cwd` and `setting_sources` to load filesystem-based subagents; inline definitions can be passed programmatically. Verified: code.claude.com/docs/en/sub-agents §CLI-defined subagents, 2026-04-06.

---

## 10. Permissions & Security

| Concept                           | Claude.ai                          | Claude Desktop                                                                  | Claude Code                                                                        |
|:--------------------------------- |:---------------------------------- |:------------------------------------------------------------------------------- |:---------------------------------------------------------------------------------- |
| File access control               | Controlled by Anthropic            | Controlled by Anthropic; local files accessible only via MCP tools user enables | `permissions.allow` / `.deny` / `.ask` rules in `settings.json` ✱                 |
| Permission rule evaluation order  | N/A                                | N/A                                                                             | `deny` rules first, then `ask`, then `allow` — first match wins ✱                  |
| MCP tool access                   | Remote connectors via Customize > Connectors (cloud-brokered) | Local MCP via Desktop extensions (`.mcpb`) + remote connectors | Local and remote MCP servers; configured in `.mcp.json` or `~/.claude.json`       |
| Bash sandbox                      | N/A                                | N/A                                                                             | Optional OS-level isolation for bash commands: `sandbox.enabled: true` ✱           |
| Org-level policy enforcement      | Via Team/Enterprise plan           | Via Team/Enterprise plan; Desktop extension allowlist managed by org owners     | Managed settings — multiple delivery mechanisms ✱                                  |
| Managed settings override user?   | N/A                                | N/A (policy enforced at Anthropic platform level, not local settings files)     | Yes — Managed > CLI args > Local > Project > User ✱                                |
| Skill execution security          | VM sandbox; upload reviewed by user | VM sandbox; same as claude.ai                                                  | Skills execute arbitrary code via bash — only use trusted sources                  |
| Network access in skills          | Controlled by Anthropic (VM)       | Controlled by Anthropic (VM)                                                    | Full — same as any program on your machine                                         |
| Sensitive file protection pattern | N/A                                | N/A                                                                             | `permissions.deny: ["Read(./.env)", "Read(./.env.*)"]`                             |

> ✱ **Permission rules (Claude Code):** `permissions.allow`, `permissions.deny`, and `permissions.ask` accept rule arrays. Syntax: `Tool` (all uses) or `Tool(specifier)` (e.g. `Bash(npm run *)`, `Read(./.env)`). Rules evaluate in order: deny first, then ask, then allow — first match wins. Arrays merge across settings scopes. Verified: code.claude.com/docs/en/settings §Permission settings, 2026-04-06.
>
> ✱ **Sandbox (Claude Code):** `sandbox.enabled: true` in `settings.json` activates OS-level isolation for bash commands — restricts filesystem writes/reads and network access to declared allowlists. Separate from Claude's tool-level permission rules: sandbox applies to all subprocess commands (e.g. `kubectl`, `terraform`), not just Claude's file tools. Available on macOS, Linux, WSL2. Verified: code.claude.com/docs/en/settings §Sandbox settings, 2026-04-06.
>
> ✱ **Claude Code managed settings delivery:** Multiple mechanisms: server-managed (via Claude.ai admin console), MDM/OS-level policy (macOS plist, Windows registry), or file-based. Linux/WSL path: `/etc/claude-code/managed-settings.json`; macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`; Windows: `C:\Program Files\ClaudeCode\managed-settings.json`. Within the managed tier, server-managed takes precedence over endpoint-managed; sources do not merge across tiers. Verified: code.claude.com/docs/en/settings, 2026-04-06.

---

## 11. Claude Code Surfaces (April 2026)

Claude Code is no longer terminal-only. All surfaces share the same engine — `CLAUDE.md` files, settings, and MCP servers work across all of them.

| Surface             | Access point                            | Notes                                                                           |
|:------------------- |:--------------------------------------- |:------------------------------------------------------------------------------- |
| Terminal CLI        | `claude` command after install          | Full-featured; supports piping, scripting, CI/CD                                |
| VS Code extension   | Extensions marketplace                  | Inline diffs, @-mentions, plan review, conversation history in editor           |
| JetBrains plugin    | JetBrains Marketplace                   | IntelliJ IDEA, PyCharm, WebStorm; interactive diff and selection context        |
| Desktop app         | Standalone download (macOS / Windows)   | Visual diff review, multiple sessions, scheduled tasks, cloud sessions — distinct from the Claude Desktop chat app |
| Web                 | `claude.ai/code`                        | No local setup; long tasks, parallel tasks, repos not checked out locally       |
| iOS / Android       | Claude mobile app                       | Continue sessions started elsewhere; start web sessions; Remote Control access  |
| Slack integration   | `@Claude` mention in Slack              | Route bug reports → pull requests; team task dispatch                           |
| Chrome extension    | Browser extension (beta)                | Debug live web applications; browser context access                             |
| Remote Control      | Any browser or phone                    | Continue an active local session from another device                            |
| Channels            | `--channels` flag; Telegram/Discord/iMessage/webhooks ✱ | Push external events into a running Claude Code session     |

> ✱ **Channels:** External event sources (Telegram, Discord, iMessage, or custom webhooks) can push messages into a running Claude Code session via the `--channels` flag. Channel plugins are allowlisted by managed settings in enterprise deployments. Verified: code.claude.com/docs/en/overview integration table, 2026-04-06.

---

## 12. Scheduling & Automation (Claude Code only)

| Mechanism               | Where it runs              | How to create                        | Use case                                        |
|:----------------------- |:-------------------------- |:------------------------------------ |:----------------------------------------------- |
| Cloud scheduled tasks   | Anthropic-managed infra    | Web UI, Desktop app, or `/schedule`  | Runs when your machine is off; PR reviews, CI   |
| Desktop scheduled tasks | Your machine               | Desktop app                          | Requires machine on; accesses local files       |
| `/loop` command         | Current CLI session        | CLI — `/loop [interval] <prompt>`    | Repeats a prompt within a session (polling)     |
| CLI pipe / scripting    | Your machine or CI runner  | Shell: `tail log \| claude -p "..."` | One-shot automation; log analysis; bulk ops     |
| GitHub Actions          | GitHub CI                  | Workflow YAML                        | PR review automation, issue triage              |
| GitLab CI/CD            | GitLab CI                  | Pipeline YAML                        | Same as GitHub Actions, on GitLab               |
| Channels                | Claude Code session        | `--channels` + plugin config         | React to external events: webhooks, chat apps   |
| Agent teams             | Multiple local sessions    | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | Parallel autonomous work across independent agents |

> Verified: code.claude.com/docs/en/overview, code.claude.com/docs/en/skills (`/loop` is now a bundled skill), code.claude.com/docs/en/agent-teams, 2026-04-06.

---

## Quick Mental Model

| Question                                    | Claude.ai                                               | Claude Desktop                                                             | Claude Code                                                                  |
|:------------------------------------------- |:------------------------------------------------------- |:-------------------------------------------------------------------------- |:---------------------------------------------------------------------------- |
| Who is Claude?                              | Configured by Project Instructions                      | Configured by Custom Instructions (appended to internal system prompt)     | Configured by Anthropic's internal system prompt + `--append-system-prompt`  |
| What should Claude know about this project? | Configured by Project Instructions + uploaded knowledge | Configured by Project Instructions + uploaded knowledge                    | Configured by `CLAUDE.md` (user message, not system prompt injection)        |
| What has Claude learned about this project? | Configured by Memory system                             | Configured by Memory system (same account, shared memory)                  | Configured by `MEMORY.md` (Auto memory — Claude writes it)                   |
| What can Claude do?                         | Configured by plan settings                             | Configured by plan settings + MCP extensions + Cowork (agentic tasks)      | Configured by `settings.json` permissions + permission modes + sandbox       |
| What does Claude know how to do?            | Configured by Skills (uploaded zip)                     | Configured by Skills (same as claude.ai) + Desktop extensions (MCP)        | Configured by Skills (filesystem `.claude/skills/`)                          |
| How does Claude connect to external tools?  | Remote MCP connectors (cloud-brokered)                  | Local MCP Desktop extensions + remote connectors                           | Local + remote MCP servers via `.mcp.json`                                   |
| Who drives the conversation?                | You                                                     | You (chat) / Claude (Cowork tasks)                                         | Claude — goal-directed agent loop                                            |
| What orchestration is available?            | None                                                    | Cowork multi-step tasks; Dispatch mobile-to-desktop                        | Subagents, agent teams (experimental), hooks                                 |
| Where does work live?                       | Anthropic's cloud                                       | Anthropic's cloud (chat); your machine (Cowork files)                      | Your repo                                                                    |
| Windows install?                            | Native app                                              | Native app (MSIX or direct installer)                                       | Native (Git for Windows required) — WSL optional                            |
| Where can I run it?                         | claude.ai (web / mobile)                                | Claude Desktop app (macOS / Windows)                                        | Terminal, VS Code, JetBrains, Desktop app, Web, iOS, Slack, Chrome, CI/CD   |

---

*Verified against docs.claude.com, code.claude.com, and support.claude.com — April 2026.*
*✱ marks corrections or additions from prior version of this document.*
*Last updated: 2026-04-06*

*Changes from v1.4:*
*— §2: `--system-prompt` (replace) vs `--append-system-prompt` (append) distinguished. CLAUDE.md delivery-as-user-message row added.*
*— §3: Memory import/export, incognito chats, and past-chat search rows added for claude.ai / Desktop.*
*— §4: Plugin marketplace distribution row added (Claude Code). Skills in Office add-ins row added (Desktop).*
*— §5: `allowed-tools:`, `model:`, `effort:`, `hooks:`, and shell injection rows added.*
*— §7: Permission modes, plan mode, hooks system, agent teams, computer use, and improved compaction row added.*
*— §8: `query()` vs `ClaudeSDKClient` distinction added. Third-party provider support row added.*
*— §9: Major expansion — agent teams distinction, background execution, persistent memory, model override, maxTurns, @-mention / --agent invocation.*
*— §10: `permissions.allow` / `.ask` rows added. Rule evaluation order row added. Sandbox row added.*
*— §11: Channels surface row added.*
*— §12: Channels and agent teams rows added.*
*— Quick Mental Model: MCP row added; orchestration row added; CLAUDE.md delivery note corrected; permissions/sandbox noted.*

| Field        | Value                  |
|--------------|------------------------|
| Version      | 1.5                    |
| Last Updated | 2026-04-06             |
| Status       | Review                 |
