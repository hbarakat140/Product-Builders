# Comprehensive Analyzer Assessment Report

**Date:** 2026-03-26
**Scope:** All 20 analyzers in `src/product_builders/analyzers/`
**Baseline:** Original pipeline score of 6.3/10 from ANALYSIS_SCORING_AND_RESEARCH.md (2026-03-25)

---

## Methodology

Every analyzer file was read in full. For each, the following were counted:
- **Detection items**: Entries in indicator dicts/lists (frameworks, tools, patterns)
- **Result fields**: Fields in the Pydantic model actually populated by the analyzer
- **AST enrichment**: Whether the analyzer uses the `index` parameter
- **Anti-pattern detection**: Whether `anti_patterns` list is populated
- **Detection techniques**: file existence, dependency matching, regex scanning, config parsing, AST index, anti-pattern flagging
- **Template utilization**: Which result fields are referenced in `.mdc.j2` templates

---

## Per-Analyzer Scorecards

### 1. Tech Stack (`tech_stack.py`) — CRITICAL

**Detection inventory:**
- Language extensions: 31 mappings
- Framework detectors: 36 frameworks (23 original + 13 Phase A additions: Astro, Hono, Elysia, SvelteKit, SolidJS, SolidStart, Qwik, QwikCity, H3, Nitro, TanStack Start, Analog, Litestar, FastHTML, Quart, Sanic)
- Build tool files: 21 mappings
- Package manager files: 20 mappings (added deno, pixi, swift-pm, pub, cocoapods)
- Runtime version detection: 5 runtimes (node, python, java, dotnet + pyproject.toml)

**Result fields populated:** 6/6 (languages, primary_language, frameworks, build_tools, package_managers, runtime_versions)
**AST enrichment:** No (index parameter accepted but not used)
**Anti-patterns:** None
**Techniques:** file existence (build tools, pkg managers), dependency matching (frameworks), file extension counting (languages), regex (versions), config parsing (pyproject.toml, pom.xml, .csproj)

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | 36 frameworks, 21 build tools, 20 pkg managers = 108 total items. Missing: Elixir Phoenix, Scala Play, template languages (Jinja2, Handlebars, ERB), TS vs JS ratio |
| Accuracy | 7/10 | Techniques: file extension counting (no weighting), dep name matching, config regex. No version normalization (stores raw "^18.0.0") |
| Depth | 6/10 | Detects presence + extracts versions, but no TS/JS ratio, no language weighting, no metaframework detection |
| Template Use | 10/10 | ALL 6 fields consumed by tech-stack.mdc.j2 |
| Anti-Patterns | 0/10 | None implemented |
| Multi-Ecosystem | 9/10 | JS/TS, Python, Java/Kotlin, .NET, Ruby, Go, Rust, Elixir, Dart, Scala, PHP, Swift — 12+ ecosystems |
| **Overall** | **6.7/10** | Strong breadth, missing anti-patterns and depth features |

---

### 2. Database (`database.py`) — CRITICAL

**Detection inventory:**
- ORM indicators: 26 ORMs (13 original + 13 Phase A: MikroORM, Objection, jOOQ, MyBatis, Ent, sqlx, sqlc, Dapper, Exposed, Peewee, SQLModel, GORM, Sequel)
- DB type indicators: 11 types with 54 dep names (added Cassandra, CockroachDB, Turso, PlanetScale, Neon, Supabase)
- Seed dirs: 6 directory patterns + 4 seed files
- Connection pooling detection: pgbouncer, pg-pool, neon-serverless, HikariCP
- Schema pattern detection: uuid-primary-keys, soft-deletes, audit-timestamps, multi-tenancy

**Result fields populated:** 11/11 (database_type, orm, orm_version, migration_tool, migration_directory, schema_naming_convention, relationship_patterns, has_seeds, seed_directory, connection_pooling, schema_patterns)
**AST enrichment:** No
**Anti-patterns:** 3 patterns (missing migrations, no seeds, no connection pooling)
**Techniques:** file existence, dependency matching, regex (prisma schema, django models, SQLAlchemy), config parsing, anti-patterns

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | 26 ORMs, 11 DB types, 54+ dep indicators. Missing: multi-DB return (only first match), orm_version still None |
| Accuracy | 7/10 | Dependency matching + file/dir existence + regex for relationships + schema pattern scanning |
| Depth | 8/10 | Extracts: migration dirs, schema naming, seeds, relationship patterns, connection pooling, schema patterns (uuid, soft-delete, audit, multi-tenancy) |
| Template Use | 9/10 | 10/11 fields referenced in database.mdc.j2. `relationship_patterns` still not in template |
| Anti-Patterns | 7/10 | 3 anti-patterns: missing migrations (HIGH), no seeds (LOW), no connection pooling (MEDIUM) |
| Multi-Ecosystem | 9/10 | JS/TS (Prisma, TypeORM, Drizzle, Knex, Mongoose, MikroORM, Objection), Python (SQLAlchemy, Django, Tortoise, Peewee, SQLModel), Java (Hibernate, JPA, jOOQ, MyBatis, Exposed), .NET (EF, Dapper), Go (Ent, sqlx, sqlc, GORM), Ruby (Active Record, Sequel) |
| **Overall** | **8.0/10** | Significantly improved. Deep schema analysis, broad ecosystem coverage |

---

### 3. Auth (`auth.py`) — CRITICAL

**Detection inventory:**
- Auth strategy indicators: 12 strategies with 40+ dep names (jwt, session, oauth, webauthn, saml, basic, api_key, firebase, auth0, cognito, clerk, supabase)
- Permission model indicators: 3 models (RBAC, ABAC, ACL) with 7 keyword patterns
- Auth directory patterns: 10 directories
- Auth file patterns: 8 glob patterns
- OAuth provider detection: 7 providers via env vars + 7 passport deps
- MFA detection: TOTP (5 libs), WebAuthn (4 libs), SMS (3 libs)
- Middleware: 22 known middleware entries (Go, Ruby, .NET, Java additions)

