# Analysis Intelligence Improvements — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix the 4 highest-ROI issues identified in the deep analysis scoring (zone detection, BaaS mappings, blocked command filtering, template numbering) to lift the pipeline score from 6.3/10 to ~7.2/10.

**Architecture:** All changes are to existing modules — no new packages. Fix heuristic detection gaps, make blocked commands dynamic, and correct template output. Each task is independent and can be committed separately.

**Tech Stack:** Python 3.11+, Pydantic v2, Jinja2, Click, pytest

---

## Task 1: Fix Zone Detection Path-Matching

The `auto_detect_zones()` function only checks `repo_path / pattern` directly. It misses patterns under `src/` (e.g., `src/app/api` is missed because detector checks for `app/api` at repo root).

**Files:**
- Modify: `src/product_builders/generators/scopes.py:80-93`
- Test: `tests/test_generators/test_scopes.py` (create)

**Step 1: Write the failing test**

```python
# tests/test_generators/test_scopes.py
"""Tests for zone auto-detection and scope generation."""
from pathlib import Path
from product_builders.generators.scopes import auto_detect_zones


def test_detects_api_zone_under_src(tmp_path: Path) -> None:
    """src/app/api/ should be detected as 'api' zone."""
    (tmp_path / "src" / "app" / "api").mkdir(parents=True)
    zones = auto_detect_zones(tmp_path)
    zone_names = [z.name for z in zones]
    assert "api" in zone_names


def test_detects_tests_zone_nested(tmp_path: Path) -> None:
    """Nested __tests__/ dirs should be detected as 'tests' zone."""
    (tmp_path / "src" / "lib" / "__tests__").mkdir(parents=True)
    zones = auto_detect_zones(tmp_path)
    zone_names = [z.name for z in zones]
    assert "tests" in zone_names


def test_detects_database_zone_nested(tmp_path: Path) -> None:
    """supabase/migrations/ should be detected as 'database' zone."""
    (tmp_path / "supabase" / "migrations").mkdir(parents=True)
    zones = auto_detect_zones(tmp_path)
    zone_names = [z.name for z in zones]
    assert "database" in zone_names


def test_detects_direct_pattern(tmp_path: Path) -> None:
    """Direct pattern like tests/ at root should still work."""
    (tmp_path / "tests").mkdir()
    zones = auto_detect_zones(tmp_path)
    zone_names = [z.name for z in zones]
    assert "tests" in zone_names


def test_no_duplicate_zones(tmp_path: Path) -> None:
    """Multiple matching patterns for same zone should not duplicate."""
    (tmp_path / "tests").mkdir()
    (tmp_path / "src" / "__tests__").mkdir(parents=True)
    zones = auto_detect_zones(tmp_path)
    zone_names = [z.name for z in zones]
    assert zone_names.count("tests") == 1
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_generators/test_scopes.py -v`
Expected: FAIL on `test_detects_api_zone_under_src`, `test_detects_tests_zone_nested`, `test_detects_database_zone_nested`

**Step 3: Implement the fix**

In `src/product_builders/generators/scopes.py`, replace the `auto_detect_zones()` function (lines 80-93):

```python
def auto_detect_zones(repo_path: Path) -> list[Zone]:
    """Detect zones by scanning repo for known directory patterns.

    Checks both direct patterns (e.g., ``tests/``) and ``src/``-prefixed
    variants (e.g., ``src/app/api/``).  Also uses ``rglob`` to find nested
    matches like ``src/lib/__tests__/``.
    """
    zones: list[Zone] = []
    seen_zone_names: set[str] = set()

    for zone_name, patterns in ZONE_DETECTORS.items():
        found_paths: list[str] = []
        for pattern in patterns:
            # Direct check: repo_root / pattern
            candidate = repo_path / pattern
            if candidate.is_dir():
                found_paths.append(f"{pattern}/**")
                continue
            # Prefixed check: repo_root / src / pattern
            src_candidate = repo_path / "src" / pattern
            if src_candidate.is_dir():
                found_paths.append(f"src/{pattern}/**")
                continue
            # Glob fallback: find nested occurrences (e.g., */__tests__)
            leaf = Path(pattern).name
            for match in repo_path.glob(f"**/{leaf}"):
                if match.is_dir() and ".git" not in match.parts:
                    rel = match.relative_to(repo_path)
                    found_paths.append(f"{rel}/**")
                    break  # one match per pattern is enough

        if found_paths and zone_name not in seen_zone_names:
            seen_zone_names.add(zone_name)
            zones.append(Zone(name=zone_name, paths=found_paths))

    return zones
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_generators/test_scopes.py -v`
Expected: All 5 tests PASS

