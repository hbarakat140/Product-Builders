# Testing & CI/CD Analyzer Research

Deep research conducted 2026-03-26 covering test frameworks, E2E tools, CI/CD platforms, deployment patterns, and anti-patterns across all major ecosystems.

## Testing Detection Checklist

### Test Framework Detection

| Framework | Ecosystem | Config Files | Dependencies | Detection Pattern |
|-----------|-----------|-------------|-------------|-------------------|
| Jest | JS/TS | `jest.config.js/ts/mjs`, `jest` in package.json | `jest`, `@jest/core` | `describe`, `it`, `expect` |
| Vitest | JS/TS | `vitest.config.ts`, `vite.config.ts` (test) | `vitest` | `describe`, `it`, `expect`, `vi.mock` |
| Mocha | JS/TS | `.mocharc.yml`, `.mocharc.js` | `mocha` | `describe`, `it`, `chai` |
| Ava | JS/TS | `ava` in package.json | `ava` | `test()`, `t.is()` |
| Bun test | JS/TS | `bunfig.toml` | Bun built-in | `bun test`, `describe`, `expect` |
| pytest | Python | `pytest.ini`, `pyproject.toml` [tool.pytest] | `pytest` | `test_*.py`, `def test_` |
| unittest | Python | Built-in | Built-in | `unittest.TestCase`, `self.assert*` |
| JUnit 5 | Java | `build.gradle`, `pom.xml` | `junit-jupiter` | `@Test`, `@ExtendWith`, `Assertions.*` |
| TestNG | Java | `testng.xml` | `testng` | `@Test`, `@DataProvider` |
| Spock | Groovy/Java | `build.gradle` | `spock-core` | `extends Specification`, `def "should"` |
| RSpec | Ruby | `.rspec`, `spec/spec_helper.rb` | `rspec` | `describe`, `it`, `expect` |
| Minitest | Ruby | `test/test_helper.rb` | `minitest` | `class *Test < Minitest::Test` |
| xUnit | .NET | `*.csproj` | `xunit` | `[Fact]`, `[Theory]`, `Assert.*` |
| NUnit | .NET | `*.csproj` | `NUnit` | `[Test]`, `[TestFixture]` |
| MSTest | .NET | `*.csproj` | `MSTest.TestFramework` | `[TestMethod]`, `[TestClass]` |
| Go testing | Go | Built-in | Built-in | `_test.go`, `func Test*`, `t.Run` |
| cargo test | Rust | Built-in | Built-in | `#[test]`, `#[cfg(test)]` |
| PHPUnit | PHP | `phpunit.xml` | `phpunit/phpunit` | `extends TestCase`, `test*()` |
| Pest | PHP | `Pest.php` | `pestphp/pest` | `test()`, `it()`, `expect()` |

### E2E Frameworks (8)

| Framework | Package | Config File | Key Features |
|-----------|---------|------------|-------------|
| Playwright | `@playwright/test` | `playwright.config.ts` | Multi-browser, auto-wait, trace viewer |
| Cypress | `cypress` | `cypress.config.ts/js` | Time-travel debug, real browser |
| Selenium | `selenium-webdriver` | `selenium` config | Cross-browser, multi-language |
| Puppeteer | `puppeteer` | Launch options | Chrome DevTools Protocol |
| TestCafe | `testcafe` | `.testcaferc.json` | No WebDriver, auto-wait |
| Nightwatch | `nightwatch` | `nightwatch.conf.js` | Selenium-based, built-in assertions |
| WebdriverIO | `webdriverio` | `wdio.conf.ts/js` | Extensible, multi-protocol |
| Detox | `detox` | `.detoxrc.js` | React Native E2E |

### API Testing Tools (8)

