# NYAVERIS AI — implementation plan

1. Foundation: React/Vite/TypeScript, Express, design tokens, shared deterministic engines.
2. Database: dedicated Supabase project, normalized schema, membership RLS, transactional RPCs and synthetic seed.
3. Pay slice: authenticated worker/admin dashboard, pay comparison, review, response, worker confirmation, ProofLoop.
4. Safety slice: anonymous submission, hashed token tracking, admin updates and timeline.
5. Rest slice: healthcare overnight scheduling, policy warnings, interactive what-if and confirmed scheduling.
6. Language/AI: English, Tamil, Hindi core UI; server Gemini structured explanations with deterministic fallback.
7. Verification: engines, API authorization, live RLS, end-to-end workflows, mobile and production smoke tests.
8. Delivery: Cloud Run container, setup/deploy documentation, demonstration and compliance checklists.

## Historical implementation status

The core pay, ProofLoop, anonymous safety and rest-risk slices are implemented with persisted synthetic construction and healthcare data. Supabase Auth, tenant RLS, server authorization and transaction-backed history are configured. The production build, 36 unit/API tests, 8 browser tests and 23 live database security assertions passed. Source is saved to the public NYAVERIS-AI repository on its sole `main` branch.

The Google CLI is installed and authenticated, project access is verified, and deployment approval is recorded. The last Google API checks still returned billing disabled for the requested project, so Cloud Run deployment is pending. Gemini remains on the verified text fallback at the owner's request. LinkedIn publication and official Innovator submission remain pending. README.md records secondary product limitations; the full hackathon acceptance list is not claimed complete until the live Cloud Run deployment and external deliverables are verified.

## Current continuation — 1 November 2026

The local candidate also includes SaaS onboarding, employee management, protected invitations, daily/hourly policy snapshots, calendar management and multilingual speech controls. Shared application files are synchronized with the participant submission. Current verification and remaining release prerequisites are recorded in [current activation/submission audit](https://github.com/Dr-M-Suchithra-lab/ACM-SRM-PromptWars-2026/blob/192425004-AFTAN-FAIZ/students/192425004-AFTAN-FAIZ/docs/ACTIVATION_2026-11-01.md).

Previous approval A permits the exact SaaS migration only after a restorable backup is confirmed; B permits provider configuration once private credentials and a verified sender are supplied; C permits deployment after prerequisites pass. These approvals persist. Normal publication is separately authorized only to application main and the participant branch/folder. No resets, reseeding or new cloud project is authorized. Vercel remains the requested deployment target; do not configure Cloud Run without a new request.
