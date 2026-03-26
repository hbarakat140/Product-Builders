# DevOps, Code Quality & Infrastructure Analyzer Research

Deep research conducted 2026-03-26 covering framework detection, code quality tools, environment management, git workflows, i18n, performance monitoring, and industry shifts.

## Tech Stack Detection Checklist

### Missing Frameworks (17)

| Framework | Ecosystem | Package | Config File | Category |
|-----------|-----------|---------|------------|----------|
| Astro | JS/TS | `astro` | `astro.config.mjs` | Static/SSR hybrid |
| Hono | JS/TS | `hono` | `hono` imports | Edge-first web framework |
| Elysia | JS/TS (Bun) | `elysia` | Elysia server setup | Bun web framework |
| SvelteKit | JS/TS | `@sveltejs/kit` | `svelte.config.js` | Svelte metaframework |
| SolidJS | JS/TS | `solid-js` | `solid` Vite plugin | Reactive UI framework |
| SolidStart | JS/TS | `@solidjs/start` | `app.config.ts` | Solid metaframework |
| Qwik | JS/TS | `@builder.io/qwik` | `qwik.config.ts` | Resumable framework |
| QwikCity | JS/TS | `@builder.io/qwik-city` | QwikCity routes | Qwik metaframework |
| Deno Fresh | JS/TS (Deno) | `fresh` | `fresh.config.ts` | Deno web framework |
| Litestar | Python | `litestar` | Litestar app config | Modern Python ASGI |
| FastHTML | Python | `fasthtml` | FastHTML app setup | Python HTML framework |
| TanStack Start | JS/TS | `@tanstack/start` | TanStack router config | Full-stack React |
| Analog | JS/TS | `@analogjs/platform` | `analog.config.ts` | Angular metaframework |
| H3 | JS/TS | `h3` | H3 event handlers | Minimal HTTP framework |
| Nitro | JS/TS | `nitropack` | `nitro.config.ts` | Universal server engine |
| Bun runtime | JS/TS | `bun` binary | `bunfig.toml` | JavaScript runtime |
| Deno runtime | JS/TS | `deno` binary | `deno.json`, `deno.jsonc` | JavaScript runtime |

### Metaframework Detection

| Stack | Components | Detection Pattern |
|-------|-----------|-------------------|
| T3 Stack | Next.js + tRPC + Prisma + Tailwind + NextAuth | All five dependencies present |
| MERN | MongoDB + Express + React + Node.js | `mongoose` + `express` + `react` |
| MEAN | MongoDB + Express + Angular + Node.js | `mongoose` + `express` + `@angular/core` |
| JAMstack | JavaScript + APIs + Markup | Static site generator + headless CMS + CDN deploy |
| LAMP | Linux + Apache + MySQL + PHP | `apache2`, `mysql`, PHP config |
| Django + HTMX | Django + HTMX + Alpine.js | `django` + `htmx` + `alpinejs` |

### Monorepo Tools (9)

| Tool | Config File | Detection Pattern |
|------|------------|-------------------|
| Turborepo | `turbo.json` | `pipeline:`, `turbo run` |
| Nx | `nx.json`, `project.json` | `targets:`, `nx run` |
| pnpm workspaces | `pnpm-workspace.yaml` | `packages:` glob patterns |
| yarn workspaces | `package.json` `workspaces` field | Yarn Berry or Classic |
| npm workspaces | `package.json` `workspaces` field | npm 7+ |
| Lerna | `lerna.json` | Legacy -- often paired with Nx now |
| Rush | `rush.json` | Microsoft monorepo tool |
| Moon | `.moon/workspace.yml` | Task runner + monorepo |
| Bazel | `WORKSPACE`, `BUILD` | Google build system |

### Missing Package Managers

| Manager | Ecosystem | Config File | Detection |
|---------|-----------|------------|-----------|
| Deno | JS/TS | `deno.json`, `deno.lock` | `deno` imports, `jsr:` specifiers |
| conda/mamba | Python/ML | `environment.yml`, `conda-lock.yml` | `conda install`, `mamba install` |
| pixi | Python/Rust | `pixi.toml`, `pixi.lock` | `pixi install`, conda-forge |
| Swift PM | Swift | `Package.swift` | `dependencies:` in Package.swift |
| Pub | Dart/Flutter | `pubspec.yaml`, `pubspec.lock` | `pub get`, `flutter pub` |
| CocoaPods | iOS | `Podfile`, `Podfile.lock` | `pod install` |

---

## Code Quality Detection Checklist

### Linters Per Ecosystem

