# CLI reference (overview)

| Command | Purpose |
|--------|---------|
| `wizard` | Interactive quick start by phase (install through lifecycle); use `--phase`, `-y`, `--repo`, `--name` for scripting |
| `analyze` | Run heuristic analyzers; write `analysis.json` and scopes |
| `generate` | Generate Cursor rules, hooks, permissions, onboarding from profile |
| `setup` | Write role-specific `.cursor/` governance into the current directory |
| `export` | Copy generated rules, hooks, scopes, and docs into a target repo |
| `list` | List known products / profiles |
| `bulk-analyze` | Analyze multiple repositories (manifest or monorepo) |
| `check-drift` | Compare git HEAD and/or heuristic fingerprints to the cached profile |
| `metrics` | Show recent `metrics.jsonl` events for a product |
| `feedback` | Append rule accuracy notes to `feedback.yaml` |

## Environment

| Variable | Meaning |
|----------|---------|
| `PB_HOME` | Repository root for default paths |
| `PB_PROFILES_DIR` | Directory containing `profiles/<product>/` |
| `PB_STANDARDS_DIR` | Company standards YAML directory |

## Outputs (typical)

- `profiles/<name>/analysis.json` — `ProductProfile` snapshot  
- `profiles/<name>/scopes.yaml` — Zones and contributor scopes  
- `profiles/<name>/.cursor/rules/*.mdc` — Cursor rules  
- `profiles/<name>/.cursor/hooks.json` — Cursor hooks  
- `profiles/<name>/.cursor/cli.json` — CLI permissions  
- `profiles/<name>/docs/onboarding-*.md` — Role onboarding  

## overrides.yaml

After running `analyze`, you can create `profiles/<name>/overrides.yaml` to override any analysis field before generation. When you run `generate`, the pipeline loads this file and merges its values into the profile. This lets you correct misdetected frameworks, add missing dependencies, or tweak any dimension without re-running analysis.

```yaml
# profiles/my-product/overrides.yaml
tech_stack:
  primary_language: typescript
  frameworks:
    - name: next
      version: "14"
```

## Smart command filtering

Blocked commands in generated hooks respect the project's actual dependencies. Tool-specific commands (e.g., `prisma migrate`, `drizzle push`) are only blocked when that tool is detected in the tech stack. This prevents false-positive blocks for tools not present in the project.

## Zone detection

Zones are detected in `src/`-prefixed paths and nested directories. For example, `src/components/`, `src/lib/utils/`, and `src/app/api/` are all recognized as distinct zones during scope generation, giving finer-grained contributor scopes.

## BaaS detection

The analyzer maps backend-as-a-service platforms to their underlying database types:

| Platform / Tool | Detected DB type |
|----------------|-----------------|
| Supabase | `postgresql` |
| Firebase | `firebase` |
| DynamoDB | `dynamodb` |
| PlanetScale | `mysql` |

Additional framework signals are also detected: **shadcn** as a UI library, and **Next.js App Router** patterns map to a `REST` API style.

## Testing template

Generated test rules use sequential numbering (e.g., `001-unit-tests.mdc`, `002-integration-tests.mdc`) for deterministic ordering.

For full architecture, see the repository **ARCHITECTURE.md**.