| Tool | Package | Usage Pattern | Ecosystem |
|------|---------|--------------|-----------|
| Supertest | `supertest` | `request(app).get()` | Node.js |
| httpx | `httpx` | `AsyncClient`, `client.get()` | Python |
| REST Assured | `rest-assured` | `given().when().then()` | Java |
| Newman | `newman` | Postman collection runner | CLI |
| Hurl | `hurl` | `.hurl` files | CLI, language-agnostic |
| Pactum | `pactum` | `spec().get()` | Node.js |
| Karate | `karate` | `.feature` files | Java/JVM |
| Dredd | `dredd` | API Blueprint/OpenAPI testing | CLI |

### Visual Regression (7)

| Tool | Package | Integration | Type |
|------|---------|-------------|------|
| Chromatic | `chromatic` | Storybook | SaaS |
| Percy | `@percy/cli` | Multi-framework | SaaS |
| Applitools | `@applitools/eyes-*` | Multi-framework | SaaS (AI-powered) |
| BackstopJS | `backstopjs` | Standalone | Open source |
| Playwright screenshots | `@playwright/test` | Playwright | Built-in |
| Loki | `loki` | Storybook | Open source |
| reg-suit | `reg-suit` | Standalone | Open source |

### Contract Testing

| Tool | Package | Pattern | Use Case |
|------|---------|---------|----------|
| Pact | `@pact-foundation/pact` | Consumer-driven contracts | Microservices |
| Spring Cloud Contract | `spring-cloud-contract` | Provider contracts | Java/Spring |

### Coverage Tools

| Tool | Ecosystem | Config | Threshold Parsing |
|------|-----------|--------|-------------------|
| Istanbul/nyc | JS/TS | `.nycrc`, nyc in package.json | `branches`, `functions`, `lines`, `statements` |
| c8 | JS/TS | `c8` in package.json | V8 native coverage |
| Vitest built-in | JS/TS | `vitest.config.ts` coverage | `coverage.thresholds` |
| coverage.py | Python | `.coveragerc`, `pyproject.toml` | `fail_under` |
| JaCoCo | Java | `build.gradle`, `pom.xml` | `minimumCoverageRatio` |
| SimpleCov | Ruby | `.simplecov`, `spec_helper.rb` | `minimum_coverage` |
| coverlet | .NET | `coverlet.runsettings` | `threshold` |
| go cover | Go | Built-in | `-coverprofile`, `-coverpkg` |
| cargo-tarpaulin | Rust | `tarpaulin.toml` | `--fail-under` |

### Mocking Libraries (18+)

| Library | Ecosystem | Pattern |
|---------|-----------|---------|
| MSW (Mock Service Worker) | JS/TS | `http.get()`, `graphql.query()`, service worker interception |
| nock | Node.js | `nock('url').get()`, HTTP interception |
| Sinon | JS/TS | `sinon.stub()`, `sinon.spy()`, `sinon.mock()` |
| pytest-mock | Python | `mocker.patch()` |
| responses | Python | `@responses.activate`, HTTP mocking |
| requests-mock | Python | `requests_mock.Mocker` |
| vcrpy | Python | `@vcr.use_cassette`, HTTP recording |
| factory_boy | Python | `factory.Factory`, model factories |
| Faker | Multi-language | `faker.name()`, data generation |
| Mockito | Java | `@Mock`, `when().thenReturn()` |
| WireMock | Java | HTTP mock server |
| MockK | Kotlin | `mockk<T>()`, `every {}` |
| Moq | .NET | `Mock<T>()`, `Setup()` |
| NSubstitute | .NET | `Substitute.For<T>()` |
| gomock | Go | `ctrl.NewController()`, `EXPECT()` |
| testify/mock | Go | `mock.Mock`, `On().Return()` |
| mockall | Rust | `#[automock]`, `expect_*()` |
| VCR | Ruby | `VCR.use_cassette`, HTTP recording |

### Test Organization Patterns