**Step 5: Commit**

```bash
git add tests/test_generators/test_scopes.py src/product_builders/generators/scopes.py
git commit -m "fix: zone detection now finds patterns under src/ and nested dirs"
```

---

## Task 2: Add BaaS/Meta-Framework Mappings

Add Supabase → postgresql, shadcn → component library, and Next.js App Router → REST API detection.

**Files:**
- Modify: `src/product_builders/analyzers/database.py:105-112` (DB_TYPE_INDICATORS)
- Modify: `src/product_builders/analyzers/design.py:15-31` (_COMPONENT_LIBS)
- Modify: `src/product_builders/analyzers/api.py` (_detect_api_style)
- Test: `tests/test_analyzers/test_database.py` (create)
- Test: `tests/test_analyzers/test_design.py` (create)
- Test: `tests/test_analyzers/test_api.py` (create)

### Step 1: Write failing tests

```python
# tests/test_analyzers/test_database.py
"""Tests for database analyzer BaaS detection."""
import json
from pathlib import Path
from product_builders.analyzers.database import DatabaseAnalyzer


def test_detects_supabase_as_postgresql(tmp_path: Path) -> None:
    """Supabase JS client should map to postgresql database type."""
    pkg = {"dependencies": {"@supabase/supabase-js": "^2.99.1"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    analyzer = DatabaseAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.database_type == "postgresql"


def test_detects_firebase_as_nosql(tmp_path: Path) -> None:
    """Firebase should map to firebase/nosql."""
    pkg = {"dependencies": {"firebase": "^10.0.0"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    analyzer = DatabaseAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.database_type == "firebase"


def test_detects_planetscale_as_mysql(tmp_path: Path) -> None:
    """PlanetScale client should map to mysql."""
    pkg = {"dependencies": {"@planetscale/database": "^1.0.0"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    analyzer = DatabaseAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.database_type == "mysql"
```

```python
# tests/test_analyzers/test_design.py
"""Tests for design analyzer component library detection."""
import json
from pathlib import Path
from product_builders.analyzers.design import DesignUIAnalyzer


def test_detects_shadcn(tmp_path: Path) -> None:
    """shadcn package should be detected as component library."""
    pkg = {"dependencies": {"shadcn": "^4.0.5"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    analyzer = DesignUIAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.component_library == "shadcn"


def test_detects_shadcn_ui(tmp_path: Path) -> None:
    """@shadcn/ui should also be detected."""
    pkg = {"dependencies": {"@shadcn/ui": "^1.0.0"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    analyzer = DesignUIAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.component_library == "shadcn"
```

```python
# tests/test_analyzers/test_api.py
"""Tests for API analyzer Next.js App Router detection."""
import json
from pathlib import Path
from product_builders.analyzers.api import APIAnalyzer


def test_detects_nextjs_app_router_as_rest(tmp_path: Path) -> None:
    """Next.js with app/api/ routes should detect api_style as rest."""
    pkg = {"dependencies": {"next": "^15"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    (tmp_path / "src" / "app" / "api" / "users").mkdir(parents=True)
    (tmp_path / "src" / "app" / "api" / "users" / "route.ts").write_text(
        "export async function GET() { return Response.json({}) }"
    )
    analyzer = APIAnalyzer()
    result = analyzer.analyze(tmp_path)
    assert result.api_style == "rest"
```

