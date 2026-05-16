# Gap Analysis — chief-of-droids-3-tiers-upgrade v01 / v02 / v03

Same substrate, same skill, three independent runs. Predictability is read from the variance across mechanical, structural, and interpretive dimensions.

## Headline counts

| Metric | v01 | v02 | v03 | Spread |
|:---|:---:|:---:|:---:|:---:|
| Total warnings (resolved + unresolved) | 48 | 39 | 22 | 2.2× |
| Unresolved warnings | 10 | 9 | 15 | 1.7× |
| Info events | 6 | 7 | 6 | low |
| Blocking | 0 | 0 | 0 | identical |
| Requirement rows (total) | 71 | 49 | 58 | 1.45× |

Total-warning spread is misleading on its own — v01 itemises per-glossary-term (29 warnings), v02 rolls them into one. Granularity of reporting is itself a predictability dimension; see Dimension 3 below.

## Requirement enumeration per category

| Category | v01 | v02 | v03 |
|:---|:---:|:---:|:---:|
| FR | 20 | 16 | 16 |
| IR-IN | 6 | 4 | ≥4 |
| IR-OUT | 6 | 3 | ≥4 |
| DR | 4 | 3 | 3 |
| TR | 3 | 2 | 3 |
| NFR | 5 | 2 | 4 |
| SEC | **N/A** | **3** | **3** |
| CON | 12 | 9 | 10 |
| ERR | 10 | 5 | 7 |
| OBS | 5 | 2 | ≥3 |

The FR axis is the most visible gap: v01 produced 25% more FRs than v02/v03. v01 also went substantially deeper on ERR (10 vs 5/7) and OBS (5 vs 2/≥3).

## Interpretive divergences (the real predictability cost)

### 1. SEC section — categorical semantic split

| Run | Behaviour | Justification cited |
|:---|:---|:---|
| v01 | Rendered `N/A` | "skill rule forbids synthesis" — no auth/encryption/audit signal in substrate |
| v02 | 3 SEC reqs | "drawn from governance / authoring rules" |
| v03 | 3 SEC reqs | "inferred from sentinel path convention + scope statement" |

This is a binary semantic split on the same substrate. v01 reads the no-synthesis rule strictly; v02/v03 reinterpret governance signals as SEC-class. Same skill, opposite output. **Highest-impact gap in the set.**

### 2. Title handling

| Run | Output |
|:---|:---|
| v01 | Kept "— Design Notes" suffix verbatim, flagged for confirmation |
| v02 | Stripped suffix → "Two-Tier CLAUDE.md Architecture" |
| v03 | Stripped suffix → "Two-Tier CLAUDE.md Architecture" |

Different reading of the same "use substrate H1 verbatim" rule. v01 preserves; v02/v03 normalise.

### 3. Finding granularity (Phase 3 — glossary)

| Run | Auto-derived glossary terms | Warnings emitted |
|:---|:---:|:---:|
| v01 | 29 | 29 (one per term) |
| v02 | ~all of 30 | 1 (rolled up) |
| v03 | 5 listed individually | 5 |

Same underlying observation ("auto-derived terms need user verification") reported at three different levels of granularity. Affects counts in summary tables and any downstream metric that treats warnings as atomic.

### 4. Compound-SHALL findings (EARS atomicity)

| Run | Entries flagged |
|:---|:---|
| v01 | FR-004, FR-010, FR-014, CON-004, ERR-002 (5) |
| v02 | CON-001, CON-004, CON-005 (3) |
| v03 | FR-016, CON-003, CON-004 (3) |

Only **CON-004 is common to all three**. ID drift across runs (FR-014 ≠ FR-016) compounds the problem: even when the same substrate sentence triggers a finding, it surfaces under a different requirement ID.

### 5. NFR-001 / NFR-002 swap

| Run | Reliability anchor (~92–93%) lands on | TBD lands on |
|:---|:---|:---|
| v01 | — | NFR-001 |
| v02 | NFR-001 (`≥ 92%`) | NFR-002 |
| v03 | NFR-002 (`92–93%`) | NFR-001 |

