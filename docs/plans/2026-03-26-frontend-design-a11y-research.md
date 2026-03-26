# Frontend, Design Systems & Accessibility Research

Deep research for Product Builders static code analysis tool. Everything here is detectable OFFLINE by scanning repository files, `package.json` dependencies, config files, directory structures, and source code patterns.

---

## 1. Design System Detection Checklist

### 1.1 Component Libraries to Detect

**Currently detected** (in `design.py`): Material UI, Ant Design, Chakra UI, Mantine, PrimeReact, PrimeVue, Radix UI, Headless UI, Vuetify, Quasar, Bootstrap, React Bootstrap, shadcn, Base UI, NextUI, Park UI, DaisyUI.

**Missing -- should add:**

| Library | Package Name(s) | Notes |
|---------|-----------------|-------|
| Ark UI | `@ark-ui/react`, `@ark-ui/vue`, `@ark-ui/solid`, `@ark-ui/svelte` | Headless, built on Zag.js. Cross-framework (React/Vue/Solid/Svelte). 45+ accessible components. |
| React Aria | `react-aria`, `react-aria-components`, `@react-aria/*` | Adobe headless library. Growing fast in 2025. |
| Flowbite | `flowbite`, `flowbite-react`, `flowbite-vue`, `flowbite-svelte` | Tailwind component library. Cross-framework. |
| HeroUI (formerly NextUI) | `@heroui/react` | NextUI was renamed to HeroUI. Detect both. |
| Agnostic UI | `agnostic-react`, `agnostic-vue`, `agnostic-svelte`, `agnostic-angular` | Framework-agnostic. |
| Skeleton | `@skeletonlabs/skeleton` | Svelte + Tailwind component library. |
| Element Plus | `element-plus` | Vue 3 component library. |
| Naive UI | `naive-ui` | Vue 3 component library. |
| Vuetify 3 | `vuetify` | Already detected, but note v3 shift. |
| Angular Material | `@angular/material` | Angular ecosystem standard. |
| Angular CDK | `@angular/cdk` | Headless primitives for Angular. |
| PrimeNG | `primeng` | Angular component library. |
| Svelte Headless UI | `svelte-headless-ui` | Svelte equivalent of Headless UI. |
| Kobalte | `@kobalte/core` | SolidJS headless component library. |
| Corvu | `corvu` | SolidJS headless UI primitives. |

### 1.2 CSS Approaches to Detect

**Currently detected**: Tailwind, styled-components, Emotion, Sass/SCSS, Less, CSS Modules (via file scan).

**Missing -- should add:**

| Approach | Package/Config | Detection Method |
|----------|---------------|------------------|
| Vanilla Extract | `@vanilla-extract/css` | package.json dependency |
| Panda CSS | `@pandacss/dev` | package.json or `panda.config.ts`/`panda.config.js` |
| StyleX | `@stylexjs/stylex` | package.json dependency |
| UnoCSS | `unocss` | package.json or `uno.config.ts`/`uno.config.js` |
| Linaria | `@linaria/core` | package.json dependency (zero-runtime) |
| CSS-in-JS (generic) | `goober` | Tiny CSS-in-JS alternative |
| PostCSS | `postcss` | `postcss.config.js`/`.postcssrc` config files |
| Lightning CSS | `lightningcss` | package.json dependency |
| Tailwind v4 | No config file needed | Detect via `@import "tailwindcss"` in CSS files (v4 has no config file) |
| Stitches | `@stitches/react` | package.json (declining but still in production) |

**Key trend**: Tailwind CSS dominates with 68% adoption in new projects. styled-components is declining (7% of new projects). Zero-runtime CSS-in-JS (Vanilla Extract, Panda CSS, StyleX) is the emerging alternative. Detection should flag styled-components as "legacy" in new projects.

### 1.3 Design Token Formats to Detect

**Currently detected**: JSON tokens, YAML tokens, SCSS tokens, CSS custom properties files.

**Missing -- should add:**

| Format | Detection | Notes |
|--------|-----------|-------|
| W3C DTCG Format | Files with `$type` and `$value` keys in JSON | First stable spec published Oct 2025 (2025.10). Look for `$type`, `$value`, `$description` in `.json`/`.tokens.json` files. |
| Style Dictionary config | `config.json` or `style-dictionary.config.js` with token references | style-dictionary package in deps + config file |
| Figma Tokens (Tokens Studio) | `tokens.json` with `$themes` key, or `tokens/` directory with `*.tokens.json` | Tokens Studio plugin exports |
| Theme UI | `theme.ts`/`theme.js` with token-like structure | `theme-ui` in package.json |
| Tailwind config as tokens | `tailwind.config.ts` `theme.extend` section | Tailwind config IS the token source for many teams |
| CSS custom properties | `:root { --color-*` patterns in `.css` files | Scan for `--` prefix variables in `:root` |
| Design Tokens as TypeScript | `tokens.ts` / `theme.ts` exporting typed objects | Common in shadcn/Mantine setups |

### 1.4 Icon Libraries to Detect

**Not currently detected at all. NEW dimension data.**

