# FairShift — Saakshi AI

**Every hour verified. Every concern heard. Every action accounted for.**

FairShift is a worker-first fairness and accountability platform built for **PromptWars 2026**, ACM Student Chapter, SRMIST, aligned with **UN SDG 8: Decent Work and Economic Growth**. It supports construction sites and healthcare departments through one tenant-aware application.

Workers should not need to decode payroll spreadsheets or repeatedly explain an unresolved hazard. The **Fairness Twin + ProofLoop Engine** compares confirmed work with employer payroll, explains discrepancies, opens a review, records the employer response, and gives the worker the final confirmation step.

## Implemented workflows

- **FairPay Twin:** deterministic integer-paise calculations; overnight shifts; unpaid breaks; organization policies; expected-vs-recorded comparison; persisted payroll reviews; employer correction; worker-confirmed closure.
- **ProofLoop / Fairness Replay:** a readable event timeline with timestamps, roles, input/output snapshots and before/after payroll amounts. Business changes and events commit together. Application roles cannot edit/delete the history.
- **SafeSignal:** anonymous concern submission without an employee-account link; cryptographically random reference/token; SHA-256 token hashes in a private schema; secret-based tracking; sequential employer mitigation workflow.
- **RestGuard:** configured long-shift, rest-window, overlap, repeated-overtime and consecutive-day warnings; interactive schedule what-if; explicit administrator confirmation before persistence.
- **Two interfaces and two sectors:** responsive worker workspace and employer command center; separate synthetic construction and hospital organizations, accounts, schedules, policies and permissions.
- **Saarthi:** English, Tamil and Hindi core interface translations and text guidance; optional browser speech; optional server-side Google Gemini structured explanations with validated fallbacks. **Live Gemini is disabled by the owner's choice during verification.**

The seed contains the required construction example: **10 payable hours × configured ₹100/hour, 8 regular hours, 1.5× overtime → ₹1,100 expected vs ₹950 recorded → ₹150 potential difference.** The hospital has a **07:00 → 13:00 six-hour rest gap** against an eleven-hour demonstration policy. Moving the proposed start to 18:00 clears that rest warning. These are configured example policies, not universal legal requirements.

## Stack and structure

React 19, TypeScript, Vite, Tailwind CSS 4, shadcn-style Radix UI primitives, Lucide, React Router; Node 24, Express 5, Zod; Supabase Auth and PostgreSQL; official Google Gen AI SDK; Vitest, Playwright and axe-core. Exact dependency versions and `package-lock.json` are committed. The single-service Cloud Run Dockerfile serves compiled React and Express APIs together.

```text
src/                    Worker/admin views, translations, reusable UI
shared/                 Deterministic pay/rest engines and Zod contracts
server/                 Authenticated API, safety gateway, AI service
supabase/migrations/    Reproducible schema, RLS and transactional operations
supabase/seed.sql        Synthetic construction / healthcare records
scripts/                Auth provisioning and live RLS security checks
tests/                  Unit, API, fallback, browser and accessibility checks
deploy/                 Nonsecret Cloud Run configuration example
docs/                   Architecture, setup, deployment, demo and submission guides
```

## Run

```powershell
npm ci
# Set .env from .env.example, or use this workspace's already configured ignored .env.
npm run dev
# In another terminal:
npm run dev:web
```

Open **http://127.0.0.1:5173** and choose a worker/employer demo. Role/industry switching signs in as a different real synthetic Supabase identity. Normal email/password sign-in is available at `/login`. Anonymous concern submission/tracking is available at `/safety` without an employee session.

```powershell
npm run typecheck
npm test
npm run test:rls
npm run test:e2e
npm run build
```

Browser tests need a running frontend/backend and Chrome on Windows (or installed Playwright Chromium elsewhere). Live RLS tests need the dedicated provisioned project. Tests append clearly marked synthetic QA records; never point them at production employee data. See [setup](docs/SETUP.md) for fresh-project provisioning and environment details.

## Deployment

Deploy only to **Google Cloud Run** using the Dockerfile and [deployment guide](docs/DEPLOYMENT.md). Target project supplied by the owner: `project-7b32515b-99e7-45cb-a03`. Express binds `0.0.0.0:$PORT`; `/health` provides a readiness check. `.gcloudignore` and `.dockerignore` exclude secrets and caches. Put runtime passwords/optional Gemini credentials in Secret Manager.

**A real Cloud Run URL is not yet recorded as verified.** Follow the verification steps before submitting. Local build success alone does not mean a deployment succeeded.

## Security and inclusion

Every exposed table has RLS. Business requests verify Auth identity and protected memberships server-side, then run with the user's token. The safety gateway is a dedicated least-privilege Auth account, with no payroll or organization access. No broad Supabase secret key is required at runtime. No user-editable metadata grants roles. Anonymous token hashes stay in an unexposed schema; tokens are never sent to AI or put in URLs. HTTP protections include CSP/security headers, body limits, validation, no-store responses and rate limits.

Anonymous reports can still contain identifying information, and infrastructure may retain access logs; anonymity is not guaranteed. ProofLoop is append-only for application roles, not an immutable or tamper-proof ledger. AI does not calculate wages, decide legal rights, dismiss complaints or resolve cases. No surveillance features or uploads are included.

Mobile layouts, keyboard focus, semantic controls, labeled dialogs, regional language selection, text fallbacks and reduced-motion support are implemented. Automated accessibility checks complement, and do not replace, a manual assistive-technology audit.

## SDG 8 impact

FairShift makes potential underpayment visible, gives workers an actionable review mechanism, helps employers document corrections, provides a privacy-conscious path for hazards, and detects preventable scheduling risks. The employer sees actionable records while the worker keeps a voice in resolution. See the [demonstration guide](docs/DEMO.md).

## Scope and known limitations

- Policies lock after the first confirmed shift to protect historical calculations. Versioned rate changes, dedicated daily-rate policies and a policy editor are future work. The current calculator uses hourly policies.
- Workspace responses are capped at 500 records per table. This is suitable for the seeded demonstration; larger deployments require server-side pagination/aggregate queries before claiming complete organization-wide metrics.
- The current schedule-entry form uses Asia/Kolkata, matching both configured organizations. Wider deployments need full IANA wall-time entry, including DST ambiguity handling.
- Rate limiting is per instance. The deployment starts at one maximum instance; scale-out needs infrastructure-level abuse protection.
- Live Gemini calls, container execution, cloud deployment and broader manual accessibility review require their respective external setup/verification. Text fallbacks are available without Gemini.
- CSV import, attachments/certificates, signed receipts, realtime notifications, production onboarding and automated demo reset are intentionally not included.
- Core navigation, forms and guidance support Tamil/Hindi; some technical audit names, brand microcopy, administrator explanations and synthetic record contents remain English. Obtain native-speaker review before a public workforce rollout.

## Submission

Repository: **https://github.com/AFTAN18/FAIRSHIFT.git**. Maintain exactly one branch, `main`, and an initial source repository below 10 MB. See [submission checklist](docs/SUBMISSION_CHECKLIST.md), [test report](docs/TEST_REPORT.md) and [LinkedIn draft](docs/LINKEDIN_DRAFT.md). Do not submit to the Innovator Dashboard until the repository, real Cloud Run URL and demonstration are stable; the latest of at most two submissions replaces the previous score.