| Ecosystem | Linters | Config Files |
|-----------|---------|-------------|
| JS/TS | ESLint 9 (`eslint.config.js` flat config), Biome 2.x (`biome.json`), oxlint (`oxlintrc.json`) | `eslint.config.js`, `biome.json`, `.oxlintrc.json` |
| Python | Ruff (`ruff.toml`, `pyproject.toml`), Pylint (`.pylintrc`), Flake8 (`.flake8`), mypy (`mypy.ini`) | `ruff.toml`, `.pylintrc`, `.flake8`, `mypy.ini` |
| Go | golangci-lint (`.golangci.yml`) | `.golangci.yml`, `.golangci.yaml` |
| Rust | clippy (built-in) | `clippy.toml`, `Cargo.toml` lint config |
| Ruby | RuboCop (`.rubocop.yml`) | `.rubocop.yml` |
| Java | Checkstyle (`checkstyle.xml`), PMD (`pmd-ruleset.xml`), SpotBugs | `checkstyle.xml`, `pmd-ruleset.xml` |
| Kotlin | ktlint (`.editorconfig`), detekt (`detekt.yml`) | `.editorconfig`, `detekt.yml` |
| PHP | PHP_CodeSniffer (`phpcs.xml`), PHPStan (`phpstan.neon`) | `phpcs.xml`, `phpstan.neon` |
| CSS | Stylelint (`.stylelintrc`) | `.stylelintrc`, `.stylelintrc.json` |

### Formatters

| Formatter | Ecosystem | Config File | Notes |
|-----------|-----------|------------|-------|
| Prettier | JS/TS/CSS/HTML | `.prettierrc`, `prettier.config.js` | Most popular multi-language |
| Biome | JS/TS/JSON/CSS | `biome.json` | Lint + format combined |
| dprint | JS/TS/JSON/Markdown | `dprint.json` | Fast Rust-based |
| Oxfmt | JS/TS | Part of oxc toolchain | Experimental |
| Ruff format | Python | `ruff.toml`, `pyproject.toml` | Replaces Black |
| Black | Python | `pyproject.toml` [tool.black] | Legacy -- Ruff replacing |
| gofmt/gofumpt | Go | Built-in / `gofumpt` | Go standard formatting |
| rustfmt | Rust | `rustfmt.toml` | Rust standard formatting |
| google-java-format | Java | Maven/Gradle plugin | Google style |
| clang-format | C/C++ | `.clang-format` | LLVM formatter |

### Import Ordering

| Tool | Ecosystem | Config | Notes |
|------|-----------|--------|-------|
| eslint-plugin-import | JS/TS | ESLint config | Import sorting/validation |
| eslint-plugin-simple-import-sort | JS/TS | ESLint config | Auto-fixable sorting |
| isort | Python | `pyproject.toml` [tool.isort] | Python import sorting |
| Ruff isort | Python | `ruff.toml` (isort rules) | Replaces standalone isort |
| goimports | Go | Built-in | Go import formatting |

### Quality Platforms

| Platform | Config | Integration |
|----------|--------|-------------|
| SonarQube/SonarCloud | `sonar-project.properties` | CI integration, quality gates |
| CodeClimate | `.codeclimate.yml` | GPA scoring, maintainability |
| Codacy | `.codacy.yml` | Automated code review |
| Codecov | `codecov.yml` | Coverage reporting |
| Coveralls | `.coveralls.yml` | Coverage tracking |
| CodeQL | `.github/codeql/` | GitHub security scanning |

### Commit Conventions

| Convention | Detection | Pattern |
|-----------|-----------|---------|
| Conventional Commits | `commitlint.config.js`, `@commitlint/*` | `type(scope): description` |
| Gitmoji | `gitmoji` in deps, emoji in commits | Emoji prefix commits |
| Angular format | Angular commit guidelines | `type(scope): description` |
| Commitizen | `cz` in package.json, `.cz.toml` | Interactive commit prompts |

---

## Environment & Config Detection

### Config Approaches (12)

| Approach | Config File | Detection Pattern |
|----------|------------|-------------------|
| dotenv | `.env`, `.env.local`, `.env.*` | `process.env.*`, `os.environ` |
| dotenvx | `.env` with encryption | `dotenvx` CLI, encrypted `.env` |
| YAML config | `config/*.yml`, `config/*.yaml` | YAML config loading libraries |
| JSON config | `config/*.json` | JSON config loading |
| Spring Config | `application.yml`, `application.properties` | Spring Boot config |
| .NET Config | `appsettings.json`, `appsettings.*.json` | .NET configuration |
| HashiCorp Vault | Vault client config | `VAULT_ADDR`, vault SDK |
| AWS SSM | Parameter Store references | `ssm:` prefix, AWS SDK |
| Azure Key Vault | Key Vault client | `@azure/keyvault-*` |
| GCP Secret Manager | Secret Manager client | `@google-cloud/secret-manager` |
| Doppler | Doppler CLI config | `doppler run`, `DOPPLER_TOKEN` |
| Infisical | Infisical SDK | `@infisical/sdk`, `.infisical.json` |