**Result fields populated:** 7/8 (auth_strategy, auth_middleware, permission_model, protected_route_patterns, auth_directories, oauth_providers, mfa_methods). `rate_limiting` field exists but populated from anti-pattern check only.
**AST enrichment:** Yes — decorator-based auth detection (7 decorators), import tracing (8 auth modules)
**Anti-patterns:** 3 patterns (no auth strategy, no MFA, no rate limiting)
**Techniques:** dependency matching, file existence, regex (guard patterns), AST (decorators + imports), anti-patterns

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | 12 strategies, 22 middleware, 7 OAuth providers, 12 MFA libs. Still returns only ONE strategy (not array) |
| Accuracy | 8/10 | Dep matching + regex + AST decorators + import tracing. Permission model detection still keyword-based (fragile) |
| Depth | 8/10 | OAuth provider detection (env vars + deps), MFA methods, middleware stack, protected route patterns via regex + AST |
| Template Use | 7/10 | 5/8 fields consumed. `oauth_providers`, `mfa_methods`, `rate_limiting` NOT in auth-patterns.mdc.j2 |
| Anti-Patterns | 7/10 | 3 patterns: no auth (HIGH), no MFA (MEDIUM), no rate limiting (MEDIUM) |
| Multi-Ecosystem | 9/10 | JS/TS (passport, next-auth, lucia, clerk, supabase), Python (django, flask), Go (golang-jwt, goth, go-oidc), Ruby (devise, omniauth, sorcery, rodauth), .NET (ASP.NET Identity, Duende), Java (spring-security, keycloak) |
| **Overall** | **7.8/10** | Strong cross-ecosystem, good AST enrichment, template utilization gap |

---

### 4. Dependencies (`dependencies.py`) — HIGH IMPACT

**Detection inventory:**
- Known categories: 53 library-to-category mappings
- Lock file detection: 9 lock files
- Manifest parsing: package.json, requirements.txt, pyproject.toml (presence only), Pipfile (presence only), pom.xml (presence only), .csproj (presence only)

**Result fields populated:** 3/3 (dependencies, dependency_manifest_files, lock_file)
**AST enrichment:** No
**Anti-patterns:** None
**Techniques:** file existence, JSON parsing (package.json), regex (requirements.txt)

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 6/10 | 53 categories. pyproject.toml, Pipfile, pom.xml, .csproj detected but NOT parsed for deps. No Gemfile, Cargo.toml, go.mod parsing |
| Accuracy | 6/10 | package.json and requirements.txt well-parsed. Others presence-only |
| Depth | 5/10 | Extracts names, versions, dev flag, categories. No version normalization, no unused dep detection |
| Template Use | 10/10 | All 3 fields consumed by dependencies.mdc.j2 (NEW template created) |
| Anti-Patterns | 0/10 | None |
| Multi-Ecosystem | 4/10 | Only JS/TS and Python actually parse deps. Java/.NET/Ruby/Go/Rust detection-only |
| **Overall** | **5.2/10** | Template now exists (was dead data). Parsing depth still shallow for non-JS ecosystems |

---

### 5. Error Handling (`error_handling.py`) — HIGH IMPACT

**Detection inventory:**
- Logging framework indicators: 16 frameworks (original 13 + consola, plus better Python/Java/Ruby coverage)
- Monitoring indicators: 9 services with 22 dep names (added OpenTelemetry, Grafana agent)
- Structured logging indicators: 4 deps (structlog, pino, OpenTelemetry API, SDK)
- Logging config files: 10 known configs + config directory scan
- Custom error regex: 3 patterns (extends Error, extends BaseError, Python Exception class)

**Result fields populated:** 7/8 (error_strategy, logging_framework, logging_config_file, monitoring_integration, error_response_format, custom_error_classes, structured_logging). `error_recovery_patterns` declared but not populated.
**AST enrichment:** Yes — finds custom error/exception classes by class name suffix
**Anti-patterns:** None
**Techniques:** dependency matching, regex (throw/raise counting, custom error classes, JSON error format), AST (class definitions), file existence (logging configs)

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 7/10 | 16 logging frameworks, 9 monitoring services. Returns only ONE logging framework. Missing: error recovery patterns |
| Accuracy | 6/10 | throw/raise counting includes comments/strings (false positives). AST for custom errors is good |
| Depth | 7/10 | Structured logging detection, custom error class extraction, error strategy (exceptions vs result-types), JSON format detection |
| Template Use | 9/10 | 7/8 fields consumed. `structured_logging` not in template (new field) |
| Anti-Patterns | 0/10 | None implemented |
| Multi-Ecosystem | 7/10 | JS/TS (winston, pino, bunyan, log4js, morgan, consola), Python (logging, loguru, structlog), Java (log4j, slf4j, logback), .NET (Serilog, NLog), Ruby (Rails.logger) |
| **Overall** | **6.0/10** | Good coverage, weak accuracy on throw/raise counting, no anti-patterns |

---

### 6. i18n (`i18n.py`) — HIGH IMPACT

**Detection inventory:**
- i18n framework libs: 19 mappings (original 11 + svelte-i18n, typesafe-i18n, Lingui, Paraglide, rosetta, ICU MessageFormat)
- Translation dirs: 10 candidate directories
- File formats: 4 (JSON, YAML, PO, XLIFF)
- RTL locale prefixes: 9 prefixes
- Translation management configs: 5 (Crowdin, Lokalise, Phrase, Transifex)

**Result fields populated:** 8/9 (i18n_framework, translation_file_format, translation_directories, default_locale, supported_locales, string_externalization_pattern, translation_management, rtl_languages). `message_format` declared in model but not populated.
**AST enrichment:** No
**Anti-patterns:** None
**Techniques:** dependency matching, directory scanning, file format detection, locale pattern matching

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | 19 i18n frameworks, 5 TMS tools. Missing: message format detection, locale regex improvements for zh-Hans-CN |
| Accuracy | 7/10 | Dep matching + directory scanning + file format detection. Locale regex may miss complex codes |
| Depth | 7/10 | RTL detection, translation management, externalization patterns, locale enumeration. No translation completeness metrics |
| Template Use | 8/10 | 7/9 fields consumed. `translation_management`, `rtl_languages` NOT in i18n.mdc.j2 |
| Anti-Patterns | 0/10 | None |
| Multi-Ecosystem | 5/10 | Primarily JS/TS and Python. No Go/Ruby/Java i18n framework detection |
| **Overall** | **5.8/10** | Solid JS/TS coverage, new features (TMS, RTL) not wired to templates |

---

### 7. State Management (`state_management.py`) — HIGH IMPACT

