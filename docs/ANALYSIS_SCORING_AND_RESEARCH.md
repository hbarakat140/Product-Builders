# Product Builders: Deep Analysis, Scoring & Strategic Research

**Date:** 2026-03-25
**Scope:** End-to-end evaluation of the analysis-to-generation pipeline, market landscape research (80+ tools), and strategic recommendations for adding intelligence.

**Profiles evaluated:** seeker1 (Truth Seekr — Next.js/Supabase), product-builders (self-analysis — Python/FastAPI)

---

## Executive Summary

**Current Pipeline Score: 6.3/10 (B-)**

The pipeline has a strong architectural foundation (governance design 8/10, extensibility 8.5/10) but fails at the "last mile" of analysis accuracy (6/10) and rule relevance (5/10). The root cause: all 20 analyzers are purely heuristic (regex + file existence + dependency name lookups) with zero code understanding.

**Approved Strategy: Three-Layer Intelligence Model**

```
Layer 1: Heuristics (keep)     → WHAT exists (files, deps, configs)
Layer 2: Tree-sitter AST (add) → HOW code is structured (imports, functions, components)
Layer 3: Cursor AI (add)       → WHY patterns exist (domain, rationale, conventions)
```

No LLM APIs required. Tree-sitter is fully offline. Cursor (already available in enterprise) provides the AI intelligence through its native interface.

---

## Part 1: Pipeline Scoring

### Summary Table

| # | Category | Score | Verdict |
|---|----------|------:|---------|
| 1 | Analysis Accuracy | **6.0/10** | Core stack solid; misses BaaS/meta-framework patterns |
| 2 | Analysis Completeness | **5.0/10** | ~30% field population; many detectable dimensions left null |
| 3 | Rule Quality | **6.5/10** | Well-structured .mdc; content falls to generic boilerplate |
| 4 | Rule Relevance | **5.0/10** | Half universal best-practices, half irrelevant to actual project |
| 5 | Governance Design | **8.0/10** | Excellent 3-layer model; weakened by static blocked commands |
| 6 | Scope/Zone Accuracy | **4.0/10** | Only 3/7 zones detected; path-matching bug misses src/app/api |
| 7 | Code Quality | **6.5/10** | Clean architecture, zero test coverage for core modules |
| 8 | Extensibility | **8.5/10** | Well-defined ABC + registry extension points |
| 9 | Developer Experience | **6.0/10** | Solid CLI with Rich output; lacks dry-run, diff, overrides |
| 10 | Overall System Design | **7.5/10** | Clean pipeline, Pydantic IR, offline-first, lifecycle features |
| | **Weighted Average** | **6.3/10** | |

### 1. Analysis Accuracy — 6/10

**What works:**
- Language detection: TypeScript 95.6%, SQL 2.9%, CSS 1.5% for seeker1 — correct
- Framework detection: Correctly identified Next.js ^15, React ^19 via dependency name matching
- Auth strategy: Correctly identified `supabase` from `@supabase/supabase-js`
- Test framework: Correctly identified `vitest` from config file presence
- CSS methodology: Correctly returned `tailwind` from `tailwindcss` in dependencies

**What's inaccurate:**

| Issue | Impact | Root Cause |
|-------|--------|------------|
| database_type: null despite Supabase | Rules miss all DB guidance | `DB_TYPE_INDICATORS` has no Supabase → postgresql mapping |
| component_library: null despite shadcn v4 | Design rules miss component conventions | `_COMPONENT_LIBS` dict doesn't include `shadcn` |
| logging_framework: null for TypeScript | Error handling rules generic | Only checks npm packages (winston, pino), not console.log |
| auth_middleware: empty | Auth rules miss middleware patterns | Only checks for passport, express-jwt — not Supabase's `createServerClient` |
| api_style: null despite 8 API route files | API rules not generated | Doesn't recognize Next.js App Router as REST API |
| False positive: auth.protected_route_patterns in product-builders | JS patterns detected in Python project | Generic pattern list not language-filtered |
| Placeholder: custom_error_classes: ["XxxError"] | Not real class names | Regex matches pattern names, not actual classes |