### Feature Flag Platforms (11)

| Platform | Package | Config Pattern |
|----------|---------|---------------|
| LaunchDarkly | `launchdarkly-*`, `@launchdarkly/*` | SDK key, feature flag evaluation |
| Flagsmith | `flagsmith` | Flagsmith client initialization |
| Unleash | `unleash-client`, `unleash-proxy-client` | Unleash URL, API token |
| GrowthBook | `@growthbook/growthbook` | GrowthBook SDK config |
| PostHog | `posthog-js`, `posthog-node` | Feature flag evaluation |
| Statsig | `statsig-js`, `statsig-node` | Statsig SDK initialization |
| Split.io | `@splitsoftware/splitio` | Split SDK config |
| DevCycle | `@devcycle/nodejs-server-sdk` | DevCycle client |
| Flipt | `@flipt-io/flipt` | Flipt client config |
| OpenFeature | `@openfeature/server-sdk` | Vendor-neutral standard |
| ConfigCat | `configcat-js`, `configcat-node` | ConfigCat SDK |

### Container & Orchestration

| Tool | Config File | Detection Pattern |
|------|------------|-------------------|
| Docker | `Dockerfile`, `.dockerignore` | `FROM`, `RUN`, `EXPOSE` |
| Docker Compose | `docker-compose.yml`, `compose.yml` | `services:`, container orchestration |
| Kubernetes | `k8s/*.yaml`, `manifests/` | `apiVersion:`, `kind:` |
| Helm | `Chart.yaml`, `values.yaml`, `templates/` | Helm charts |
| Kustomize | `kustomization.yaml` | `resources:`, overlays |
| Skaffold | `skaffold.yaml` | Dev/deploy pipeline |
| Tilt | `Tiltfile` | Local K8s development |
| DevContainer | `.devcontainer/devcontainer.json` | VS Code dev containers |

### Infrastructure-as-Code

| Tool | Config File | License/Notes |
|------|------------|---------------|
| Terraform | `*.tf`, `.terraform.lock.hcl` | BSL license (HashiCorp) |
| OpenTofu | `*.tf`, `.terraform.lock.hcl` | CNCF open source fork |
| Pulumi | `Pulumi.yaml`, `Pulumi.*.yaml` | Multi-language IaC |
| AWS CDK | `cdk.json`, `lib/*-stack.ts` | AWS-specific IaC |
| CDKTF | `cdktf.json` | Deprecated -- migrating to Terraform/OpenTofu |
| CloudFormation | `template.yaml` (CF) | AWS native |
| SAM | `template.yaml` (SAM) | Serverless on AWS |
| Ansible | `playbook.yml`, `ansible.cfg`, `roles/` | Configuration management |
| Crossplane | Crossplane compositions | Kubernetes-native IaC |

---

## Git Workflow Detection

### Branching Strategies

| Strategy | Detection Pattern | Notes |
|----------|-------------------|-------|
| Trunk-based | Short-lived feature branches, frequent main merges | Best practice -- 28% faster delivery |
| GitHub Flow | `main` + feature branches, PR-based | Simple and effective |
| GitFlow | `main` + `develop` + `feature/*` + `release/*` + `hotfix/*` | Legacy -- complex branching |
| GitLab Flow | Environment branches (`staging`, `production`) | GitLab-oriented |
| Release branches | `release/v*` branches | Versioned release workflow |

### Release Management

| Tool | Config File | Pattern |
|------|------------|---------|
| semantic-release | `.releaserc`, `release.config.js` | Automated semver from conventional commits |
| release-please | `release-please-config.json` | Google's release PR automation |
| Changesets | `.changeset/config.json` | Manual changeset files, monorepo support |
| standard-version | `.versionrc` | Deprecated -- replaced by release-please |
| GoReleaser | `.goreleaser.yml` | Go binary cross-compilation and release |
| python-semantic-release | `pyproject.toml` [tool.semantic_release] | Python semantic versioning |

### Changelog Tools

