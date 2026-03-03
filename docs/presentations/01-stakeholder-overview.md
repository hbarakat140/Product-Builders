---
marp: true
theme: default
paginate: true
header: "Product Builders"
footer: "Confidential — March 2026"
---

<!-- _class: lead -->

# Product Builders

### Enabling Product Teams to Contribute Code Safely via AI

March 2026

---

# The Challenge

- **50+ products** across React, Java Spring, Python Django, .NET, and more
- **Product managers, designers, and QA** want to contribute features — not just spec them
- **Cursor AI** can generate code, but it doesn't know each product's architecture, conventions, or safety rules
- Without guardrails, AI-generated code **breaks CI, violates patterns, and introduces risk**

**Goal:** Let non-engineers contribute production code via AI — safely, at scale.

---

# What Happens Today

| Without Product Builders | With Product Builders |
|---|---|
| PM asks AI for a feature | PM asks AI for a feature |
| AI generates generic code | AI generates **product-compatible** code |
| Code fails CI, uses wrong patterns | Code follows existing patterns |
| Engineer rewrites it from scratch | Engineer reviews and approves |
| PM gives up after 2 attempts | PM ships features independently |

**Success metric:** PM-authored PRs pass CI and AI review on first attempt at **80%+ rate**

---

# What We're Building

Two deliverables:

### 1. CLI Tool (Python)
- Analyzes any product codebase automatically
- Generates tailored AI rules, safety hooks, and permissions
- One-time setup per product (~15 min)

### 2. Web Application
- Documentation and getting-started guides
- Per-role onboarding (PM, Designer, Engineer, QA)
- Product catalog and CLI distribution

**No external AI APIs needed** — uses Cursor itself for deep analysis.

---

# How It Works — The Big Picture

```
                    ┌─────────────────────────────┐
                    │     Product Codebase         │
                    │  (React, Java, Python, etc.) │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │   Product Builders CLI       │
                    │   Analyzes 18 dimensions:    │
                    │   tech stack, database,      │
                    │   auth, conventions, etc.    │
                    └──────────┬──────────────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
     ┌────────────┐   ┌──────────────┐  ┌───────────┐
     │  14 AI     │   │  Safety      │  │ Onboarding│
     │  Rule      │   │  Hooks &     │  │ Guide     │
     │  Files     │   │  Permissions │  │           │
     └────────────┘   └──────────────┘  └───────────┘
```

Analyze once → Generate rules → Every contributor benefits.

---

# The PM Experience

### Getting Started (one-time, 5 minutes)

1. Clone the product repo
2. Run `product-builders setup --profile pm`
3. Open Cursor — **done.** Rules and safety auto-load.

### Day-to-Day

PM opens Cursor and says: *"Add user preferences feature"*

The AI **already knows:**
- Which framework and components to use
- Which files the PM can touch
- Which patterns to follow
- When to redirect to engineering

---

# Safety: Defense in Depth

Three layers ensure AI-generated code stays within bounds:

### Layer 1 — Rules (Soft Guidance)
AI is told the contributor's scope and the product's patterns.
*"You may only modify files in `src/components/`"*

### Layer 2 — Hooks (Smart Blocking)
If AI tries to edit a restricted file, it's blocked with a helpful message.
*"This is a database migration. Want me to create a Jira issue instead?"*

### Layer 3 — Permissions (Hard Deny)
Physical filesystem restrictions. Even if Layers 1-2 fail, the AI **cannot** access restricted paths.

---

# Graceful Boundaries — Not Brick Walls

When a PM asks for something outside their scope, the AI **redirects helpfully**:

> **PM:** "Add a new database table for user preferences"
>
> **AI:** "Database schema changes need engineering involvement.
> I can help you:
> 1. Draft a Jira issue describing the table you need
> 2. Build the frontend that will USE the preferences once the table exists
>
> Which would you like?"

The AI is **a collaborator, not a gatekeeper.**

---

# Five Contributor Profiles

| Profile | Can Write | Read-Only | Blocked |
|---|---|---|---|
| **Engineer** | Everything | — | — |
| **Technical PM** | Frontend + API | Backend, Tests | DB, Infra, Security |
| **Product Manager** | Frontend only | API, Backend | DB, Infra, Security |
| **Designer** | UI components only | Frontend logic | Everything else |
| **QA / Tester** | Tests only | All code | DB, Infra, Security |

Each product team **customizes** these defaults via a simple `scopes.yaml` file.

---

# What the AI Learns About Each Product

**18 analysis dimensions** — everything that causes AI code to break:

| Critical | High Impact | Medium Impact |
|---|---|---|
| Tech stack | Dependencies | Project structure |
| Database & ORM | Error handling | Conventions |
| Auth patterns | i18n/l10n | Security patterns |
| | State management | Testing |
| | Environment & config | CI/CD, Design/UI |
| | Git workflow | API, Accessibility |
| | | Performance |

Plus **deep analysis** via Cursor: architecture, domain model, implicit conventions.

---

# Rollout Strategy

### Phase 1-3: Build + Pilot (first deliverable)
- CLI foundation + 8 core analyzers + rule generation + governance
- Pilot with **2-3 selected products**
- Validate with real PMs and designers

### Phase 4: Scale
- Remaining 10 analyzers (security, testing, CI/CD, design system, etc.)
- Roll out to more products

### Phase 5: Automation
- Automated drift detection (are rules still accurate?)
- Lifecycle management at scale for 50+ products
- Metrics and observability

**Build for scale, test with pilot first.**

---

# Long-Term Vision

Today: **CLI + Web App** (local rules, per-product setup)

Tomorrow: **MCP-Native Platform**

- **Zero-friction onboarding** — no local setup; connect to server and work
- **Multi-IDE support** — same rules for Cursor, Claude Code, Windsurf
- **Centralized governance** — profiles managed server-side
- **Real-time rule updates** — change a rule, every session picks it up
- **Analytics** — adoption metrics, PR pass rates, rule effectiveness

The current architecture **evolves** toward this — no rewrite needed.

---

# What We Need From You

### Decisions That Need Stakeholder Input

| # | Decision | Impact | When |
|---|---|---|---|
| **DP-3** | Which 2-3 products to pilot? | Determines priority | Before pilot |
| **DP-4** | Pilot timeline and success criteria | Planning | Before pilot |
| **DP-7** | Design system integration strategy | DS adoption | Phase 4 |
| **DP-8** | PM support model (Slack, buddy, office hours?) | Adoption risk | Before pilot |

### Decisions That Are Engineering-Internal

DP-1 (shared libraries), DP-2 (AI review tool), DP-5 (zone definitions), DP-6 (Cursor Enterprise), DP-9 (staleness thresholds) — covered in the engineering workshop.

---

# Ideal Pilot Composition

We recommend **3 products** representing different complexity levels:

| Pilot Product | Characteristics | What It Validates |
|---|---|---|
| **Product A** | Simple frontend-only (React) | PM can ship UI changes end-to-end |
| **Product B** | Full-stack with database | Governance layers block unsafe operations |
| **Product C** | Uses shared design system | DS rules produce consistent UI code |

**Pilot duration:** 4-6 weeks with 2-3 PMs per product.

---

# Risk Management

| Risk | Mitigation |
|---|---|
| PM adoption lower than expected | Guided first contribution, buddy system, low-risk starting tasks |
| AI-generated code doesn't meet 80% target | Rule validation, deep analysis review, feedback loop |
| Engineer resistance to PM-authored PRs | Pilot retrospective, executive sponsorship |
| Rules become stale after product updates | Automated drift detection, CI integration |
| Cursor API changes break hooks | Version compatibility layer, regression tests |

---

# Why This Matters

- **Reduces engineering bottleneck** for product-led features
- **Accelerates time-to-market** for UI/UX improvements
- **Scales contribution** without proportional engineering headcount
- **Maintains code quality** — AI follows the same patterns engineers use
- **No new infrastructure** — uses tools teams already have

> 50+ products. Dozens of contributors. One system to make it safe.

---

# Next Steps

1. **Select pilot products** (DP-3) — need 2-3 candidates
2. **Define pilot timeline** (DP-4) — start date, duration, success criteria
3. **Identify pilot PMs** — who will participate?
4. **Define support model** (DP-8) — Slack channel, buddy, office hours?
5. **Engineering kickoff** — Phase 1 implementation begins

### Ready to discuss?

---

<!-- _class: lead -->

# Appendix

---

# No Cursor Enterprise Required

All governance uses **project-level files** committed to each repo:
- `.cursor/rules/` — AI rule files
- `.cursor/hooks.json` — safety hooks
- `.cursor/cli.json` — filesystem permissions

If Cursor Enterprise becomes available later, it's **additive** (enforced team rules, audit logs, sandbox mode) — not required.

---

# Zero External Dependencies

| Component | Runs on |
|---|---|
| Heuristic analysis (18 analyzers) | Fully local/offline |
| Deep analysis | Cursor itself (no API keys) |
| Rule generation | Local templates (Jinja2) |
| Safety hooks | Local scripts |

**No LLM API keys. No new infrastructure. No additional cost.**

The only requirement is Cursor, which teams already use.