### 2. Analysis Completeness — 5/10

**Field population audit (seeker1):**

| Dimension | Populated / Total | Key Gaps |
|-----------|------------------:|----------|
| tech_stack | 5/6 | runtime_versions empty |
| database | **0/9** | All null despite Supabase |
| auth | 2/7 | middleware, token_handling, session_management null |
| dependencies | **3/3** | Comprehensive |
| error_handling | 1/6 | Only error_strategy |
| i18n | 0/6 | Legitimate — no i18n |
| state_management | 1/4 | Only React Context/hooks |
| env_config | 2/7 | Missing Docker, feature flags |
| git_workflow | **0/8** | All null despite being a git repo |
| structure | **6/7** | Good |
| conventions | 2/8 | No formatter, naming convention |
| security | **0/6** | All null |
| testing | 2/9 | Nested `__tests__` not found |
| cicd | 0/5 | Legitimate — no CI config |
| design_ui | 2/10 | Missing shadcn |
| accessibility | 3/6 | Reasonable |
| api | 1/8 | Only route_structure |
| performance | 2/7 | Next.js builtins detected |
| frontend_patterns | **5/8** | Good |
| user_flows | **5/7** | Good — 21 routes |
| **Total** | **~42/141** | **~30% population** |

Deep analysis fields (architecture_deep, domain_model_deep, implicit_conventions_deep) are all empty — expected, as they require Cursor-assisted Phase 2.

### 3. Rule Quality — 6.5/10

**Structural quality (strong):**
- Proper YAML frontmatter on every .mdc (description, globs, alwaysApply, priority)
- Conditional generation via `_should_generate()` — skips irrelevant rules
- Security rules have 7 company standards with severity levels + checklist
- Bootstrap meta-rule provides structured 4-step deep analysis workflow

**Content quality (mixed):**

| Rule File | Quality | Issue |
|-----------|---------|-------|
| project-overview.mdc | Good | Clear stack + contributor context |
| security.mdc | Good | Comprehensive 7-standard framework |
| coding-conventions.mdc | Fair | Only linter is project-specific |
| testing.mdc | Poor | 4 rules, numbering gap (1,2,5,6), no coverage targets |
| architecture.mdc | Poor | Lists dirs, says "flat" for a structured Next.js app |
| bootstrap-meta-rule.mdc | Excellent | Structured 4-step deep analysis |
| contributor-guide.mdc | Good | Role-specific zones and behavioral rules |

**Template numbering bug:** testing.mdc outputs rules 1, 2, 5, 6 — skipping 3 and 4 because conditional Jinja2 blocks are false but numbering is hardcoded.

### 4. Rule Relevance — 5/10

**Relevant rules:**
- Tech stack: TypeScript, Next.js ^15, React ^19, npm, ESLint
- Design: Tailwind CSS methodology
- Auth: Supabase strategy
- PM access: frontend_ui writable, backend_logic read-only

**Irrelevant/generic rules:**

| Rule | Problem |
|------|---------|
| "Use parameterized queries" | Project uses Supabase client SDK, not raw SQL |
| Blocked: prisma:migrate, alembic, flyway | None exist in this Supabase project |
| "Organization: flat" | Misleading — clear component/lib/app/api structure |

**Missing project-specific rules (should exist):**
- No Supabase rules (RLS, client vs server, anon key exposure)
- No Next.js App Router rules (Server Components, `use client`, Server Actions)
- No AI SDK usage rules (@anthropic-ai/sdk, openai both in deps)
- No shadcn/ui component conventions
- No document processing pipeline rules (mammoth, pdf-parse)

### 5. Governance Design — 8/10

**Three-layer model (excellent):**

| Layer | Mechanism | Enforcement |
|-------|-----------|-------------|
| Layer 1 | Soft rules (.mdc) | Guidance, conventions |
| Layer 2 | Smart hooks (hooks.json) | Contextual blocking with explanatory messages |
| Layer 3 | Hard deny (cli.json) | Filesystem-level write deny |

