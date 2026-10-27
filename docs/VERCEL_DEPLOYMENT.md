# NYAVERIS AI — Vercel production deployment

Verified production URL: **https://nyaveris-ai.vercel.app**.

## Existing project preserved

The original project was renamed in place from `fairshift` to `nyaveris-ai`. No duplicate project was created.

- Project ID: `prj_GSHTnszr49w8p7rico2kgkwjmAiA` (unchanged).
- Workspace: `aftan-faizs-projects` (unchanged).
- GitHub: `AFTAN18/NYAVERIS-AI`, repository ID `1435298663`, production branch `main`.
- Framework: Vite, Node.js 24, build command `npm run build`, static output `dist`.
- API: existing exported Express handler in `api/[...path].ts`; no permanent process required.
- `vercel.json` preserves API routing, direct SPA navigation, security headers and function limits.
- The eight existing production environment variables and their values were preserved. Passwords remain Vercel Secrets; no values are included in this document.

The new address is registered as a verified production project domain, rather than only as a deployment alias. Future production deployments therefore continue to receive it. The existing legacy domain was retained to avoid breaking earlier links.

## Authentication URLs

In the dedicated Supabase project, the owner confirmed these Auth URL settings:

- Site URL: `https://nyaveris-ai.vercel.app`.
- Additional redirect allow-list entry: `https://nyaveris-ai.vercel.app/**`.
- Existing localhost and legacy entries retained.

Settings page: https://supabase.com/dashboard/project/vkkjuopfidvfhzsqzius/auth/url-configuration.

The current sign-in uses Supabase email/password authentication, and API calls use the same application origin with verified bearer sessions. There is no separate application CORS-origin list to change. Auth URL allow-list settings also support future email confirmation, recovery or redirect-based sign-in flows. No database schemas, memberships, account credentials or business logic were changed during the project/domain update.

## Verified on the production domain

On 27 October 2026:

- `/`, `/health`, `/api/health`, `/api/config` and direct `/app/pay` returned successful responses.
- The browser title and branding displayed NYAVERIS AI.
- Unauthenticated `/api/workspace` was denied with HTTP 401.
- Real synthetic worker email/password sign-in succeeded from the new origin.
- The authenticated session survived a page refresh.
- The worker pay dashboard loaded its persisted ₹1,100/₹950 comparison.
- Employer access and the workforce dashboard worked.
- Switching to the hospital organization loaded the six-hour rest warning.
- Logout returned to the sign-in screen.

Executed browser check:

```powershell
$env:TEST_BASE_URL='https://nyaveris-ai.vercel.app'
npm run test:e2e -- --grep 'production domain supports'
```

Result: **1 passed**, covering the complete read-only domain/authentication/dashboard smoke flow. It does not submit or change payroll, safety or schedule records.

## Future deployment

From this checkout, verify `vercel project inspect --non-interactive` resolves to the project ID above. Use the existing GitHub integration on `main`, or deploy through the authenticated Vercel CLI. Do not create a new project merely because its name changed. The local `.vercel/project.json` remains ignored and now records the new project name with the same project and organization IDs.

The official FairShift challenge name remains a problem-statement reference. Vercel is the requested development host; the original hackathon's Cloud Run requirement remains a separate outstanding submission requirement.
