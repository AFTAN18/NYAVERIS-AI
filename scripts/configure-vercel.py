"""Upload required environment values to the explicitly linked FairShift project.

Values travel through stdin, never CLI arguments, stdout, or tracked files.
"""
import json
import pathlib
import shutil
import subprocess

root = pathlib.Path(__file__).resolve().parents[1]
link = json.loads((root / '.vercel/project.json').read_text())
if link.get('projectId') != 'prj_GSHTnszr49w8p7rico2kgkwjmAiA' or link.get('orgId') != 'team_6vANYH69QjISvoyXFvxfplkq':
    raise SystemExit('Project link does not match the verified FairShift Vercel target.')
values = {}
for line in (root / '.env').read_text(encoding='utf-8-sig').splitlines():
    if '=' in line and not line.lstrip().startswith('#'):
        key, value = line.split('=', 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
values['VITE_SUPABASE_URL'] = values.get('SUPABASE_URL', '')
values['VITE_SUPABASE_PUBLISHABLE_KEY'] = values.get('SUPABASE_PUBLISHABLE_KEY', '')
public = ['SUPABASE_URL', 'SUPABASE_PUBLISHABLE_KEY', 'VITE_SUPABASE_URL', 'VITE_SUPABASE_PUBLISHABLE_KEY', 'ENABLE_DEMO', 'SAFETY_GATEWAY_EMAIL']
secret = ['DEMO_PASSWORD', 'SAFETY_GATEWAY_PASSWORD']
if values.get('GEMINI_API_KEY') and values.get('GEMINI_MODEL'):
    secret.append('GEMINI_API_KEY')
    public.append('GEMINI_MODEL')
npm = shutil.which('npm.cmd') or shutil.which('npm')
if not npm:
    raise SystemExit('npm is required')
for key in public + secret:
    if not values.get(key):
        raise SystemExit('Missing required value: ' + key)
    command = [npm, 'exec', '--yes', '--package=vercel@65.4.0', '--', 'vercel', 'env', 'add', key,
               '--environment', 'production', '--type', 'secret' if key in secret else 'config',
               '--project', link['projectId'], '--scope', 'aftan-faizs-projects', '--force', '--yes']
    result = subprocess.run(command, cwd=root, input=values[key].encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        message = result.stderr.decode(errors='replace')
        for value in values.values():
            if len(value) > 8:
                message = message.replace(value, '[REDACTED]')
        raise SystemExit('Environment setup failed for ' + key + ': ' + message)
    print('Configured ' + key + ' as ' + ('Secret' if key in secret else 'Config'))