The substrate carries one quantitative signal and one qualitative obligation. All three runs find both, but the order they occupy NFR-001 vs NFR-002 is non-deterministic.

### 6. Categorisation of workspace-wins precedence and tool routing

| Run | Placement |
|:---|:---|
| v01 | FR-013 (with self-acknowledged "trivial no-op" tension) |
| v02 | FR-011 + CON-001/003; FR-015/016 (tool routing) flagged as possibly CON-class |
| v03 | Distributed; no specific FR/CON debate flagged |

FR-vs-CON categorisation surfaces as an open question in v02 only.

## Areas of strong agreement (predictable)

| Check | v01 | v02 | v03 |
|:---|:---:|:---:|:---:|
| No blocking issues | ✓ | ✓ | ✓ |
| ID format `<CAT>-NNN` valid | ✓ | ✓ | ✓ |
| ID sequences dense | ✓ | ✓ | ✓ |
| No duplicate IDs | ✓ | ✓ | ✓ |
| Phase 6 format pass | ✓ | ✓ | ✓ |
| Slug "3-tiers" vs substrate "two-tier" flagged | ✓ | ✓ | ✓ |
| Purpose paragraph requires user review | ✓ | ✓ | ✓ |
| NFR with TBD measurement flagged | ✓ | ✓ | ✓ |
| Glossary has auto-derived entries (somewhere) | ✓ | ✓ | ✓ |
| ERR entries use Unwanted-Behavior EARS + cross-link FR | ✓ | ✓ | ✓ |
| No RFC 2119 keywords leaked into EARS statements | ✓ | ✓ | ✓ |

Mechanical hygiene and substrate-anchored flags reproduce perfectly. The skill is deterministic on **what it parses**, non-deterministic on **what it synthesises**.

## Predictability verdict

**Low–medium.**

| Dimension | Predictability |
|:---|:---|
| Mechanical checks (ID format, density, duplicates, format pass) | **High** — perfect reproducibility |
| Substrate-anchored findings (purpose, slug, TBD NFR, glossary verify) | **High** — all three runs surface the same issues |
| Requirement count and category sizing | **Low** — 1.45× spread on total rows, 25% spread on FR |
| Synthesis-vs-N/A decisions (SEC the worst) | **Very low** — categorical splits on identical substrate |
| Specific entries flagged for compound EARS | **Low** — only CON-004 common across all three |
| Finding granularity (1 vs N warnings per observation) | **Low** — affects every summary count |
| ID assignment stability (which signal lands on which NNN) | **Low** — even when both runs flag the same thing, the ID differs |

## Recommendations to raise predictability

1. **SEC rule arbitration.** The skill needs an explicit rule for "governance/authoring obligations" — either they are SEC-class (and v01 is non-compliant) or they are not (and v02/v03 are over-synthesising). Current text leaves the judgement to the run.
2. **Title-suffix policy.** Decide whether "— Design Notes", "— Draft", "— Proposal" suffixes are stripped or preserved. Codify.
3. **Granularity rule for Phase 3.** Choose one of: per-term warnings (v01), rolled-up summary (v02), or short list (v03). Currently each run picks its own.
4. **Stable ID assignment.** Within a category, define an ordering rule (substrate document order? alphabetical by subject?) so that the same substrate sentence always lands on the same NNN.
5. **Atomic-SHALL pass should be exhaustive.** Three runs flagging different subsets means the pass is heuristic rather than mechanical. Either run a strict regex (`SHALL` occurrence count > 1 per requirement → flag) and accept the resulting volume, or define exceptions.
6. **Required FR / IR / NFR / CON sizing bands** would surface as test guards; currently a 25% delta on FR count passes silently.

---

| Field        | Value      |
|:-------------|:-----------|
| Version      | 1.0        |
| Last Updated | 2026-05-15 |
| Status       | Draft      |