- Escalation model correct: Engineers bypass layers 2/3; PM/Designer get all 3
- ScopeConfig with Zone + ContributorScope as YAML single-source-of-truth is clean
- Hook messages are user-friendly

**Weakness:** Blocked commands are hardcoded per role profile, not derived from analysis.

### 6. Scope/Zone Accuracy — 4/10

**Detected for seeker1: 3 zones**

| Zone | Paths | Assessment |
|------|-------|------------|
| frontend_ui | `src/components/**` | Correct but incomplete |
| backend_logic | `src/lib/**` | Mixes client utils and backend logic |
| configuration | `.env*`, `config/**` | Reasonable default |

**Missing zones:**

| Zone | Path | Why Missed |
|------|------|-----------|
| api | `src/app/api/**` | Detector checks `repo_path / "app/api"` not `src/app/api` |
| tests | `src/lib/*/__tests__/` | Only checks root-level test dirs |
| database | `supabase/migrations/` | Checks `repo_path / "migrations"` not `supabase/migrations` |
| types | `src/types/` | No detector pattern |

**Root cause:** `auto_detect_zones()` does `(repo_path / pattern).is_dir()` — no glob traversal, no `src/` prefix cross-referencing.

### 7. Code Quality — 6.5/10

**Strengths:** Clean ABC, Pydantic v2, `safe_analyze()` fault tolerance, modern Python 3.11+ types.

**Known bugs:** 5 CRITICAL, 14 HIGH, 18 MEDIUM, 10 LOW (see docs/code-review-report.md).

**Test coverage: SEVERE GAP** — 0 tests for 20 analyzers, 0 tests for 6 generators. Only drift, validation, and webapp have tests.

### 8. Extensibility — 8.5/10

Well-defined extension workflow: Subclass BaseAnalyzer → implement name/dimension/analyze → add model field → register. Same pattern for generators. No plugin system (package-only), but clean patterns.

### 9. Developer Experience — 6/10

Good: Click CLI, Rich output, wizard, setup, feedback, --verbose, -y mode.
Missing: No --dry-run, no diff, no inspect, no --output-dir, dead overrides.yaml mechanism.

### 10. Overall System Design — 7.5/10

Clean pipeline (Analyze → ProductProfile → Generate → Artifacts), Pydantic IR, offline-first, two-phase design (heuristic + Cursor deep), lifecycle features (drift, metrics, feedback).

Gaps: No override/enrichment pipeline, no incremental analysis, no analyzer dependency graph.

---

## Part 2: Intelligence Gap Analysis

### Current State: 0% AI

Every analyzer works by one or more of these techniques:

| Technique | Example | Intelligence Level |
|-----------|---------|-------------------|
| File existence check | "Does prisma/schema.prisma exist?" | None |
| Dependency name lookup | "Is 'next' in package.json dependencies?" | None |
| Config file parsing | "What's in eslint.config.mjs?" | None |
| Regex pattern scanning | "Does any file contain `throw `?" | Minimal |
| Directory structure listing | "What dirs are in src/?" | None |

There is no AST parsing, no semantic code understanding, no dependency graph analysis, no architecture inference. The deep analysis module (`src/product_builders/deep_analysis/__init__.py`) is an empty skeleton with a one-line docstring.

### Analyzer-by-Analyzer Intelligence Map

