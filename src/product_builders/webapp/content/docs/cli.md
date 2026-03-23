# CLI reference (overview)

| Command | Purpose |
|--------|---------|
| `analyze` | Run heuristic analyzers; write `analysis.json` and scopes |
| `generate` | Generate Cursor rules, hooks, permissions, onboarding from profile |
| `setup` | Guided setup for a product |
| `export` | Export or sync generated files for a contributor profile |
| `list` | List known products / profiles |
| `bulk-analyze` | Analyze multiple repositories |
| `check-drift` | Compare repo state to stored profile (when implemented) |
| `feedback` | Submit or record feedback (when wired) |

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

For full architecture, see the repository **ARCHITECTURE.md**.
