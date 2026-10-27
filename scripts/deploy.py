"""Cloud Run deployment with a billing guard and stdin-only secret upload.

Run only after reviewing the possible Cloud Build / Run / Registry / Secret Manager costs.
Without --apply this prints the deployment plan and creates no cloud resources.
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--project', default='project-7b32515b-99e7-45cb-a03')
parser.add_argument('--region', default='asia-south1')
parser.add_argument('--gcloud', default='gcloud')
parser.add_argument('--apply', action='store_true')
args = parser.parse_args()
if not re.fullmatch(r'[a-z][a-z0-9-]{4,61}[a-z0-9]', args.project):
    raise SystemExit('Invalid Google Cloud project ID')
if not re.fullmatch(r'[a-z]+-[a-z]+[0-9]', args.region):
    raise SystemExit('Invalid region')

def run(*command, input_bytes=None, allow_failure=False):
    result = subprocess.run([args.gcloud, *command], cwd=ROOT, input=input_bytes,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode and not allow_failure:
        # gcloud receives secrets through stdin only, never in command arguments.
        raise SystemExit(result.stderr.decode('utf-8', errors='replace'))
    return result

plan = {'project': args.project, 'region': args.region,
        'service': 'fairshift-saakshi-ai', 'minInstances': 0, 'maxInstances': 1,
        'memory': '512Mi', 'cpu': 1, 'database': 'Supabase only',
        'runtimeAccount': 'fairshift-runtime', 'secretKeys': ['DEMO_PASSWORD', 'SAFETY_GATEWAY_PASSWORD']}
print(json.dumps(plan, indent=2))
if not args.apply:
    print('Plan only. Use --apply after billing and deployment cost approval.')
    raise SystemExit(0)
billing = json.loads(run('billing', 'projects', 'describe', args.project, '--format=json').stdout)
if not billing.get('billingEnabled'):
    raise SystemExit('Billing is disabled. The project owner must link billing before deployment. No resources created.')

env = {}
env_path = ROOT / '.env'
if env_path.exists():
    for line in env_path.read_text(encoding='utf-8-sig').splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            key, value = line.split('=', 1)
            env[key.strip()] = value.strip().strip('"').strip("'")
env.update(os.environ)
for key in ['SUPABASE_URL', 'SUPABASE_PUBLISHABLE_KEY', 'DEMO_PASSWORD', 'SAFETY_GATEWAY_PASSWORD']:
    if not env.get(key):
        raise SystemExit(f'Missing {key}; no resource changes made')

run('services', 'enable', 'run.googleapis.com', 'cloudbuild.googleapis.com',
    'artifactregistry.googleapis.com', 'secretmanager.googleapis.com', '--project', args.project, '--quiet')
account = f'fairshift-runtime@{args.project}.iam.gserviceaccount.com'
if run('iam', 'service-accounts', 'describe', account, '--project', args.project, allow_failure=True).returncode:
    run('iam', 'service-accounts', 'create', 'fairshift-runtime', '--display-name=FairShift runtime',
        '--project', args.project, '--quiet')

bindings = []
secrets = [('DEMO_PASSWORD', 'fairshift-demo-password'), ('SAFETY_GATEWAY_PASSWORD', 'fairshift-safety-password')]
if env.get('GEMINI_API_KEY') and env.get('GEMINI_MODEL'):
    secrets.append(('GEMINI_API_KEY', 'fairshift-gemini-key'))
for key, secret in secrets:
    exists = run('secrets', 'describe', secret, '--project', args.project, allow_failure=True).returncode == 0
    if exists:
        run('secrets', 'versions', 'add', secret, '--data-file=-', '--project', args.project,
            input_bytes=env[key].encode())
    else:
        run('secrets', 'create', secret, '--replication-policy=automatic', '--data-file=-',
            '--project', args.project, input_bytes=env[key].encode())
    run('secrets', 'add-iam-policy-binding', secret, f'--member=serviceAccount:{account}',
        '--role=roles/secretmanager.secretAccessor', '--project', args.project, '--quiet')
    bindings.append(f'{key}={secret}:latest')

config = {'NODE_ENV': 'production', 'SUPABASE_URL': env['SUPABASE_URL'],
          'SUPABASE_PUBLISHABLE_KEY': env['SUPABASE_PUBLISHABLE_KEY'], 'ENABLE_DEMO': env.get('ENABLE_DEMO', 'false'),
          'SAFETY_GATEWAY_EMAIL': env.get('SAFETY_GATEWAY_EMAIL', 'safety.gateway@demo.fairshift.example'),
          'GEMINI_MODEL': env.get('GEMINI_MODEL', '')}
(ROOT / '.local').mkdir(exist_ok=True)
config_path = ROOT / '.local' / 'cloud-run.env.yaml'
config_path.write_text(json.dumps(config), encoding='utf-8')  # JSON is valid YAML; contains public configuration only.
run('run', 'deploy', 'fairshift-saakshi-ai', '--project', args.project, '--region', args.region,
    '--source', '.', '--service-account', account, '--allow-unauthenticated', '--port', '8080',
    '--memory', '512Mi', '--cpu', '1', '--min-instances', '0', '--max-instances', '1', '--concurrency', '40',
    '--env-vars-file', str(config_path), '--set-secrets', ','.join(bindings), '--quiet')
url = run('run', 'services', 'describe', 'fairshift-saakshi-ai', '--project', args.project,
          '--region', args.region, '--format=value(status.url)').stdout.decode().strip()
with urllib.request.urlopen(url + '/health', timeout=30) as response:
    if response.status != 200 or json.load(response).get('status') != 'ok':
        raise SystemExit('Deployment returned a URL but the health check did not pass')
print(json.dumps({'url': url, 'health': 'verified', 'next': 'Run the browser suite against TEST_BASE_URL=' + url}))
