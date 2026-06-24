# YAML basics

A short guide to YAML, the data format used by most config tools (Docker Compose, Kubernetes, GitHub Actions, Ansible). YAML stands for "YAML Ain't Markup Language". Think of it as a human-friendly way to write structured data, like a JSON that you can actually read.

## Core rules

- Indentation is meaningful. Use spaces, never tabs. Two spaces per level is the common convention.
- Structure comes from key-value pairs, lists, and nesting.
- Files end in `.yaml` or `.yml` (both work, pick one and stay consistent).
- Comments start with `#`.

```yaml
# This is a comment
name: my-app
version: 1.0
enabled: true
```

## The three building blocks

### 1. Key-value pairs (mappings)

The most common structure. A key, a colon, a space, then the value.

```yaml
host: localhost
port: 8080
debug: false
```

The space after the colon matters. `port:8080` is wrong, `port: 8080` is right.

### 2. Lists (sequences)

A dash and a space for each item.

```yaml
fruits:
  - apple
  - banana
  - cherry
```

### 3. Nesting

Combine the two by indenting. This is where most of YAML's power (and most beginner errors) come from.

```yaml
server:
  host: localhost
  port: 8080
  routes:
    - /home
    - /about
```

Here `server` holds a mapping, and `routes` inside it holds a list. The indentation is what tells YAML that `host` belongs to `server` and not to the top level.

## Data types

YAML guesses the type from how the value looks.

```yaml
a_string: hello world      # text, quotes optional
a_number: 42               # integer
a_float: 3.14              # decimal
a_boolean: true            # true or false
nothing: null              # null (can also be written ~)
a_date: 2026-06-24         # date
```

Watch out: some bare words get read as booleans. `yes`, `no`, `on`, `off` may become true or false in older parsers. If you mean the literal text, quote it: `answer: "no"`.

## Strings: when to quote

Most strings need no quotes. Quote when the value contains special characters (`:`, `#`, `@`) or when you want to force it to stay a string.

```yaml
plain: just text
quoted: "text with: a colon"
single: 'text with a # hash'
```

### Multi-line strings

Two styles you will see often.

```yaml
# Block scalar with | keeps line breaks
description: |
  Line one.
  Line two.

# Folded scalar with > turns line breaks into spaces
summary: >
  This becomes
  one single line.
```

Use `|` for things like scripts or messages where line breaks matter. Use `>` for long prose you want to wrap in the file but keep as one line.

## Most frequent use cases

### Application config

The bread and butter of YAML. A typical app settings file.

```yaml
app:
  name: billing-service
  environment: production
  log_level: info

database:
  host: db.internal
  port: 5432
  name: billing
  pool_size: 10

features:
  new_checkout: true
  beta_reports: false
```

### Docker Compose

Defining services for local development or deployment.

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    depends_on:
      - api

  api:
    build: ./api
    environment:
      DATABASE_URL: postgres://db:5432/app
    restart: always
```

### Kubernetes manifest

Describing a deployment.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: web
          image: my-app:1.2.0
          ports:
            - containerPort: 80
```

### CI/CD pipeline (GitHub Actions)

This is the use case most teams hit daily. A workflow that runs tests on every push and deploys on the main branch.

```yaml
name: CI Pipeline

# When to run
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out code
        uses: actions/checkout@v4

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test

  deploy:
    needs: test          # only runs if test job passes
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Check out code
        uses: actions/checkout@v4

      - name: Deploy
        run: ./deploy.sh
        env:
          API_KEY: ${{ secrets.API_KEY }}
```

A few things worth noticing here, because they show up in almost every pipeline.

- `on` controls the trigger (push, pull request, schedule, manual).
- `jobs` holds named jobs that run in parallel by default.
- `needs` creates a dependency, so `deploy` waits for `test`.
- `steps` is a list, each step is either a reusable action (`uses`) or a shell command (`run`).
- Secrets are injected with `${{ secrets.NAME }}`, never hard-coded.

## Reuse: anchors and aliases

When you repeat the same block, define it once with an anchor (`&`) and reuse it with an alias (`*`). Handy for keeping pipelines and compose files dry.

```yaml
defaults: &common
  retries: 3
  timeout: 30

job_a:
  <<: *common      # merge in the common values
  name: first

job_b:
  <<: *common
  name: second
```

## Common mistakes

- Using tabs instead of spaces. This is the number one cause of YAML errors. Configure your editor to convert tabs to spaces.
- Inconsistent indentation. All siblings must line up at the same column.
- Missing the space after a colon (`key:value` fails).
- Unquoted strings that look like other types, like a version `1.10` being read as the number `1.1`. Quote it: `version: "1.10"`.
- Trailing colons or stray characters that break the parse.

## Quick validation

When in doubt, check the file before you commit it.

- Online: paste into a YAML linter (for example yamllint.com).
- Command line: `yamllint myfile.yaml` or `python -c "import yaml,sys; yaml.safe_load(open('myfile.yaml'))"`.

## Cheat sheet

| You want | You write |
|----------|-----------|
| A value | `key: value` |
| A list | `- item` under the key |
| Nesting | indent two spaces |
| A comment | `# text` |
| Keep line breaks | `\|` block |
| Fold into one line | `>` block |
| Force a string | quote it |
| Reuse a block | `&anchor` then `*alias` |

## Sources

- Official YAML 1.2 specification: https://yaml.org/spec/1.2.2/
- GitHub Actions workflow syntax: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
- Docker Compose file reference: https://docs.docker.com/compose/compose-file/
- Kubernetes object management: https://kubernetes.io/docs/concepts/overview/working-with-objects/
