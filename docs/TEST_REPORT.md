# Verification report — 27 October 2026

The application was verified locally against the compiled production Express service at `http://127.0.0.1:8080`, using real synthetic records in the dedicated Supabase project. No Cloud Run deployment, live Gemini provider response or Docker execution is claimed by these results.

| Check | Executed result |
|---|---|
| Vitest unit/API/AI fallback suite | **36 passed, 0 failed** |
| Playwright production-server suite | **8 passed, 0 failed** in the final consolidated run |
| Live Supabase authorization/RLS checks | **23 assertions passed** after the final database constraint migration |
| TypeScript / production build | Passed |
| Automated worker-dashboard axe WCAG A/AA audit | Passed with no reported violations in the tested view |
| Dependency audit | Zero known vulnerabilities reported |
| Staged source and browser-bundle secret scans | Passed; configured backend secret values absent |
| Repository compliance | Single `main` branch; initial tracked source 540,287 bytes, strictly below 10 MB |
| Initial GitHub Actions CI | [Passed](https://github.com/AFTAN18/FAIRSHIFT/actions/runs/40459524074) |

The browser suite exercised the full worker request → employer correction → worker confirmation flow through actual UI forms, transactional ProofLoop history, anonymous submission and tracking, administrator safety acknowledgement, rejection of a wrong tracking token, hospital rest what-if, confirmed schedule persistence, Tamil/Hindi navigation, narrow 360px layout, and keyboard access. The schedule-persistence test restored the original hospital demonstration schedule while retaining its audit history.

Security assertions include worker ownership, administrator tenant isolation, unauthenticated denial, denied direct policy/audit writes, restricted gateway permissions, private tracking-hash protection, guarded RPC authorization, and rejection of fractional-minute timestamps even through direct administrator RPC calls.

Initial failures included a Windows sandbox temporary-file rename restriction (zero tests executed in that attempt), missing downloadable Chromium, IPv6 localhost binding, selectors targeting an unconfirmed shift and implicit form-label text, insufficient text contrast, and a mobile grid overflow. Fixes were rerun rather than suppressing assertions. Installed Chrome is used for browser verification.

A later run exposed an asynchronous refresh that could close a newly opened Replay dialog. The mutation ordering was corrected, stale workspace responses are ignored across identity changes, and the complete eight-test production suite then passed. One accessibility run timed out during simultaneous SDK extraction; its subsequent complete run passed without weakening assertions.

## External verification limits

- Supabase is configured and all three migrations are applied to the dedicated application project. Its security advisor reports two intentional informational notices for private deny-all tables and a warning that leaked-password protection is disabled. Review that Auth setting before a real workforce rollout.
- Gemini is intentionally unconfigured at the owner's request; English/Tamil/Hindi fallback behavior is tested. Provider-generated output was not tested against a live key.
- Google CLI authentication and target-project access were verified. The latest deployment prerequisite checks still returned `billingEnabled=false` for `project-7b32515b-99e7-45cb-a03`, despite deployment approval. No verified Cloud Run URL exists.
- Docker is unavailable locally. The production build and same-origin frontend/API service were tested directly; the Dockerfile is prepared but an image was not executed.
- LinkedIn publication, official Innovator Dashboard submission, manual screen-reader review and native-speaker language review remain outstanding. Product limitations, including locked historical pay policies, hourly-only policies and capped workspace queries, are listed in README.md.
