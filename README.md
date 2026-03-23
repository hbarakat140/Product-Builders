# Product Builders

A CLI tool and web application that analyzes product codebases and generates tailored Cursor rules, governance (hooks, permissions), and onboarding guides — enabling PMs, designers, and engineers to contribute via AI agents that respect each product's architecture and conventions.

## Documentation

- [PROJECT_PROPOSAL.md](PROJECT_PROPOSAL.md) — High-level proposal and major decisions
- [ARCHITECTURE.md](ARCHITECTURE.md) — Solution architecture, diagrams, implementation phases
- [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) — Implementation plan and todos
- [docs/HOOKS_RESEARCH.md](docs/HOOKS_RESEARCH.md) — Cursor hooks validation research (preToolUse, ENAMETOOLONG, best practices)

## Installation

```bash
pip install -e .
# CLI: product-builders --help
```

Optional web UI and API docs:

```bash
pip install -e ".[webapp]"
```

## CLI (quick start)

```bash
product-builders analyze /path/to/repo --name my-product --heuristic-only
product-builders generate --name my-product
```

See `--help` on each command for options.

### Validation & drift (Phase 5)

```bash
product-builders generate --name my-product --validate   # structural checks on generated artifacts
product-builders check-drift --name my-product --repo /path/to/repo
product-builders check-drift --name my-product --repo /path/to/repo --full   # re-run analyzers, compare fingerprints
product-builders metrics --name my-product              # tail metrics.jsonl events
```

`analyze` records **git HEAD** in the profile for git-based drift. Legacy profiles without a SHA get a hint until you re-analyze.

## Web application

FastAPI + Jinja2 — landing page, install/download instructions, OpenAPI at `/api/docs`.

```bash
pip install -e ".[webapp]"
python -m product_builders.webapp --reload
# or: uvicorn product_builders.webapp.app:app --reload
# or: product-builders-web --reload
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000). Health check: `GET /health`.

| Path | Purpose |
|------|---------|
| `/` | Landing |
| `/docs` | Shipped documentation (getting started, CLI overview, governance) |
| `/docs/{slug}` | Rendered markdown page |
| `/products` | **Catalog** — profiles under `PB_PROFILES_DIR` with `analysis.json` metadata |
| `/products/{name}` | Product detail + links to `docs/onboarding-*.md` |
| `/products/{name}/onboarding/{role}` | Rendered onboarding for a role (e.g. `engineer`) |
| `/api/products` | JSON list for integrations |
| `/download` | CLI install instructions |
| `/api/docs` | OpenAPI (Swagger) |