### Step 2: Run tests to verify they fail

Run: `python -m pytest tests/test_analyzers/ -v`
Expected: FAIL — supabase not in DB_TYPE_INDICATORS, shadcn not in _COMPONENT_LIBS, Next.js not detected as REST

### Step 3: Implement the fixes

**database.py** — Add BaaS mappings to `DB_TYPE_INDICATORS` (after line 112):

```python
DB_TYPE_INDICATORS: dict[str, list[str]] = {
    "postgresql": [
        "pg", "postgres", "postgresql", "psycopg2", "psycopg", "Npgsql", "asyncpg",
        "@supabase/supabase-js", "@supabase/ssr", "supabase",
        "@neon/serverless", "@neondatabase/serverless",
    ],
    "mysql": [
        "mysql", "mysql2", "mysqlclient", "PyMySQL", "MySql.Data",
        "@planetscale/database",
    ],
    "sqlite": ["sqlite3", "better-sqlite3", "sqlite", "Microsoft.Data.Sqlite"],
    "mongodb": ["mongoose", "mongodb", "pymongo", "Motor", "MongoDB.Driver"],
    "redis": ["redis", "ioredis", "aioredis"],
    "mssql": ["mssql", "tedious", "pyodbc", "Microsoft.Data.SqlClient"],
    "firebase": ["firebase", "firebase-admin", "@firebase/firestore"],
    "dynamodb": ["@aws-sdk/client-dynamodb", "boto3"],
}
```

**design.py** — Add shadcn and modern component libraries to `_COMPONENT_LIBS` (add entries):

```python
"shadcn": "shadcn",
"@shadcn/ui": "shadcn",
"@base-ui/react": "base-ui",
"@nextui-org/react": "nextui",
"@park-ui/react": "park-ui",
"daisyui": "daisyui",
```

**api.py** — Add Next.js App Router detection in `_detect_api_style()`. Find the method and add before the final `return None`:

```python
# Next.js App Router API routes
if "next" in dep_names:
    api_dirs = list(repo_path.glob("**/app/api"))
    if api_dirs:
        return "rest"
```

### Step 4: Run tests

Run: `python -m pytest tests/test_analyzers/ -v`
Expected: All tests PASS

### Step 5: Commit

```bash
git add src/product_builders/analyzers/database.py src/product_builders/analyzers/design.py src/product_builders/analyzers/api.py tests/test_analyzers/
git commit -m "feat: add BaaS detection (Supabase, Firebase, PlanetScale) and modern component libraries (shadcn)"
```

---

## Task 3: Filter Blocked Commands by Detected Tech Stack

Currently blocked commands are hardcoded per role (prisma, alembic, flyway for all projects). They should be filtered based on what the analysis actually detected.

**Files:**
- Modify: `src/product_builders/profiles/base.py`
- Modify: `src/product_builders/generators/cursor_hooks.py` (where blocked commands are used)
- Test: `tests/test_generators/test_hooks.py` (create)

### Step 1: Write failing test

