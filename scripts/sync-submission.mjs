// Keep shared NYAVERIS AI application files in sync. Never commits, pushes,
// deploys, applies SQL, deletes files, or copies credentials/generated output.
import { readFileSync, writeFileSync, readdirSync, lstatSync, existsSync, mkdirSync } from 'node:fs';
import { resolve, dirname, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const app = resolve(fileURLToPath(new URL('..', import.meta.url)));
const submission = resolve(app, 'students/192425004-AFTAN-FAIZ');
const directories = ['src', 'public', 'api', 'server', 'shared', 'tests', 'supabase/migrations'];
const standalone = ['supabase/seed.sql', 'package.json', 'package-lock.json',
  'tsconfig.json', 'vite.config.ts', 'vercel.json', 'playwright.config.ts',
  'index.html', 'components.json', 'Dockerfile', '.dockerignore', '.vercelignore',
  '.env.example', 'scripts/provision.ts', 'scripts/rls-test.ts',
  'scripts/rls-readonly-test.ts', 'scripts/serverless-security-test.ts',
  'scripts/verify-backend.mjs'];
const forbidden = new Set(['.git', '.vercel', '.local', '.temp', 'node_modules',
  'dist', 'dist-server', 'test-results', 'playwright-report']);
const args = process.argv.slice(2);
const direction = args[0] === '--from' && ['app', 'submission'].includes(args[1]) && args.length === 2
  ? args[1] : undefined;
if (args.length && !direction && !(args.length === 1 && args[0] === '--check'))
  throw new Error('Use --check (default), --from app, or --from submission');
if (!existsSync(submission)) throw new Error('Expected submission folder is missing');

function safe(root, name) {
  const target = resolve(root, name);
  const rel = relative(root, target);
  if (rel.startsWith('..' + sep) || rel === '..' || resolve(root) === target)
    throw new Error('Path escapes the selected application root');
  const parts = rel.split(sep);
  if (parts.some(p => forbidden.has(p) || (p.startsWith('.env') && p !== '.env.example')))
    throw new Error('Excluded path requested');
  let current = root;
  for (const part of parts) {
    current = resolve(current, part);
    if (existsSync(current) && lstatSync(current).isSymbolicLink())
      throw new Error('Refusing a symbolic-link path');
  }
  return target;
}
function walk(root, name) {
  const path = safe(root, name);
  if (!existsSync(path)) return [];
  if (!lstatSync(path).isDirectory()) return [name.replaceAll('\\', '/')];
  return readdirSync(path).flatMap(child => {
    if (forbidden.has(child) || (child.startsWith('.env') && child !== '.env.example')) return [];
    return walk(root, name + '/' + child);
  });
}
const paths = [...new Set([...standalone, ...directories.flatMap(name =>
  [...walk(app, name), ...walk(submission, name)])])].sort();
const differences = paths.filter(name => {
  const a = safe(app, name), b = safe(submission, name);
  return !existsSync(a) || !existsSync(b) || !readFileSync(a).equals(readFileSync(b));
});
if (!direction) {
  console.log(JSON.stringify({ status: differences.length ? 'drift' : 'synchronized',
    sharedFiles: paths.length, differences, excludes: 'secrets, caches and repository-specific documents/tools' }, null, 2));
  if (differences.length) process.exitCode = 1;
} else {
  const source = direction === 'app' ? app : submission;
  const destination = direction === 'app' ? submission : app;
  const missing = differences.filter(name => !existsSync(safe(source, name)));
  if (missing.length) throw new Error('Source lacks shared files; resolve manually without deleting: ' + missing.join(', '));
  for (const name of differences) {
    const target = safe(destination, name);
    mkdirSync(dirname(target), { recursive: true });
    writeFileSync(target, readFileSync(safe(source, name)));
  }
  console.log(JSON.stringify({ status: 'synchronized', from: direction,
    updatedFiles: differences, sharedFiles: paths.length,
    deletedFiles: 0, gitOrCloudActions: false }, null, 2));
}