| Analyzer | Primary Technique | Can Understand Code? | Key Limitation |
|----------|------------------|---------------------|----------------|
| tech_stack | Dep name + file parsing | No | Can't detect framework usage patterns |
| database | Dep name + file existence | No | No Supabase → PostgreSQL mapping |
| auth | Dep name + regex scan (30 files) | No | Can't trace auth middleware chain |
| dependencies | Manifest parsing | No | Can't categorize most deps |
| error_handling | Dep name + regex scan (30 files) | No | python-logging detection bug |
| i18n | Dep name + dir existence | No | Can't detect inline string patterns |
| state_management | Dep name + dir existence | No | Can't trace data flow |
| env_config | File existence | No | Can't parse env var usage |
| git_workflow | File existence + YAML parsing | No | Can't analyze commit history patterns |
| structure | Dir listing | No | Can't infer module purpose |
| conventions | Config file existence + filename sampling | No | Can't analyze naming patterns in code |
| security | Dep name + file existence | No | Can't assess security posture |
| testing | Config file + dep name + dir existence | No | Can't find nested test dirs |
| cicd | File existence + YAML parsing | No | Can't analyze build pipeline |
| design_ui | Dep name + file existence | No | Missing shadcn, Radix UI |
| accessibility | Dep name + regex scan | No | Can't assess WCAG compliance |
| api | Dep name + dir existence | No | Can't parse route handlers |
| performance | Dep name + regex scan | No | Can't assess bundle impact |
| frontend_patterns | Dep name + regex scan (20 files) | No | Can't understand component composition |
| user_flows | File glob for route files | No | Can't trace navigation flow |

### What Tree-sitter AST Would Add

| Capability | Current (regex) | With Tree-sitter AST |
|-----------|----------------|---------------------|
| Import statements | Regex: `import.*from` | AST `import_statement` node — exact module resolution |
| Module dependency graph | Can't do it | Parse all imports → directed graph → real module boundaries |
| Function signatures | Can't do it | Extract exports, params, return types |
| Component hierarchy | Can't do it | Parse JSX/TSX → parent-child component tree |
| Class/interface definitions | Regex: `class \w+` | Full class structure, inheritance, methods |
| Architecture layering | Says "flat" for everything | Import graph reveals UI → lib → api → db direction |
| Route handlers | Lists route files | Parse route files: HTTP methods, middleware, response patterns |
| Convention inference | Counts kebab/camel filenames | Variable naming, function patterns, abstraction levels |

### What Still Needs Cursor AI (After AST)

| Capability | Why AST Isn't Enough |
|-----------|---------------------|
| Domain model understanding | AST sees `interface User { role: string }` but can't explain business meaning |
| Architecture rationale | Knows dependency direction, not WHY that pattern was chosen |
| Security posture assessment | Sees middleware exists, can't judge sufficiency |
| Convention judgment | Detects patterns, can't distinguish intentional vs accidental |
| Business logic quality | Parses structure, can't evaluate logic |

### Projected Impact

| Metric | Current | + AST | + AST + Cursor |
|--------|---------|-------|---------------|
| Analysis Accuracy | 6/10 | 8/10 | 9/10 |
| Analysis Completeness | 5/10 (30%) | 7/10 (55%) | 9/10 (80%+) |
| Zone Accuracy | 4/10 | 7/10 | 8/10 |
| Rule Relevance | 5/10 | 6.5/10 | 8/10 |
| **Overall Score** | **6.3/10** | **7.5/10** | **8.5/10** |

---

## Part 3: Market Research

### Landscape Overview

We analyzed 80+ tools across 7 categories. The market is polarized: tools are either fully LLM-based (require API keys) or purely template/heuristic-based. Very few combine both. No tool generates role-scoped multi-layer governance.

### Category 1: Cursor Rules Generators

| Tool | Stars | Method | Uses LLM | Multi-Tool |
|------|-------|--------|----------|------------|
| awesome-cursorrules | 38,677 | Curated collection | No | Cursor |
| claude-code-templates | 23,558 | Interactive CLI installer | No | Claude Code |
| steipete/agent-rules | 5,650 | Curated collection | No | Multi |
| Ruler | 2,591 | Declarative distribution (.ruler/) | No | 15+ agents |
| dotai (udecode) | 1,141 | Shell sync | No | Multi |
| Rulesync | 934 | Format conversion between tools | No | 21+ tools |
| rulebook-ai | 581 | Pack-based universal format | No | 10+ tools |
| ClaudeForge | 324 | LLM analysis + scoring | Yes | Claude Code |
| ai-rules-builder | 251 | Visual web builder + MCP | No | 3 tools |
| CursorFocus | 170 | Heuristic scanning (like ours) | No | Cursor |
| claude-rules | 140 | Heuristic detection + curated rules | No | Multi |
| AgentRules Architect | 110 | LLM 6-phase pipeline | Yes (multi) | Multi |
| PRPM | 101 | Package manager for AI rules | No | 9+ tools |
| ai-rulez | 95 | YAML compiler + AI enforcement | Optional | 18+ tools |
| Caliber | 92 | Heuristic + LLM hybrid | Yes | Multi |
| block/ai-rules | 83 | Declarative distribution (Block/Square) | No | 11 agents |
| Rulefy | 27 | LLM analysis (Claude) | Yes | Cursor |
| cc-rig | 22 | Template presets | No | Claude Code |

