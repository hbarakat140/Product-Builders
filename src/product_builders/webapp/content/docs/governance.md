# Governance model (three layers)

Generated governance stacks three complementary mechanisms:

## Layer 1 — Rules (`.mdc`)

Soft guidance for the AI: stack, conventions, security, testing, contributor scopes, etc.  
Templates are Jinja2-driven from the `ProductProfile`.

## Layer 2 — Hooks (`hooks.json`)

**Smart blocking** of dangerous operations (`preToolUse`, `beforeShellExecution`) with clear messages — not a full sandbox, but high-signal guardrails.

## Layer 3 — Permissions (`cli.json`)

**Hard** filesystem allow/deny rules for the Cursor CLI — strongest enforcement layer.

## Scopes

`scopes.yaml` defines **zones** (directory globs) and what each **contributor role** may read, write, or must avoid. Generators use this for rules and onboarding.

---

See **docs/HOOKS_RESEARCH.md** in the repo for hook semantics and platform limits.
