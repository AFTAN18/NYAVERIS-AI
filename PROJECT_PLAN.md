# FairShift — implementation plan

1. Foundation: React/Vite/TypeScript, Express, design tokens, shared deterministic engines.
2. Database: dedicated Supabase project, normalized schema, membership RLS, transactional RPCs and synthetic seed.
3. Pay slice: authenticated worker/admin dashboard, pay comparison, review, response, worker confirmation, ProofLoop.
4. Safety slice: anonymous submission, hashed token tracking, admin updates and timeline.
5. Rest slice: healthcare overnight scheduling, policy warnings, interactive what-if and confirmed scheduling.
6. Language/AI: English, Tamil, Hindi core UI; server Gemini structured explanations with deterministic fallback.
7. Verification: engines, API authorization, live RLS, end-to-end workflows, mobile and production smoke tests.
8. Delivery: Cloud Run container, setup/deploy documentation, demonstration and compliance checklists.

External dependencies: Google Cloud account/CLI/billing and deployment authorization; Gemini key; public GitHub repository creation; LinkedIn and Innovator submission.