**Built-in IDE features:**
- Cursor `/Generate Cursor Rules` (v0.49+) — LLM-based, built into Cursor
- Claude Code `/init` — LLM-based CLAUDE.md generation

**Web generators:**
- cursor.directory (75k+ devs), Agent Rules Builder (agentrulegen.com), CursorRules.org, cursorrules.top, CursorPractice, agnt.one — all template or AI-based web tools

**Self-improving pattern:** SashiDo approach — meta-rule tells Cursor to evolve rules over time

### Category 2: AI Code Analysis Platforms

| Tool | Approach | Generates Rules? | Pricing | Relevance |
|------|----------|-----------------|---------|-----------|
| CodeScene | Behavioral + static + ML | Yes (quality gates) | Subscription | HIGH |
| SonarQube | Static + LLM (Agentic Analysis) | Yes (quality gates) | Free OSS + paid | MEDIUM-HIGH |
| Greptile | Semantic graph + LLM | Yes (custom rules) | $30/dev/month | HIGH |
| Qodo | Multi-agent LLM (15+ agents) | Yes (rulesets) | Free + $30/user | VERY HIGH |
| Semgrep | Rule DSL + LLM (Multimodal) | Yes (rule registry) | Free OSS + paid | HIGH |
| Sourcegraph | Cross-repo index + LLM | Partial | $59/user/month | MEDIUM-HIGH |
| Codacy | Static + AI coaching | Yes (merge gates) | Free + $18/month | MEDIUM |
| CodeAnt AI | AI + static + custom rules | Yes | $10-20/user/month | MEDIUM-HIGH |
| Ellipsis AI | LLM + auto-fix | Yes (style guides) | $20/user/month | HIGH |
| SIG Sigrid | Static + benchmark + private LLM | Yes (governance) | Enterprise | HIGH |
| ai-doc-gen (Divar) | Multi-agent LLM → .cursor/rules | Yes | Open source (702 stars) | VERY HIGH |
| Codegraph (optave) | AST + semantic, fully local | Yes (boundaries) | Open source | VERY HIGH |

### Category 3: Codebase-to-Context Tools

| Tool | Approach | No API Keys? | Relevance |
|------|----------|-------------|-----------|
| Repomix | Tree-sitter compression + MCP | Yes | HIGH |
| Code2Prompt | Rust CLI + Handlebars + MCP | Yes | HIGH |
| GitIngest | Web tool (replace hub→ingest) | Yes | MEDIUM |
| Yek | Rust, priority-ordered (230x faster) | Yes | MEDIUM |
| CTX | "Context as Code" YAML config + MCP | Yes | HIGH |

### Category 4: AST / Graph-Based Intelligence

| Tool | Approach | No API Keys? | Relevance |
|------|----------|-------------|-----------|
| ast-grep | Tree-sitter structural search + lint | Yes | VERY HIGH |
| Axon | Graph-powered intelligence + MCP | Yes | VERY HIGH |
| CodePrism | Universal AST + 19 MCP tools | Yes | VERY HIGH |
| Code-Graph-RAG | Tree-sitter + knowledge graph | Partial | HIGH |
| FalkorDB Code Graph | Graph DB + GraphRAG | Partial | MEDIUM |
| Tree-sitter MCP Server | Direct AST access for AI | Yes | HIGH |

### Category 5: AI Coding Assistants (Context Engines)

