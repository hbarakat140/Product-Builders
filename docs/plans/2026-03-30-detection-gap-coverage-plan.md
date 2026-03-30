# Detection Gap Coverage Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Improve analyzer field population from ~21% to ~50%+ and zone detection from 3/10 to 7/10 by fixing the top 10 highest-impact detection gaps.

**Architecture:** Each fix is isolated to one analyzer or scopes.py. TDD: write failing test, implement minimal fix, verify. Fixes 9 (tech stack frameworks) and 12 (i18n) are already implemented in codebase — skipped.

**Tech Stack:** Python 3.13, pytest, Pydantic v2

---

### Task 1: Fix Auth rate_limiting Bug

**Files:**
- Modify: `src/product_builders/analyzers/auth.py`
- Test: `tests/test_analyzers/test_auth.py`

**Step 1: Write the failing test**

Add to `tests/test_analyzers/test_auth.py`:

```python
def test_detects_rate_limiting_express(tmp_path: Path) -> None:
    pkg = {"dependencies": {"express-rate-limit": "^7.0.0"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    analyzer = AuthAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.rate_limiting == "express-rate-limit"


def test_rate_limiting_anti_pattern_only_when_null(tmp_path: Path) -> None:
    pkg = {"dependencies": {"express-rate-limit": "^7.0.0"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    analyzer = AuthAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert not any("rate limiting" in ap.lower() for ap in result.anti_patterns)
```

**Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_analyzers/test_auth.py::test_detects_rate_limiting_express tests/test_analyzers/test_auth.py::test_rate_limiting_anti_pattern_only_when_null -v`
Expected: FAIL — `rate_limiting` is never set

**Step 3: Implement rate limiting detection**

In `auth.py`, add after `mfa_methods = self._detect_mfa_methods(dep_names)`:

```python
        rate_limiting = self._detect_rate_limiting(dep_names)
```

Assign in result constructor:
```python
        result = AuthResult(
            ...
            rate_limiting=rate_limiting,
        )
```

Add the method to `AuthAnalyzer`:

```python
    def _detect_rate_limiting(self, dep_names: set[str]) -> str | None:
        rate_limit_libs: dict[str, str] = {
            "express-rate-limit": "express-rate-limit",
            "rate-limiter-flexible": "rate-limiter-flexible",
            "@nestjs/throttler": "nestjs-throttler",
            "flask-limiter": "flask-limiter",
            "django-ratelimit": "django-ratelimit",
            "bucket4j": "bucket4j",
            "slowapi": "slowapi",
            "@upstash/ratelimit": "upstash-ratelimit",
        }
        for dep, name in rate_limit_libs.items():
            if dep in dep_names:
                return name
        return None
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_analyzers/test_auth.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add src/product_builders/analyzers/auth.py tests/test_analyzers/test_auth.py
git commit -m "fix: detect rate limiting libraries, eliminate false anti-pattern"
```

---

### Task 2: Zone Detection — App Router + Deduplication

**Files:**
- Modify: `src/product_builders/generators/scopes.py`
- Test: `tests/test_generators/test_scopes.py`

**Step 1: Write the failing tests**

Add to `tests/test_generators/test_scopes.py`:

```python
def test_detects_app_router_api(tmp_path: Path) -> None:
    (tmp_path / "src" / "app" / "api" / "users").mkdir(parents=True)
    zones = auto_detect_zones(tmp_path)
    zone_names = [z.name for z in zones]
    assert "api" in zone_names


def test_zone_deduplicates_paths(tmp_path: Path) -> None:
    # Create structure that could match multiple patterns for same zone
    (tmp_path / "src" / "models").mkdir(parents=True)
    (tmp_path / "models").mkdir(parents=True)
    zones = auto_detect_zones(tmp_path)
    db_zones = [z for z in zones if z.name == "database"]
    if db_zones:
        assert len(db_zones[0].paths) == len(set(db_zones[0].paths))
```

**Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_generators/test_scopes.py::test_detects_app_router_api -v`
Expected: FAIL — `api` zone not detected

**Step 3: Implement fixes**

In `scopes.py`, add to the `api` zone patterns list:

```python
    ("api", [
        "src/api", "src/routes", "src/controllers", "src/endpoints",
        "app/api", "app/routes", "app/controllers",
        "routes", "controllers", "api",
        "src/app/api",  # Next.js App Router
    ]),
```

In `auto_detect_zones()`, add deduplication before creating Zone (around line 122):

