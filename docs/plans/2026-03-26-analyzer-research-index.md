# Analyzer Best Practices Research Index

Deep research conducted 2026-03-26 by 5 specialized agents covering industry best practices, tools, and detection patterns for all 20 Product Builders analyzers.

## Research Documents

1. **[Analyzer Deep Research](2026-03-26-analyzer-deep-research.md)** -- Per-analyzer audit of all 20 analyzers: capabilities, gaps, improvements, prioritized action plan
2. **[Auth & Security Research](2026-03-26-auth-security-research.md)** -- OWASP Top 10:2025, auth libraries per ecosystem, session management, rate limiting, secrets management, anti-patterns
3. **[Database & State Management Research](2026-03-26-database-state-mgmt-research.md)** -- ORMs, migration tools, state libraries, data fetching, form state, real-time, caching strategies
4. **[Testing & CI/CD Research](2026-03-26-testing-cicd-research.md)** -- Test frameworks, E2E, API testing, visual regression, CI platforms, deployment patterns, release management
5. **[Frontend, Design & Accessibility Research](2026-03-26-frontend-design-a11y-research.md)** -- Component libraries, CSS approaches, WCAG 2.2, a11y tools, routing patterns, animation
6. **[DevOps, Code Quality & Infrastructure Research](2026-03-26-devops-quality-research.md)** -- Framework trends, linters/formatters, feature flags, git workflows, i18n, performance, IaC

## Key Cross-Cutting Findings

- **2 dead dimensions**: Dependencies and CI/CD analyzers produce data no template consumes
- **10+ wasted model fields**: Stored but never referenced in any template
- **17 missing frameworks**: Astro, Hono, Elysia, SvelteKit, SolidJS, Qwik, Litestar, etc.
- **30+ missing auth/security patterns**: WebAuthn, MFA, OWASP headers, rate limiting, secrets management
- **40+ missing testing patterns**: Visual regression, contract testing, mutation testing, property-based
- **50+ missing config files**: oxlint, golangci-lint, Helm, Kustomize, semantic-release, etc.
- **Industry shifts**: Biome 2.0, uv, Ruff, OpenTofu, trunk-based dev, INP replacing FID

## How to Use This Research

These documents serve as the specification for improving the 20 analyzers. Each document contains:
- **Detection checklists** -- what to look for in repos
- **Per-ecosystem libraries** -- standard tools per language/framework
- **Configuration files** -- which files to parse and what to extract
- **Anti-patterns** -- what bad practices to flag with severity levels
- **Gap analysis** -- what the current analyzers miss vs. these findings