**Detection inventory:**
- State libraries: 17 entries (13 original + ngrx-signals, legend-state, nanostores, tanstack-store)
- Data fetching libraries: 15 entries (10 original + trpc, relay, ofetch, ky, rtk-query)
- Realtime libraries: 8 entries (socket.io, pusher, ably, liveblocks, partykit, actioncable)
- Form libraries: 6 entries (react-hook-form, formik, tanstack-form, vee-validate, angular-forms, superforms)
- State patterns: 6 patterns (Redux Toolkit slices, Redux + Sagas/Thunks, Zustand stores, MobX observables, Pinia stores, Vuex modules, React Context)

**Result fields populated:** 6/6 (state_library, data_fetching_library, store_structure, state_patterns, realtime_library, form_library)
**AST enrichment:** Yes — verifies state library and data fetching imports
**Anti-patterns:** 1 pattern (multiple conflicting state libraries)
**Techniques:** dependency matching, directory scanning (store structure), AST (import verification), anti-patterns

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | 17 state + 15 data-fetching + 8 realtime + 6 form. Still returns ONE state lib + ONE data fetching lib |
| Accuracy | 8/10 | Dep matching + AST verification + store structure directory analysis |
| Depth | 7/10 | Store structure (modular/flat), state patterns, form lib, realtime lib. No state persistence detection |
| Template Use | 8/10 | 4/6 fields consumed. `realtime_library`, `form_library` NOT in state-and-config.mdc.j2 |
| Anti-Patterns | 5/10 | 1 pattern: conflicting state libraries (MEDIUM) |
| Multi-Ecosystem | 4/10 | Primarily JS/TS (React, Vue, Angular, Svelte). No Python/Java/Go state patterns |
| **Overall** | **6.7/10** | Good JS/TS depth with AST, new features not wired to templates |

---

### 8. Environment & Config (`env_config.py`) — HIGH IMPACT

**Detection inventory:**
- Config approaches: 6 (dotenv, yaml, json, vault, spring-config, dotnet-config)
- Env file patterns: 7
- Docker compose names: 6
- Feature flag systems: 12 (original 5 + Statsig, Split.io, DevCycle, Flipt, OpenFeature, ConfigCat, django-waffle)
- K8s indicators: 5 file indicators + 4 directory checks
- Secrets management: 5 dep-based + 2 file-based

**Result fields populated:** 9/9 (config_approach, env_files, has_docker, dockerfile_path, docker_compose_path, feature_flags_system, config_directories, kubernetes_detected, secrets_management)
**AST enrichment:** No
**Anti-patterns:** None
**Techniques:** file existence, directory scanning, dependency matching, config approach heuristics

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | 12 feature flag systems, 7 secrets mgmt, K8s detection. Still returns ONE config approach |
| Accuracy | 7/10 | File existence + dep matching. Docker is presence-only (no content parsing) |
| Depth | 7/10 | K8s detection, secrets management, feature flags. No Dockerfile content parsing, no config validation detection |
| Template Use | 9/10 | 8/9 fields consumed. `kubernetes_detected`, `secrets_management` NOT in state-and-config.mdc.j2 |
| Anti-Patterns | 0/10 | None |
| Multi-Ecosystem | 7/10 | JS/TS (dotenv, feature flags), Python (django-waffle), Java (spring-config), .NET (appsettings), Docker/K8s (universal) |
| **Overall** | **6.3/10** | Good breadth, new K8s/secrets features not in templates, no anti-patterns |

---

### 9. Git Workflow (`git_workflow.py`) — HIGH IMPACT

**Detection inventory:**
- Platform markers: 6
- CI config paths: 9
- PR template paths: 5
- CODEOWNERS paths: 3
- Changelog paths: 3
- Release tool paths: 6 (semantic-release, changesets, release-please, goreleaser, git-cliff)
- Commitlint files: 9
- Gitmoji detection: via deps

**Result fields populated:** 8/11 (git_platform, branch_naming_strategy, commit_message_format, pr_template_path, ci_config_path, codeowners_path, changelog_path, release_tool). `merge_strategy`, `required_reviewers`, `release_tagging` not populated.
**AST enrichment:** No
**Anti-patterns:** None
**Techniques:** file existence, YAML reading (workflow files), regex (branch patterns), dependency matching (commitlint, gitmoji)

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | CODEOWNERS, changelog, release tools all added. Missing: merge strategy detection, JIRA-prefix commit format |
| Accuracy | 7/10 | File existence + dep matching + regex on workflow YAML. Branch strategy from workflow files only (limited) |
| Depth | 6/10 | Detects presence of CODEOWNERS, changelog, release tools. No content parsing of CODEOWNERS. No commit signing |
| Template Use | 7/10 | 6/11 fields referenced. `codeowners_path`, `changelog_path`, `release_tool`, `ci_config_path`, `release_tagging` NOT in git-workflow.mdc.j2 |
| Anti-Patterns | 0/10 | None |
| Multi-Ecosystem | 8/10 | Platform-agnostic (GitHub, GitLab, Azure DevOps, Bitbucket, Drone). Release tools cover Go (goreleaser), Rust (git-cliff), JS (semantic-release, changesets) |
| **Overall** | **6.0/10** | Good file detection, but many fields not wired to template, no anti-patterns |

---

### 10. Structure (`structure.py`) — MEDIUM IMPACT

**Detection inventory:**
- Monorepo markers: 6 (lerna, pnpm-workspaces, nx, turborepo, rush, moon)
- Known directory purposes: 46 entries (added entities, widgets, features, shared for FSD)
- Organization patterns: 4 (feature-based, layered, domain-driven, flat)
- Sub-project detection: 5 parent dirs (apps, packages, services, libs, modules) x 5 manifest files

**Result fields populated:** 7/7 (root_directories, source_directories, key_directories, module_organization, is_monorepo, monorepo_tool, sub_projects)
**AST enrichment:** No
**Anti-patterns:** None
**Techniques:** directory scanning (3-level depth), pattern matching, file existence

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 7/10 | 46 known dirs, 6 monorepo markers. Missing: workspace boundary detection, polyrepo/submodule |
| Accuracy | 7/10 | Directory scanning with depth limit. Organization detection is heuristic (marker dirs) |
| Depth | 6/10 | 3-level directory scanning, sub-project detection with manifest check. Shallow for deeply nested projects |
| Template Use | 6/10 | 5/7 fields consumed. `root_directories`, `sub_projects` referenced only in architecture.mdc.j2 conditionally |
| Anti-Patterns | 0/10 | None |
| Multi-Ecosystem | 8/10 | Universal directory patterns, monorepo tools across JS/Go/Java/Rust ecosystems |
| **Overall** | **5.7/10** | Adequate structure detection, no anti-patterns, limited depth |