| Tool | Approach | Key Feature |
|------|----------|------------|
| Cursor Indexing | AST chunking + embeddings + Merkle tree | Built-in @codebase queries |
| Aider | Tree-sitter repo map + graph ranking | .aider.conventions file |
| Continue.dev | Local embeddings (transformers.js) | @repo-map context provider |
| Augment Code | 400K+ file context engine | Cross-repo intelligence |
| Tabnine | Vector + graph + agentic retrieval | Org-native agents |

### Category 6: Code Review with Governance

| Tool | Key Feature | Relevance |
|------|------------|-----------|
| CodeRabbit | Custom review rules, 2M+ repos | MEDIUM |
| Panto AI | Architectural rule enforcement | MEDIUM-HIGH |
| Bito AI | Configurable rules + Confluence validation | MEDIUM-HIGH |
| Claude Code Review | Multi-agent, convention compliance | MEDIUM-HIGH |
| GitHub Copilot Review | 60M reviews, agentic architecture | MEDIUM |
| Snyk DeepCode | Symbolic + generative AI, data flow | MEDIUM |

### Category 7: Multi-Agent Sync / Distribution

| Tool | Stars | Tools Supported |
|------|-------|----------------|
| Ruler | 2,591 | 15+ agents |
| dotai | 1,141 | Multi |
| Rulesync | 934 | 21+ tools |
| rulebook-ai | 581 | 10+ tools |
| ai-rulez | 95 | 18+ tools |
| block/ai-rules | 83 | 11 agents |
| Saddle | — | 6+ tools |

### Key Market Insights

1. **No one generates role-scoped governance.** Our unique differentiator — 5 roles × 3 enforcement layers (rules + hooks + permissions) — has no competitor.

2. **Tree-sitter + MCP is the emerging standard.** Used by Cursor itself, Aider, ast-grep, Axon, CodePrism, Repomix, Continue.dev. Fully local, zero API keys.

3. **The market is converging on hybrid (deterministic + AI).** Semgrep Multimodal and SonarQube Agentic Analysis both launched hybrid models in March 2026. Our heuristic + Cursor-assisted model aligns with this trend.

4. **Closest competitors:**
   - ai-doc-gen — generates .cursor/rules via multi-agent LLM (requires API keys)
   - Codegraph — fully local AST + MCP, generates architecture boundaries (no governance layers)
   - Caliber — heuristic fingerprint + LLM generation (requires API keys)
   - CursorFocus — heuristic scanning like ours (no governance, no roles)

5. **Cursor's built-in `/Generate Cursor Rules` is NOT a competitor.** It generates .mdc files for one developer. It does NOT generate hooks.json, cli.json, scopes.yaml, onboarding guides, review checklists, role-based access, drift detection, metrics, or bulk analysis.

---

## Part 4: Strategic Recommendations

### Approved Strategy: Three-Layer Intelligence Model

```
Layer 1: Heuristics (keep + fix) → WHAT exists
Layer 2: Tree-sitter AST (add)   → HOW code is structured
Layer 3: Cursor AI (add)         → WHY patterns exist
```

**Enterprise constraint:** Users have Cursor but no LLM API access. All intelligence must come from offline tools (heuristics, AST) or Cursor's native AI interface.

**Why NOT MCP:** The CLI already generates .cursor/rules/ files that Cursor reads natively. The webapp already provides a UI. Adding an MCP server would add integration complexity for zero user benefit. The existing CLI + Cursor workflow is sufficient.

### Layer 1: Heuristics (Fix Existing)

**What to fix (no new infrastructure):**

| Fix | Files | Impact |
|-----|-------|--------|
| Zone detection path-matching bug | `generators/scopes.py` | Unlocks 4+ missing zones |
| BaaS mappings (Supabase→PostgreSQL) | `analyzers/database.py` | Fills database dimension |
| shadcn component library detection | `analyzers/design.py` | Fills design_ui dimension |
| Filter blocked commands by tech stack | `profiles/base.py` | Eliminates irrelevant governance |
| Fix testing.mdc numbering | `templates/testing.mdc.j2` | Correct rule numbering |
| Wire overrides.yaml into pipeline | `config.py`, `cli.py` | User-correctable analysis |

