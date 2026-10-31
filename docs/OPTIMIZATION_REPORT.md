# NYAVERIS AI engineering optimization — 27 October 2026

Scope: preserve branding, UI, API contracts, business rules, database, environment names and domain. Historical evaluation values are not edited or reassessed. After local verification, the owner explicitly authorized publishing these improvements to the existing GitHub/Vercel project. No evaluation submission is performed.

## Baseline (before edits)

- Clean `main`, one local branch. React/Vite UI, shared deterministic engines, Express exported as one Vercel Node function, Supabase Auth/PostgreSQL/RLS, optional server-side Gemini.
- Strict TypeScript already enabled. `npm run typecheck` passed. No ESLint dependency, config or lint script exists; ESLint was unavailable rather than passed.
- `npm test`: sandbox failed before test execution with Windows temporary-file EPERM. Rerun outside sandbox: **45 tests passed, 5 files**, 1.44s.
- `npm run build`: passed; 1,953 transformed modules, 59.32s Vite wall time. Existing upstream Zod pure-comment annotation warnings are nonfatal.
- Frontend assets: CSS 62,938 bytes; JS 278,452 + 423,161 + 173,821 + 85,635 = **961,069 bytes**. Build time is environment-sensitive; asset bytes are the reproducible comparison.
- `npm run check:security`: passed, 70 tracked files / 590,378 bytes, one branch, configured secrets absent from tracked source and browser assets.
- `npm audit --audit-level=high --json`: **zero known vulnerabilities** at every severity.
- Existing read-only Playwright subset against local production build on port 8091: **6 passed**, 34.3s. Includes branding, worker dashboard axe scan (zero violations), password sign-in/session reload/logout, both industry dashboards, Tamil guidance, Hindi navigation, ProofLoop, 360px mobile layout and unsaved what-if.

## Audit findings and decisions

- `src/App.tsx` combines many render helpers and orchestration. Avoid a broad rewrite: nested form components previously caused remount bugs. Extract only the API transport and stable field primitive.
- API response JSON implicitly propagated `any` into typed state; add explicit response contracts at one transport boundary. This does not claim runtime response-schema validation.
- Form hints are visible but not associated with their controls for assistive technology; add unique `aria-describedby` IDs while preserving existing descriptions and labels.
- Gemini timeout remains scheduled after a completed response; release it in `finally` without changing the timeout or fallback behavior.
- Seven unused imports/parameters found by stronger TypeScript diagnostics; remove them and enforce unused-code checks going forward.
- Existing test coverage concentrates on happy-path engine/API validation; add targeted financial boundaries, timeout lifecycle, transport errors and isolated authenticated-route integration tests.
- Existing browser mutation suites create payroll/safety records or change policies/schedules. Do not execute these against the connected hosted dataset under this task's no-data-change requirement. Mocked integration tests do not replace PostgreSQL transaction or RLS execution tests.

## Read-only Supabase review

Catalog queries confirmed RLS on all **14** public/private application tables. Application roles have **no direct write table grants**. Public RPC wrappers are invoker functions; privileged helpers are private with empty search paths. Authorization uses protected membership records, not user-editable metadata. SQL migrations and data remain untouched.

