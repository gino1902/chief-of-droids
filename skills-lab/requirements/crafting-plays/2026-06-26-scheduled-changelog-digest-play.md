# Scheduled changelog digest play

> Stand up a recurring, self-hosted, AI-summarised email digest of an external
> changelog, delivered to a personal mailbox on a chosen cadence.
>
> ⚠️ Unverified. Treat as provisional until validated against a second instance.

## When to trigger

A user wants to stay up to date with a source that changes over time, without checking it by hand, and wants the update pushed to them on a schedule rather than pulled. The payload is low sensitivity (public release notes, a changelog, a docs feed), and the user is happy to own the accounts and keys behind it.

Recognition signal: the request is "send me X every N weeks so I do not have to look", where X is a curated summary of what changed in some external source.

Concrete examples:
- "Email me the new Claude Code major features every 2 weeks." (the originating session)
- "Send me a weekly digest of a competitor's changelog."
- "Once a month, summarise what changed in a framework's release notes."
- "Notify me when a public API I depend on ships breaking changes, batched fortnightly."

## Why it matters

It removes a recurring manual chore and replaces it with a curated, AI-filtered summary that arrives on its own. The dominant value is the deliverable: a working, configurable pipeline (scheduler, gather step, new-item detection, AI summary, email) that the user owns end to end and can re-point at other sources by editing one file. The problem it solves is staying current on a moving source at a cadence the user sets, without standing up bespoke infrastructure each time.

## The play

### Optimal workflow

1. Pin down the recurring need: the source, the cadence, the recipient, and the output format. Reuse the format from the session that already produced the content once, so the digest matches something the user has approved.
2. Decompose into the fixed pipeline: trigger, gather, detect what is new, summarise, deliver. Every option below is a different way to host the same five steps.
3. Run the compliance and data-residency check before choosing architecture. Establish whether this is personal or corporate, who the data controller is, where secrets may live, and whether a personal third-party account is allowed. Re-run this check whenever the user clarifies the data's nature.
4. Present architecture options with honest pros and cons, gated by the compliance result. The axes that matter are where the scheduler runs, where the secret lives, and whose identity owns it.
5. Probe enablers concretely rather than assume. Test outbound network egress, available schedulers, reachability of the AI and email endpoints, and any managed-settings restrictions, before committing.
6. Scaffold a standalone repo with behaviour in a single config file, identity drawn from the CI context at run time, and secrets kept out of code entirely.
7. Make cadence config-driven: run the check daily and gate the actual send on a `last_sent` value plus a `cadence_days` setting. This sidesteps cron's lack of a clean fortnightly expression and daylight-saving drift.
8. Verify offline before any key exists: syntax check, config parse, and a live run of the data-gathering step (changelog fetch plus release dates).
9. Hand the account and secret steps to the user with exact, copy-ready instructions, since these need interactive logins the agent cannot perform.
10. Test via manual dispatch: a dry-run preview first, then a real send, reading the run log to diagnose. Use distinct log lines for "previewed" versus "sent" so the two are never confused.

### Critical moves

| Move | Why it is load-bearing |
| :--- | :--- |
| Separate compliance from architecture, and redo it when the data's nature changes | When the user clarified the email was personal, not corporate, the recommended option flipped. Running on a corporate account would have leaked personal data inward into employer-visible tooling. |
| Behaviour in config, identity from CI context, secrets outside code | Keeps the repo portable and shareable, and is what let the GitHub identity stay out of the config entirely. |
| Cadence in config, not cron | A daily check plus a `last_sent` gate gives exact fortnightly behaviour with no cron month-boundary or DST problems. |
| New-item detection via release dates plus a committed state file | Querying npm publish times windows the changelog precisely, and the `last_sent` state file stops repeats and gaps across runs. |
| Dry-run-then-send test protocol with distinct log lines | The real send only works if `dry_run` is off, and a green dry run looks identical to a real send unless the log distinguishes them. |

### Pits to avoid

