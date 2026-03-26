# Getting started

Product Builders turns a repository into **Cursor rules**, **hooks**, **CLI permissions**, and **onboarding guides** — so AI agents and humans share the same guardrails.

## Flow

1. **Analyze** — Offline scan of the repo (stack, structure, security, tests, CI/CD, …).
2. **Override** (optional) — Create `profiles/<name>/overrides.yaml` to correct or extend any analysis field before generation.
3. **Deep analysis** (optional) — Enrich the profile using the bootstrap meta-rule in Cursor.
4. **Generate** — Emit `.mdc` rules, `hooks.json`, `cli.json`, scopes, and role onboarding under a profile directory. If `overrides.yaml` exists, its values are merged into the profile automatically.

## Install

```bash
pip install -e .
pip install -e ".[webapp]"   # optional: this documentation server
```

## Commands

```bash
product-builders analyze /path/to/repo --name my-product --heuristic-only
product-builders generate --name my-product
product-builders setup --name my-product   # interactive / full pipeline per CLI
```

Use `product-builders --help` and `product-builders <command> --help` for options.

## Deep Analysis (Optional)

After running `analyze`, you can enrich the profile with Cursor-assisted deep analysis:

1. Open the product repo in Cursor
2. Tell Cursor: "run deep analysis"
3. Cursor follows the bootstrap meta-rule through 3 sequential steps (architecture, domain model, conventions)
4. Cursor writes findings to `deep-analysis.yaml` with file-path evidence
5. Ingest the results: `product-builders ingest-deep --name <product> --repo /path/to/repo`
6. Regenerate rules: `product-builders generate --name <product>`

The bootstrap rule adapts its questions based on your tech stack (e.g., Django-specific questions for Python/Django projects, React-specific for TypeScript/React).

## AST-Enhanced Analysis (Optional)

For deeper code pattern recognition, install the optional AST dependency:

```bash
pip install product-builders[ast]
```

This enables tree-sitter-based analysis during `analyze` that extracts:
- Import graphs and module dependencies
- Function signatures and decorators
- JSX component hierarchies
- Actual naming patterns from code symbols

Enhanced analyzers: auth, error handling, conventions, API patterns, frontend patterns, state management. The enhancement is automatic -- no additional commands needed.

## Profiles

Generated artifacts live under `profiles/<name>/` (override with `PB_PROFILES_DIR`). The **catalog** lists every profile that exists on this server.