```python
# tests/test_generators/test_hooks.py
"""Tests for hooks generator blocked command filtering."""
from product_builders.profiles.base import filter_blocked_commands


def test_supabase_project_excludes_prisma_commands() -> None:
    """A Supabase project should not block prisma or alembic commands."""
    all_commands = [
        "prisma:migrate", "prisma:db push",
        "alembic upgrade", "alembic downgrade",
        "flyway migrate",
        "npm publish", "yarn publish",
        "docker build", "docker push",
        "rm -rf", "git push --force", "git push -f", "git reset --hard",
    ]
    detected_stack = {"@supabase/supabase-js", "next", "react"}
    filtered = filter_blocked_commands(all_commands, detected_stack)
    assert "prisma:migrate" not in filtered
    assert "prisma:db push" not in filtered
    assert "alembic upgrade" not in filtered
    assert "flyway migrate" not in filtered
    # Universal safety commands should remain
    assert "rm -rf" in filtered
    assert "git push --force" in filtered
    assert "npm publish" in filtered


def test_prisma_project_keeps_prisma_commands() -> None:
    """A Prisma project should still block prisma commands for non-engineers."""
    all_commands = ["prisma:migrate", "prisma:db push", "rm -rf"]
    detected_stack = {"prisma", "next", "react"}
    filtered = filter_blocked_commands(all_commands, detected_stack)
    assert "prisma:migrate" in filtered


def test_empty_stack_keeps_all_commands() -> None:
    """When no stack is detected, keep all blocked commands (safe default)."""
    all_commands = ["prisma:migrate", "rm -rf"]
    filtered = filter_blocked_commands(all_commands, set())
    assert filtered == all_commands
```

### Step 2: Run test to verify it fails

Run: `python -m pytest tests/test_generators/test_hooks.py -v`
Expected: FAIL — `filter_blocked_commands` does not exist

### Step 3: Implement

Add to `src/product_builders/profiles/base.py`:

```python
# Mapping: command prefix → required dependency for the command to be relevant
_TOOL_SPECIFIC_COMMANDS: dict[str, set[str]] = {
    "prisma:migrate": {"prisma", "@prisma/client"},
    "prisma:db push": {"prisma", "@prisma/client"},
    "alembic upgrade": {"alembic", "sqlalchemy"},
    "alembic downgrade": {"alembic", "sqlalchemy"},
    "flyway migrate": {"flyway"},
    "docker build": {"docker"},
    "docker push": {"docker"},
}


def filter_blocked_commands(
    commands: list[str], detected_deps: set[str]
) -> list[str]:
    """Remove tool-specific blocked commands when the tool isn't in the project.

    Universal safety commands (rm -rf, git push --force, npm publish, etc.)
    are always kept.  Tool-specific commands (prisma:migrate, alembic upgrade)
    are only kept when a related dependency is detected.

    If ``detected_deps`` is empty, all commands are kept (safe default).
    """
    if not detected_deps:
        return list(commands)

    result: list[str] = []
    for cmd in commands:
        required = _TOOL_SPECIFIC_COMMANDS.get(cmd)
        if required is None:
            # Universal command — always keep
            result.append(cmd)
        elif required & detected_deps:
            # Tool-specific and tool IS present — keep
            result.append(cmd)
        # else: tool-specific and tool NOT present — skip
    return result
```

### Step 4: Run tests

Run: `python -m pytest tests/test_generators/test_hooks.py -v`
Expected: All 3 tests PASS

### Step 5: Wire into generators

Modify `src/product_builders/generators/cursor_hooks.py` to call `filter_blocked_commands()` when building hooks. The generate method receives the profile — extract dependency names from `profile.dependencies.dependencies` and pass them to the filter.

### Step 6: Commit

```bash
git add src/product_builders/profiles/base.py src/product_builders/generators/cursor_hooks.py tests/test_generators/test_hooks.py
git commit -m "feat: filter blocked commands by detected tech stack"
```

---

## Task 4: Fix Testing Template Numbering

The `testing.mdc.j2` template has hardcoded rule numbers 1-6, causing gaps (1,2,5,6) when conditional rules 3 and 4 are skipped.

**Files:**
- Modify: `src/product_builders/generators/templates/testing.mdc.j2`
- Test: `tests/test_generators/test_templates.py` (create)

### Step 1: Write failing test