| Library | Package Name(s) | Notes |
|---------|-----------------|-------|
| Lucide | `lucide-react`, `lucide-vue-next`, `lucide-svelte`, `lucide-angular` | 1,450+ icons. Default for shadcn/ui. |
| Heroicons | `@heroicons/react`, `heroicons` | By Tailwind team. 316 icons in 4 styles. |
| Phosphor | `@phosphor-icons/react`, `phosphor-react` | 6 weight options. Flexible hierarchy. |
| Tabler Icons | `@tabler/icons-react`, `@tabler/icons-vue`, `@tabler/icons-svelte` | 5,600+ icons. |
| Feather Icons | `feather-icons`, `react-feather` | Lucide is the maintained fork. |
| Material Icons | `@mui/icons-material`, `material-icons` | Google Material icons. |
| FontAwesome | `@fortawesome/fontawesome-free`, `@fortawesome/react-fontawesome` | Legacy standard. |
| React Icons | `react-icons` | Meta-package wrapping multiple icon sets. |
| Iconify | `@iconify/react`, `@iconify/vue` | Universal icon framework. 200,000+ icons. |
| Hugeicons | `hugeicons-react` | 4,000+ icons. Growing in 2025. |

### 1.5 Component Documentation Tools to Detect

**Not currently detected. NEW dimension data.**

| Tool | Package/Config | Detection |
|------|---------------|-----------|
| Storybook | `@storybook/react`, `@storybook/vue3`, `.storybook/` directory | package.json deps OR `.storybook/main.js` config dir |
| Histoire | `histoire` | package.json + `histoire.config.ts` |
| Ladle | `@ladle/react` | package.json dependency. Vite-native, same story format as Storybook. |
| Docusaurus | `@docusaurus/core` | package.json + `docusaurus.config.js` |
| Styleguidist | `react-styleguidist` | package.json + `styleguide.config.js` |
| Nextra | `nextra`, `nextra-theme-docs` | package.json (Next.js-based docs) |
| VitePress | `vitepress` | package.json (Vue-based docs) |
| Chromatic | `chromatic` | Visual regression testing for Storybook |

### 1.6 Font Optimization to Detect

**Not currently detected. NEW dimension data.**

| Pattern | Detection Method | Notes |
|---------|-----------------|-------|
| next/font | `import { Inter } from 'next/font/google'` or `next/font/local` in source | Auto self-hosts, zero layout shift. Best practice for Next.js. |
| @fontsource | `@fontsource/*` packages in deps | Self-hosted fonts via npm. |
| font-display: swap | `font-display: swap` in CSS files | Prevents FOIT (Flash of Invisible Text). |
| Variable fonts | `.woff2` files with "variable" in name, or `font-variation-settings` in CSS | Single file, multiple weights. Performance win. |
| Google Fonts link tag | `fonts.googleapis.com` in HTML/index files | Legacy approach -- flag as improvable if next/font available. |
| Typekit/Adobe Fonts | `use.typekit.net` in HTML files | Commercial font service. |
| Font subsetting | `unicode-range` in CSS or `glyphhanger` in deps | Advanced optimization. |

---

## 2. Accessibility Detection Checklist

### 2.1 WCAG 2.2 Requirements Detectable Statically

Of 9 new WCAG 2.2 success criteria, only one (2.5.8 Target Size Minimum) is reliably automatable. However, many WCAG 2.0/2.1 criteria ARE statically detectable:

**Statically detectable via source code scan:**

| WCAG SC | Name | What to detect | How |
|---------|------|---------------|-----|
| 1.1.1 | Non-text Content | `<img>` without `alt`, `<svg>` without `aria-label`/`aria-labelledby` | Scan JSX/HTML for img tags missing alt |
| 1.3.1 | Info and Relationships | `<input>` without associated `<label>`, `<fieldset>` without `<legend>` | Scan for orphaned inputs, missing htmlFor/for |
| 1.3.2 | Meaningful Sequence | `tabIndex` > 0 (anti-pattern) | Scan for `tabIndex={n}` where n > 0 |
| 1.3.5 | Identify Input Purpose | `autocomplete` attribute on form inputs | Check for `autocomplete` on login/address forms |
| 1.4.3 | Contrast (Minimum) | Contrast checking tools in deps | Detect axe-core, pa11y, color contrast plugins |
| 2.1.1 | Keyboard | `onClick` without `onKeyDown`/`onKeyPress` on non-interactive elements | Scan for click handlers on `<div>`, `<span>` without keyboard handlers |
| 2.4.1 | Bypass Blocks | Skip links in layout/root component | Scan for "skip to content" or "skip to main" links |
| 2.4.2 | Page Titled | `<title>` or `document.title` or `Head > title` | Scan for title management per page/route |
| 2.4.4 | Link Purpose | `<a>` with only icon children (no text, no aria-label) | Scan for links with only `<img>`/`<svg>` children |
| 2.4.6 | Headings and Labels | Heading hierarchy (h1 -> h2 -> h3 without skipping) | Scan for heading level skips |
| 2.5.8 | Target Size (Minimum) | CSS min-height/min-width on interactive elements | Scan for click targets < 24x24px |
| 3.3.1 | Error Identification | `aria-invalid`, `aria-errormessage`, error message associations | Scan form components for error state handling |
| 3.3.2 | Labels or Instructions | `<label>` for every `<input>`, `aria-label` for icon buttons | Scan for unlabeled form controls |
| 4.1.2 | Name, Role, Value | Custom components with `role` and `aria-*` attributes | Scan for interactive custom elements lacking ARIA |

### 2.2 A11y Testing Tools (expand current detection)

**Currently detected** (in `accessibility.py`): axe-core, @axe-core/react, jest-axe, react-axe, pa11y, lighthouse, @testing-library/jest-dom, eslint-plugin-jsx-a11y, vue-axe.

**Missing -- should add:**