- Do not scaffold the project inside an unrelated existing repo. The chosen path sat inside a corporate repo, so it had to become a standalone git repo and be gitignored from the parent. GitHub Actions also only runs workflows at a repo root, so a subfolder workflow would never fire.
- Do not let the commit author default to the corporate email on a personal project. The first commit carried the sqli email and had to be reset to the GitHub no-reply address.
- Do not assume a card on file means API credits. The Anthropic Console API is prepaid. The first real summarise call failed with a 400 "credit balance is too low" despite a card being present. Buy credits or enable auto-reload.
- Do not confuse the API key with the Organization ID. The key is the `sk-ant-` secret used to authenticate. The org ID is a non-secret identifier and is not needed.
- Do not assume a claude.ai login grants API access. The Console API is a separate product with separate billing.
- Remember API keys are shown only once. If not saved at creation, they cannot be retrieved and a new one must be made.
- Watch the free email-sender restriction. Resend's built-in `onboarding@resend.dev` sender only delivers to the account's own email until a domain is verified. Signing up via GitHub can make the account email differ from the intended recipient, so a send to the wrong address silently does not arrive.
- Do not trust a green run as proof of delivery. A run with `dry_run` still on exits green with `sent=false` and sends nothing. Confirm with the explicit log line and the provider's send log.
- Do not try to push from the agent's shell. No reachable key authenticated to GitHub there, so the push had to run in the user's own terminal.
- Do not chase a key by fingerprint that is not present on the machine. Time was lost hunting a key whose private half lived in an unreachable agent.
- Know the GitHub SSH signal: "Server accepts key" followed by "Permission denied (publickey)" means the key format is valid but the public key is not registered on the account. The fix is adding the key on GitHub, not generating a new one.
- The Node 20 deprecation warning in the Actions log is cosmetic and not the cause of a failed run.

## When to use it

- The need is genuinely recurring, not a one-off.
- The payload is public or low sensitivity.
- The user can hold their own accounts and keys (AI provider, email provider, code host).
- The source exposes a machine-readable changelog and a reliable way to date releases.
- Reliable unattended execution matters, so a hosted CI runner fits.

## When not to use it

- The request is a single summary. Just produce it inline.
- The payload contains sensitive or corporate data. Then controllership, a data-processing agreement, and residency dominate, which is a different and heavier play.
- Sub-hour latency is required. A daily-check cadence is too coarse.
- Org policy forbids personal third-party keys, or mandates the corporate account. The personal-CI shape no longer applies.
- A managed scheduler or notification product already covers this need.
- The user wants zero ongoing cost and will not hold an AI key. Drop AI summarisation and the play loses its main value.

## Expected outcome

A standalone repo that, on the user's cadence, emails an AI-filtered digest of the tracked source to a personal mailbox, owned entirely by the user and re-pointable by editing one config file.

Checkable in concrete terms:
- A manual dry run prints the grouped digest in the run log with no email sent.
- A manual real send ends with an explicit "sent" line and lands a test email in the recipient inbox.
- Editing `cadence_days` or adding a source entry changes behaviour with no code change.
- No secret or personal address appears anywhere in the committed code.

## Tradeoffs

### Architecture and hosting

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Where the scheduler runs | Corporate cloud routine, least setup | Local machine, full control but only runs when awake | Personal CI (GitHub Actions), reliable and off the corporate account |
| Build location | Inside the existing repo, convenient | Standalone repo, more setup | Standalone repo, required by the Actions-at-root rule and by isolation from corporate code |
| Identity source | Declared in config | Drawn from CI context at run time | CI context, so no GitHub identity sits in the repo |

### Data and delivery

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Email delivery channel | MCP or Gmail connector, no key to store | Transactional API (Resend), needs a key | Transactional API, reliable in headless runs where connectors may be absent |
| Secret storage | Embedded in the job config | CI encrypted secret | CI encrypted secret, a proper store rather than plaintext in config |
| New-item detection | Stateless date window | Committed `last_sent` state file | State file, precise across month boundaries where a fixed window misses a day |
| Cadence mechanism | Cron expression | Daily check plus config gate | Config gate, exact fortnightly with no DST or month-length problems |
| Summarisation | AI summary | Keyword filtering, no key | AI summary, for quality, at the cost of an API key and prepaid billing |

### Process

| Decision | Pole A | Pole B | Chosen position |
| :--- | :--- | :--- | :--- |
| Compliance timing | Assess after building | Assess before architecture | Before, and redone when the data's nature was clarified |
| Verification before keys | Trust it works once keys exist | Prove the non-key parts offline first | Offline proof first, so only billing and delivery remained to test |
| First send | Send directly | Dry-run preview, then send | Preview first, with distinct log lines to tell the two apart |

---

| Field        | Value      |
| :----------- | :--------- |
| Version      | 1.0        |
| Last Updated | 2026-06-26 |
| Status       | Draft      |
| Pairs with   | claude-code-digest repo (github.com/gino1902/claude-code-digest): config.yml, digest.mjs, .github/workflows/digest.yml |