Existing security advisor: leaked-password protection disabled ([guidance](https://supabase.com/docs/guides/auth/password-security#password-strength-and-leaked-password-protection)). Three private deny-all tables intentionally have RLS without client policies.

Existing performance advisor: six unindexed foreign keys and three policies with per-row auth evaluation ([index guidance](https://supabase.com/docs/guides/database/database-linter?lint=0001_unindexed_foreign_keys), [RLS guidance](https://supabase.com/docs/guides/database/database-linter?lint=0003_auth_rls_initplan)). No evidence of current user-visible latency; defer database changes until an isolated environment and representative query measurements are available. Do not remove indexes solely because the advisor reports no usage.

## Final verification

Implemented:

- Extracted a typed, independently tested API transport to `src/lib/api.ts`; explicit response types now reach workspace, demo session, assistant and safety state. HTTP methods, paths, headers and payloads are preserved.
- Extracted stable `src/components/Field.tsx`; preserved accessible names and existing descriptions, added unique associations for hints. No form-state remount refactor.
- Cleared the Saarthi deadline timer in `finally`; provider model, prompt, deadline, output schema and multilingual fallback remain unchanged.
- Removed unused imports/parameters; enforced `noUnusedLocals` and `noUnusedParameters` with existing strict TypeScript.
- Scoped Tailwind detection to UI sources using its [documented source configuration](https://tailwindcss.com/docs/detecting-classes-in-source-files). Test/report prose no longer changes generated utilities.
- Expanded axe checks found real secondary-text contrast failures (2.43:1–3.61:1) on safety/payroll/RestGuard screens. Reused the existing darker `#53665e`, amber `#7c652f` and green `#3c6547` for affected hints, labels and scheduling results. These targeted text-color corrections are the only intended visible difference; layout, typography, branding and palette stay intact.
- Secret/source-size checks now include new untracked source as well as tracked files, preventing review-time additions from escaping the scan.
- Added `test:rls:readonly` for SELECT-only hosted isolation verification. Corrected stale architecture documentation about deployment, versioned policies and shared rate limits.

Tests added: API transport success/error/network cases; exact overtime thresholds; break ordering; DST offsets; maximum shift lengths; unsafe currency; overlapping prior shifts; AI success/failure/deadline cleanup; real Express routing with mocked Supabase identity/membership/RPC boundaries; anonymous randomness/hash-only persistence arguments; protected assistant fallback; expanded safety/payroll/admin WCAG scans and dialog keyboard tests.

Completed commands/results:

| Check | Result |
| --- | --- |
| `npm run typecheck` | Pass, including both new unused-code diagnostics |
| `npm test` | **90 passed**, 8 files (baseline 45; 45 focused additions) |
| `npm run build` | Pass; existing upstream Zod annotation warnings only |
| `npm exec -- prettier --check` on changed TS/TSX/JSON | Pass |
| `npm run test:rls:readonly` | **11 live SELECT-only assertions passed** |
| `npm run check:security` | Pass, includes untracked additions; one branch and source below 10 MB |
| `npm audit --audit-level=high --json` | Zero known vulnerabilities at all severities; dependencies/lockfile unchanged |
| `git diff --check` | Pass |
| ESLint | Not configured/installed in baseline; not reported as passed. No new lint dependency added |

Browser regression results and release verification are recorded below after completion.

Measured production assets: JavaScript **961,323 bytes** (baseline 961,069, +254 bytes / 0.027% for typed transport error handling and field descriptions). CSS **61,105 bytes** (baseline 62,938, −1,833). Combined assets **1,022,428 bytes**, **1,579 bytes smaller** than baseline. Rounded Vite gzip totals decrease by approximately 0.19 kB. No runtime dependencies, API requests or database queries added. Build wall times vary with warm caches and are not evidence of a runtime speedup.

Before the explicitly documented contrast correction, mobile landing and desktop pay PNG hashes were exactly identical to baseline after extraction and Tailwind source scoping. Final screenshots should differ only in the targeted secondary text colors.

Unchanged by hash: wage/rest engine source, dependency lockfile and Vercel configuration. No SQL migrations, policies, records, environment values or API contracts changed. Authentication tests create ordinary sign-in activity and local API requests consume existing throttle counters; no shifts, pay, cases, policy or audit-history records were written by this work.

Limitations: hosted write-workflow/RLS mutation suites intentionally not rerun, since they create records or modify policies/schedules. Isolated RPC tests verify application orchestration, not database transactions. Live Gemini remains unconfigured by owner choice; deterministic translations and provider-adapter fallback paths are verified. Automated axe checks cover selected WCAG rules and do not establish full WCAG conformance. No official evaluation rerun or score increase claimed. The original hackathon guide's Cloud Run requirement remains distinct from the requested Vercel deployment.

Changed files: `src/App.tsx`, `src/components/Field.tsx`, `src/lib/api.ts`, `src/index.css`, `server/ai.ts`, `tsconfig.json`, `scripts/provision.ts`, `scripts/security-check.ts`, `scripts/rls-readonly-test.ts`, `package.json`, `tests/ai.test.ts`, `tests/api-client.test.ts`, `tests/authenticated-api.test.ts`, `tests/engine-boundaries.test.ts`, `tests/e2e/quality-regression.spec.ts`, `README.md`, `docs/ARCHITECTURE.md`, this report.
