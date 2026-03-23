# Getting started

Product Builders turns a repository into **Cursor rules**, **hooks**, **CLI permissions**, and **onboarding guides** — so AI agents and humans share the same guardrails.

## Flow

1. **Analyze** — Offline scan of the repo (stack, structure, security, tests, CI/CD, …).
2. **Deep analysis** (optional) — Enrich the profile using the bootstrap meta-rule in Cursor.
3. **Generate** — Emit `.mdc` rules, `hooks.json`, `cli.json`, scopes, and role onboarding under a profile directory.

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

## Profiles

Generated artifacts live under `profiles/<name>/` (override with `PB_PROFILES_DIR`). The **catalog** lists every profile that exists on this server.