| Tool | Package Name | Category |
|------|-------------|----------|
| Playwright a11y | `@axe-core/playwright` | E2E accessibility testing |
| Cypress a11y | `cypress-axe` | E2E accessibility testing |
| Storybook a11y addon | `@storybook/addon-a11y` | Component-level a11y testing |
| eslint-plugin-vuejs-a11y | `eslint-plugin-vuejs-accessibility` | Vue static a11y linting |
| Angular ESLint a11y | `@angular-eslint/template-accessibility` | Angular static a11y linting |
| WAVE API | `@wave/api` | Automated WAVE scanning |
| react-aria | `react-aria`, `react-aria-components` | Accessible primitives (implies a11y focus) |
| Radix UI | `@radix-ui/*` | Built-in ARIA (implies a11y focus) |
| Ark UI | `@ark-ui/*` | WAI-ARIA baked in |
| vitest-axe | `vitest-axe` | Vitest accessibility matcher |

### 2.3 ARIA Patterns to Verify

**Currently detected**: Simple boolean -- "does `aria-` or `role=` appear in code?"

**Should expand to detect specific patterns:**

| Pattern | What to scan for | Significance |
|---------|-----------------|--------------|
| Landmark roles | `<nav>`, `<main>`, `<aside>`, `<header>`, `<footer>`, `role="navigation"`, `role="main"`, `role="complementary"`, `role="banner"`, `role="contentinfo"` | Page structure for screen readers |
| Live regions | `aria-live="polite"`, `aria-live="assertive"`, `role="alert"`, `role="status"`, `role="log"` | Dynamic content announcements |
| Dialog/modal | `role="dialog"`, `role="alertdialog"`, `aria-modal="true"` | Modal accessibility |
| Tabs | `role="tablist"`, `role="tab"`, `role="tabpanel"` | Tab widget accessibility |
| Combobox/listbox | `role="combobox"`, `role="listbox"`, `role="option"` | Autocomplete/select accessibility |
| Tree view | `role="tree"`, `role="treeitem"` | Hierarchical navigation |
| Disclosure | `aria-expanded`, `aria-controls` | Expandable sections |
| Tooltip | `role="tooltip"`, `aria-describedby` on triggers | Tooltip accessibility |
| Breadcrumb | `aria-label="Breadcrumb"` or `role="navigation"` with breadcrumb context | Navigation context |
| Progress | `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax` | Loading/progress indicators |

**Suggested output field**: `aria_patterns: list[str]` instead of just `aria_usage_detected: bool`.

### 2.4 Form Accessibility Patterns (Critical)

**Not currently detected as a distinct concern. Should add sub-detection within accessibility or frontend_patterns.**

| Pattern | Detection Method | Why Critical |
|---------|-----------------|--------------|
| Label-input association | `<label htmlFor="x">` matching `<input id="x">`, or `<label>` wrapping `<input>` | WCAG 1.3.1, 3.3.2. #1 form a11y issue. |
| `aria-required="true"` or `required` | Scan form inputs for required indicators | Programmatic required field indication |
| `aria-invalid="true"` | Scan form error states for aria-invalid | Error state communication |
| `aria-describedby` for errors | Error messages linked to inputs via aria-describedby | Error message association |
| `aria-errormessage` | Newer ARIA pattern for error messages | WCAG 3.3.1 |
| `<fieldset>` + `<legend>` | Groups of related inputs (radio buttons, checkboxes) | Group labeling |
| Visible error messages | Error text near invalid fields, not just color | WCAG 1.4.1 (not color alone) |
| Submit button presence | `<button type="submit">` or `<input type="submit">` in forms | Form completion |
| Autocomplete attributes | `autocomplete="email"`, `autocomplete="current-password"` etc. | WCAG 1.3.5 |

### 2.5 Focus Management Patterns to Detect

**Currently detected**: Simple boolean `keyboard_navigation` based on `onKeyDown`/`onKeyPress`/`tabIndex`.

**Should expand:**

| Pattern | Detection Method | Notes |
|---------|-----------------|-------|
| Skip links | `"skip to main"`, `"skip to content"`, `"skip-link"` in source | WCAG 2.4.1 Bypass Blocks |
| Focus trap library | `focus-trap`, `focus-trap-react`, `@headlessui/react` (built-in) | Modal focus containment |
| Focus restoration | `useRef` + `focus()` patterns near modal close handlers | Return focus after modal close |
| Focus visible | `focus-visible`, `:focus-visible` in CSS, `outline` styles | WCAG 2.4.7 Focus Visible |
| Tab order management | `tabIndex={-1}` for programmatic focus, `tabIndex={0}` for focusability | Keyboard navigation |
| Roving tabindex | Pattern of `tabIndex={0}` on active item, `tabIndex={-1}` on others | Composite widget keyboard nav |
| Inert attribute | `inert` HTML attribute | Background content during modals |

### 2.6 Color Contrast Tools/Patterns

**Currently detected**: Only eslint-plugin-jsx-a11y presence.

**Should expand:**

| Tool/Pattern | Detection Method |
|-------------|-----------------|
| axe-core contrast rules | `axe-core` in deps (includes contrast checking) |
| Tailwind contrast plugin | `@tailwindcss/typography` or contrast-related Tailwind config |
| CSS custom property contrast tokens | `--color-text-*`, `--color-bg-*` naming patterns (implies token-managed contrast) |
| Dark mode support | `dark:` prefix in Tailwind classes, `prefers-color-scheme` media query, `data-theme` attribute | Implies multi-theme contrast management |
| High contrast mode | `forced-colors` media query, `-ms-high-contrast` | Windows high contrast support |
| Figma contrast checker | Presence in design workflow (not detectable in code, but Storybook a11y addon covers it) |

---

## 3. Frontend Patterns Detection Checklist

### 3.1 Component Patterns

**Not currently detected at all. NEW capability via AST analysis.**

