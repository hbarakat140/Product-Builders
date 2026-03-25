# Product Builders

**Product Builders** is a Python CLI and optional web app that **analyzes product repositories** (offline heuristics) and **generates tailored [Cursor](https://cursor.com) artifacts**: rules (`.mdc`), hooks (`hooks.json`), CLI permissions (`cli.json`), onboarding guides, review checklists, and `scopes.yaml` for contributor access zones. The goal is to let PMs, designers, QA, and engineers work with AI assistants **without bypassing** each product’s architecture, security boundaries, or conventions.

---

## Table of contents

- [What you get](#what-you-get)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick start by phase](#quick-start-by-phase)
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
| **Heuristic profile** (`analysis.json`) | Structured snapshot of stack, DB, auth, errors, security, tests, CI/CD, BaaS (Supabase, Firebase, DynamoDB, PlanetScale, Neon), component libraries (shadcn, base-ui, nextui, park-ui, daisyui), and many more dimensions |
| **Cursor rules** (`.cursor/rules/*.mdc`) | Product-specific guidance for the AI |
| **Hooks** (`.cursor/hooks.json`) | Layer 2: contextual blocking with messages (e.g. read-only zones) |
| **Permissions** (`.cursor/cli.json`) | Layer 3: hard deny for paths/commands per role |
| **`scopes.yaml`** | Single source of truth for zones → drives all three governance layers |
| **Onboarding & checklist** | Role docs and CI-friendly review checklist |
| **Metrics** (`metrics.jsonl`) | Optional events from validate, drift checks, etc. |

Analysis is **fully offline** (no LLM calls in the core pipeline). A **bootstrap meta-rule** can be generated for deeper, Cursor-assisted analysis when you do not pass `--heuristic-only`.

**Recent improvements:** BaaS-aware database detection (Supabase to postgresql, Firebase to firebase, DynamoDB, PlanetScale to mysql, Neon to postgresql), smart blocked-command filtering (dangerous commands like `prisma:migrate` or `alembic upgrade` are only blocked when that tool is actually in the project's dependencies), `overrides.yaml` support for post-analysis corrections, and improved zone detection with nested directory support.

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

## Quick start by phase

Roadmap phases (see [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md)) map to how you **install**, **analyze**, **generate**, and **operate** the tool. Use either the **interactive wizard** or the **copy-paste blocks** below.

### Interactive wizard

Runs prompts (and can invoke `analyze`, `generate`, `check-drift` for you):

```bash
product-builders wizard
```

| Flag | Use |
|------|-----|
| **`--phase N`** | Only run phase **1**–**5** (see table below). |
| **`-y` / `--yes`** | Skip “continue?” prompts between phases (for scripting). |
| **`--repo`**, **`--name`**, **`--profile`** | Pre-fill paths and product name; with **`-y --phase 2`** both **`--repo`** and **`--name`** are required. |
| **`--heuristic-only`** | Phase 2: same as **`analyze --heuristic-only`**. |
| **`--validate` / `--no-validate`** | Phase 3: control validation without a prompt. |

Examples:

```bash
# Guided tour (all phases, interactive)
product-builders wizard

# Foundation only: Python check, paths, pip reminders, create profiles dir
product-builders wizard --phase 1 -y

# Scripted analyze + generate
product-builders wizard -y --phase 2 --repo /path/to/repo --name my-app
product-builders wizard -y --phase 3 --name my-app --validate

# Phase 5 with automatic drift check (needs both repo and name)
product-builders wizard -y --phase 5 --name my-app --repo /path/to/repo
```

### Phase 1: Foundation

**Goal:** Tooling, Python **3.11+**, profile and standards directories.

```bash
pip install -e .
pip install -e ".[webapp]"    # optional: catalog + docs site
pip install -e ".[dev]"       # optional: tests, ruff, mypy
product-builders --version
```

Set **`PB_PROFILES_DIR`** / **`PB_STANDARDS_DIR`** / **`PB_HOME`** if defaults are wrong for your layout (see [Configuration & directories](#configuration--directories)).

### Phase 2: Core analysis

**Goal:** Offline heuristics (tech stack, structure, deps, conventions, **database**, **auth**, **error handling**, **git**). Writes **`analysis.json`** under **`PB_PROFILES_DIR/<name>/`**.

```bash
product-builders analyze /path/to/repo --name my-product
# Skip Cursor bootstrap meta-rule:
product-builders analyze /path/to/repo --name my-product --heuristic-only
```

### Phase 3: Rules and governance

**Goal:** Cursor **`.mdc`** rules, **hooks**, **cli.json**, **scopes.yaml**, onboarding, review checklist. The `generate` command automatically applies `profiles/<name>/overrides.yaml` if present, so you can correct analysis mistakes without re-scanning.

```bash
product-builders generate --name my-product
product-builders generate --name my-product --profile engineer
product-builders generate --name my-product --validate
```

Copy artifacts into a repo contributors use:

```bash
product-builders export --name my-product --target /path/to/repo
# or from inside that repo:
product-builders setup --name my-product --profile engineer
```

### Phase 4: Extended dimensions

**Goal:** Security, testing, CI/CD, design, API, i18n, state, env, performance, etc.

There is **no separate command**: a normal **`analyze`** already fills these dimensions. Re-run analyze when the codebase changes significantly.

```bash
product-builders analyze /path/to/repo --name my-product
```

### Phase 5: Lifecycle and quality

**Goal:** Structural validation, drift vs git or full re-scan, metrics, feedback.

```bash
product-builders generate --name my-product --validate
product-builders check-drift --name my-product --repo /path/to/repo
product-builders check-drift --name my-product --repo /path/to/repo --full
product-builders metrics --name my-product
product-builders feedback --name my-product --rule database --issue "ORM hint wrong for module X"
```

Automated bulk analysis via Cursor Background Agent API is **deferred** (see implementation plan).

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
2. *(Optional)* **Override** analysis results by creating `profiles/<name>/overrides.yaml` to correct any detection mistakes.
3. **Generate** rules, hooks, permissions, docs, and checklist into that profile directory (optionally for a **contributor role**). Overrides are applied automatically if present.
4. **Export** (or **setup** in a clone) to copy governance into the **actual product repo** contributors use.
5. Optionally run **validate** on generate, **check-drift** when the repo moves on, and **feedback** to record rule issues.

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
| **`wizard`** | Interactive **quick start by phase** (install path through lifecycle); optional **`-y`**, **`--phase`**, **`--repo`**, **`--name`**. |

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
| **`overrides.yaml`** | Optional user-editable overrides to correct analysis results without re-scanning |
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

**`scopes.yaml`** maps **zones** (e.g. `frontend_ui`, `database`) to **glob patterns** and lists which **contributor roles** may read, write, or must not touch each zone. Zone detection now supports `src/`-prefixed paths and nested directories (e.g., `src/app/api/`, `src/lib/__tests__/`, `supabase/migrations/`), not just root-level patterns. Generators consume the profile’s **`ScopeConfig`** (from YAML or auto-detection) to produce aligned rules, hooks, and permissions.

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