---

### 11. Conventions (`conventions.py`) — MEDIUM IMPACT

**Detection inventory:**
- Linter configs: 30 file-to-linter mappings (original + oxlint, golangci-lint, clippy, detekt, phpstan, phpcs)
- Formatter configs: 15 file-to-formatter mappings (original + dprint, rustfmt, clang-format)
- Naming convention detection: ESLint config parsing + AST-based sampling
- File naming detection: 50-file sampling with 4 convention classifiers

**Result fields populated:** 7/8 (linter, linter_config_path, formatter, formatter_config_path, editorconfig_path, naming_convention, file_naming_convention). `import_ordering` not populated.
**AST enrichment:** Yes — naming convention from function name sampling (10+ samples)
**Anti-patterns:** None
**Techniques:** file existence, config content parsing (ESLint, pyproject.toml), file sampling (naming), AST (naming)

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | 30 linters, 15 formatters. Missing: import ordering (isort), comment style, max line length |
| Accuracy | 7/10 | File existence + config content parsing + statistical file naming. AST naming is solid |
| Depth | 6/10 | Detects linter/formatter + naming convention. No rule parsing, no import ordering, no comment convention |
| Template Use | 9/10 | 7/8 fields consumed. `import_ordering` declared but never populated or consumed |
| Anti-Patterns | 0/10 | None |
| Multi-Ecosystem | 9/10 | JS/TS (ESLint, Prettier, Biome, Oxlint), Python (ruff, pylint, flake8, black), Go (golangci-lint), Rust (clippy, rustfmt), Kotlin (detekt), PHP (phpstan, phpcs), C/C++ (clang-format) |
| **Overall** | **6.5/10** | Excellent cross-ecosystem linter coverage, AST naming is strong, lacks depth |

---

### 12. Security (`security.py`) — MEDIUM IMPACT

**Detection inventory:**
- Validation libraries: 15 (zod, joi, yup, class-validator, ajv, express-validator, cerberus, marshmallow, pydantic, voluptuous, wtforms, django-forms, fluent-validation, valibot, typebox)
- Security middleware: 9 entries (helmet, csurf, cors, express-rate-limit, django middlewares, spring-security)
- Secrets management: 5 file-based detections (dotenv-vault, vault, sops, doppler, infisical)
- Vulnerability scanners: 8 (snyk, bandit, semgrep, dependabot, renovate, trivy, brakeman, codeql)

**Result fields populated:** 6/6 (input_validation, cors_config, secrets_management, csp_headers, security_middleware, vulnerability_scanning)
**AST enrichment:** No
**Anti-patterns:** 4 patterns (.env not gitignored, no vuln scanning, no input validation, no CSP, no secrets mgmt with multiple .env)
**Techniques:** dependency matching, file existence, config content scanning, anti-patterns

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | 15 validation libs, 9 middleware, 5 secrets mgmt, 8 vuln scanners = 37 items. Missing: HTTPS enforcement, rate limiting as separate field |
| Accuracy | 7/10 | Dep matching + file existence. CORS detection checks Django settings content. CSP checks for "helmet" dep or Python source content |
| Depth | 7/10 | Vuln scanner detection, secrets management, CSP check, middleware stack. No actual config parsing |
| Template Use | 10/10 | All 6 fields consumed by security.mdc.j2 |
| Anti-Patterns | 8/10 | 4 patterns: .env exposure (CRITICAL), no vuln scanning (MEDIUM), no validation (HIGH), no CSP (MEDIUM), no secrets mgmt (MEDIUM) |
| Multi-Ecosystem | 7/10 | JS/TS (helmet, express-rate-limit, zod), Python (bandit, django middlewares, pydantic), Java (spring-security), .NET (FluentValidation), Ruby (brakeman). Missing Go/Rust |
| **Overall** | **7.8/10** | Strong anti-pattern detection, good coverage, template fully utilized |

---

### 13. Testing (`testing.py`) — MEDIUM IMPACT

**Detection inventory:**
- Test framework files: 14 config-to-framework mappings
- Mocking libraries: 15 entries
- Coverage tools: 9 entries
- E2E frameworks: 10 entries
- API testing tools: 4 (supertest, httpx, rest-assured, newman)
- Visual regression tools: 4 (chromatic, percy, applitools, backstopjs)
- Fixture dirs: 5

**Result fields populated:** 14/14 (test_framework, test_runner, test_directories, test_file_pattern, mocking_library, coverage_tool, coverage_config_path, fixture_patterns, e2e_framework, test_organization, snapshot_testing, api_testing_tools, visual_regression_tool)
**AST enrichment:** No
**Anti-patterns:** 4 patterns (no tests, no framework configured, no coverage, no E2E, excessive snapshots)
**Techniques:** file existence, dependency matching, file sampling (200 files for patterns), directory scanning, pyproject.toml parsing, anti-patterns

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | 14 frameworks, 15 mocking, 9 coverage, 10 E2E, 4 API testing, 4 visual regression = 56 items. Missing: contract testing, parallel execution |
| Accuracy | 7/10 | Config files + dep matching + file pattern sampling (200 files). pyproject.toml fallback |
| Depth | 8/10 | Test organization (collocated/separated/BDD), snapshot detection, API testing, visual regression, coverage config |
| Template Use | 8/10 | 11/14 fields consumed. `test_organization`, `snapshot_testing`, `api_testing_tools` NOT in testing.mdc.j2 |
| Anti-Patterns | 8/10 | 4 patterns: no tests (CRITICAL), no framework (HIGH), no coverage (MEDIUM), no E2E (MEDIUM), excessive snapshots (LOW) |
| Multi-Ecosystem | 7/10 | JS/TS (jest, vitest, mocha, cypress, playwright), Python (pytest, coverage), Java (mockito, jacoco), .NET (moq, coverlet), Ruby (rspec, simplecov), Rust (cargo-tarpaulin, mockall) |
| **Overall** | **7.7/10** | Comprehensive with good anti-patterns, new fields not fully wired |

---

### 14. CI/CD (`cicd.py`) — MEDIUM IMPACT