| Pattern | Detection Method | Description |
|---------|-----------------|-------------|
| Test pyramid | Test count ratio (unit >> integration >> E2E) | Healthy test distribution |
| Collocated tests | `*.test.ts` alongside `*.ts` source files | Tests next to source |
| Separated tests | `test/`, `tests/`, `__tests__/` directories | Tests in separate tree |
| BDD | `.feature` files, Gherkin syntax | Behavior-Driven Development |
| Property-based | `fast-check`, `hypothesis`, `jqwik` | Generative testing |
| Mutation testing | `stryker`, `mutmut`, `pitest` | Test quality validation |
| Testing Library | `@testing-library/*` | User-centric DOM testing |
| Testcontainers | `testcontainers`, `@testcontainers/*` | Container-based integration tests |

### Test Quality Signals

| Signal | Detection Method | Interpretation |
|--------|-----------------|---------------|
| Test count | Count test files and test functions | Basic coverage indicator |
| Test-to-source ratio | Test files / source files | Target: 0.5-1.0+ |
| Coverage badges | Badge URLs in README | Public coverage commitment |
| CI integration | Test commands in CI config | Automated test execution |
| Parallelization | `--parallel`, `--workers`, `-j` flags | Test speed optimization |
| Watch mode | `--watch` scripts | Developer experience |
| Pre-commit hooks | `husky`, `lint-staged`, `pre-commit` | Quality gates |
| Snapshot count | `.snap` files, `toMatchSnapshot` | Snapshot test usage |

---

## CI/CD Detection Checklist

### Platforms (16)

| Platform | Config File(s) | Detection Pattern |
|----------|---------------|-------------------|
| GitHub Actions | `.github/workflows/*.yml` | `on:`, `jobs:`, `runs-on:` |
| GitLab CI | `.gitlab-ci.yml` | `stages:`, `script:`, `image:` |
| Azure Pipelines | `azure-pipelines.yml` | `trigger:`, `pool:`, `steps:` |
| Jenkins | `Jenkinsfile` | `pipeline {}`, `stage()`, `steps {}` |
| CircleCI | `.circleci/config.yml` | `version:`, `jobs:`, `workflows:` |
| Travis CI | `.travis.yml` | `language:`, `script:` |
| Bitbucket Pipelines | `bitbucket-pipelines.yml` | `pipelines:`, `step:` |
| Google Cloud Build | `cloudbuild.yaml` | `steps:`, `images:` |
| AWS CodeBuild | `buildspec.yml` | `phases:`, `artifacts:` |
| Drone CI | `.drone.yml` | `kind: pipeline`, `steps:` |
| Woodpecker CI | `.woodpecker.yml` | `pipeline:`, `steps:` |
| Buildkite | `.buildkite/pipeline.yml` | `steps:`, `agents:` |
| TeamCity | `.teamcity/settings.kts` | Kotlin DSL config |
| Tekton | `tekton/` directory | `apiVersion: tekton.dev` |
| Dagger | `dagger.json`, `*.cue` | Dagger SDK usage |
| AppVeyor | `appveyor.yml` | `build:`, `test:`, `deploy:` |

### Deployment Targets (18+)

| Target | Config File(s) | Detection Pattern |
|--------|---------------|-------------------|
| Docker | `Dockerfile`, `.dockerignore` | `FROM`, `RUN`, `COPY` |
| Docker Compose | `docker-compose.yml`, `compose.yml` | `services:`, `volumes:` |
| Kubernetes | `k8s/`, `*.yaml` (k8s manifests) | `apiVersion:`, `kind: Deployment` |
| Helm | `Chart.yaml`, `values.yaml` | `helm install`, templates dir |
| Vercel | `vercel.json` | `vercel` in scripts, Vercel CLI |
| Netlify | `netlify.toml` | `[build]`, `netlify` in scripts |
| Fly.io | `fly.toml` | `[http_service]`, `flyctl` |
| Render | `render.yaml` | `services:`, Render config |
| Railway | `railway.toml`, `railway.json` | Railway CLI |
| Heroku | `Procfile`, `app.json` | `web:`, `heroku` in scripts |
| Google App Engine | `app.yaml` | `runtime:`, `handlers:` |
| AWS SAM | `template.yaml` (SAM) | `Transform: AWS::Serverless` |
| AWS CDK | `cdk.json` | CDK constructs, `lib/*-stack.ts` |
| Serverless Framework | `serverless.yml` | `provider:`, `functions:` |
| SST | `sst.config.ts` | SST constructs |
| Terraform | `*.tf` | `resource`, `provider`, HCL |
| Pulumi | `Pulumi.yaml` | Pulumi SDK imports |
| Ansible | `playbook.yml`, `ansible.cfg` | `hosts:`, `tasks:` |
| Kamal | `config/deploy.yml` | `service:`, `image:`, Kamal config |

