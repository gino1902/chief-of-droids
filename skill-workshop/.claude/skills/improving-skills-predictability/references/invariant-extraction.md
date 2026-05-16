# Invariant extraction heuristics

Goal: walk the substrate once and produce a set of invariants the downstream runs are expected to preserve. Keep the set small enough to enumerate in the report — prefer discriminating invariants over exhaustive ones. Target 20–60 invariants total across all classes.

## Five generic classes

### Domain concepts

Take what the substrate treats as a defined or recurring noun phrase:

- Capitalized multi-word phrases used three or more times.
- Glossary entries (any section titled "Glossary", "Terms", "Definitions", or bullet lists with the pattern `**Term** — definition`).
- Named architectural elements ("dispatcher", "two-tier model", "sentinel record" — substrate-specific).
- Numbered framings ("six-capability", "three-layer") — keep both the number and the noun.

For each concept, record: the literal phrase as written in the substrate, the line range, and whether the substrate provides a definition.

### Schemas

Treat as a schema:

- Any fenced code block tagged `json`, `yaml`, `yml`, `xml`, `mermaid`, `proto`, `sql`, `toml`.
- Any markdown table whose first row contains "field", "key", "column", "attribute", or similar.
- Any bullet list of the form `- field: type — description` (≥3 entries).

For each schema, record the schema name (nearest preceding heading), the field names in order, and the line range.

### Paths

Anything that looks like a filesystem path, URI, or anchor:

- Substrings matching `[a-zA-Z0-9._-]+/[a-zA-Z0-9._/-]+` inside code spans or backticks.
- URLs (`https?://…`).
- Anchor references (`#section-name`).
- Templated paths (`<placeholder>/file.md`).

Paths are byte-level invariants. Record the literal string.

### Verbatim strings

Any string the substrate appears to quote or treat as literal:

- Strings inside backticks that aren't paths or code identifiers.
- Strings inside double-quotation marks longer than one word.
- Error messages, prompt fragments, button labels, log lines.

Record the literal string and the line.

### Policies / constraints

Any sentence containing a modal keyword:

- `MUST`, `MUST NOT`, `SHALL`, `SHALL NOT`, `SHOULD`, `SHOULD NOT`, `MAY`, `WILL`, `WILL NOT`, and their lowercase equivalents when used in a normative context.

For each policy, record: the keyword, the subject of the sentence (1–6 words), and the line range. When a sentence carries multiple clauses joined by "and"/"or", split them — each clause is its own invariant.

## Pruning rules

After extraction, drop invariants that:

- Appear only in incidental prose (e.g., a domain concept used once in a passing sentence with no definition).
- Have a span longer than 300 characters (too coarse to score against).
- Are pure formatting artifacts (table separators, decorative dividers).

If the resulting set is fewer than 10 invariants, the substrate may be too thin to score predictability against — surface a warning in the report's preamble but continue.

## Recording format (in memory)

```
{
  "class": "concept | schema | path | verbatim | policy",
  "literal": "string as written in the substrate",
  "anchor": "1–6 word handle for the report table",
  "source_span": "lines L1–L2",
  "definition": "optional, only for concepts and schemas"
}
```
