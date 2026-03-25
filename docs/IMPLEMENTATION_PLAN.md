# Product Builders — Implementation Plan

> **Document type**: Implementation plan and todos  
> **Last updated**: Mar 2026  
> **Related**: [ARCHITECTURE.md](../ARCHITECTURE.md), [PROJECT_PROPOSAL.md](../PROJECT_PROPOSAL.md)

---

## Todos

| ID | Task | Phase | Status |
|----|------|-------|--------|
| finalize-architecture | Pre-implementation: Finalize solution architecture with expert validation | Pre | **done** |
| project-proposal | Create project proposal document (major decisions, flows, rationale) | Pre | **done** |
| scaffold | Create project scaffold (pyproject.toml, requirements.txt, package structure, README) | Phase 1 | **done** |
| models | Define ProductProfile dataclass and all analysis result models (18 dimensions) | Phase 1 | **done** |
| base-classes | Implement BaseAnalyzer and BaseGenerator ABCs | Phase 1 | **done** |
| cli | Build CLI skeleton with click (analyze, generate, setup, export, list, bulk-analyze) | Phase 1 | **done** |
| company-standards | Create company standards YAML schema with example files | Phase 1 | **done** |
| tech-stack-analyzer | Implement tech stack analyzer | Phase 2 | **done** |
| structure-analyzer | Implement project structure analyzer | Phase 2 | **done** |
| deps-analyzer | Implement dependency analyzer | Phase 2 | **done** |
| conventions-analyzer | Implement conventions analyzer | Phase 2 | **done** |
| database-analyzer | Implement data model & database analyzer (CRITICAL) | Phase 2 | **done** |
| error-logging-analyzer | Implement error handling & logging analyzer | Phase 2 | **done** |
| auth-analyzer | Implement authentication & authorization patterns analyzer (CRITICAL) | Phase 2 | **done** |
| git-workflow-analyzer | Implement git workflow & conventions analyzer | Phase 2 | **done** |
| templates | Create Jinja2 templates for all Cursor rule types (17 rule files) | Phase 3 | **done** |
| cursor-generator | Implement Cursor rules generator | Phase 3 | **done** |
| hooks-generator | Implement Cursor hooks generator (Layer 2: smart blocking with helpful messages) | Phase 3 | **done** |
| permissions-generator | Implement CLI permissions generator (Layer 3: hard deny via cli.json) | Phase 3 | **done** |
| scopes-system | Implement scopes.yaml system (zone definitions + contributor permissions → generates all 3 layers) | Phase 3 | **done** |
| bootstrap-rule-gen | Implement multi-step bootstrap meta-rule generator (4-step deep analysis via Cursor) | Phase 3 | **done** |
| export-command | Implement export/sync command (with --profile flag for contributor-specific export) | Phase 3 | **done** |
| onboarding-generator | Implement PM onboarding guide generator | Phase 3 | **done** |
| company-standards-integration | Integrate company standards (YAML) into generated rule templates | Phase 3 | **done** |
| review-checklist-gen | Implement AI review checklist generator (for CI integration) | Phase 3 | **done** |
| security-analyzer | Implement security analyzer (+ optional CodeGuard integration) | Phase 4 | **done** |
| testing-analyzer | Implement testing analyzer | Phase 4 | **done** |
| cicd-analyzer | Implement CI/CD analyzer | Phase 4 | **done** |
| design-analyzer | Implement design/UI analyzer | Phase 4 | **done** |
| frontend-patterns-analyzer | Implement frontend patterns analyzer (layout, form, modal, list, error, loading patterns) | Phase 4 | **done** |
| user-flows-analyzer | Implement user flows analyzer (route structure, navigation graph, task flows) | Phase 4 | **done** |
| a11y-analyzer | Implement accessibility analyzer | Phase 4 | **done** |
| api-analyzer | Implement API analyzer | Phase 4 | **done** |
| i18n-analyzer | Implement i18n/l10n analyzer | Phase 4 | **done** |
| state-mgmt-analyzer | Implement state management analyzer | Phase 4 | **done** |
| env-config-analyzer | Implement environment & configuration analyzer | Phase 4 | **done** |
| perf-analyzer | Implement performance patterns analyzer | Phase 4 | **done** |
| webapp-scaffold | Create webapp scaffold (FastAPI + Jinja2, landing page, CLI download page) | Phase 1 | **done** |
| webapp-docs | Build documentation pages and per-profile onboarding guides in webapp | Phase 3 | **done** |
| webapp-catalog | Build product catalog page (read-only list of analyzed products) | Phase 3 | **done** |
| rule-validation | Implement rule validation & quality testing framework | Phase 5 | **done** |
| rule-lifecycle | Implement rule lifecycle management (re-analysis triggers, drift detection) | Phase 5 | **done** |
| bg-agent-api | Integrate Cursor Background Agent API for automated bulk analysis | Phase 5 | **deferred** (API TBD; no in-repo stub) |
| metrics | Implement metrics & observability for rule effectiveness | Phase 5 | **done** (JSONL + `metrics` CLI) |
| zone-detection-improvements | Zone detection: support `src/`-prefixed paths and nested directories (e.g. `src/app/api/`, `src/lib/__tests__/`, `supabase/migrations/`) | Phase 2 | **done** (commit 580627b) |
| baas-component-detection | BaaS-aware database detection (Supabase, Firebase, DynamoDB, PlanetScale, Neon) and modern component library detection (shadcn, base-ui, nextui, park-ui, daisyui) | Phase 2 | **done** (commit 2f5f457) |
| blocked-command-filtering | Smart blocked-command filtering: only block tool-specific commands (prisma:migrate, alembic upgrade, flyway migrate, etc.) when the tool is in the project's dependencies | Phase 3 | **done** (commit 0ed031c) |
| template-numbering-fix | Testing template sequential numbering fix (no gaps when optional rules are skipped) | Phase 3 | **done** (commit b135dfc) |
| overrides-yaml-wiring | Wire overrides.yaml into the generate pipeline (`profiles/<name>/overrides.yaml` applied during generation) | Phase 3 | **done** (commit d242ce4) |
| node-modules-exclusion | Fix node_modules exclusion in analysis | Phase 2 | **done** (commit a8614c1) |

---

## Overview

Build a CLI tool and web application that automatically analyze product codebases and generate tailored Cursor rules, governance (hooks, permissions), and onboarding guides — enabling PMs, designers, and engineers to contribute via AI agents that respect each product's architecture, conventions, security, and quality standards.

**Two deliverables:** Python CLI (analysis, generation, setup) + FastAPI webapp (documentation, onboarding, CLI distribution).

---

## Implementation Phases Summary

| Phase | Focus | Deliverable | Status |
|-------|-------|-------------|--------|
| **Phase 1** | Foundation | Scaffold, models, base classes, CLI skeleton, company standards | **done** |
| **Phase 2** | Core analyzers | 8 analyzers: tech stack, structure, deps, conventions, database, auth, error handling, git workflow | **done** |
| **Phase 3** | Rule generation + governance | 17 rule templates, generators, scopes system, bootstrap, export, onboarding, review checklist, company standards integration | **done** |
| **Phase 4** | Remaining analyzers | 12 analyzers: security, testing, cicd, design, frontend patterns, user flows, a11y, api, i18n, state mgmt, env config, performance | **done** |
| **Phase 5** | Automation & lifecycle | Rule validation, drift detection, feedback, versioning, Background Agent API, metrics | **done** (bg-agent deferred) |

---

For full architecture details, diagrams, governance design, and decision points, see [ARCHITECTURE.md](../ARCHITECTURE.md).
