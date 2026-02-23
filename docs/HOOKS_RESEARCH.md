# Cursor Hooks Research — Deep Dive

> **Purpose**: Validate the Product Builders Layer 2 (hooks) proposal. What is the real truth about Cursor hooks? What are the options? What do other tools do?
>
> **Date**: Feb 2026

---

## Executive Summary

**The Product Builders plan is partially correct.** The `preToolUse` hook **does exist** in Cursor and **can intercept file writes** (Write/Edit tools) before they execute. It can block with a helpful message — exactly what Layer 2 requires. However, there is a **known Windows bug** (ENAMETOOLONG) when editing large files that may affect reliability. A **defense-in-depth strategy** using both `preToolUse` and `cli.json` is recommended.

---

## 1. The Real Truth: Cursor Hooks API

### 1.1 Two Hook Systems (and Some Confusion)

Cursor has **two overlapping hook systems** that are easy to conflate:

| System | Source | Hooks | Use Case |
|--------|--------|-------|----------|
| **Original Cursor hooks** | GitButler blog, older docs | `beforeShellExecution`, `beforeReadFile`, `afterFileEdit`, `beforeMCPExecution`, `beforeSubmitPrompt`, `stop` | Shell blocking, file read redaction, audit |
| **preToolUse / postToolUse** | Third-party hooks (Claude Code compatibility), Cursor native | `preToolUse`, `postToolUse` + lifecycle | **Tool-level interception** — Write, Edit, Read, Bash, MCP |