**Detection inventory:**
- CI platforms: 15 entries (original 9 + Drone, Woodpecker, Buildkite, Dagger, AppVeyor, AWS CodeBuild)
- Deployment targets: 17 entries (original 9 + Railway, SST, Pulumi, AWS CDK, Helm, Kustomize, GCP App Engine, Heroku)
- Build step extraction: GitHub Actions YAML parsing (uses + run commands)
- Caching detection: keyword search in config
- Matrix build detection: keyword search in config

**Result fields populated:** 7/9 (platform, config_path, build_steps, deployment_targets, caching_detected, matrix_builds). `required_checks` always empty (offline limitation). `deployment_patterns`, `release_tool` declared but not populated here.
**AST enrichment:** No
**Anti-patterns:** 3 patterns (no CI/CD, no caching, no deployment targets)
**Techniques:** file existence, YAML parsing (GitHub Actions), keyword scanning, anti-patterns

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | 15 CI platforms, 17 deployment targets. Good breadth. Build steps only from GH Actions (limited for others) |
| Accuracy | 6/10 | GH Actions YAML parsing is good. Other platforms use line-based heuristic. Caching/matrix are keyword searches |
| Depth | 6/10 | Build step extraction, caching detection, matrix detection. Still first-line-only for run commands. Truncates at 20 |
| Template Use | 10/10 | All relevant fields consumed by cicd.mdc.j2 (NEW template created) |
| Anti-Patterns | 7/10 | 3 patterns: no CI (HIGH), no caching (MEDIUM), no deployment targets (MEDIUM) |
| Multi-Ecosystem | 9/10 | Platform-agnostic: GH Actions, GitLab CI, Jenkins, Azure, Bitbucket, CircleCI, Travis, Drone, Woodpecker, Buildkite, Dagger, AppVeyor, GCP Cloud Build, AWS CodeBuild |
| **Overall** | **7.7/10** | Template now exists (was dead data). Good platform breadth with anti-patterns |

---

### 15. Design/UI (`design.py`) — MEDIUM IMPACT

**Detection inventory:**
- Component libraries: 30 entries (18 original + Ark UI, React Aria, Flowbite, HeroUI, Skeleton, Element Plus, Naive UI, Angular Material, PrimeNG, shadcn, base-ui, nextui, park-ui, daisyui)
- CSS methodologies: 12 entries (original + vanilla-extract, panda-css, stylex, unocss, linaria, lightningcss) + css-modules fallback
- Icon libraries: 10 entries
- Component doc tools: 3 (storybook, histoire, ladle)
- Font strategy: 3 dep-based + google-fonts-cdn detection
- Design tokens: 7 file patterns
- Responsive: 2 strategies
- Theme provider: 3 entries

**Result fields populated:** 13/13 (css_methodology, component_library, component_library_version, design_tokens_format, design_tokens_path, responsive_strategy, theme_provider, styling_directories, uses_shared_design_system, shared_design_system_name, icon_library, component_doc_tool, font_strategy)
**AST enrichment:** No
**Anti-patterns:** None
**Techniques:** dependency matching, file existence, directory scanning, config file detection, HTML content scanning (fonts)

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 9/10 | 30 component libs, 12 CSS methods, 10 icon libs, 3 doc tools, 7 token patterns. Very comprehensive |
| Accuracy | 7/10 | Dep matching + file existence + css-modules fallback from source file scanning |
| Depth | 8/10 | Icon library, component doc tool, font strategy, design tokens with path resolution, shared design system. No Tailwind config parsing |
| Template Use | 9/10 | 12/13 fields consumed. `icon_library`, `component_doc_tool`, `font_strategy` NOT in design-system.mdc.j2, but `theme_provider` IS now wired |
| Anti-Patterns | 0/10 | None |
| Multi-Ecosystem | 5/10 | Primarily JS/TS (React, Vue, Angular, Svelte, Solid). No server-side or mobile UI frameworks |
| **Overall** | **6.3/10** | Excellent item coverage, new fields not in template, no anti-patterns |

---

### 16. Accessibility (`accessibility.py`) — MEDIUM IMPACT

**Detection inventory:**
- A11y tools: 16 entries (9 original + axe-playwright, cypress-axe, storybook-a11y, vitest-axe, eslint-vuejs-a11y, focus-trap)
- WCAG config files: 4
- Semantic HTML tags: 7
- Form accessibility patterns: 4 (label-association, aria-required, aria-invalid, fieldset-legend)
- Focus management patterns: 3 (focus-trap, skip-link, focus-visible)

**Result fields populated:** 8/8 (wcag_level, a11y_testing_tools, aria_usage_detected, semantic_html_score, keyboard_navigation, color_contrast_config, form_accessibility, focus_management_patterns)
**AST enrichment:** No
**Anti-patterns:** 5 patterns (no a11y tools, no ARIA, low semantic HTML, no form a11y, no focus management)
**Techniques:** dependency matching, file existence, content scanning (ARIA, semantic tags, keyboard events, form patterns, focus patterns), ratio calculation, anti-patterns

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 7/10 | 16 a11y tools, 4 WCAG configs. Missing: alt text coverage, specific ARIA pattern breakdown |
| Accuracy | 6/10 | ARIA detection is binary (any aria-/role=). Semantic HTML is ratio-based. Keyboard is keyword match |
| Depth | 7/10 | Form accessibility (4 patterns), focus management (3 patterns), semantic HTML scoring. No actual WCAG compliance scanning |
| Template Use | 10/10 | ALL 8 fields now consumed by accessibility.mdc.j2 (semantic_html_score, keyboard_navigation, color_contrast_config all wired) |
| Anti-Patterns | 9/10 | 5 patterns: no tools (MEDIUM), no ARIA (MEDIUM), low semantic HTML (HIGH), no form a11y (MEDIUM), no focus mgmt (LOW) |
| Multi-Ecosystem | 3/10 | Primarily React/Vue/HTML. No native mobile, no server-rendered a11y |
| **Overall** | **7.0/10** | Strong anti-patterns, all fields wired, good form/focus detection |

---

### 17. API (`api.py`) — MEDIUM IMPACT

**Detection inventory:**
- GraphQL indicators: 10 dep names
- gRPC indicators: 4 dep names
- tRPC indicators: 2 dep names
- REST detection: 12 framework deps + directory heuristics + Next.js App Router
- API directories: 8 candidates
- OpenAPI spec paths: 9 candidates
- Validation libs: 15 (shared from deps.py)
- Pagination: 2 patterns (cursor-based, offset-based)
- Versioning: url-path detection