| Pattern | Detection Method | Significance |
|---------|-----------------|--------------|
| Compound components | Components exported together from same module, Context.Provider + useContext pattern | Advanced React pattern, indicates mature codebase |
| Custom hooks | `use[A-Z]*` function exports in `hooks/` directory or `use*.ts` files | Standard React pattern |
| Higher-Order Components | `with[A-Z]*` function exports wrapping components | Legacy pattern, still used for cross-cutting concerns |
| Render props | Props typed as `(args) => ReactNode`, `children` as function | Mostly replaced by hooks but still valid |
| Provider pattern | `*Provider` and `*Context` exports, `createContext` usage | State distribution pattern |
| Container/Presentation | `*Container` + `*View`/`*Presenter` naming pairs | Separation of concerns |
| Atomic Design | Directory structure: `atoms/`, `molecules/`, `organisms/`, `templates/` | Component hierarchy pattern |
| Feature-Sliced Design | Directory structure: `entities/`, `features/`, `shared/`, `widgets/`, `pages/` | Russian-origin architecture pattern |
| Composition pattern | Components accepting `children` and composing them | Modern preferred approach |
| Slot pattern | Named slots (`header`, `footer`, `sidebar` props) | Vue/Svelte native, React via props |

### 3.2 Routing Patterns (Expand Current Detection)

**Currently detected**: Routing library name from package.json.

**Should expand to detect route structure patterns:**

| Pattern | Detection Method | Framework |
|---------|-----------------|-----------|
| Dynamic routes | `[id]`, `[slug]` directory names in `app/` or `pages/` | Next.js, Nuxt, SvelteKit |
| Catch-all routes | `[...slug]`, `[[...slug]]` directory names | Next.js |
| Parallel routes | `@folder` directory names (e.g., `@modal`, `@sidebar`) | Next.js App Router |
| Intercepting routes | `(.)folder`, `(..)folder`, `(...)folder` directory names | Next.js App Router |
| Route groups | `(group)` directory names (parenthesized) | Next.js App Router |
| Named layouts | `layout.tsx`, `layout.vue`, `+layout.svelte` files | Next.js, Nuxt, SvelteKit |
| Loading files | `loading.tsx`, `loading.vue` per route | Next.js App Router |
| Error files | `error.tsx`, `error.vue` per route | Next.js App Router |
| Not-found files | `not-found.tsx` per route | Next.js App Router |
| Template files | `template.tsx` (re-renders on navigation) | Next.js App Router |
| Route params | `:id` or `$id` in route config objects | React Router, Remix |
| Middleware files | `middleware.ts` at project root | Next.js middleware |
| Route guards | `canActivate`, `beforeRouteEnter` patterns | Angular, Vue Router |

### 3.3 Error Handling Patterns (Expand)

**Currently detected**: `ErrorBoundary` or `componentDidCatch` string presence.

**Should expand:**

| Pattern | Detection | Notes |
|---------|-----------|-------|
| Error Boundary component | `ErrorBoundary` in code or `react-error-boundary` in deps | Standard React error handling |
| Suspense boundary | `<Suspense fallback=` in JSX | Async loading boundary |
| Nested error boundaries | Multiple `ErrorBoundary` wrappers at different levels | Granular error isolation |
| Global error handler | `window.onerror`, `window.addEventListener('error'` | Catch-all |
| Unhandled rejection handler | `window.addEventListener('unhandledrejection'` | Promise error catching |
| try/catch in async | `try { await` patterns in components | Imperative error handling |
| Error monitoring | Sentry, Bugsnag, Datadog RUM integration | Production error tracking |
| Fallback UI | Components named `*Fallback`, `*Error`, `*ErrorState` | Error state rendering |
| Next.js error files | `error.tsx`, `global-error.tsx` in app directory | Next.js built-in error handling |

### 3.4 Loading/Skeleton Patterns (Expand)

**Currently detected**: Skeleton, Spinner, Suspense, isLoading strings.

**Should expand:**

| Pattern | Detection | Notes |
|---------|-----------|-------|
| Next.js loading files | `loading.tsx` / `loading.js` in app directory | File-convention loading states |
| Streaming SSR | `<Suspense>` wrapping server components | React 18+ streaming |
| Skeleton libraries | `react-loading-skeleton`, `@mui/material/Skeleton`, `react-content-loader` | Purpose-built skeleton libs |
| Progressive loading | Multiple nested `<Suspense>` boundaries | Cascading loading states |
| Optimistic updates | `useOptimistic` (React 19), `optimisticUpdate` patterns | Instant feedback pattern |
| Placeholder images | `blur` placeholder, `blurDataURL` in Next.js Image | Image loading UX |
| Infinite scroll | `IntersectionObserver`, `react-infinite-scroll-component`, `@tanstack/react-virtual` | List loading pattern |

### 3.5 Animation Libraries (Expand)

**Currently detected**: framer-motion, react-spring, gsap, anime.js, lottie.

**Missing -- should add:**

| Library | Package Name | Notes |
|---------|-------------|-------|
| Motion (new name) | `motion` | Framer Motion was renamed to Motion in 2025. ~32KB gzipped. |
| Motion One | `motion` (same package, but detect `motion/react` imports) | Framework-agnostic animation. |
| AutoAnimate | `@formkit/auto-animate` | Zero-config drop-in animations for lists. |
| React Transition Group | `react-transition-group` | Low-level animation primitives. |
| Rive | `@rive-app/react-canvas` | Interactive animation runtime. |
| Three.js | `three`, `@react-three/fiber` | 3D rendering/animation. |
| View Transitions API | `document.startViewTransition` in source | Native browser API. |
| Svelte transitions | `transition:` directive in `.svelte` files | Svelte built-in. |
| Vue transitions | `<Transition>`, `<TransitionGroup>` in `.vue` files | Vue built-in. |
| FLIP animations | `flip` library or manual FLIP pattern | Performance animation technique. |