The **unofficial** [cursor-hooks schema](https://unpkg.com/cursor-hooks/schema/hooks.schema.json) only lists the original 6 hooks and has `additionalProperties: false` — it is **outdated**. It does not include `preToolUse` or `postToolUse`.

### 1.2 preToolUse — Confirmed and Documented

**Official source**: [Cursor Third Party Hooks](https://cursor.com/docs/agent/third-party-hooks)

- `preToolUse` is a **native Cursor hook** (not just Claude Code)
- Cursor maps Claude Code's `PreToolUse` → `preToolUse` when third-party skills are enabled
- Supports **tool matchers** (regex) to filter which tools trigger the hook

**Native Cursor format** (`.cursor/hooks.json`):

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      {
        "command": "./hooks/validate-scope.sh",
        "matcher": "Write|Edit"
      }
    ]
  }
}
```

**Tool matchers** (from Claude SDK, mapped in Cursor):

| Matcher | Tools |
|---------|-------|
| `Write` | File creation |
| `Edit` or `Edit|MultiEdit` | File edits |
| `Read` | File reads |
| `Shell` or `Bash` | Shell commands |
| `*` or `""` | All tools |
| `mcp__.*` | MCP tools |

### 1.3 preToolUse Payload and Blocking

**Input** (via stdin as JSON):

- `tool_name`: e.g. `"Write"`, `"Edit"`, `"Bash"`
- `tool_input`: Tool-specific args. For Write/Edit: `file_path`, `content` (or `old_string`/`new_string` for Edit)

**Blocking** (two methods):

1. **Exit code 2** — Simple block; Cursor treats as deny
2. **JSON output** — Structured response:
   ```json
   {
     "permissionDecision": "deny",
     "permissionDecisionReason": "This file (migrations/001_add_users.sql) is a database migration. As a Product Manager, database schema changes require engineering team involvement. I can help you create a Jira issue describing the database change you need instead."
   }
   ```

**Source**: [Claude API Docs — Hooks](https://platform.claude.com/docs/en/agent-sdk/hooks) (Cursor maps Claude format; behavior is equivalent)

**Key insight**: "To filter by file path, check `tool_input.file_path` inside your callback." — Exactly what Product Builders needs for scope enforcement.

---

## 2. Known Issues and Limitations

### 2.1 ENAMETOOLONG on Windows (Critical for Large Files)

**Source**: [Cursor Forum — preToolUse hook fails with ENAMETOOLONG](https://forum.cursor.com/t/pretooluse-hook-fails-with-enametoolong-for-large-files/150346)

- **Symptom**: When editing large files, the hook fails with `ENAMETOOLONG` before the script executes
- **Cause**: The entire file content is passed in `tool_input.content`; Cursor appears to pass the payload via spawn args/env, exceeding Windows command-line length limits (~32KB)
- **Impact**: Scope-check hooks that only need `file_path` still receive full content — if Cursor passes everything as args, large files break
- **Suggested fixes** (from forum):
  1. Stream data via stdin instead of spawn args
  2. Add config option to exclude `tool_input.content` from hook payload
  3. Write hook input to temp file and pass path

**Mitigation for Product Builders**: 
- Scope checks only need `file_path` — if Cursor ever supports excluding content, or passes via stdin, we're fine
- For now: **test on Windows with large files** during pilot. If ENAMETOOLONG occurs, fall back to cli.json-only for file scope (Layer 3)
- Most PM/designer edits (components, styles, pages) touch smaller files — risk may be acceptable

### 2.2 updated_input Ignored for Task Tool

**Source**: [Cursor Forum — preToolUse updated_input silently ignored](https://forum.cursor.com/t/pretooluse-hook-updated-input-is-silently-ignored-for-the-task-tool/151985)

- `updated_input` (modifying tool params before execution) is ignored for the Task tool
- **Not relevant** for scope enforcement — we only need allow/deny, not input modification

### 2.3 beforeReadFile vs preToolUse for Reads

- `beforeReadFile`: Can block **file reads** (redact secrets, block sensitive files). Different payload structure.
- `preToolUse` with matcher `Read`: Can also intercept reads at tool level.
- For Product Builders: We care about **writes** (scope enforcement). Reads are secondary — PM may need to read backend code for context even if they can't edit it.

---

## 3. Comparison: Enforcement Options

| Mechanism | File Write Block | Helpful Message | Shell Block | Works on Windows (Large Files) |
|-----------|------------------|-----------------|------------|-------------------------------|
| **preToolUse** (Write\|Edit) | Yes | Yes | No (use Shell matcher) | Risk: ENAMETOOLONG |
| **beforeShellExecution** | No | Yes | Yes | Yes |
| **cli.json** (Write deny) | Yes | No (silent deny) | Partial (Shell deny) | Yes |
| **Rules only** | No (soft) | Yes (in rules) | No | N/A |

### Recommended Layering

1. **Layer 1 (Rules)**: Soft guidance — always include scope in `contributor-guide.mdc` with redirects
2. **Layer 2a (preToolUse, Write|Edit)**: Smart blocking for file scope — implement, test on Windows. If ENAMETOOLONG, document and fall back
3. **Layer 2b (preToolUse, Shell or beforeShellExecution)**: Block dangerous shell commands with helpful messages
4. **Layer 3 (cli.json)**: Hard deny — always generate. Guarantees enforcement even if hooks fail

---

## 4. What Other Tools Do

### 4.1 Oasis Security × Cursor

**Source**: [Oasis Blog — Governing Agentic Access](https://www.oasis.security/blog/cursor-oasis-governing-agentic-access)

- Uses `beforeMCPExecution` for logging and policy enforcement
- Hooks intercept "at the source" — before execution
- Can return `allow` / `warn` / `step-up` / `deny`
- Use cases: Payload DLP, command guardrails, production step-up, approved MCPs only

**Takeaway**: Hooks are the standard mechanism for governance. Oasis focuses on MCP; we focus on file scope.

### 4.2 GitHub Copilot CLI

**Source**: [GitHub Docs — Copilot CLI Hooks](https://docs.github.com/en/copilot/tutorials/copilot-cli-hooks)

- Has `preToolUse` hook — fires before any tool
- Repo-scoped: `.github/hooks/*.json`
- Common patterns: Block `rm -rf`, `curl | bash`, `sudo`
- Same conceptual model: intercept → validate → allow/deny

### 4.3 Claude Code (Anthropic SDK)

**Source**: [Claude API Docs — Hooks](https://platform.claude.com/docs/en/agent-sdk/hooks)

- **Canonical example**: Block writes to `.env` using PreToolUse with matcher `Write|Edit`
- Check `tool_input.file_path`, return `permissionDecision: "deny"` + `permissionDecisionReason`
- Matchers: `Bash`, `Read`, `Edit|MultiEdit`, `Write`

**Takeaway**: File path validation via PreToolUse is a documented, supported pattern. Cursor inherits this.

### 4.4 Coder AI Governance

**Source**: [Coder Docs — AI Governance](https://coder.com/docs/ai-coder/ai-governance)

- Enterprise: Agent boundaries, AI Bridge, centralized MCP management
- Different model: Process-level firewalls, not per-tool hooks
- Product Builders targets project-level, not enterprise infra

### 4.5 .cursorignore — Not a Solution

**Source**: [Cursor Docs — Ignore Files](https://cursor.com/docs/context/ignore-files)

- `.cursorignore` excludes files from **codebase indexing**
- **Chat and Composer have access to all files** regardless of .cursorignore
- Cannot be used for scope enforcement

---

## 5. Best Practices (Synthesized)

1. **Use matchers** — `"Write|Edit"` for file scope; `"Shell"` for commands. Avoid `*` (all tools) for performance.
2. **Return structured JSON** — `permissionDecision` + `permissionDecisionReason` gives the AI context to self-correct. Better than exit 2 alone.
3. **Keep hooks fast** — Scope check is a path match against a small allowlist; should be milliseconds.
4. **Defense in depth** — Never rely on hooks alone. cli.json is the hard guarantee.
5. **Test on Windows** — ENAMETOOLONG is Windows-specific. Include a large-file test in pilot.
6. **Hook script robustness** — Parse JSON from stdin; handle malformed input gracefully; exit 0 = allow when in doubt (or fail-open per your policy).

---

## 6. Implementation Options for Product Builders

### Option A: Full preToolUse for File Scope (Recommended to Try)

- Implement `preToolUse` with matcher `Write|Edit`
- Hook script: Read JSON from stdin → extract `tool_input.file_path` → check against `scopes.yaml` for current profile → return deny + reason or allow
- **Pros**: Helpful messages, matches plan
- **Cons**: ENAMETOOLONG risk on Windows
- **Action**: Implement, test on Windows with large file. If broken, fall back to Option B.

### Option B: cli.json Only for File Scope

- Rely entirely on `cli.json` Write allow/deny for file scope
- Use `preToolUse` or `beforeShellExecution` only for **shell** blocking (e.g. `prisma:migrate`, `rm`)
- **Pros**: No ENAMETOOLONG; shell blocking still gives helpful messages
- **Cons**: File scope blocks are silent (no "create Jira issue instead")

### Option C: Hybrid with Feature Flag

- Implement both preToolUse (files) and cli.json
- Add config: `use_pre_tool_use_for_file_scope: true|false`
- Default true; set false for Windows or if issues arise
- **Pros**: Flexibility
- **Cons**: More code paths to maintain

### Option D: Request Cursor Enhancement

- File issue/feedback: "Add option to exclude tool_input.content from preToolUse payload for path-only validation"
- Would solve ENAMETOOLONG for scope-check use case
- **Action**: Can submit as feature request; don't block implementation on it

---

## 7. Recommended Hook Script Structure

```bash
#!/usr/bin/env bash
# .cursor/hooks/scope-check.sh
# Reads JSON from stdin, outputs JSON to stdout

input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
tool_name=$(echo "$input" | jq -r '.tool_name // empty')

# Only check Write/Edit
if [[ "$tool_name" != "Write" && "$tool_name" != "Edit" ]]; then
  echo '{"permissionDecision": "allow"}'
  exit 0
fi

# Check file_path against scopes (logic from scopes.yaml + profile)
if ! python -m product_builders check-scope --path "$file_path" --profile "$PROFILE"; then
  reason=$(python -m product_builders check-scope --path "$file_path" --profile "$PROFILE" --reason-only)
  echo "{\"permissionDecision\": \"deny\", \"permissionDecisionReason\": \"$reason\"}"
  exit 0  # Exit 0 so JSON is used; Cursor blocks based on permissionDecision
fi

echo '{"permissionDecision": "allow"}'
exit 0
```

**Note**: Profile could come from `.cursor/contributor-profile.json` (gitignored) written by `setup --profile`.

---

## 8. Conclusion

| Question | Answer |
|----------|--------|
| Does preToolUse exist? | **Yes** — native Cursor + Claude Code mapping |
| Can it intercept file writes? | **Yes** — matcher `Write|Edit`, `tool_input.file_path` |
| Can it block with helpful message? | **Yes** — `permissionDecision: "deny"` + `permissionDecisionReason` |
| Is there a risk? | **Yes** — ENAMETOOLONG on Windows for large files |
| What should Product Builders do? | Implement preToolUse for Layer 2; always include cli.json (Layer 3); test on Windows; document fallback |

**The original validation plan overstated the gap.** The GitButler blog covered the *original* 6 hooks; Cursor has since added preToolUse/postToolUse (via Claude Code compatibility and native support). The Product Builders Layer 2 design is **feasible**. The main caveat is the Windows ENAMETOOLONG bug — mitigate with testing and a cli.json fallback.
