# Git hooks and code quality basics

A short guide to Git hooks and the tooling built around them: Husky, lint-staged, linters, formatters, and how the same checks run in CI. Covers a TypeScript/JavaScript and Python stack. Think of the whole thing as one idea applied at different moments: run automated checks on your code before it goes anywhere.

## The big picture

Code quality checks run at three moments, each one a safety net behind the previous.

```
you save a file      →  editor runs the formatter (instant)
you run git commit   →  hook runs lint + quick tests (seconds)
you push / open a PR →  CI runs everything (minutes)
```

Hooks catch problems early on your machine. CI is the real gate because hooks can be skipped. The editor step is comfort, not enforcement.

## What is a Git hook

A hook is a script that Git runs automatically at a lifecycle event. If the script exits with a non-zero code, Git aborts the operation.

The events you will actually use:

| Hook | Fires when | Typical use |
|------|-----------|-------------|
| `pre-commit` | before a commit is created | lint, format check, fast tests |
| `commit-msg` | after you write the message | enforce message conventions |
| `pre-push` | before `git push` | slower test suites |

Natively, hooks live in `.git/hooks/` as plain executable scripts. Try it:

```bash
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
echo "running checks..."
exit 1   # non-zero = commit blocked
EOF
chmod +x .git/hooks/pre-commit
git commit -m "test"   # blocked
```

The catch: `.git/` is never committed, so these scripts stay on your machine only. Your teammates get nothing. Every hook manager exists to solve exactly this problem.

## The linter and formatter layer

Before wiring hooks, you need something for them to run.

- A linter finds problems: unused variables, unreachable code, suspicious patterns. It reasons about the code.
- A formatter fixes style: indentation, quotes, line length. It only moves characters around.

Standard picks per language:

| Language | Linter | Formatter |
|----------|--------|-----------|
| JS / TS | ESLint | Prettier |
| Python | Ruff | Ruff (`ruff format`) |

Ruff covers both jobs in Python and has largely replaced the older Flake8 + Black combo because it is much faster.

### Minimal ESLint + Prettier setup (TS/JS)

```bash
npm install --save-dev eslint prettier typescript-eslint
```

```javascript
// eslint.config.js (flat config, the current format)
import tseslint from "typescript-eslint";

export default tseslint.config(
  ...tseslint.configs.recommended,
);
```

```json
// .prettierrc
{
  "singleQuote": true,
  "semi": true
}
```

```bash
npx eslint .              # find problems
npx prettier --write .    # fix formatting
```

### Minimal Ruff setup (Python)

```bash
pip install ruff
```

```toml
# pyproject.toml
[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I"]   # errors, pyflakes, import sorting
```

```bash
ruff check .        # lint
ruff format .       # format
```

## Husky: shared hooks for Node projects

Husky makes hooks part of the repo. It points Git at a committed `.husky/` directory instead of the untracked `.git/hooks/`.

```bash
npm install --save-dev husky
npx husky init
```

This does three things:

1. Creates `.husky/` with a sample `pre-commit` file.
2. Adds `"prepare": "husky"` to `package.json`, so every `npm install` activates the hooks.
3. Sets `core.hooksPath=.husky` in the local Git config.

A hook file is just shell commands. Since Husky v9 there is no boilerplate to source:

```bash
# .husky/pre-commit
npx lint-staged
```

```bash
# .husky/pre-push
npm test
```

Commit the `.husky/` directory. Anyone who clones and runs `npm install` gets the same hooks.

To skip a hook once (broken linter, emergency fix):

```bash
git commit --no-verify -m "hotfix"
```

This is why CI must repeat the same checks. A hook is a convenience, not a guarantee.

## lint-staged: only check what you touched

Running `eslint .` on a large repo at every commit is slow and noisy. lint-staged runs commands only on the files staged for this commit.

```bash
npm install --save-dev lint-staged
```

```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx,js}": ["eslint --fix", "prettier --write"],
    "*.py": ["ruff check --fix", "ruff format"],
    "*.{json,md,yml,yaml}": ["prettier --write"]
  }
}
```

Keys are glob patterns, values are commands to run on the matching staged files. With `--fix` and `--write`, small issues get repaired and re-staged automatically, so most commits just pass.

Wire it into the hook and you are done:

```bash
# .husky/pre-commit
npx lint-staged
```

## commitlint: enforce commit message style

