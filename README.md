# Product Builders

**Product Builders** is a Python CLI and optional web app that **analyzes product repositories** (offline heuristics) and **generates tailored [Cursor](https://cursor.com) artifacts**: rules (`.mdc`), hooks (`hooks.json`), CLI permissions (`cli.json`), onboarding guides, review checklists, and `scopes.yaml` for contributor access zones. The goal is to let PMs, designers, QA, and engineers work with AI assistants **without bypassing** each product’s architecture, security boundaries, or conventions.

---

## Table of contents

- [What you get](#what-you-get)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration & directories](#configuration--directories)
- [Typical workflow](#typical-workflow)
- [CLI reference](#cli-reference)
- [Product profile layout](#product-profile-layout)
- [Governance layers & scopes](#governance-layers--scopes)
- [Company standards](#company-standards)
- [Web application](#web-application)
- [Development](#development)
- [Documentation](#documentation)
- [License](#license)

---

## What you get

| Output | Purpose |
|--------|---------|
| **Heuristic profile** (`analysis.json`) | Structured snapshot of stack, DB, auth, errors, security, tests, CI/CD, and many more dimensions |
| **Cursor rules** (`.cursor/rules/*.mdc`) | Product-specific guidance for the AI |
| **Hooks** (`.cursor/hooks.json`) | Layer 2: contextual blocking with messages (e.g. read-only zones) |
| **Permissions** (`.cursor/cli.json`) | Layer 3: hard deny for paths/commands per role |
| **`scopes.yaml`** | Single source of truth for zones → drives all three governance layers |
| **Onboarding & checklist** | Role docs and CI-friendly review checklist |
| **Metrics** (`metrics.jsonl`) | Optional events from validate, drift checks, etc. |

Analysis is **fully offline** (no LLM calls in the core pipeline). A **bootstrap meta-rule** can be generated for deeper, Cursor-assisted analysis when you do not pass `--heuristic-only`.

---

## Requirements

- **Python 3.11** (supported range: `>=3.11,<4.0` per `pyproject.toml`)
- **Git** (optional but recommended — used to record **HEAD** for drift detection)

---

## Installation

From the repository root:

```bash
pip install -e .
```

Entry points:

- **`product-builders`** — main CLI
- **`product-builders-web`** — dev server for the web app (after installing the `webapp` extra)

### Optional extras

```bash
# Web UI + API (FastAPI, uvicorn, markdown rendering)
pip install -e ".[webapp]"

# Tests, coverage, Ruff, mypy
pip install -e ".[dev]"
```

---

## Configuration & directories

Paths default to a layout relative to the package / checkout unless you override them.

| Variable | Purpose | Default (if unset) |
|----------|---------|---------------------|
| **`PB_HOME`** | Root used to derive profiles and standards | Parent of the `src` tree in a dev checkout |
| **`PB_PROFILES_DIR`** | Where each product’s profile directory lives | `{PB_HOME}/profiles` |
| **`PB_STANDARDS_DIR`** | Company standards YAML files | `{PB_HOME}/company_standards` |

**Product names** must match `[a-zA-Z0-9][a-zA-Z0-9._-]*` (no `..`). Each product gets a folder under `PB_PROFILES_DIR` with `analysis.json` and generated artifacts.

---

## Typical workflow

1. **Analyze** a repository and cache a profile under your profiles directory.
2. **Generate** rules, hooks, permissions, docs, and checklist into that profile directory (optionally for a **contributor role**).
3. **Export** (or **setup** in a clone) to copy governance into the **actual product repo** contributors use.
4. Optionally run **validate** on generate, **check-drift** when the repo moves on, and **feedback** to record rule issues.

```bash
# 1. Scan repo → profiles/<name>/analysis.json (+ analyzers output)
product-builders analyze /path/to/repo --name my-product

# 2. Regenerate artifacts from profile (add --validate for structural checks)
product-builders generate --name my-product

# 3a. Copy into the product repo
product-builders export --name my-product --target /path/to/repo

# 3b. Or, from inside the product repo: install role-specific governance into cwd
product-builders setup --name my-product --profile engineer
```

**Monorepo / many products:**

```bash
product-builders bulk-analyze --manifest products.yaml
# products.yaml example:
#   products:
#     - name: app-frontend
#       path: /path/to/monorepo/apps/web
```

```bash
product-builders bulk-analyze --monorepo /path/to/monorepo
```

---

## CLI reference

Global options: **`--version`**, **`-v` / `--verbose`** (debug logging).

| Command | Description |
|---------|-------------|
| **`analyze`** | Run heuristic analyzers on `repo_path`; write `analysis.json` and related outputs. Options: **`--name`** (required), **`--heuristic-only`**, **`--sub-project`** (path inside monorepo). |
| **`generate`** | Regenerate rules, hooks, permissions, onboarding, checklist from cached profile. Options: **`--name`**, **`--profile`** (role alias), **`--validate`**. |
| **`setup`** | Write governance for a role into **current directory** (`.cursor/`, etc.). Options: **`--name`**, **`--profile`** (required). |
| **`export`** | Copy generated artifacts from profile dir to a **target** repo. Options: **`--name`**, **`--target`**, **`--profile`**. |
| **`list`** | List analyzed products (from `analysis.json` under profiles dir). |
| **`bulk-analyze`** | Analyze many products via **`--manifest`** YAML or **`--monorepo`** discovery. |
| **`check-drift`** | Compare cached profile to repo (**git HEAD** and/or **`--full`** heuristic fingerprint). |
| **`metrics`** | Show recent **`metrics.jsonl`** events for a product. |
| **`feedback`** | Append an entry to **`feedback.yaml`** for a product (rule accuracy notes). |

Role aliases for **`--profile`** (see **`resolve_role`** in code): **`engineer`**, **`eng`**, **`pm`**, **`product_manager`**, **`designer`**, **`qa`**, **`qa_tester`**, **`tester`**, **`technical-pm`**, **`technical_pm`**, **`tech_pm`**, and more. Run **`product-builders <command> --help`** for flags; invalid roles list valid aliases in the error message.

### Validation & drift

```bash
product-builders generate --name my-product --validate
product-builders check-drift --name my-product --repo /path/to/repo
product-builders check-drift --name my-product --repo /path/to/repo --full
product-builders metrics --name my-product --limit 80
```

`analyze` stores **git HEAD** in the profile when available so **`check-drift`** can detect stale rules without a full re-scan. **`--full`** re-runs analyzers and compares fingerprints (slower, no git required).

---

## Product profile layout

Under **`PB_PROFILES_DIR/<product-name>/`** you will typically see:

| Path | Role |
|------|------|
| **`analysis.json`** | Full **`ProductProfile`** (metadata + analyzer dimensions) |
| **`scopes.yaml`** | Zone paths and per-role allow / read-only / forbid lists |
| **`.cursor/rules/*.mdc`** | Generated Cursor rules |
| **`.cursor/hooks.json`** | Hook definitions |
| **`.cursor/cli.json`** | Filesystem / command restrictions |
| **`docs/onboarding-*.md`** | Role onboarding markdown |
| **`review-checklist.md`** | Checklist for human or CI review |
| **`feedback.yaml`** | Optional feedback log from **`feedback`** command |
| **`metrics.jsonl`** | Append-only metrics from validate / drift / etc. |

---

## Governance layers & scopes

1. **Rules (soft)** — `.mdc` files teach the model what to respect.
2. **Hooks (smart block)** — `hooks.json` blocks edits with an explanation (e.g. read-only zone).
3. **Permissions (hard deny)** — `cli.json` enforces filesystem boundaries for the CLI/agent.

**`scopes.yaml`** maps **zones** (e.g. `frontend_ui`, `database`) to **glob patterns** and lists which **contributor roles** may read, write, or must not touch each zone. Generators consume the profile’s **`ScopeConfig`** (from YAML or auto-detection) to produce aligned rules, hooks, and permissions.

---

## Company standards

YAML files under **`PB_STANDARDS_DIR`** are loaded and merged into rule generation (via **`CursorRulesGenerator`**) so org-wide policies can augment product-specific templates without forking every rule file.

---

## Web application

FastAPI + Jinja2: landing pages, shipped docs as markdown, product catalog, and OpenAPI.

```bash
pip install -e ".[webapp]"
python -m product_builders.webapp --reload
# or: uvicorn product_builders.webapp.app:app --reload
# or: product-builders-web --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). **`GET /health`** for health checks.

| Path | Purpose |
|------|---------|
| **`/`** | Landing |
| **`/docs`** | Documentation index |
| **`/docs/{slug}`** | Rendered markdown page |
| **`/products`** | Catalog of profiles under **`PB_PROFILES_DIR`** with **`analysis.json`** |
| **`/products/{name}`** | Product detail + onboarding links |
| **`/products/{name}/onboarding/{role}`** | Rendered onboarding for a role |
| **`/api/products`** | JSON list for integrations |
| **`/download`** | CLI install instructions |
| **`/api/docs`** | OpenAPI (Swagger) |

---

## Development

```bash
pip install -e ".[dev]"
py -m pytest tests -q
ruff check src tests
ruff format src tests
mypy src/product_builders
```

Package code lives under **`src/product_builders/`**. Analyzers and generators register via **`analyzers/registry.py`** and **`generators/registry.py`**.

---

## Documentation

| Document | Contents |
|----------|----------|
| [PROJECT_PROPOSAL.md](PROJECT_PROPOSAL.md) | Goals, decisions, scope |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Architecture, diagrams, phases |
| [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) | Implementation status and todos |
| [docs/HOOKS_RESEARCH.md](docs/HOOKS_RESEARCH.md) | Cursor hooks research (preToolUse, limits, practices) |
| [docs/code-review-report.md](docs/code-review-report.md) | Python quality review notes |

---

## License

MIT — see [pyproject.toml](pyproject.toml) metadata.