```python
        if found_paths and zone_name not in seen_zone_names:
            seen_zone_names.add(zone_name)
            deduped = list(dict.fromkeys(found_paths))
            zones.append(Zone(name=zone_name, paths=deduped))
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_generators/test_scopes.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add src/product_builders/generators/scopes.py tests/test_generators/test_scopes.py
git commit -m "fix: add App Router API zone pattern, deduplicate zone paths"
```

---

### Task 3: Zone Detection — Python Packages + Monorepo

**Files:**
- Modify: `src/product_builders/generators/scopes.py`
- Test: `tests/test_generators/test_scopes.py`

**Step 1: Write the failing tests**

Add to `tests/test_generators/test_scopes.py`:

```python
def test_detects_python_package_as_backend_logic(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "myapp"\n')
    pkg = tmp_path / "src" / "myapp"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("")
    zones = auto_detect_zones(tmp_path)
    zone_names = [z.name for z in zones]
    assert "backend_logic" in zone_names


def test_detects_monorepo_nested_zones(tmp_path: Path) -> None:
    (tmp_path / "turbo.json").write_text('{"pipeline": {}}')
    web = tmp_path / "apps" / "web" / "src" / "components"
    web.mkdir(parents=True)
    api = tmp_path / "apps" / "api" / "src" / "routes"
    api.mkdir(parents=True)
    zones = auto_detect_zones(tmp_path)
    zone_names = [z.name for z in zones]
    assert "frontend_ui" in zone_names
    assert "api" in zone_names
```

**Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_generators/test_scopes.py::test_detects_python_package_as_backend_logic tests/test_generators/test_scopes.py::test_detects_monorepo_nested_zones -v`
Expected: FAIL

**Step 3: Implement Python package detection**

Add at the end of `auto_detect_zones()`, before `return zones`:

```python
    # Python package detection: src/*/  with __init__.py -> backend_logic
    if "backend_logic" not in seen_zone_names:
        if (repo_path / "pyproject.toml").exists() or (repo_path / "setup.py").exists():
            src = repo_path / "src"
            if src.is_dir():
                for child in src.iterdir():
                    if child.is_dir() and (child / "__init__.py").exists():
                        rel = child.relative_to(repo_path)
                        seen_zone_names.add("backend_logic")
                        zones.append(Zone(name="backend_logic", paths=[f"{rel}/**"]))
                        break

    # Monorepo nested zone detection
    monorepo_markers = ["turbo.json", "nx.json", "lerna.json", "pnpm-workspace.yaml"]
    if any((repo_path / m).exists() for m in monorepo_markers):
        for sub_root_name in ("apps", "packages", "services"):
            sub_root = repo_path / sub_root_name
            if not sub_root.is_dir():
                continue
            for project_dir in sub_root.iterdir():
                if not project_dir.is_dir():
                    continue
                sub_zones = auto_detect_zones(project_dir)
                for sz in sub_zones:
                    prefix = project_dir.relative_to(repo_path)
                    prefixed_paths = [f"{prefix}/{p}" for p in sz.paths]
                    if sz.name not in seen_zone_names:
                        seen_zone_names.add(sz.name)
                        zones.append(Zone(name=sz.name, paths=prefixed_paths))
                    else:
                        for z in zones:
                            if z.name == sz.name:
                                z.paths.extend(prefixed_paths)
                                break
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_generators/test_scopes.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add src/product_builders/generators/scopes.py tests/test_generators/test_scopes.py
git commit -m "feat: detect Python package zones and monorepo nested zones"
```

---

### Task 4: Database — Supabase Migration Detection

**Files:**
- Modify: `src/product_builders/analyzers/database.py`
- Test: `tests/test_analyzers/test_database.py`

**Step 1: Write the failing test**

Add to `tests/test_analyzers/test_database.py`:

```python
def test_detects_supabase_migrations(tmp_path: Path) -> None:
    """Supabase project with supabase/migrations/ should detect migration tool and directory."""
    pkg = {"dependencies": {"@supabase/supabase-js": "^2.0.0"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    mig = tmp_path / "supabase" / "migrations"
    mig.mkdir(parents=True)
    (mig / "20240101000000_init.sql").write_text("CREATE TABLE users (id uuid);")
    (tmp_path / "supabase" / "config.toml").write_text('[db]\nport = 54322\n')
    analyzer = DatabaseAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.migration_tool == "supabase-cli"
    assert result.migration_directory is not None
    assert "supabase" in result.migration_directory
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_analyzers/test_database.py::test_detects_supabase_migrations -v`
Expected: FAIL

**Step 3: Implement Supabase migration detection**

Add a new entry to `ORM_INDICATORS` dict in `database.py`:

```python
    "supabase": {
        "orm": "supabase-js",
        "deps": ["@supabase/supabase-js"],
        "migration_tool": "supabase-cli",
        "migration_dir": "supabase/migrations",
    },
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_analyzers/test_database.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add src/product_builders/analyzers/database.py tests/test_analyzers/test_database.py
git commit -m "feat: detect Supabase CLI migrations in supabase/migrations/"
```

---

### Task 5: Auth — Framework-Specific Protected Routes

**Files:**
- Modify: `src/product_builders/analyzers/auth.py`
- Test: `tests/test_analyzers/test_auth.py`

**Step 1: Write the failing tests**

Add to `tests/test_analyzers/test_auth.py`:

```python
def test_detects_nextjs_middleware_auth(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(json.dumps({"dependencies": {"next": "^15"}}))
    (tmp_path / "middleware.ts").write_text(
        "import { NextResponse } from 'next/server';\n"
        "export function middleware(request) { return NextResponse.next(); }\n"
    )
    analyzer = AuthAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert any("middleware" in p.lower() for p in result.protected_route_patterns)


def test_detects_sveltekit_hooks_auth(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "hooks.server.ts").write_text(
        "export const handle = async ({ event, resolve }) => { return resolve(event); };\n"
    )
    analyzer = AuthAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert any("hooks.server" in p for p in result.protected_route_patterns)
```

**Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_analyzers/test_auth.py::test_detects_nextjs_middleware_auth tests/test_analyzers/test_auth.py::test_detects_sveltekit_hooks_auth -v`
Expected: FAIL

**Step 3: Implement framework-specific auth detection**

In `auth.py`, add a new method and call it in `analyze()` after `auth_dirs`:

```python
    def _detect_framework_auth_patterns(self, repo_path: Path) -> list[str]:
        """Detect framework-specific auth middleware patterns."""
        patterns: list[str] = []
        # Next.js middleware
        for name in ("middleware.ts", "middleware.js"):
            if (repo_path / name).exists():
                patterns.append(f"next.js middleware ({name})")
                break
        # SvelteKit hooks
        for name in ("src/hooks.server.ts", "src/hooks.server.js"):
            if (repo_path / name).exists():
                patterns.append(f"sveltekit hooks ({name})")
                break
        # Remix root loader
        for name in ("app/root.tsx", "app/root.jsx"):
            if (repo_path / name).exists():
                content = self.read_file(repo_path / name)
                if content and ("loader" in content or "getSession" in content):
                    patterns.append(f"remix root loader ({name})")
                    break
        return patterns
```

Call it in `analyze()` and extend `protected_route_patterns`:

```python
        framework_patterns = self._detect_framework_auth_patterns(repo_path)
        # Extend after result creation:
        result.protected_route_patterns.extend(framework_patterns)
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_analyzers/test_auth.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add src/product_builders/analyzers/auth.py tests/test_analyzers/test_auth.py
git commit -m "feat: detect Next.js middleware, SvelteKit hooks, Remix loader auth patterns"
```

---

### Task 6: Dependencies — Monorepo Workspace Manifests

**Files:**
- Modify: `src/product_builders/analyzers/dependencies.py`
- Test: `tests/test_analyzers/test_dependencies.py`

**Step 1: Write the failing test**

Add to `tests/test_analyzers/test_dependencies.py`:

```python
def test_detects_monorepo_workspace_deps(tmp_path: Path) -> None:
    (tmp_path / "turbo.json").write_text('{}')
    root_pkg = {"dependencies": {"typescript": "^5"}}
    (tmp_path / "package.json").write_text(json.dumps(root_pkg))
    web = tmp_path / "apps" / "web"
    web.mkdir(parents=True)
    web_pkg = {"dependencies": {"next": "^15", "react": "^19"}}
    (web / "package.json").write_text(json.dumps(web_pkg))
    analyzer = DependencyAnalyzer()
    result = analyzer.analyze(tmp_path)
    dep_names = [d.name for d in result.dependencies]
    assert "next" in dep_names
    assert "react" in dep_names
    assert "typescript" in dep_names
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_analyzers/test_dependencies.py::test_detects_monorepo_workspace_deps -v`
Expected: FAIL — workspace deps not merged

**Step 3: Implement monorepo workspace scanning**

In `dependencies.py`, in the `analyze()` method, after collecting root deps, add monorepo detection. Read the file first to find the exact insertion point, then add:

```python
        # Monorepo workspace manifest collection
        monorepo_markers = ["turbo.json", "nx.json", "lerna.json", "pnpm-workspace.yaml"]
        if any((repo_path / m).exists() for m in monorepo_markers):
            for sub_root in ("apps", "packages", "services", "libs"):
                sr = repo_path / sub_root
                if not sr.is_dir():
                    continue
                for project_dir in sr.iterdir():
                    if not project_dir.is_dir():
                        continue
                    sub_pkg = project_dir / "package.json"
                    if sub_pkg.exists():
                        manifest_files.append(str(sub_pkg.relative_to(repo_path)))
                        data = self.read_json(sub_pkg)
                        if data:
                            for section in ("dependencies", "devDependencies"):
                                for name, version in data.get(section, {}).items():
                                    if name not in seen:
                                        seen.add(name)
                                        deps.append(DependencyInfo(
                                            name=name,
                                            version=self._normalize_version(version) if version else None,
                                            is_dev=(section == "devDependencies"),
                                            category=CATEGORY_MAP.get(name),
                                        ))
```

Note: You'll need to read the full `analyze()` method first to find exact variable names used (may be `deps`, `manifest_files`, `seen`).

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_analyzers/test_dependencies.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add src/product_builders/analyzers/dependencies.py tests/test_analyzers/test_dependencies.py
git commit -m "feat: collect dependencies from monorepo workspace manifests"
```

---

### Task 7: Git Workflow — Husky Hook Detection

**Files:**
- Modify: `src/product_builders/analyzers/git_workflow.py`
- Test: `tests/test_analyzers/test_git_workflow.py`

**Step 1: Write the failing test**

Add to `tests/test_analyzers/test_git_workflow.py`:

```python
def test_detects_husky_commit_hooks(tmp_path: Path) -> None:
    husky = tmp_path / ".husky"
    husky.mkdir()
    (husky / "commit-msg").write_text("npx --no -- commitlint --edit $1\n")
    analyzer = GitWorkflowAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.commit_message_format == "conventional"
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_analyzers/test_git_workflow.py::test_detects_husky_commit_hooks -v`
Expected: FAIL

**Step 3: Implement Husky detection**

In `git_workflow.py`, in `_detect_commit_format()`, add before the final `return None`:

```python
        # Check .husky/commit-msg for commitlint
        husky_commit_msg = repo_path / ".husky" / "commit-msg"
        if husky_commit_msg.exists():
            content = self.read_file(husky_commit_msg)
            if content and "commitlint" in content:
                return "conventional"
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_analyzers/test_git_workflow.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add src/product_builders/analyzers/git_workflow.py tests/test_analyzers/test_git_workflow.py
git commit -m "feat: detect commit message conventions from Husky hooks"
```

---

### Task 8: Security — CSP + Supply Chain Detection

**Files:**
- Modify: `src/product_builders/analyzers/security.py`
- Test: `tests/test_analyzers/test_security.py`

**Step 1: Write the failing tests**

Add to `tests/test_analyzers/test_security.py`:

```python
def test_detects_csp_in_nextjs_middleware(tmp_path: Path) -> None:
    (tmp_path / "middleware.ts").write_text(
        "const cspHeader = 'Content-Security-Policy';\n"
        "response.headers.set(cspHeader, policy);\n"
    )
    analyzer = SecurityAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.csp_headers is True


def test_detects_npm_audit_in_scripts(tmp_path: Path) -> None:
    pkg = {"scripts": {"audit": "npm audit"}, "dependencies": {}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    analyzer = SecurityAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.vulnerability_scanning is not None
```

**Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_analyzers/test_security.py::test_detects_csp_in_nextjs_middleware tests/test_analyzers/test_security.py::test_detects_npm_audit_in_scripts -v`
Expected: FAIL

**Step 3: Implement CSP and supply chain detection**

In `security.py`, expand `_detect_csp()` to also scan middleware files:

```python
        # Check middleware files for CSP header
        for mw in ("middleware.ts", "middleware.js"):
            content = self.read_file(repo_path / mw)
            if content and "Content-Security-Policy" in content:
                return True
        # Check Django settings
        for settings in ("settings.py", "src/settings.py", "config/settings.py"):
            content = self.read_file(repo_path / settings)
            if content and ("CSP_" in content or "django-csp" in content):
                return True
```

In `_detect_vuln_scanner()`, add before `return None`:

```python
        # Check package.json scripts for audit commands
        pkg = self.read_json(repo_path / "package.json")
        if pkg:
            scripts = pkg.get("scripts", {})
            for script_val in scripts.values():
                if isinstance(script_val, str):
                    if "npm audit" in script_val or "yarn audit" in script_val:
                        return "npm-audit"
        # Check for pip-audit / safety
        for tool, name in [("pip-audit", "pip-audit"), ("safety", "safety"), ("cargo-audit", "cargo-audit")]:
            deps = self.collect_dependency_names(repo_path)
            if tool in deps:
                return name
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_analyzers/test_security.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add src/product_builders/analyzers/security.py tests/test_analyzers/test_security.py
git commit -m "feat: detect CSP in middleware files and npm/pip/cargo audit tools"
```

---

### Task 9: Performance — Image Optimization + Bundle Analysis

**Files:**
- Modify: `src/product_builders/analyzers/performance.py`
- Test: `tests/test_analyzers/test_performance.py`

**Step 1: Write the failing tests**

Add to `tests/test_analyzers/test_performance.py`:

```python
def test_detects_next_image_import(tmp_path: Path) -> None:
    pkg = {"dependencies": {"next": "^15"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    src = tmp_path / "src"
    src.mkdir()
    (src / "page.tsx").write_text("import Image from 'next/image';\n")
    analyzer = PerformanceAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.image_optimization is not None


def test_detects_bundle_analyzer(tmp_path: Path) -> None:
    pkg = {"devDependencies": {"@next/bundle-analyzer": "^15"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    analyzer = PerformanceAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.bundle_size_config is not None
```

**Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_analyzers/test_performance.py::test_detects_next_image_import tests/test_analyzers/test_performance.py::test_detects_bundle_analyzer -v`
Expected: FAIL (image already detects `next` dep but test checks import; bundle analyzer not detected)

**Step 3: Implement bundle analysis detection**

In `_detect_bundle_config()`, add detection for analysis tools. Read the method first to find exact insertion point, then add:

```python
        # Bundle analysis tools
        bundle_analysis_deps = {
            "webpack-bundle-analyzer": "webpack-bundle-analyzer",
            "@next/bundle-analyzer": "next-bundle-analyzer",
            "vite-plugin-visualizer": "vite-plugin-visualizer",
            "rollup-plugin-visualizer": "rollup-plugin-visualizer",
            "source-map-explorer": "source-map-explorer",
        }
        for dep, name in bundle_analysis_deps.items():
            if dep in deps:
                return name
```

In `_detect_image_optimization()`, add `@astrojs/image` and `unpic`:

```python
        if "@astrojs/image" in deps:
            return "astro-image"
        if "unpic" in deps or "@unpic/react" in deps:
            return "unpic"
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_analyzers/test_performance.py -v`
Expected: ALL PASS

**Step 5: Commit**

```bash
git add src/product_builders/analyzers/performance.py tests/test_analyzers/test_performance.py
git commit -m "feat: detect bundle analysis tools and expanded image optimization libraries"
```

---

### Task 10: Run Full Verification

**Step 1: Run complete test suite**

Run: `python -m pytest tests/ -v --tb=short`
Expected: ALL PASS (should be ~260+ tests)

**Step 2: Run analyzers against this repo to measure improvement**

```python
python -c "
from pathlib import Path
from product_builders.analyzers.registry import get_all_analyzers
repo = Path('.')
total_p, total_t = 0, 0
for a in get_all_analyzers():
    r = a.safe_analyze(repo)
    fields = {k: v for k, v in r.__dict__.items() if not k.startswith('_') and k not in ('status','error_message','raw_data','anti_patterns')}
    p = sum(1 for v in fields.values() if v is not None and v != [] and v != '' and v is not False and v != 0)
    total_p += p; total_t += len(fields)
print(f'Field population: {total_p}/{total_t} ({100*total_p//total_t}%)')
"
```

Expected: Improvement from 21% to ~30%+ on self-analysis (Python CLI has legitimately empty frontend dimensions)

**Step 3: Run zone detection to measure improvement**

```python
python -c "
from pathlib import Path
from product_builders.generators.scopes import auto_detect_zones
zones = auto_detect_zones(Path('.'))
print(f'Zones detected: {len(zones)}')
for z in zones:
    print(f'  {z.name}: {z.paths}')
"
```

Expected: Should now detect `backend_logic` zone for this Python project

**Step 4: Final commit if any cleanup needed**

```bash
git add -A && git commit -m "chore: detection gap coverage complete"
```