### Layer 2: Tree-sitter AST (Add)

**What Tree-sitter enables:**

| New Capability | Analyzer Impact |
|---------------|----------------|
| Import/dependency graph | architecture, structure — real module boundaries instead of "flat" |
| Function signature extraction | api — actual route handlers, middleware chains |
| Component tree analysis | frontend_patterns — parent-child composition |
| Class/interface parsing | domain model — entity relationships, types |
| Naming pattern analysis | conventions — real variable/function naming conventions |
| Export analysis | structure — what modules expose, public API surface |

**Implementation approach:** Add `tree_sitter` as optional dependency. Create `src/product_builders/ast/` module with language-specific parsers. Each analyzer can optionally call AST methods when available for deeper analysis.

**Languages to support first:** TypeScript/JavaScript (most common frontend), Python (our own stack).

### Layer 3: Cursor AI (Add via Smart Bootstrap Prompts)

**The workflow:**

```
1. User runs: product-builders analyze <name>
   → Heuristics + AST fill what they can (~55-60% fields)
   → Generates smart bootstrap-meta-rule.mdc
     that knows EXACTLY what's missing

2. User opens repo in Cursor
   → Bootstrap rule activates automatically
   → Tells Cursor: "Analyze these specific gaps:
      - What's the architecture layering pattern?
      - What domain entities exist and how do they relate?
      - What implicit conventions does the team follow?"
   → Cursor outputs structured YAML blocks

3. User runs: product-builders enrich <name>
   → Ingests Cursor's YAML output
   → Validates against schema
   → Merges into analysis.json (now 80%+ fields)
   → Regenerates all rules with richer data
```

**Key improvement over current bootstrap meta-rule:** Current prompts are generic (same for every project). Smart prompts are gap-aware — they only ask about what's missing, with project-specific context from heuristic + AST results.

**Example current prompt:**
> "Analyze the codebase architecture. What layering pattern is used?"

**Example smart prompt:**
> "I detected Next.js 15 App Router with Supabase auth. Import graph shows: src/app/ → src/lib/ → @supabase/supabase-js. 21 routes, 8 API handlers. The heuristic couldn't determine: (1) Is src/lib/ a service layer or utility collection? (2) What RLS policies exist in supabase/migrations/? (3) Are Server Components and Client Components intentionally separated? Output findings as YAML matching this schema: [structured template]"

---

## Part 5: Our Differentiators

### What no competitor offers

| Capability | Product Builders | Closest Competitor | Gap |
|-----------|-----------------|-------------------|-----|
| Role-scoped rules (5 roles) | Yes | None | No competitor |
| Three governance layers (rules + hooks + permissions) | Yes | None | No competitor |
| Zone-based access control (scopes.yaml) | Yes | Codegraph (boundaries only) | We add role mapping |
| Onboarding guides per role | Yes | None | No competitor |
| Review checklists from analysis | Yes | CodeRabbit (manual rules) | We auto-generate |
| Bulk analysis across repos | Yes | Caliber (similar) | Comparable |
| Drift detection | Yes | Caliber (similar) | Comparable |
| Company standards injection | Yes | Semgrep (rule registry) | Different mechanism |
| Fully offline core (no API keys) | Yes | Codegraph, CursorFocus | Comparable |
| Structured versioned profile (analysis.json) | Yes | None at this level | No competitor |

### Our position in the market

**We are a governance platform, not a rules generator.** The competitive moat is not "we generate .mdc files" (anyone can do that). The moat is:

1. **Structured analysis** — versioned, diffable, auditable analysis.json
2. **Role-based governance** — different rules for different contributors
3. **Three enforcement layers** — soft guidance → smart blocking → hard deny
4. **Enterprise lifecycle** — drift detection, metrics, feedback, bulk operations
5. **Portfolio scale** — analyze and govern dozens of repos from one tool

---

## Appendix: Top 10 Improvement Actions (by ROI)

