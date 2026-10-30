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

## Keep both NYAVERIS AI repositories synchronized

- The application repository is `AFTAN18/NYAVERIS-AI` (workspace root). The organizer submission is `Dr-M-Suchithra-lab/ACM-SRM-PromptWars-2026`, branch `192425004-AFTAN-FAIZ`, folder `students/192425004-AFTAN-FAIZ/`.
- Whenever shared application code, tests, configuration or migration files change, update the counterpart in the same task. From the application repository root, run `node scripts/sync-submission.mjs --check` before handoff. Resolve intentional differences with `--from app` or `--from submission` only after reviewing the changed-file list.
- Preserve unique work. Do not overwrite repository-specific READMEs, prompt histories, screenshots, deployment helpers or security-check scripts. Never copy private environment files, credentials, Git/Vercel metadata, dependencies or generated output.
- Both copies use the same existing Supabase project. Mirror proposed migrations but apply an approved migration only once; never create another project, reset or reseed it.
- Synchronization is local preparation. Commits, pushes, production configuration changes, migrations and deployments still require explicit approval. Never update organizer `main` or another student's work.