Optional but common. It checks messages against the Conventional Commits format (`feat: ...`, `fix: ...`, `chore: ...`), which enables automated changelogs and semantic versioning later.

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional
echo "export default { extends: ['@commitlint/config-conventional'] };" > commitlint.config.js
```

```bash
# .husky/commit-msg
npx commitlint --edit "$1"
```

Now `git commit -m "stuff"` fails, `git commit -m "fix: handle empty payload"` passes.

## The Python-native alternative: pre-commit

If your repo is mostly Python (or polyglot without a `package.json`), the `pre-commit` framework is the better fit. It plays the same role as Husky + lint-staged combined, and it manages tool installation for you: each check declares its own repo and version, and the framework installs it in an isolated environment.

```bash
pip install pre-commit
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: check-yaml
      - id: check-added-large-files
```

```bash
pre-commit install          # writes the git hook
pre-commit run --all-files  # first run, whole repo
```

Like lint-staged, it only checks changed files on commit. Bypass is the same `--no-verify`.

Rule of thumb: Node project, use Husky + lint-staged. Python project, use pre-commit. Mixed repo, pick one as the single hook owner (two tools both claiming `pre-commit` will conflict) and have it call the other stack's commands.

> ⚠️ Unverified — pin `rev` values to current releases when you set this up, the ones above age quickly.

## Running the same checks in CI

CI is where the checks become mandatory. The principle: whatever the hook runs, CI runs too, on all files, on every push and pull request.

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint-node:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
      - run: npm ci
      - run: npx eslint .
      - run: npx prettier --check .
      - run: npm test

  lint-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff
      - run: ruff check .
      - run: ruff format --check .
```

Two details worth noticing:

- CI uses `--check` variants (`prettier --check`, `ruff format --check`) instead of fixing. CI should report, never mutate.
- `npm ci` instead of `npm install`: exact lockfile install, reproducible.

Then protect the branch: in GitHub, Settings → Branches → require status checks to pass before merging. That is the actual enforcement point of the whole chain.

If the repo uses `pre-commit`, CI gets even simpler because one action replays the whole config:

```yaml
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - uses: pre-commit/action@v3.0.1
```

## Putting it together

A sensible split of work across the three moments:

| Moment | Runs | Budget |
|--------|------|--------|
| editor save | formatter | instant |
| pre-commit hook | lint-staged (lint + format on changed files) | under 5 s |
| commit-msg hook | commitlint | instant |
| pre-push hook | fast test suite | under 1 min |
| CI | full lint, full format check, full tests, build | minutes |

The most common mistake is putting a full test suite in pre-commit. After the third 4-minute wait, developers start committing with `--no-verify` and the hook is dead. Keep pre-commit fast, push slow things to pre-push or CI.

## Common mistakes

- Editing `.git/hooks/` directly and wondering why teammates are unaffected. Use Husky or pre-commit.
- Forgetting that hooks need activation: `npm install` (Husky) or `pre-commit install` (pre-commit). A fresh clone has no hooks until then.
- Slow pre-commit hooks that train the team to use `--no-verify`.
- Hooks without matching CI checks. The hook is skippable, so alone it enforces nothing.
- Linter and formatter fighting each other (ESLint style rules vs Prettier). Disable ESLint's formatting rules and let Prettier own style entirely.
- Two hook managers installed at once, each overwriting the other's `pre-commit` entry point.

## Cheat sheet

| You want | You do |
|----------|--------|
| See native hooks | `ls .git/hooks/` |
| Shared hooks, Node repo | `npx husky init`, commit `.husky/` |
| Shared hooks, Python repo | `.pre-commit-config.yaml` + `pre-commit install` |
| Check only staged files | lint-staged in `.husky/pre-commit` |
| Enforce message format | commitlint in `.husky/commit-msg` |
| Skip a hook once | `git commit --no-verify` |
| Lint TS/JS | `npx eslint .` |
| Format TS/JS | `npx prettier --write .` |
| Lint + format Python | `ruff check .` and `ruff format .` |
| Enforce in CI | same commands with `--check`, then branch protection |

## Sources

- Git hooks reference: https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks
- Husky: https://typicode.github.io/husky
- lint-staged: https://github.com/lint-staged/lint-staged
- commitlint: https://commitlint.js.org
- Conventional Commits: https://www.conventionalcommits.org
- pre-commit framework: https://pre-commit.com
- ESLint: https://eslint.org/docs/latest
- Prettier: https://prettier.io/docs
- Ruff: https://docs.astral.sh/ruff/
- GitHub Actions workflow syntax: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
