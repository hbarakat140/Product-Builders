# Product Builders — Project Proposal

> **Document type**: High-level project proposal  
> **Status**: Draft — for stakeholder review  
> **Last updated**: Feb 2026  
> **Technical implementation plan**: Deferred; see [product_builders_agent_generator_cb6755d9.plan.md](product_builders_agent_generator_cb6755d9.plan.md) and [ARCHITECTURE.md](ARCHITECTURE.md)

---

## Executive Summary

Product Builders is a system that enables product managers, designers, and technical PMs to contribute code to 50+ products via Cursor AI agents — while ensuring AI-generated code stays fully compatible with each product's architecture, conventions, security, and quality standards.

The solution consists of two deliverables: a **CLI tool** that analyzes codebases and generates tailored Cursor rules and governance, and a **web application** for documentation, onboarding, and CLI distribution. No external LLM APIs are required; deep analysis uses Cursor itself.

---

## Business Context

### Scale and Challenge

- **50+ products** across diverse tech stacks (React, Java Spring, Python Django, .NET, etc.) and mixed Git platforms
- **Goal**: Enable non-engineers (PMs, designers, technical PMs, QA) to contribute features via Cursor AI
- **Constraint**: AI must produce code that passes CI, respects conventions, and does not introduce security or compatibility issues
- **Success metric**: PM-authored PRs pass CI and AI review on first attempt at **80%+ rate**

### Why This Matters

- Reduces engineering bottleneck for product-led features
- Accelerates time-to-market for UI/UX improvements
- Maintains code quality and security across all products
- Scales contribution model without proportional engineering headcount

---

## Solution Overview

### Two Deliverables

1. **CLI tool** (Python/Click)
   - Analyzes product codebases (18 dimensions)
   - Generates Cursor rules (14 `.mdc` files), hooks, and permissions
   - Produces onboarding guides and AI review checklists
   - Runs locally; no external LLM API keys
   - Commands: `analyze`, `generate`, `setup`, `export`, `list`, `bulk-analyze`
   - Monorepo support via `--sub-project` flag (namespaced rules per sub-project)

2. **Web application** (FastAPI + Jinja2)
   - Documentation and getting-started guides
   - Per-profile onboarding (Engineer, PM, Designer, Technical PM, QA)
   - CLI download page
   - Product catalog (read-only list of analyzed products in v1)

### How It Works

- **Phase 1 (Heuristic)**: CLI runs 18 analyzers locally — tech stack, database, auth, dependencies, conventions, etc. Produces a Product Profile (JSON).
- **Phase 2 (Deep)**: Tool generates a bootstrap meta-rule; Cursor runs a 4-step analysis (~10 min) using its own codebase index and LLM. Enriches the profile.
- **Output**: 14 Cursor rules, hooks, permissions, onboarding guide — all tailored to the product and contributor profile.

**Delivery is incremental.** Phase 1-3 (foundation + 8 core analyzers + rule generation + governance) for pilot products is the first deliverable. Remaining analyzers, webapp content, lifecycle automation, and monorepo support are delivered as ready.

---

## Major Decisions

### Deep Analysis Engine: Cursor Itself

- **Choice**: Use Cursor (bootstrap meta-rule + structured prompts) for deep analysis instead of external LLM APIs
- **Rationale**: No API keys, no new infrastructure; teams already use Cursor. Zero additional cost.

### Governance: Project-Level Files Only

- **Choice**: All enforcement via `.cursor/rules/`, `.cursor/hooks.json`, `.cursor/cli.json`
- **Rationale**: No dependency on Cursor Enterprise. Works for all teams regardless of licensing.

### Contributor Profiles: 5 Roles

- **Engineer**: Full access; no scope-check hooks installed (hooks.json omits scope-check for engineer profile; cli.json has no restrictions)
- **Technical PM**: Frontend + API; backend read-only; hooks warn on critical ops
- **Product Manager**: Frontend only; backend/API read-only; hooks block on dangerous ops
- **Designer**: UI zones only; strictest permissions
- **QA / Tester**: Test zones only; cannot modify production code

- **Rationale**: Different roles need different access levels. Profiles are customizable per product via `scopes.yaml`.

### Profile Assignment: `setup --profile`

- **Choice**: Contributor runs `product-builders setup --profile pm` after cloning repo
- **Rationale**: Rules (product knowledge) stay in git; hooks and permissions are local and gitignored. Governance is personalized per contributor.

### Enforcement: Three Layers

- **Layer 1 (Rules)**: Soft guidance — AI "should" follow scope
- **Layer 2 (Hooks)**: Smart blocking — `preToolUse` (matcher `Write|Edit`) intercepts file edits; `beforeShellExecution` blocks dangerous shell commands. Returns helpful message ("Create a Jira issue instead"). *Validated Feb 2026* — see [docs/HOOKS_RESEARCH.md](docs/HOOKS_RESEARCH.md) for Cursor hooks research.
- **Layer 3 (Permissions)**: Hard deny — physical filesystem deny via `cli.json`