| Tool | Config File | Pattern |
|------|------------|---------|
| git-cliff | `cliff.toml` | Highly configurable, Rust-based |
| conventional-changelog | `conventional-changelog` config | Based on conventional commits |
| auto-changelog | `.auto-changelog` | Git log to CHANGELOG |
| Keep a Changelog | `CHANGELOG.md` format | Manual, standardized format |

### Code Review Practices

| Practice | Detection | Description |
|----------|-----------|-------------|
| CODEOWNERS | `.github/CODEOWNERS`, `CODEOWNERS` | Auto-assign reviewers by path |
| PR templates | `.github/pull_request_template.md` | Standardized PR descriptions |
| Required reviewers | Branch protection rules | Minimum approval count |
| Auto-merge | Mergify (`.mergify.yml`), GitHub auto-merge | Automated merge on approval |
| PR size limits | Danger (`Dangerfile`), custom CI checks | Flag large PRs |

---

## i18n Additions

### Missing i18n Libraries

| Library | Ecosystem | Package | Pattern |
|---------|-----------|---------|---------|
| svelte-i18n | Svelte | `svelte-i18n` | `$_()`, `$t()` |
| typesafe-i18n | JS/TS | `typesafe-i18n` | Type-safe translations |
| Lingui | React | `@lingui/react` | `<Trans>`, `t` macro |
| Paraglide | JS/TS | `@inlang/paraglide-js` | Compiled i18n |
| rosetta | JS/TS | `rosetta` | Lightweight i18n |
| rust-i18n | Rust | `rust-i18n` | `t!()` macro |
| go-i18n | Go | `github.com/nicksnyder/go-i18n` | Go i18n library |
| ICU MessageFormat | Standard | `@formatjs/intl-messageformat` | Unicode standard |

### Translation Management Systems (TMS)

| Platform | Integration | Features |
|----------|-------------|----------|
| Crowdin | CLI + CI | Over-the-air, in-context editing |
| Lokalise | API + CLI | Translation memory, glossary |
| Phrase | API + CLI | Enterprise TMS |
| Transifex | API + CLI | Open source friendly |
| Weblate | Self-hosted + SaaS | Git integration, glossary |
| POEditor | API | Simple, collaborative |
| Locize | API + SDK | i18next ecosystem |
| SimpleLocalize | CLI + CI | Developer-focused |

---

## Performance Additions

### Monitoring Tools

| Tool | Type | Detection Pattern |
|------|------|-------------------|
| Vercel Analytics | RUM | `@vercel/analytics` |
| web-vitals | Library | `web-vitals` package |
| Lighthouse CI | CI | `@lhci/cli`, `.lighthouserc.js` |
| SpeedCurve | SaaS | SpeedCurve script tag |
| Calibre | SaaS | Calibre CI integration |
| DebugBear | SaaS | DebugBear monitoring |
| Sentry Performance | APM | `Sentry.init` with tracing |
| Datadog RUM | RUM | `@datadog/browser-rum` |

### Core Web Vitals 2025

| Metric | Threshold (Good) | Measurement |
|--------|------------------|-------------|
| LCP (Largest Contentful Paint) | < 2.5s | Loading performance |
| INP (Interaction to Next Paint) | < 200ms | Responsiveness (replaced FID) |
| CLS (Cumulative Layout Shift) | < 0.1 | Visual stability |

---

## Industry Shifts (2025-2026)

| # | Shift | Impact | Detection Relevance |
|---|-------|--------|-------------------|
| 1 | Terraform BSL license -- OpenTofu rising | OpenTofu as CNCF alternative | Detect both, note license difference |
| 2 | Biome 2.0 catches 85% of typescript-eslint rules | Viable ESLint replacement | Detect Biome as primary linter |
| 3 | uv replacing Poetry/pip (100x faster) | Python package management shift | Detect `uv.lock`, `pyproject.toml` with uv |
| 4 | Ruff consolidated Python linting | Single tool replaces Flake8 + isort + Black | Detect Ruff as primary Python tool |
| 5 | oxlint gaining traction as CI speed layer | Fast linting in CI, ESLint for IDE | Detect `.oxlintrc.json` |
| 6 | Trunk-based development > GitFlow | 28% faster delivery (DORA metrics) | Detect branching strategy |
| 7 | OpenFeature as vendor-neutral feature flag standard | Portable feature flag evaluation | Detect `@openfeature/*` |
| 8 | INP replaced FID as Core Web Vitals metric | Responsiveness measurement change | Update performance analyzer |
| 9 | Python overtook JavaScript on GitHub (2025) | Python ecosystem growing | Expand Python analyzer coverage |
