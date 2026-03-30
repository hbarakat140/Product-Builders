# Detection Gap Coverage Design

**Date:** 2026-03-30
**Approach:** Critical Path — fix the top 10 highest-impact gaps plus framework/i18n/security/performance detection improvements.

## Problem

Field population across analyzers is ~21-30% on real projects. Zone detection finds only 3-4 of 10 possible zones. Root causes: missing detection patterns for modern frameworks, no monorepo awareness in zones, and one false-positive bug.

## Scope

10 targeted fixes across 7 analyzers + zone detection, plus 4 detection expansion areas.

---

## Fix 1: Auth `rate_limiting` Bug (CRITICAL)

**File:** `src/product_builders/analyzers/auth.py`
**Problem:** `result.rate_limiting` is referenced but never populated. Every project triggers a false anti-pattern.

- Verify `rate_limiting` field exists on `AuthResult` in `models/analysis.py`
- Add `_detect_rate_limiting(dep_names)` checking: `express-rate-limit`, `rate-limiter-flexible`, `@nestjs/throttler`, `flask-limiter`, `django-ratelimit`, `bucket4j`
- Call it in `analyze()`, assign to `result.rate_limiting`
- Anti-pattern now only fires when field is genuinely None

## Fix 2: Zone Detection — App Router + Deduplication

**File:** `src/product_builders/generators/scopes.py`

**2a. Add Next.js App Router API paths**
- Add `"src/app/api"`, `"app/api"` to `api` zone patterns

**2b. Deduplicate zone paths**
- `found_paths` can contain duplicates when multiple patterns match the same directory via index lookup
- Deduplicate with `found_paths = list(dict.fromkeys(found_paths))` before creating Zone

## Fix 3: Zone Detection — Python Package Structure

**File:** `src/product_builders/generators/scopes.py`

- After standard zone detection, if `pyproject.toml` or `setup.py` exists:
  - Scan `src/*/` for directories containing `__init__.py`
  - Map these to `backend_logic` zone if not already detected
- Ensures Python projects like `src/product_builders/` get proper zone classification

## Fix 4: Zone Detection — Monorepo Nested Zones

**File:** `src/product_builders/generators/scopes.py`

- After initial zone detection, check for monorepo markers: `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `lerna.json`
- If monorepo, scan each sub-project root (`apps/*/`, `packages/*/`) for zone patterns
- Prefix zone paths with sub-project path: `apps/web/src/components/**`

## Fix 5: Database — Supabase Migration Detection

**File:** `src/product_builders/analyzers/database.py`

- Add `"supabase/migrations"` to migration directory candidates
- Detect `supabase/config.toml` → set `migration_tool = "supabase-cli"`
- Add `"@supabase/supabase-js"` as ORM indicator mapping to `supabase-js` (client-side ORM equivalent)

## Fix 6: Auth — Framework-Specific Protected Routes

**File:** `src/product_builders/analyzers/auth.py`

- Detect `middleware.ts` / `middleware.js` at project root → Next.js auth middleware
- Detect `src/hooks.server.ts` / `src/hooks.server.js` → SvelteKit auth hooks
- Detect `app/root.tsx` with auth loader → Remix auth pattern
- Add detected patterns to `protected_route_patterns`

## Fix 7: Dependencies — Monorepo Workspace Manifests

**File:** `src/product_builders/analyzers/dependencies.py`

- When monorepo indicators exist (`pnpm-workspace.yaml`, `turbo.json`, etc.):
  - Scan `apps/*/package.json` and `packages/*/package.json`
  - Merge discovered deps into main list
  - Track all manifest paths in `dependency_manifest_files`

## Fix 8: Git Workflow — Husky Hook Detection

**File:** `src/product_builders/analyzers/git_workflow.py`

- Check for `.husky/` directory
- `.husky/commit-msg` → infer `commit_message_format = "conventional"` (if commitlint found inside)
- `.husky/pre-commit` with `lint-staged` → note pre-commit validation exists

## Fix 9: Tech Stack — Modern Framework Detection

**File:** `src/product_builders/analyzers/tech_stack.py`

Add to `FRAMEWORK_DETECTORS`:
- Remix: `@remix-run/node`, `@remix-run/react`, `@remix-run/serve`
- Hono: `hono`
- SolidStart: `solid-start`, `@solidjs/start`
- Qwik: `@builder.io/qwik`
- Analog: `@analogjs/platform`
- Astro: `astro`
- Elysia: `elysia`

## Fix 10: Security — CSP + Supply Chain Detection

**File:** `src/product_builders/analyzers/security.py`

**CSP beyond Helmet:**
- Scan `middleware.ts` for `Content-Security-Policy` header
- Check Django `settings.py` for `CSP_` prefixed settings or `django-csp` in deps
- Check `next.config.js` for `headers()` with CSP

**Supply chain tools:**
- Add detection: `npm audit` (check `package.json` scripts), `pip-audit`, `cargo-audit`, `safety`
- Add `.github/dependabot.yml` detection (already exists — verify)

## Fix 11: Performance — Image Optimization + Bundle Analysis

**File:** `src/product_builders/analyzers/performance.py`

**Image optimization:**
- Detect `next/image` usage by scanning source files for `from 'next/image'` import
- Detect `@astrojs/image`, `unpic`

**Bundle analysis:**
- Detect: `webpack-bundle-analyzer`, `@next/bundle-analyzer`, `vite-plugin-visualizer`, `rollup-plugin-visualizer`, `source-map-explorer`

## Fix 12: i18n — Framework-Specific Detection

**File:** `src/product_builders/analyzers/i18n.py`

Add to framework detection:
- `@nuxtjs/i18n` → "nuxt-i18n"
- `@astrojs/i18n` or `astro-i18n-aut` → "astro-i18n"
- `@inlang/paraglide-js` → "paraglide"
- `typesafe-i18n` → "typesafe-i18n"
- `next-intl` (already present — verify)

---

## Verification Plan

Each fix gets at least one test:

```
test_detects_rate_limiting_express
test_rate_limiting_anti_pattern_only_when_null
test_zone_detects_app_router_api
test_zone_deduplicates_paths
test_zone_detects_python_package
test_zone_detects_monorepo_nested
test_detects_supabase_migrations
test_detects_nextjs_middleware_auth
test_detects_sveltekit_hooks_auth
test_detects_monorepo_workspace_deps
test_detects_husky_commit_hooks
test_detects_remix_framework
test_detects_hono_framework
test_detects_csp_in_middleware
test_detects_npm_audit_script
test_detects_next_image_optimization
test_detects_bundle_analyzer
test_detects_nuxt_i18n
```

Run full suite after each fix group to prevent regressions.

---

## Files Modified

| File | Fixes |
|------|-------|
| `models/analysis.py` | Verify `rate_limiting` field on AuthResult |
| `analyzers/auth.py` | #1 rate_limiting, #6 framework-specific routes |
| `generators/scopes.py` | #2 App Router zones, #3 Python packages, #4 monorepo zones, dedup |
| `analyzers/database.py` | #5 Supabase migrations |
| `analyzers/dependencies.py` | #7 monorepo workspace manifests |
| `analyzers/git_workflow.py` | #8 Husky hooks |
| `analyzers/tech_stack.py` | #9 modern frameworks |
| `analyzers/security.py` | #10 CSP + supply chain |
| `analyzers/performance.py` | #11 image + bundle |
| `analyzers/i18n.py` | #12 framework i18n |
| `tests/test_analyzers/*` | All verification tests |
