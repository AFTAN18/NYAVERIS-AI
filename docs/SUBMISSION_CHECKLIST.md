# PromptWars 2026 submission checklist

## Application

- [x] Actual React/TypeScript frontend and Express backend.
- [x] Worker and employer interfaces.
- [x] FairPay discrepancy → review → correction → worker confirmation workflow.
- [x] ProofLoop transaction-backed action history and Fairness Replay.
- [x] SafeSignal anonymous reporting and secret-based tracking.
- [x] RestGuard risk detection and schedule what-if.
- [x] Construction and healthcare synthetic organizations in Supabase.
- [x] Supabase Auth, membership authorization and RLS.
- [x] English/Tamil/Hindi core interface and text guidance.
- [x] Optional server-only Gemini adapter and graceful fallback.
- [x] Mobile and keyboard flows implemented and tested; automated accessibility checks included.
- [ ] Live Gemini provider call tested (owner selected fallback for now).
- [ ] Broader native-language and manual screen-reader review before production use.

## Technical verification

- [x] Unit/API/AI fallback tests executed.
- [x] Live Supabase RLS/denied-access checks executed.
- [x] Browser workflows exercised with real synthetic persistence.
- [x] TypeScript and production build executed.
- [x] Dependency vulnerability scan performed; patched dependencies pinned.
- [x] Secrets excluded from Git, Docker and Cloud Build upload contexts.
- [ ] Final test counts and production smoke results recorded in TEST_REPORT.md.
- [ ] Docker image run (Docker is not installed locally; Cloud Build can build from source).

## Repository and hosting

- [ ] All final source published to public `https://github.com/AFTAN18/FAIRSHIFT.git`.
- [ ] Exactly one remote branch, `main`, verified after publication.
- [ ] Initial tracked source size strictly below 10 MB, measured after staging.
- [x] Lockfile, Dockerfile, ignore files, env example and deployment guide prepared.
- [x] Required target: Google Cloud Run, project `project-7b32515b-99e7-45cb-a03`.
- [ ] Google Cloud CLI authenticated by owner.
- [ ] Billing, service APIs and IAM confirmed.
- [ ] Runtime secrets stored in Secret Manager.
- [ ] Real Cloud Run URL deployed and `/health` tested.
- [ ] Required demonstration flows rerun against that real URL.

## Public explanation and official submission

- [x] LinkedIn explanation draft prepared without secrets or unsupported deployment claims.
- [ ] Owner reviews and publishes LinkedIn project explanation; record public post URL.
- [ ] Submission contains `.git` repository URL and verified Cloud Run URL.
- [ ] Submit through the official Innovator Dashboard only after final verification.
- [ ] Track submission attempts; maximum two, latest score replaces the previous score.

No Innovator Dashboard submission has been made by this development workflow.