### 3.6 Performance Patterns to Detect

**Currently detected** (in `performance.py`): Lazy loading, code splitting, bundle config, image optimization, caching, monitoring.

**Missing React-specific patterns:**

| Pattern | Detection | Notes |
|---------|-----------|-------|
| React.memo | `React.memo(` or `memo(` imports from react | Component memoization |
| useMemo | `useMemo(` usage | Computed value memoization |
| useCallback | `useCallback(` usage | Function memoization |
| React Compiler | `babel-plugin-react-compiler` or `react-compiler-runtime` in deps | Auto-memoization (React 19+) |
| Virtualization libs | Already detected, but expand to `@tanstack/react-virtual`, `react-virtuoso` | Large list rendering |
| Image lazy loading | `loading="lazy"` attribute on images | Native browser lazy loading |
| Intersection Observer | `IntersectionObserver` in source or `react-intersection-observer` in deps | Viewport-based loading |
| Web Workers | `new Worker(` or `comlink` in deps | Off-main-thread computation |
| Service Workers | `serviceWorker.register`, `next-pwa` in deps | Offline caching |
| Bundle analyzer | `@next/bundle-analyzer`, `webpack-bundle-analyzer`, `rollup-plugin-visualizer` | Bundle size awareness |
| Tree shaking config | `sideEffects: false` in package.json | Dead code elimination |
| Font optimization | `next/font` usage or `@fontsource/*` in deps | See Section 1.6 |

**Anti-pattern detection (performance):**

| Anti-Pattern | Detection | Why it matters |
|-------------|-----------|---------------|
| Unnecessary memoization | `useMemo(() => literal)` where literal is constant | Adds overhead without benefit |
| Missing deps in hooks | ESLint `react-hooks/exhaustive-deps` rule not enabled | Stale closures, bugs |
| Inline object props to memoized components | `memo(Comp)` receiving `style={{}}` inline | Defeats memoization |
| Large bundle without splitting | Single entry point, no `dynamic()` or `React.lazy` in large apps | Slow initial load |

---

## 4. User Flow Detection Checklist

### 4.1 Route Patterns to Detect (Expand)

**Currently detected**: Route files counted, page directories found.

**Should detect structural patterns:**

| Pattern | Directory/File Pattern | Framework |
|---------|----------------------|-----------|
| Dynamic segments | `[param]` directories | Next.js/Nuxt/SvelteKit |
| Optional catch-all | `[[...slug]]` directories | Next.js |
| Route groups | `(groupName)` directories | Next.js App Router |
| Parallel routes | `@slotName` directories | Next.js App Router |
| Intercepting routes | `(.)`, `(..)`, `(..)(..)`, `(...)` prefixed dirs | Next.js App Router |
| API routes | `app/api/` or `pages/api/` directories | Next.js |
| Server actions | `"use server"` directive in files | Next.js/React 19 |
| Route params (Remix) | `$param` in filenames (e.g., `$userId.tsx`) | Remix |
| Route params (SvelteKit) | `[param]` in directory names under `src/routes/` | SvelteKit |
| Named params (Vue) | `:param` in route config objects | Vue Router |

### 4.2 Navigation Patterns to Detect (Expand)

**Currently detected**: Router type only (next-app-router, react-router, etc.).

**Should detect navigation UI components:**

| Pattern | Detection Method | Notes |
|---------|-----------------|-------|
| Tab navigation | Components named `*Tabs*`, `*TabBar*`, `role="tablist"` in JSX | Primary section switching |
| Breadcrumbs | Components named `*Breadcrumb*`, `aria-label="breadcrumb"`, `<nav>` with `<ol>` | Hierarchical navigation trail |
| Sidebar navigation | Components named `*Sidebar*`, `*SideNav*`, `*Drawer*` | Persistent side navigation |
| Drawer/hamburger | Components named `*Drawer*`, `*HamburgerMenu*`, mobile menu patterns | Mobile navigation |
| Bottom navigation | Components named `*BottomNav*`, `*BottomBar*`, `*TabBar*` | Mobile primary nav |
| Command palette | `cmdk`, `@command-ui/react`, Cmd+K pattern | Power user navigation |
| Search bar | Components named `*SearchBar*`, `*Search*`, spotlight pattern | Content discovery |
| Pagination | Components named `*Pagination*`, `page` query params | List navigation |
| Stepper/wizard | Components named `*Stepper*`, `*Wizard*`, `*MultiStep*` | Multi-step flows |
| Back button | `router.back()`, `history.back()`, `useRouter().back()` | Explicit back navigation |

### 4.3 Auth Flow Patterns to Detect (Expand)

**Auth analyzer exists but focuses on strategy. User flow should map the auth PAGES/ROUTES:**

| Flow | Detection (Route/File) | Notes |
|------|----------------------|-------|
| Login page | `login`, `signin`, `sign-in` in route/page names | Entry point |
| Signup page | `signup`, `sign-up`, `register` in route/page names | Registration |
| Forgot password | `forgot-password`, `reset-password`, `forgot` in routes | Password recovery |
| Email verification | `verify-email`, `confirm-email`, `verify` in routes | Email confirmation |
| OAuth callback | `callback`, `auth/callback`, `api/auth/callback` in routes | OAuth redirect handling |
| Magic link | `magic-link`, `passwordless` in routes | Passwordless auth |
| Two-factor auth | `2fa`, `mfa`, `two-factor`, `verify-code` in routes | MFA flow |
| Onboarding | `onboarding`, `setup`, `welcome`, `getting-started` in routes | Post-signup flow |
| Settings/profile | `settings`, `profile`, `account` in routes | User management |
| Logout handler | `logout`, `signout`, `sign-out` in routes or API handlers | Session termination |
| Invite flow | `invite`, `join`, `accept-invite` in routes | Team invitation |