| Priority | Action | Impact | Effort | Score Impact |
|----------|--------|--------|--------|-------------|
| 1 | Fix zone detection path-matching | Unlocks 4+ missing zones | Low | +1.5 on zones |
| 2 | Add BaaS/framework mappings | Fixes 5+ false negatives | Low | +0.5 on accuracy |
| 3 | Filter blocked commands by tech stack | Eliminates irrelevant governance | Low | +1.0 on relevance |
| 4 | Wire overrides.yaml into pipeline | User-correctable analysis | Medium | +0.5 on DX |
| 5 | Add unit tests for 20 analyzers | Catches bugs, enables refactoring | High | +1.0 on code quality |
| 6 | Add Tree-sitter AST analysis | Real code structure understanding | High | +2.0 on accuracy |
| 7 | Smart bootstrap prompts (gap-aware) | Cursor fills remaining analysis gaps | Medium | +1.5 on completeness |
| 8 | Add `enrich` CLI command | Ingest Cursor's deep analysis output | Medium | +1.0 on completeness |
| 9 | Fix testing.mdc template numbering | Correct rule output | Low | +0.2 on quality |
| 10 | Add --dry-run and diff commands | Better DX for rule regeneration | Low | +0.5 on DX |

**Implementing items 1-4 (all low/medium effort) would lift the score from 6.3 to ~7.2/10.**
**Adding items 5-8 (AST + smart prompts) would lift it to ~8.5/10.**

---

## References

### Rules Generator Tools
- [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) (38.7k stars)
- [claude-code-templates](https://github.com/davila7/claude-code-templates) (23.5k stars)
- [steipete/agent-rules](https://github.com/steipete/agent-rules) (5.6k stars)
- [Ruler](https://github.com/intellectronica/ruler) (2.6k stars)
- [dotai](https://github.com/udecode/dotai) (1.1k stars)
- [Rulesync](https://github.com/dyoshikawa/rulesync) (934 stars)
- [rulebook-ai](https://github.com/botingw/rulebook-ai) (581 stars)
- [ClaudeForge](https://github.com/alirezarezvani/ClaudeForge) (324 stars)
- [ai-rules-builder](https://github.com/przeprogramowani/ai-rules-builder) (251 stars)
- [CursorFocus](https://github.com/RenjiYuusei/CursorFocus) (170 stars)
- [claude-rules](https://github.com/lifedever/claude-rules) (140 stars)
- [AgentRules Architect](https://github.com/trevor-nichols/agentrules-architect) (110 stars)
- [Caliber](https://github.com/caliber-ai-org/ai-setup) (92 stars)
- [cursor.directory](https://cursor.directory/generate)

### AI Code Analysis
- [Codegraph](https://github.com/optave/codegraph) — AST + MCP, open source
- [ai-doc-gen](https://github.com/divar-ir/ai-doc-gen) (702 stars) — Multi-agent → .cursor/rules
- [Qodo](https://www.qodo.ai) — Multi-agent code review with rulesets
- [Semgrep](https://semgrep.dev) — Rule DSL + Multimodal AI
- [Greptile](https://www.greptile.com) — Semantic graph code review
- [CodeScene](https://codescene.com) — Behavioral code analysis
- [Ellipsis AI](https://www.ellipsis.dev) — Natural language style guide enforcement

### AST / Graph Intelligence
- [ast-grep](https://github.com/ast-grep/ast-grep) — Tree-sitter structural search
- [Axon](https://github.com/harshkedia177/axon) — Graph intelligence + MCP
- [CodePrism](https://github.com/rustic-ai/codeprism) — Universal AST + 19 MCP tools
- [Repomix](https://github.com/yamadashy/repomix) (52k stars) — Tree-sitter compression + MCP
- [Code2Prompt](https://github.com/mufeedvh/code2prompt) — Rust CLI + MCP
- [Aider](https://aider.chat) — Tree-sitter repo map + conventions
- [Continue.dev](https://docs.continue.dev) — Local embeddings + repo-map

### Self-Improving Patterns
- [SashiDo Self-Improving Cursor Rules](https://www.sashido.io/en/blog/cursor-self-improving-rules)
- [AGENTS.md Standard](https://agents.md) — Linux Foundation cross-agent standard