```python
# tests/test_generators/test_templates.py
"""Tests for Jinja2 template rendering correctness."""
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from product_builders.models.analysis import TestingResult
from product_builders.models.profile import ProductProfile, ProductMetadata


def _render_testing_template(profile: ProductProfile) -> str:
    """Render the testing.mdc template with the given profile."""
    template_dir = Path(__file__).resolve().parents[2] / "src" / "product_builders" / "generators" / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    tmpl = env.get_template("testing.mdc.j2")
    return tmpl.render(profile=profile, company_standards={})


def test_testing_rules_numbered_sequentially_when_all_present() -> None:
    """When all optional fields are present, rules should be 1-6."""
    profile = ProductProfile(
        metadata=ProductMetadata(name="test"),
        testing=TestingResult(
            test_framework="vitest",
            test_runner="vitest",
            test_file_pattern="**/*.test.ts",
            test_directories=["tests"],
            e2e_framework="playwright",
        ),
    )
    content = _render_testing_template(profile)
    numbers = re.findall(r"^(\d+)\.", content, re.MULTILINE)
    assert numbers == ["1", "2", "3", "4", "5", "6"]


def test_testing_rules_numbered_sequentially_when_optional_missing() -> None:
    """When test_file_pattern and test_directories are absent, no numbering gaps."""
    profile = ProductProfile(
        metadata=ProductMetadata(name="test"),
        testing=TestingResult(test_framework="vitest", test_runner="vitest"),
    )
    content = _render_testing_template(profile)
    numbers = re.findall(r"^(\d+)\.", content, re.MULTILINE)
    # Should be sequential regardless of how many rules are included
    for i, n in enumerate(numbers, 1):
        assert n == str(i), f"Expected rule {i} but got {n}"
```

### Step 2: Run test to verify it fails

Run: `python -m pytest tests/test_generators/test_templates.py -v`
Expected: FAIL on `test_testing_rules_numbered_sequentially_when_optional_missing` — numbers will be [1, 2, 5, 6]

### Step 3: Fix the template

Replace hardcoded numbers with a Jinja2 counter. In `testing.mdc.j2`, replace the rules section:

```jinja2
## Rules

{% set ns = namespace(n=1) %}
{{ ns.n }}. Every new feature and bug fix must include tests
{% set ns.n = ns.n + 1 %}
{{ ns.n }}. Use the existing test framework — do not introduce alternatives
{% set ns.n = ns.n + 1 %}
{% if profile.testing.test_file_pattern %}
{{ ns.n }}. Test file naming: `{{ profile.testing.test_file_pattern }}`
{% set ns.n = ns.n + 1 %}
{% endif %}
{% if profile.testing.test_directories %}
{{ ns.n }}. Place tests in: {{ profile.testing.test_directories | join(', ') }}
{% set ns.n = ns.n + 1 %}
{% endif %}
{{ ns.n }}. Tests must be independent — no shared mutable state between tests
{% set ns.n = ns.n + 1 %}
{{ ns.n }}. Prefer descriptive test names that explain the expected behavior
{% if profile.testing.e2e_framework %}
{% set ns.n = ns.n + 1 %}
{{ ns.n }}. E2E tests use {{ profile.testing.e2e_framework }}
{% endif %}
```

### Step 4: Run tests

Run: `python -m pytest tests/test_generators/test_templates.py -v`
Expected: Both tests PASS

### Step 5: Commit

```bash
git add src/product_builders/generators/templates/testing.mdc.j2 tests/test_generators/test_templates.py
git commit -m "fix: testing template uses sequential numbering instead of hardcoded"
```

---

## Task 5: Wire overrides.yaml into the Analysis Pipeline

`config.load_overrides()` exists but is never called. Wire it into the `generate` and `setup` commands to merge user overrides into the profile before rule generation.

**Files:**
- Modify: `src/product_builders/cli.py` (generate command, ~line 238)
- Test: `tests/test_generators/test_overrides.py` (create)

### Step 1: Write failing test