### Deployment Patterns

| Pattern | Detection Method | Description |
|---------|-----------------|-------------|
| Blue-green | Two identical environments, traffic switching | Zero-downtime releases |
| Canary | Percentage-based traffic routing | Gradual rollout |
| Rolling | Sequential instance updates | Kubernetes default |
| Feature flags | LaunchDarkly, Flagsmith, GrowthBook config | Feature-based releases |
| Preview deployments | Vercel/Netlify PR previews | Per-PR environments |
| GitOps | ArgoCD, Flux config | Git-driven deployments |

### Build Optimization

| Optimization | Detection Method | Impact |
|-------------|-----------------|--------|
| Caching | `cache:` in CI config, `actions/cache` | Faster builds |
| Parallel jobs | `strategy.matrix`, parallel stages | Reduced wall time |
| Matrix builds | `matrix:` in CI config | Multi-version testing |
| Artifact reuse | `upload-artifact`/`download-artifact` | Build once, deploy many |
| Docker layer cache | `--cache-from`, `buildx` cache | Faster image builds |
| Monorepo path filtering | `paths:` in CI triggers | Skip unchanged packages |
| Concurrency control | `concurrency:` in GitHub Actions | Cancel outdated runs |
| Reusable workflows | `uses: ./.github/workflows/*.yml` | DRY CI config |

### Release Management

| Tool | Config File | Pattern |
|------|------------|---------|
| semantic-release | `.releaserc`, `release.config.js` | Automated semver from commits |
| Changesets | `.changeset/config.json` | Manual changeset files |
| release-please | `release-please-config.json` | Google's release automation |
| standard-version | `.versionrc` | Deprecated -- flag as legacy |
| release-it | `.release-it.json` | Interactive releases |
| GoReleaser | `.goreleaser.yml` | Go binary releases |

### Anti-Patterns

#### Testing Anti-Patterns

| Anti-Pattern | Detection Method | Severity |
|-------------|-----------------|----------|
| No tests | Zero test files | Critical |
| No CI test step | Missing test command in CI config | Critical |
| Inverted pyramid | More E2E than unit tests | High |
| No coverage tracking | Missing coverage config/reporting | High |
| Snapshot overuse | > 50% of assertions are snapshots | Medium |
| Flaky test indicators | `retry`, `flaky` annotations, skip patterns | High |
| No integration tests | Only unit tests, no API/DB tests | Medium |
| Test pollution | Shared mutable state between tests | High |
| Missing assertions | Test functions without assert/expect | Medium |

#### CI/CD Anti-Patterns

| Anti-Pattern | Detection Method | Severity |
|-------------|-----------------|----------|
| No CI | Missing CI config files | Critical |
| Hardcoded secrets | Secrets in CI config (not env vars) | Critical |
| No security scanning | Missing SAST/DAST/dependency scanning | High |
| No caching | Missing cache configuration in CI | Medium |
| No dependency automation | Missing Dependabot/Renovate | Medium |
| Long pipelines | > 20 minute builds without optimization | Medium |
| No artifact versioning | Missing version tagging | Medium |
| Manual deployments | No deployment automation | High |
| No rollback strategy | Missing rollback steps/procedures | High |