### 4.4 Common User Flow Patterns to Detect

| Flow Category | Route Indicators | Notes |
|---------------|-----------------|-------|
| Dashboard | `dashboard`, `home`, `overview` routes | Main app entry after login |
| CRUD flows | `new`, `create`, `edit`, `[id]`, `delete` route patterns | Data management |
| Settings | `settings/*` nested routes (profile, billing, notifications, team) | Configuration hub |
| Admin panel | `admin/*` routes | Administrative interface |
| Checkout | `checkout`, `cart`, `payment`, `order` routes | E-commerce flow |
| Content management | `posts`, `articles`, `content`, `media` routes | CMS patterns |
| Social features | `feed`, `timeline`, `notifications`, `messages` routes | Social app patterns |

---

## 5. Per-Framework Libraries

### React Ecosystem
| Category | Libraries |
|----------|----------|
| Component libs | MUI, Ant Design, Chakra UI, Mantine, shadcn/ui, Radix UI, Headless UI, React Aria, NextUI/HeroUI, Base UI |
| Meta-frameworks | Next.js, Remix, Gatsby, Astro (with React) |
| State management | Redux Toolkit, Zustand, Jotai, Recoil, Valtio, MobX, XState |
| Data fetching | TanStack Query, SWR, Apollo Client, URQL, tRPC |
| Forms | React Hook Form, Formik, TanStack Form |
| Routing | React Router, TanStack Router, Next.js App Router, Wouter |
| Animation | Motion (Framer Motion), React Spring, GSAP, AutoAnimate |
| Testing | Jest, Vitest, Testing Library, Playwright, Cypress |
| Docs | Storybook, Ladle, Docusaurus |

### Vue Ecosystem
| Category | Libraries |
|----------|----------|
| Component libs | Vuetify, Element Plus, Naive UI, PrimeVue, Quasar, Ant Design Vue, Radix Vue, Ark UI Vue, Headless UI Vue |
| Meta-frameworks | Nuxt 3 |
| State management | Pinia (official), VueUse |
| Data fetching | TanStack Query for Vue, Apollo Vue, Nuxt useFetch |
| Forms | VeeValidate, Vuelidate, FormKit |
| Routing | Vue Router (official), Nuxt file-based routing |
| Animation | Vue built-in `<Transition>`, GSAP, Motion One |
| Testing | Vitest, Vue Test Utils, Playwright, Cypress |
| Docs | Histoire, VitePress, Storybook (Vue support) |

### Angular Ecosystem
| Category | Libraries |
|----------|----------|
| Component libs | Angular Material, Angular CDK, PrimeNG, NG-ZORRO, Nebular, Clarity |
| Meta-frameworks | Analog.js |
| State management | NgRx, NGXS, Akita, Elf, Angular Signals |
| Data fetching | HttpClient (built-in), Apollo Angular |
| Forms | Reactive Forms, Template-driven Forms (built-in) |
| Routing | Angular Router (built-in) |
| Animation | Angular Animations (built-in), GSAP |
| Testing | Jasmine + Karma, Jest, Playwright, Cypress |
| Docs | Storybook, Compodoc |

### Svelte Ecosystem
| Category | Libraries |
|----------|----------|
| Component libs | Skeleton, Svelte Headless UI, Flowbite Svelte, DaisyUI (Tailwind), Melt UI, Bits UI |
| Meta-frameworks | SvelteKit |
| State management | Svelte stores (built-in), svelte/store |
| Data fetching | SvelteKit load functions, TanStack Query for Svelte |
| Forms | Superforms, Felte |
| Routing | SvelteKit file-based routing |
| Animation | Svelte transitions (built-in), GSAP, Motion One |
| Testing | Vitest, Svelte Testing Library, Playwright |
| Docs | Histoire, Storybook (Svelte support) |

### SolidJS Ecosystem
| Category | Libraries |
|----------|----------|
| Component libs | Kobalte, Corvu, Ark UI Solid, Park UI Solid |
| Meta-frameworks | SolidStart |
| State management | Solid signals (built-in), solid-primitives |
| Data fetching | createResource (built-in), TanStack Query for Solid |
| Forms | Modular Forms |
| Routing | @solidjs/router, SolidStart file-based routing |
| Animation | Motion One (Solid), GSAP |
| Testing | Vitest, Solid Testing Library |
| Docs | Storybook (Solid support) |

---

## 6. Configuration Files to Parse

### Build & Bundler Configs
| File | What to extract |
|------|----------------|
| `package.json` | dependencies, devDependencies, scripts, sideEffects, type, browserslist |
| `tsconfig.json` | strict mode, paths, jsx setting, target, lib |
| `tailwind.config.{js,ts,cjs,mjs}` | theme tokens, plugins (daisyui, typography), content paths |
| `postcss.config.{js,cjs,mjs}` | PostCSS plugins (autoprefixer, cssnano, tailwindcss) |
| `vite.config.{ts,js}` | plugins (React, Vue, Svelte), build config |
| `next.config.{js,mjs,ts}` | images config, i18n, rewrites, redirects, headers |
| `nuxt.config.ts` | modules, css, components config |
| `svelte.config.js` | adapter, preprocessors |
| `astro.config.{mjs,ts}` | integrations, adapter |
| `webpack.config.{js,ts}` | loaders, plugins, optimization |
| `rollup.config.{js,mjs}` | plugins, output format |
| `turbo.json` | pipeline, dependsOn (Turborepo) |
| `pnpm-workspace.yaml` | monorepo workspace packages |