```python
# tests/test_generators/test_overrides.py
"""Tests for overrides.yaml merging into ProductProfile."""
import json
from pathlib import Path

import yaml

from product_builders.models.profile import ProductProfile, ProductMetadata
from product_builders.models.analysis import DatabaseResult


def apply_overrides(profile: ProductProfile, overrides: dict) -> ProductProfile:
    """Apply overrides dict to a profile, returning a new profile."""
    from product_builders.profiles.overrides import merge_overrides
    return merge_overrides(profile, overrides)


def test_override_database_type() -> None:
    """overrides.yaml should be able to set database_type."""
    profile = ProductProfile(
        metadata=ProductMetadata(name="test"),
        database=DatabaseResult(database_type=None),
    )
    overrides = {"database": {"database_type": "postgresql"}}
    updated = apply_overrides(profile, overrides)
    assert updated.database.database_type == "postgresql"


def test_override_preserves_existing_values() -> None:
    """Overrides should not wipe fields that aren't overridden."""
    profile = ProductProfile(
        metadata=ProductMetadata(name="test"),
        database=DatabaseResult(database_type="mysql", orm="prisma"),
    )
    overrides = {"database": {"database_type": "postgresql"}}
    updated = apply_overrides(profile, overrides)
    assert updated.database.database_type == "postgresql"
    assert updated.database.orm == "prisma"


def test_empty_overrides_returns_unchanged() -> None:
    """Empty overrides dict should return profile unchanged."""
    profile = ProductProfile(metadata=ProductMetadata(name="test"))
    updated = apply_overrides(profile, {})
    assert updated.model_dump() == profile.model_dump()
```

### Step 2: Run test to verify it fails

Run: `python -m pytest tests/test_generators/test_overrides.py -v`
Expected: FAIL — `product_builders.profiles.overrides` module does not exist

### Step 3: Create the overrides module

```python
# src/product_builders/profiles/overrides.py
"""Merge user-provided overrides into a ProductProfile."""
from __future__ import annotations

from product_builders.models.profile import ProductProfile


def merge_overrides(
    profile: ProductProfile, overrides: dict
) -> ProductProfile:
    """Return a new profile with override values merged in.

    Only known dimension names are accepted.  Within each dimension the
    override dict is shallow-merged (override keys win, unmentioned keys
    are preserved from the original).
    """
    if not overrides:
        return profile

    data = profile.model_dump()
    for dimension, values in overrides.items():
        if dimension in data and isinstance(values, dict) and isinstance(data[dimension], dict):
            data[dimension].update(values)
    return ProductProfile.model_validate(data)
```

### Step 4: Wire into CLI

In `src/product_builders/cli.py`, in the `generate` command (after loading the profile, before running generators), add:

```python
overrides = config.load_overrides(name)
if overrides:
    from product_builders.profiles.overrides import merge_overrides
    profile = merge_overrides(profile, overrides)
    console.print(f"[dim]Applied overrides from overrides.yaml[/dim]")
```

### Step 5: Run tests

Run: `python -m pytest tests/test_generators/test_overrides.py -v`
Expected: All 3 tests PASS

### Step 6: Commit

```bash
git add src/product_builders/profiles/overrides.py src/product_builders/cli.py tests/test_generators/test_overrides.py
git commit -m "feat: wire overrides.yaml into generate pipeline for user-correctable analysis"
```

---

## Verification

After all 5 tasks are complete:

1. **Run full test suite:**
   ```bash
   python -m pytest tests/ -v
   ```

2. **Re-analyze seeker1 and check improvements:**
   ```bash
   product-builders analyze --repo-path "C:\Users\hbbar\Documents\GitHub\Truth Seekr" --name seeker1
   ```
   Expected: database_type should now be "postgresql", component_library should be "shadcn"

3. **Regenerate rules and verify:**
   ```bash
   product-builders generate --name seeker1 --role product_manager
   ```
   Expected: No prisma/alembic/flyway in blocked commands, testing rules numbered sequentially

4. **Check zone detection:**
   Review `profiles/seeker1/scopes.yaml` — should now have api, tests, and database zones in addition to frontend_ui, backend_logic, configuration
