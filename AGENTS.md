# FairShift engineering rules

- Keep exactly one Git branch; do not create worktrees or extra branches.
- Supabase PostgreSQL is the sole application database. Never substitute local persistence.
- Money is integer paise. Calculations and scheduling rules are deterministic and tested.
- Validate API inputs. Verify Supabase identity and protected membership server-side.
- Anonymous safety credentials must be random, hashed at rest, and never logged or sent to AI.
- Update business records and ProofLoop events atomically. Events are append-only through application roles.
- Keep secrets out of source, browser bundles, and logs. Use synthetic data only.
- Run typecheck, unit/integration tests, production build and browser tests before claiming verification.
- Current requested deployment target is Vercel (Node.js Functions plus Vite frontend). Keep the portable Cloud Run container, but do not configure Google Cloud unless requested. A Vercel-only deployment does not satisfy the original hackathon's Cloud Run rule.
- Serverless handlers must not depend on process-local rate-limit state or persistent filesystem storage.
