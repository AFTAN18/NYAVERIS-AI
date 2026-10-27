# Google Cloud Run deployment

Target project supplied by the owner: `project-7b32515b-99e7-45cb-a03`. Region: `asia-south1`. The app is designed for a single Cloud Run service serving Express and compiled Vite assets. No Vercel, Netlify, Firebase or alternate application database is used.

Official references: [CLI installation](https://docs.cloud.google.com/sdk/docs/install-sdk), [source deployment](https://docs.cloud.google.com/run/docs/deploying-source-code), [Cloud Run secrets](https://docs.cloud.google.com/run/docs/configuring/services/secrets).

## Prerequisites

- Google Cloud CLI installed and signed in by the owner (`gcloud auth login`).
- Billing enabled for the selected project. Cloud Build, Artifact Registry, Secret Manager and Cloud Run can incur charges; review project quotas and budget before deployment.
- Permissions to deploy Cloud Run, build images, access Artifact Registry, and use the deployment/runtime service accounts. Ask your project administrator for least-privilege deployment access.
- The dedicated Supabase schema and synthetic Auth accounts provisioned as in SETUP.md.
- Tests and production build passed.

```powershell
gcloud config set project project-7b32515b-99e7-45cb-a03
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com
```

## Secret Manager

The reproducible helper `python scripts/deploy.py` prints the exact plan without creating resources. After the owner authorizes deployment costs and billing is enabled, run `python scripts/deploy.py --apply`. Add `--gcloud PATH_TO_GCLOUD` if the CLI is not on PATH. The helper checks billing, enables required APIs, creates a dedicated runtime service account, uploads password values through stdin into Secret Manager, grants that runtime account access only to those secrets, deploys the configured source, and verifies the real `/health` URL. It never uploads a Supabase secret/service-role key. A later browser run still needs to verify the full deployed workflows.

Store `DEMO_PASSWORD` and `SAFETY_GATEWAY_PASSWORD` as separate secrets named `fairshift-demo-password` and `fairshift-safety-password`. Add Gemini as `fairshift-gemini-key` only if live AI is desired. Use Secret Manager's console or `gcloud secrets create ... --data-file=...`; never put plaintext secret values in shell command arguments or tracked YAML. Grant the runtime service account Secret Accessor only on the required secrets.

Copy `deploy/cloud-run.env.example.yaml` to ignored `.local/cloud-run.env.yaml`. Supply only nonsecret config there. Do not upload `.env` in the build context. Both `.gcloudignore` and `.dockerignore` exclude credentials and caches.

```powershell
gcloud run deploy fairshift-saakshi-ai `
  --project project-7b32515b-99e7-45cb-a03 `
  --region asia-south1 `
  --source . `
  --allow-unauthenticated `
  --port 8080 `
  --memory 512Mi `
  --cpu 1 `
  --min-instances 0 `
  --max-instances 1 `
  --concurrency 40 `
  --env-vars-file .local/cloud-run.env.yaml `
  --set-secrets DEMO_PASSWORD=fairshift-demo-password:latest,SAFETY_GATEWAY_PASSWORD=fairshift-safety-password:latest
```

The public HTTP service serves the landing page and anonymous reporting endpoints. Business APIs still require verified Supabase Auth and organization membership. A production tenant should use a separate Supabase project and `ENABLE_DEMO=false`.

`--source .` uses the provided Dockerfile. The multi-stage build runs TypeScript checks and creates frontend/server bundles, prunes development packages, and runs as the unprivileged `node` user. Express binds `0.0.0.0:$PORT`. No local Docker is required for the Cloud Build source-deploy path.

## Verification after deployment

1. Obtain the real URL from `gcloud run services describe fairshift-saakshi-ai --region asia-south1 --format='value(status.url)'`.
2. Request `URL/health` and check a 200 response with `status: ok`.
3. Open the landing page and verify worker/admin demo login.
4. Run `TEST_BASE_URL=URL npm run test:e2e` using appropriate shell syntax and verify all required workflows.
5. Set the Supabase Auth Site URL to the deployed origin.
6. Check browser assets do not contain gateway passwords, a service-role key or a Gemini API key. Confirm CSP/connect-src uses the correct Supabase origin.
7. Capture the real tested URL in the submission checklist. A prepared container or successful local build is not proof of cloud deployment.

## Scaling and rollback

Start with one maximum instance because rate-limit state is local to the process. Before increasing replicas, add edge/infrastructure abuse controls and paginated workspace queries. Cloud Run revisions support rollback; pin the known-good revision after final verification. Avoid repeated Innovator Dashboard submissions; only submit once the real URL and repository are verified.