### Linting & Formatting
| File | What to extract |
|------|----------------|
| `eslint.config.{js,mjs,cjs}` (flat config) | plugins, rules, extends |
| `.eslintrc.{js,json,yaml}` (legacy) | plugins, rules, extends |
| `.prettierrc` / `prettier.config.js` | formatting rules |
| `biome.json` / `biome.jsonc` | Biome linting + formatting config |
| `.stylelintrc` / `stylelint.config.js` | CSS/SCSS linting rules |
| `.editorconfig` | indent style, charset, line endings |

### Testing Configs
| File | What to extract |
|------|----------------|
| `jest.config.{ts,js}` | test environment, transform, coverage |
| `vitest.config.{ts,js}` | test environment, coverage |
| `playwright.config.ts` | browsers, baseURL, projects |
| `cypress.config.{ts,js}` | baseUrl, component testing, e2e |
| `.storybook/main.{js,ts}` | framework, addons, stories glob |
| `histoire.config.ts` | framework, story patterns |

### A11y & Design Configs
| File | What to extract |
|------|----------------|
| `axe.config.{js,json}` | WCAG level, rules, tags |
| `.pa11yci` / `pa11y.json` | WCAG standard, runners, actions |
| `tokens.json` / `design-tokens.json` | Token format (DTCG, Style Dictionary) |
| `style-dictionary.config.js` | Token platforms, transforms |
| `panda.config.{ts,js}` | Panda CSS theme, tokens, patterns |
| `uno.config.{ts,js}` | UnoCSS presets, shortcuts |

### Environment & Deployment
| File | What to extract |
|------|----------------|
| `.env.example` / `.env.local.example` | Expected env vars (without secrets) |
| `docker-compose.yml` | Services, dependencies |
| `Dockerfile` | Base image, build stages |
| `vercel.json` | Deployment config |
| `netlify.toml` | Build commands, redirects |
| `fly.toml` | Fly.io deployment config |

---

## 7. Common Anti-Patterns to Flag

### Design System Anti-Patterns
| Anti-Pattern | Detection | Severity |
|-------------|-----------|----------|
| Multiple CSS methodologies | Both Tailwind AND styled-components in deps | WARN: Inconsistent styling approach |
| No component library but large app | 50+ components, no lib in deps | INFO: Consider adopting a component library |
| Inline styles in JSX | `style={{` patterns in many components | WARN: Inline styles defeat consistency |
| No design tokens | No token files, no theme config, no CSS custom properties | WARN: Hardcoded values reduce maintainability |
| Google Fonts CDN with Next.js | `fonts.googleapis.com` in HTML + `next` in deps | WARN: Use `next/font` instead for performance |
| styled-components with RSC | `styled-components` + Next.js App Router | WARN: styled-components has runtime overhead incompatible with Server Components |

### Accessibility Anti-Patterns
| Anti-Pattern | Detection | Severity |
|-------------|-----------|----------|
| No a11y tooling | Zero a11y tools in deps, no a11y ESLint plugin | ERROR: No accessibility testing infrastructure |
| Div-button pattern | `<div onClick=` without `role="button"` and `tabIndex` | ERROR: Inaccessible interactive element |
| Missing alt text | `<img` without `alt` prop | ERROR: WCAG 1.1.1 violation |
| Positive tabIndex | `tabIndex={n}` where n > 0 | WARN: Disrupts natural tab order |
| onClick without onKeyDown | `onClick` on non-interactive elements without keyboard handler | WARN: Keyboard inaccessible |
| No skip link | No "skip to main" or "skip to content" in layout root | WARN: WCAG 2.4.1 |
| No semantic HTML | Semantic score "low" (>90% divs) | WARN: Poor document structure |
| Color-only error indication | Error states using only red color, no text/icon | WARN: WCAG 1.4.1 violation |
| Missing form labels | `<input>` without associated `<label>` or `aria-label` | ERROR: WCAG 3.3.2 |
| Autoplaying media | `<video autoplay` or `<audio autoplay` without `muted` | WARN: WCAG 1.4.2 |

### Frontend Pattern Anti-Patterns
| Anti-Pattern | Detection | Severity |
|-------------|-----------|----------|
| No error boundary | App uses React but no ErrorBoundary found | WARN: Unhandled render errors crash entire app |
| No loading states | No Suspense, no skeleton, no spinner patterns found | WARN: Poor loading UX |
| Large lists without virtualization | Array `.map()` rendering 100+ items, no virtualization lib | WARN: Performance issue |
| No code splitting | Large app, single entry, no `React.lazy` / `dynamic()` | WARN: Slow initial load |
| State in URL missing | Multi-step forms/wizards without URL state | INFO: Deep linking not supported |
| Prop drilling | 4+ levels of prop passing without Context | INFO: Consider Context or state management |
| Nested ternaries in JSX | `{cond ? a : cond2 ? b : c}` patterns | WARN: Hard to read, extract to components |
| Giant components | Single component file > 300 lines | INFO: Consider splitting into smaller components |

### User Flow Anti-Patterns
| Anti-Pattern | Detection | Severity |
|-------------|-----------|----------|
| No 404 page | No `not-found`, `404` file in pages/app | WARN: Broken route UX |
| No error page | No `error`, `_error`, `500` file | WARN: No error recovery |
| Auth routes without middleware | Login/signup routes exist but no auth middleware detected | INFO: Verify auth protection |
| No loading.tsx with app router | Next.js App Router but no `loading.tsx` files | INFO: Missing route-level loading states |
| Dead routes | Route files that are not imported/referenced anywhere | WARN: Unused code |

---

## Summary of Gaps in Current Analyzers