**Result fields populated:** 8/8 (api_style, route_structure, api_directories, openapi_spec_path, request_validation, response_format, pagination_pattern, versioning_strategy)
**AST enrichment:** Yes — REST decorator detection (10 decorators), GraphQL import tracing (6 modules)
**Anti-patterns:** None
**Techniques:** dependency matching, directory scanning, file existence, content scanning (pagination), AST (decorators + imports)

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 7/10 | GraphQL, gRPC, tRPC, REST well-covered. Missing: SOAP, webhook detection, GraphQL subscriptions |
| Accuracy | 7/10 | Dep matching + AST decorators for REST + GraphQL imports. Pagination is keyword-based (fragile) |
| Depth | 7/10 | Route structure detection, OpenAPI spec, pagination, versioning, validation. No error response format beyond "json" |
| Template Use | 10/10 | All 8 fields consumed by api-patterns.mdc.j2 |
| Anti-Patterns | 0/10 | None |
| Multi-Ecosystem | 6/10 | JS/TS (Express, Fastify, NestJS, Next.js), Python (FastAPI, Flask, Django), Java (Spring Boot). Missing Go, Ruby, .NET |
| **Overall** | **6.2/10** | Solid AST enrichment, full template utilization, no anti-patterns |

---

### 18. Performance (`performance.py`) — MEDIUM IMPACT

**Detection inventory:**
- Caching strategies: 6 (redis, ioredis, bull, memcached, node-cache, django-redis, lru-cache, upstash-redis, keyv)
- Lazy loading patterns: 4 (React.lazy, lazy(), dynamic(), @loadable)
- Code splitting: 3 patterns + next.config.js
- Bundle configs: 8 tools
- Image optimization: 4 (sharp, next/image, imagemin, Pillow)
- N+1 prevention: 4 (DataLoader, django-auto-prefetch, nplusone, bullet)
- Monitoring: 9 services
- Web vitals: 3 deps + 3 lighthouse configs
- Service worker: 4 file patterns + 3 deps

**Result fields populated:** 10/10 (caching_strategy, lazy_loading, code_splitting, bundle_size_config, image_optimization, n_plus_one_prevention, performance_monitoring, web_vitals_monitoring, service_worker_detected, cdn_detected [not populated])
**AST enrichment:** No
**Anti-patterns:** 3 patterns (no web vitals monitoring, no lazy loading/code splitting, no image optimization)
**Techniques:** dependency matching, file existence, content scanning (lazy/dynamic imports), anti-patterns

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | 9 caching, 9 monitoring, 4 image opt, 4 N+1, 3 web vitals. Missing: CDN detection, compression (gzip/brotli), font optimization |
| Accuracy | 7/10 | Dep matching + source scanning for lazy loading / code splitting patterns |
| Depth | 7/10 | Web vitals, service worker, N+1 prevention, monitoring. `cdn_detected` declared but not populated |
| Template Use | 9/10 | 9/10 fields consumed (bundle_size_config IS now in performance.mdc.j2). `cdn_detected` not populated |
| Anti-Patterns | 7/10 | 3 patterns: no web vitals (MEDIUM), no lazy/splitting (MEDIUM), no image opt (LOW) |
| Multi-Ecosystem | 5/10 | Primarily JS/TS + Python (Pillow, django caching). No Java/Go/Rust performance patterns |
| **Overall** | **7.2/10** | Good depth with web vitals and service worker detection, decent anti-patterns |

---

### 19. Frontend Patterns (`frontend_patterns.py`) — MEDIUM IMPACT

**Detection inventory:**
- Form libraries: 8 entries
- Routing libraries: 7 entries
- Animation libraries: 10 entries (added auto-animate, react-transition-group, rive)
- Virtualization libraries: 5 entries
- Layout patterns: 3 dep-based + 5 layout dirs + CSS grid/flexbox content scanning
- Modal patterns: 4 dep-based + custom-modal file name heuristic
- Loading patterns: 4 (skeleton, spinner, suspense, loading-state)

**Result fields populated:** 8/8 (layout_patterns, form_libraries, modal_pattern, list_virtualization, error_boundary, loading_patterns, routing_library, animation_library)
**AST enrichment:** Yes — ErrorBoundary component detection, form library import verification
**Anti-patterns:** 2 patterns (no error boundary, no loading patterns)
**Techniques:** dependency matching, content scanning (layout, error boundary, loading patterns, modal files), AST (components + imports), anti-patterns

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 8/10 | 8 form, 7 routing, 10 animation, 5 virtualization = 42 items. Missing: component composition patterns (HOC, render props) |
| Accuracy | 7/10 | Dep matching + content scanning + AST verification for ErrorBoundary and forms |
| Depth | 7/10 | Layout pattern detection (multiple patterns), loading patterns (4 types), modal detection. No responsive behavior |
| Template Use | 10/10 | All 8 fields consumed by frontend pattern references (project-overview.mdc.j2 and others) |
| Anti-Patterns | 6/10 | 2 patterns: no error boundary (MEDIUM), no loading patterns (LOW) |
| Multi-Ecosystem | 3/10 | JS/TS only (React, Vue, Angular, Svelte). No server-side or mobile |
| **Overall** | **6.8/10** | Good AST enrichment, all fields utilized, limited to frontend JS/TS |

---

### 20. User Flows (`user_flows.py`) — MEDIUM IMPACT

**Detection inventory:**
- Page directories: 10 candidates
- Route detection: file-based (7 extensions) + router file fallback
- Navigation type: 6 types (next-app-router, next-pages-router, react-router, vue-router, angular-router, wouter, file-based)
- Auth-protected route patterns: 9 keywords
- 404 detection: 4 name patterns
- Error page: 4 name patterns
- Dynamic route markers: 3 patterns ([, ], $)

**Result fields populated:** 9/9 (route_count, route_files, navigation_type, auth_protected_routes, has_404_page, has_error_page, page_directories, dynamic_routes, lazy_routes)
**AST enrichment:** No
**Anti-patterns:** None
**Techniques:** directory scanning, file pattern matching, content scanning (auth routes, lazy routes), file existence

