# NYAVERIS AI

**Fairness You Can Trace. Trust You Can Prove.**

**Production application: [nyaveris-ai.vercel.app](https://nyaveris-ai.vercel.app).**

NYAVERIS AI is a worker-first fairness and accountability platform built for **PromptWars 2026**, ACM Student Chapter, SRMIST, aligned with **UN SDG 8: Decent Work and Economic Growth**. It implements the official **FairShift: Decent Work Platform** hackathon problem statement. It supports construction sites and healthcare departments through one tenant-aware application.

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

For SELECT-only tenant-isolation checks, use `npm run test:rls:readonly`. The [engineering optimization report](docs/OPTIMIZATION_REPORT.md) records baseline/final results and the exact read-only browser subset; it does not claim a new official evaluation score.

## Deployment

The requested development deployment is **Vercel**, using the existing project renamed in place to `nyaveris-ai`. The Vite frontend and Node.js API function share [https://nyaveris-ai.vercel.app](https://nyaveris-ai.vercel.app). See the [Vercel deployment and domain guide](docs/VERCEL_DEPLOYMENT.md).

The Dockerfile and [Cloud Run deployment guide](docs/DEPLOYMENT.md) remain available for portability. **The official FairShift hackathon submission guide requires Google Cloud Run; this verified Vercel deployment does not satisfy that hosting rule.** No verified Cloud Run URL is recorded.

## Security and inclusion

Every exposed table has RLS. Business requests verify Auth identity and protected memberships server-side, then run with the user's token. The safety gateway is a dedicated least-privilege Auth account, with no payroll or organization access. No broad Supabase secret key is required at runtime. No user-editable metadata grants roles. Anonymous token hashes stay in an unexposed schema; tokens are never sent to AI or put in URLs. HTTP protections include CSP/security headers, body limits, validation, no-store responses and rate limits.

Anonymous reports can still contain identifying information, and infrastructure may retain access logs; anonymity is not guaranteed. ProofLoop is append-only for application roles, not an immutable or tamper-proof ledger. AI does not calculate wages, decide legal rights, dismiss complaints or resolve cases. No surveillance features or uploads are included.

Mobile layouts, keyboard focus, semantic controls, labeled dialogs, regional language selection, text fallbacks and reduced-motion support are implemented. Automated accessibility checks complement, and do not replace, a manual assistive-technology audit.

## SDG 8 impact

NYAVERIS AI makes potential underpayment visible, gives workers an actionable review mechanism, helps employers document corrections, provides a privacy-conscious path for hazards, and detects preventable scheduling risks. The employer sees actionable records while the worker keeps a voice in resolution. See the [demonstration guide](docs/DEMO.md).

## Scope and known limitations

- The local candidate supports versioned hourly/daily pay policies and employee rate snapshots. New business onboarding, employee management and invitations require the proposed SaaS migration and approved rollout; these flows are not enabled in the current deployment.
- Workspace reads paginate in 500-record pages with a 10,000-record safety window. Exceeding that window fails explicitly; larger deployments need reporting-period pagination or aggregate queries.
- Schedule entry uses the organization's IANA time zone and rejects ambiguous/nonexistent daylight-saving minutes. Users must choose another minute when a clock change makes their selection ambiguous.
- Rate limits use shared PostgreSQL state and fail closed when the limiter is unavailable. Serverless handlers do not rely on process-local counters.
- Live Gemini calls, container execution, cloud deployment and broader manual accessibility review require their respective external setup/verification. Text fallbacks are available without Gemini.
- CSV import, attachments/certificates, signed receipts, realtime notifications, production onboarding and automated demo reset are intentionally not included.
- Core navigation, forms and guidance support Tamil/Hindi; some technical audit names, brand microcopy, administrator explanations and synthetic record contents remain English. Obtain native-speaker review before a public workforce rollout.

## Submission

Repository: **https://github.com/AFTAN18/NYAVERIS-AI.git**. Maintain exactly one branch, `main`, and an initial source repository below 10 MB. See [submission checklist](docs/SUBMISSION_CHECKLIST.md), [test report](docs/TEST_REPORT.md) and [LinkedIn draft](docs/LINKEDIN_DRAFT.md). Do not submit to the Innovator Dashboard until the repository, real Cloud Run URL and demonstration are stable; the latest of at most two submissions replaces the previous score.