### design.py (DesignUIAnalyzer)
- **Missing libraries**: Ark UI, React Aria, Flowbite, HeroUI, Element Plus, Naive UI, Angular Material, Kobalte
- **Missing CSS**: Vanilla Extract, Panda CSS, StyleX, UnoCSS, Linaria, PostCSS, Tailwind v4 (no config)
- **Missing tokens**: W3C DTCG format detection, Style Dictionary config, Tailwind-as-tokens
- **Missing entirely**: Icon library detection, component documentation tool detection, font optimization detection
- **Missing anti-patterns**: Multiple CSS methods, styled-components with RSC

### accessibility.py (AccessibilityAnalyzer)
- **Missing tools**: cypress-axe, @axe-core/playwright, @storybook/addon-a11y, vue a11y plugin, angular a11y, vitest-axe
- **ARIA too shallow**: Only boolean detection. Should enumerate specific ARIA patterns (landmarks, live regions, dialog, tabs, etc.)
- **Missing form a11y**: Label-input association, aria-required, aria-invalid, fieldset/legend, error message association
- **Missing focus**: Skip links, focus trap libraries, focus restoration, focus-visible, roving tabindex
- **Missing contrast**: Dark mode support, high contrast mode, CSS custom property token-based contrast
- **Missing WCAG 2.2**: Target size detection (2.5.8)

### frontend_patterns.py (FrontendPatternsAnalyzer)
- **Missing animation**: AutoAnimate, React Transition Group, Rive, Three.js, View Transitions API
- **Missing component patterns**: Compound components, custom hooks, HOCs, provider pattern, atomic design, FSD
- **Missing routing depth**: Dynamic routes, parallel routes, intercepting routes, route groups -- just library name detected
- **Missing performance**: React.memo, useMemo, useCallback usage detection, React Compiler
- **Missing loading**: Next.js loading.tsx convention, streaming SSR, skeleton libraries, optimistic updates

### user_flows.py (UserFlowsAnalyzer)
- **Missing route patterns**: Dynamic segments, catch-all, parallel, intercepting, route groups
- **Missing nav UI**: Breadcrumbs, sidebar, drawer, bottom nav, tabs, command palette, pagination, stepper
- **Missing auth flows**: Login/signup/forgot-password/callback/2FA page detection
- **Missing user flows**: Dashboard, CRUD, settings, admin, checkout, social patterns

Sources:
- [Netguru: Design Systems Trends 2025](https://www.netguru.com/blog/key-design-systems-trends-and-best-practices)
- [UXPin: Best Design System Examples](https://www.uxpin.com/studio/blog/best-design-system-examples/)
- [Figma: Schema 2025 Design Systems](https://www.figma.com/blog/schema-2025-design-systems-recap/)
- [W3C: WCAG 2.2](https://w3c.github.io/wcag/guidelines/22/)
- [AllAccessible: WCAG 2.2 Complete Guide 2025](https://www.allaccessible.org/blog/wcag-22-complete-guide-2025)
- [W3C: ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [MDN: ARIA Live Regions](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions)
- [TestParty: Form Accessibility Guide](https://testparty.ai/blog/form-accessibility-guide)
- [TheWCAG: Accessible Forms 2026](https://www.thewcag.com/examples/forms)
- [web.dev: Keyboard Focus](https://web.dev/learn/accessibility/focus)
- [AllAccessible: Color Contrast Guide 2025](https://www.allaccessible.org/blog/color-contrast-accessibility-wcag-guide-2025)
- [Jeff Bruchado: CSS-in-JS 2025 Trends](https://jeffbruchado.com.br/en/blog/css-in-js-2025-tailwind-styled-components-trends)
- [W3C DTCG Specification 2025.10](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)
- [Style Dictionary: DTCG Support](https://styledictionary.com/info/dtcg/)
- [Makers Den: React UI Libraries 2025](https://makersden.io/blog/react-ui-libs-2025-comparing-shadcn-radix-mantine-mui-chakra)
- [Redmonk: shadcn/ui and Copypasta](https://redmonk.com/kholterhoff/2025/04/22/ui-component-libraries-shadcn-ui-and-the-revenge-of-copypasta/)
- [Ark UI](https://ark-ui.com/)
- [Park UI](https://park-ui.com)
- [PkgPulse: Storybook vs Ladle vs Histoire](https://www.pkgpulse.com/blog/storybook-8-vs-ladle-vs-histoire-2026)
- [DEV: React Animation Libraries 2025](https://dev.to/raajaryan/react-animation-libraries-in-2025-what-companies-are-actually-using-3lik)
- [Next.js: Parallel Routes](https://nextjs.org/docs/app/api-reference/file-conventions/parallel-routes)
- [Next.js: Intercepting Routes](https://nextjs.org/docs/app/api-reference/file-conventions/intercepting-routes)
- [Next.js: Font Optimization](https://nextjs.org/docs/app/getting-started/fonts)
- [React: Suspense](https://react.dev/reference/react/Suspense)
- [Patterns.dev: Compound Pattern](https://www.patterns.dev/react/compound-pattern/)
- [GeeksforGeeks: React Architecture Patterns](https://www.geeksforgeeks.org/reactjs/react-architecture-pattern-and-best-practices/)
- [LaunchDarkly: React Architecture 2025](https://launchdarkly.com/docs/blog/react-architecture-2025)
- [jsdev.space: 15 React Anti-Patterns](https://jsdev.space/react-anti-patterns-2025/)
- [Silktide: Automated WCAG 2.2 Testing](https://silktide.com/wcag-2-2/)
- [TestParty: WCAG 2.2 New Success Criteria](https://testparty.ai/blog/wcag-22-new-success-criteria)