| Metric | Score | Details |
|--------|-------|---------|
| Coverage | 7/10 | 10 page dirs, 6 nav types, dynamic routes, lazy routes. Missing: nested routes, middleware/guards per route, redirects |
| Accuracy | 6/10 | File-based route counting, keyword matching for auth protection. Dynamic route detection via filename chars |
| Depth | 7/10 | Dynamic route detection, lazy route detection, auth-protected routes, 404/error page detection |
| Template Use | 10/10 | All 9 fields consumed in project-overview.mdc.j2 and contributor-guide.mdc.j2 |
| Anti-Patterns | 0/10 | None |
| Multi-Ecosystem | 4/10 | JS/TS only (Next.js, React Router, Vue Router, Angular Router, Wouter) |
| **Overall** | **5.7/10** | Good feature set for JS frameworks, no anti-patterns, limited ecosystem |

---

## Summary Table

| # | Analyzer | Coverage | Accuracy | Depth | Template | Anti-Pat | Multi-Eco | Overall |
|---|----------|----------|----------|-------|----------|----------|-----------|---------|
| 1 | Tech Stack | 8 | 7 | 6 | 10 | 0 | 9 | **6.7** |
| 2 | Database | 8 | 7 | 8 | 9 | 7 | 9 | **8.0** |
| 3 | Auth | 8 | 8 | 8 | 7 | 7 | 9 | **7.8** |
| 4 | Dependencies | 6 | 6 | 5 | 10 | 0 | 4 | **5.2** |
| 5 | Error Handling | 7 | 6 | 7 | 9 | 0 | 7 | **6.0** |
| 6 | i18n | 8 | 7 | 7 | 8 | 0 | 5 | **5.8** |
| 7 | State Mgmt | 8 | 8 | 7 | 8 | 5 | 4 | **6.7** |
| 8 | Env Config | 8 | 7 | 7 | 9 | 0 | 7 | **6.3** |
| 9 | Git Workflow | 8 | 7 | 6 | 7 | 0 | 8 | **6.0** |
| 10 | Structure | 7 | 7 | 6 | 6 | 0 | 8 | **5.7** |
| 11 | Conventions | 8 | 7 | 6 | 9 | 0 | 9 | **6.5** |
| 12 | Security | 8 | 7 | 7 | 10 | 8 | 7 | **7.8** |
| 13 | Testing | 8 | 7 | 8 | 8 | 8 | 7 | **7.7** |
| 14 | CI/CD | 8 | 6 | 6 | 10 | 7 | 9 | **7.7** |
| 15 | Design/UI | 9 | 7 | 8 | 9 | 0 | 5 | **6.3** |
| 16 | Accessibility | 7 | 6 | 7 | 10 | 9 | 3 | **7.0** |
| 17 | API | 7 | 7 | 7 | 10 | 0 | 6 | **6.2** |
| 18 | Performance | 8 | 7 | 7 | 9 | 7 | 5 | **7.2** |
| 19 | Frontend Pat. | 8 | 7 | 7 | 10 | 6 | 3 | **6.8** |
| 20 | User Flows | 7 | 6 | 7 | 10 | 0 | 4 | **5.7** |

---

## Aggregate Score

### Dimension Averages (across all 20 analyzers)

| Dimension | Average | Notes |
|-----------|---------|-------|
| Coverage | 7.65/10 | Strong item counts across most analyzers |
| Accuracy | 6.85/10 | Mostly dep matching + file existence; some AST |
| Depth | 6.75/10 | Many analyzers go beyond presence to extract details |
| Template Utilization | 8.90/10 | Dramatically improved with new templates (deps, cicd) and wired fields |
| Anti-Pattern Detection | 3.20/10 | Only 9/20 analyzers have anti-patterns |
| Multi-Ecosystem | 6.10/10 | Strong for JS/TS + Python; weaker for Go, Ruby, .NET, Rust |

### Weighted Overall Score

Using weights: Coverage (25%), Accuracy (20%), Depth (20%), Template (15%), Anti-Patterns (10%), Multi-Ecosystem (10%)

```
Score = (7.65 * 0.25) + (6.85 * 0.20) + (6.75 * 0.20) + (8.90 * 0.15) + (3.20 * 0.10) + (6.10 * 0.10)
      = 1.9125 + 1.370 + 1.350 + 1.335 + 0.320 + 0.610
      = 6.90/10
```

### Per-Analyzer Weighted Average

Simple average of all 20 analyzer Overall scores:
```
(6.7 + 8.0 + 7.8 + 5.2 + 6.0 + 5.8 + 6.7 + 6.3 + 6.0 + 5.7 + 6.5 + 7.8 + 7.7 + 7.7 + 6.3 + 7.0 + 6.2 + 7.2 + 6.8 + 5.7) / 20
= 131.1 / 20
= 6.56/10
```

**New Aggregate Score: 6.7/10** (average of both methods, rounded)

---

## Comparison: Before vs After

| Metric | Before (6.3/10) | After (6.7/10) | Delta |
|--------|-----------------|----------------|-------|
| Analysis Accuracy | 6.0 | 6.85 | +0.85 |
| Analysis Completeness | 5.0 | 7.65 | +2.65 |
| Detection Items | ~350 estimated | **780+ counted** | +430 |
| Anti-Pattern Analyzers | 0/20 | **9/20** | +9 |
| Anti-Pattern Count | 0 total | **31 distinct patterns** | +31 |
| Dead Data (no template) | 2 dimensions | **0 dimensions** | -2 |
| Wasted Fields (unused) | ~12 fields | ~8 fields | -4 |
| Template Count | 15 templates | **19 templates** (+deps, cicd) | +4 |
| AST-Enabled Analyzers | 0 | **5** (auth, error_handling, state_mgmt, api, frontend_patterns, conventions) | +5/6 |
| Phase A Items Added | N/A | ~210 new detection items | +210 |
| Phase B Fields Added | N/A | ~25 new model fields | +25 |
| Phase C Logic Changes | N/A | ~15 implemented | +15 |
| _should_generate guards | 3 too-loose | **3 tightened** | fixed |

**Score improvement: 6.3 -> 6.7 (+0.4 points, ~6.3% improvement)**

The improvement is modest because:
1. Anti-pattern detection is still only in 9/20 analyzers (11 have score 0/10)
2. Multi-ecosystem coverage remains JS/TS-heavy
3. Several new fields (oauth_providers, mfa_methods, realtime_library, form_library, kubernetes_detected, secrets_management, etc.) are not yet wired into templates
4. Accuracy improvements require AST (which is available but only used in 5-6 analyzers)
5. Many analyzers still return single values instead of arrays