- **Rationale**: Defense in depth; helpful UX when blocked. Layer 3 guarantees enforcement even if hooks fail (e.g. ENAMETOOLONG on Windows for large files).

### Design System Analysis: First-Class Capability

- **Choice**: Two-stage approach — analyze the design system itself (from Storybook, source repo, or manual curation), then per-product detection and rule generation
- **Rationale**: DS not yet integrated into all products. AI must know the correct UI components, tokens, and patterns. DS adoption is configurable per product. Four scenarios: uses shared DS, own design, should adopt DS, no structured design.
- **Research**: Existing MCP server (`mcp-design-system-extractor`) extracts components, props, tokens from Storybook instances.

### Frontend Patterns & User Flows

- **Choice**: Three layers for UI guidance — design system (what to use), frontend patterns (how components combine), user flows (sequence of steps)
- **Rationale**: Agents need to know not just components but layout patterns, form conventions, modal usage, create/edit flows, and navigation structure. New analyzers: `frontend_patterns.py` (layout, form, modal, list, error, loading) and `user_flows.py` (route structure, navigation graph). Optional product config (`frontend-patterns.yaml`, `user-flows.yaml`) to supplement or override inference.

### Long-Term Vision: MCP-Native Platform (Option D)

- **Choice**: Architecture allows evolution toward MCP Gateway, centralized auth, dynamic rules, multi-IDE (Cursor, Claude Code, Windsurf)
- **Rationale**: Not required for v1; design enables future zero-friction onboarding and multi-IDE support.

---

## Main Flows

### One-Time Setup (Platform Team)

1. Run `product-builders analyze /path/to/repo --name "product-x"`
2. CLI runs heuristic analysis; generates bootstrap meta-rule
3. Platform team opens product in Cursor; runs 4-step deep analysis
4. Run `product-builders export --name "product-x" --target /repo`
5. Rules, hooks, and `scopes.yaml` are committed to product repo

### Contributor Onboarding

1. Contributor clones product repo
2. Runs `product-builders setup --profile pm` (or designer, technical_pm, qa, engineer)
3. Opens Cursor; rules and hooks auto-load
4. Follows the **guided first contribution** ("Hello World" task in onboarding guide) to learn the flow with zero risk
5. Progresses from low-risk tasks (copy/style changes) to feature work as confidence builds

### Day-to-Day Contribution

1. PM asks Cursor: "Add user preferences feature"
2. Cursor is constrained by 14 rules + hooks
3. AI generates code compatible with product
4. PM creates PR

### Maintenance

- Re-analyze after major releases
- Feedback loop: developers flag inaccurate rules; fed into next regeneration
- Template updates: regenerate all products from cached profiles

---

## Governance Without Cursor Enterprise

All enforcement uses project-level files. Company-wide standards are injected as `.mdc` files committed to every repo.

If Cursor Enterprise becomes available later, these would be additive:
- Enforced Team Rules (dashboard)
- Sandbox Mode
- Audit Logs
- Background Agent API for bulk automation

---

## Long-Term Vision (Option D)

Evolution toward MCP-native platform:

- **MCP Gateway**: Centralized auth, dynamic rule delivery
- **Multi-IDE**: Same rules for Cursor, Claude Code, Windsurf
- **Zero-friction onboarding**: No local setup; connect to MCP server and work
- **Server-controlled profiles**: Profile assignment centralized

**Prerequisites**: MCP authorization spec stable; CLI + webapp proven with pilot first.

**Migration path**: CLI analyzers become Core Engine; webapp becomes Admin Portal; MCP Gateway is new component. Evolution, not rewrite.

---

## Decision Points for Expert Discussion

- **DP-1**: Shared internal libraries inventory
- **DP-2**: AI review tool selection (CodeRabbit, Copilot, etc.)
- **DP-3**: Pilot product selection (2–3 products)
- **DP-4**: Pilot timeline
- **DP-5**: Zone definitions per product (`scopes.yaml`)
- **DP-6**: Cursor Enterprise (parked; not blocking)
- **DP-7**: Design system integration strategy (extraction method, DS inventory, per-product adoption)
- **DP-8**: PM support model and escalation path (Slack channel, buddy system, office hours, FAQ)
- **DP-9**: Automated rule staleness detection and maintenance operations (drift thresholds, notifications, automation level)

---

## References

- [ARCHITECTURE.md](ARCHITECTURE.md) — Full architecture, diagrams, resolved decisions
- [docs/HOOKS_RESEARCH.md](docs/HOOKS_RESEARCH.md) — Cursor hooks validation research (preToolUse, ENAMETOOLONG, best practices)
- [product_builders_agent_generator_cb6755d9.plan.md](product_builders_agent_generator_cb6755d9.plan.md) — Implementation plan and todos