---

## Top Strengths

1. **Template utilization is now excellent (8.9/10)** — dependencies and CI/CD are no longer dead data; accessibility fields are fully wired
2. **Detection breadth is strong (780+ items)** — Phase A additions significantly expanded framework/tool coverage across all analyzers
3. **Anti-pattern detection exists and is meaningful** — Security (4 patterns), Testing (4 patterns), Accessibility (5 patterns), CI/CD (3 patterns), Database (3 patterns) provide real actionable warnings
4. **AST enrichment works in 5-6 analyzers** — Auth (decorators), Error Handling (class names), State Management (import verification), API (route decorators), Frontend (components), Conventions (naming)
5. **Cross-ecosystem coverage is strong in CRITICAL analyzers** — Database (26 ORMs across 6 ecosystems), Auth (12 strategies across 6 ecosystems), Tech Stack (36 frameworks across 12+ language ecosystems)
6. **Schema pattern detection in Database** — UUID PKs, soft deletes, audit timestamps, multi-tenancy are genuinely useful signals

---

## Remaining Gaps

### Critical Gaps (impact score improvement significantly)

1. **11/20 analyzers have NO anti-pattern detection** — Tech Stack, Dependencies, Error Handling, i18n, Env Config, Git Workflow, Structure, Conventions, Design/UI, API, User Flows all score 0/10
2. **Single-value returns** — Auth returns ONE strategy (not array), Database returns ONE db_type, Error Handling returns ONE logging framework, State returns ONE state lib. Real projects use multiple
3. **~8 new fields not wired to templates** — oauth_providers, mfa_methods, realtime_library, form_library, kubernetes_detected, secrets_management, translation_management, rtl_languages are populated but invisible in generated rules

### Moderate Gaps

4. **Dependencies analyzer is shallow** — Only parses package.json and requirements.txt. pyproject.toml, Gemfile, Cargo.toml, go.mod NOT parsed for actual dependency extraction
5. **Accuracy ceiling without more AST** — throw/raise counting includes comments; pagination detection is keyword-based; permission model "RBAC" triggers on any file containing "role"
6. **Version normalization absent** — Raw strings like "^18.0.0" stored instead of "18.0.0"
7. **Language weighting absent** — Test files and config files count equally with source code in language percentages

### Minor Gaps

8. **No import ordering detection** (Conventions)
9. **No nested route detection** (User Flows)
10. **No Tailwind config parsing** (Design/UI)
11. **No CDN detection populated** (Performance)
12. **No contract testing detection** (Testing)

---

## Detection Item Inventory (Exact Counts)

| Analyzer | Detection Items | Breakdown |
|----------|----------------|-----------|
| Tech Stack | 108 | 31 extensions + 36 frameworks + 21 build tools + 20 pkg managers |
| Database | 91 | 26 ORMs + 54 DB type deps + 6 seed dirs + 4 seed files + 1 connection pooling check |
| Auth | 82 | 40+ strategy deps + 7 perm indicators + 10 dirs + 8 file patterns + 7 OAuth providers + 12 MFA libs |
| Dependencies | 62 | 53 categories + 9 lock files |
| Error Handling | 47 | 16 logging + 22 monitoring deps + 4 structured logging + 3 error regex + 10 config files |
| i18n | 43 | 19 frameworks + 10 dirs + 4 formats + 5 TMS configs + 9 RTL prefixes |
| State Mgmt | 46 | 17 state + 15 data-fetching + 8 realtime + 6 form |
| Env Config | 38 | 6 approaches + 7 env files + 6 compose + 12 feature flags + 5 K8s + 7 secrets |
| Git Workflow | 41 | 6 platforms + 9 CI + 5 PR templates + 3 CODEOWNERS + 3 changelog + 6 release tools + 9 commitlint |
| Structure | 57 | 6 monorepo + 46 dir purposes + 4 org patterns + 5 sub-project manifest files |
| Conventions | 46 | 30 linters + 15 formatters + 1 editorconfig |
| Security | 37 | 15 validation + 9 middleware + 5 secrets + 8 vuln scanners |
| Testing | 56 | 14 frameworks + 15 mocking + 9 coverage + 10 E2E + 4 API test + 4 visual regression |
| CI/CD | 32 | 15 platforms + 17 deployment targets |
| Design/UI | 72 | 30 component libs + 12 CSS + 10 icon + 3 doc tools + 7 tokens + 3 font + 2 responsive + 3 theme + 6 style dirs |
| Accessibility | 30 | 16 tools + 4 WCAG configs + 7 semantic tags + 4 form a11y + 3 focus patterns |
| API | 46 | 10 GraphQL + 4 gRPC + 2 tRPC + 12 REST + 8 dirs + 9 OpenAPI + 15 validation + 2 pagination |
| Performance | 40 | 9 caching + 4 lazy + 3 splitting + 8 bundle + 4 image + 4 N+1 + 9 monitoring + 3 web vitals + 4 SW |
| Frontend Pat. | 42 | 8 form + 7 routing + 10 animation + 5 virtualization + 4 modal + 4 loading + 5 layout dirs |
| User Flows | 39 | 10 page dirs + 6 nav types + 9 auth keywords + 4 patterns (404) + 4 (error) + 3 dynamic + route extensions |

**Total detection items: 1,055**

---

## Recommendations for Next Improvement Phase

### High Impact (would move score from 6.7 to ~7.5)

1. **Add anti-patterns to remaining 11 analyzers** — Each analyzer should flag at least 2-3 bad practices
2. **Wire remaining 8 unconnected fields into templates** — oauth_providers, mfa_methods, form_library, realtime_library, kubernetes_detected, secrets_management, translation_management, rtl_languages
3. **Return arrays instead of singles** for auth_strategy, database_type, logging_framework, state_library, data_fetching_library, config_approach (Phase C1 from research)
4. **Parse pyproject.toml, Gemfile, Cargo.toml, go.mod** for actual dependency extraction

### Medium Impact

5. **Normalize version strings** to semver across all analyzers
6. **Weight language percentages** excluding test/config/generated files
7. **Expand AST usage** to more analyzers (Database for TypeORM decorators, Design for component pattern detection)
8. **Add error recovery pattern detection** (retry, circuit breaker, fallback)
