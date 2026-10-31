import "dotenv/config";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { execFileSync } from "node:child_process";
import assert from "node:assert/strict";
const tracked = execFileSync("git", ["ls-files", "--cached", "-z"], {
  encoding: "utf8",
})
  .split("\0")
  .filter(Boolean);
const untracked = execFileSync(
  "git",
  ["ls-files", "--others", "--exclude-standard", "-z"],
  {
    encoding: "utf8",
  },
)
  .split("\0")
  .filter(Boolean);
const files = [...new Set([...tracked, ...untracked])];
assert.ok(
  files.length > 0,
  "Stage source files before checking repository contents",
);
const sensitive = [
  "DEMO_PASSWORD",
  "SAFETY_GATEWAY_PASSWORD",
  "SUPABASE_SECRET_KEY",
  "GEMINI_API_KEY",
]
  .map((k) => process.env[k])
  .filter((v): v is string => !!v && v.length > 10);
let bytes = 0;
for (const file of files) {
  assert.ok(
    !/^\.env(?:\.|$)/.test(file) || file === ".env.example",
    "Private environment file staged",
  );
  assert.ok(
    !/^(node_modules|dist|dist-server|\.local|test-results|playwright-report)\//.test(
      file,
    ),
    "Generated/cache files staged",
  );
  const buffer = readFileSync(file);
  bytes += buffer.byteLength;
  for (const secret of sensitive)
    assert.ok(
      !buffer.toString("utf8").includes(secret),
      `A configured secret was found in ${file}`,
    );
}
assert.ok(
  bytes < 10000000,
  "Initial tracked source must be strictly below 10 MB",
);
function walk(root: string): string[] {
  return readdirSync(root).flatMap((name) => {
    const p = `${root}/${name}`;
    return statSync(p).isDirectory() ? walk(p) : [p];
  });
}
for (const file of walk("dist")) {
  const contents = readFileSync(file, "utf8");
  for (const secret of sensitive)
    assert.ok(
      !contents.includes(secret),
      `A backend secret was found in browser asset ${file}`,
    );
  assert.ok(
    !contents.includes("sb_secret_"),
    "Secret key prefix found in browser bundle",
  );
}
const branches = execFileSync(
  "git",
  ["for-each-ref", "--format=%(refname)", "refs/heads"],
  { encoding: "utf8" },
)
  .trim()
  .split("\n")
  .filter(Boolean);
assert.ok(branches.length <= 1, "More than one local branch exists");
console.log(
  JSON.stringify({
    status: "passed",
    trackedFiles: tracked.length,
    untrackedFilesScanned: untracked.length,
    trackedBytes: bytes,
    initialRepositoryBelow10MB: true,
    secretValuesAbsent: true,
    browserBundleSecretScan: "passed",
    localBranchCount: branches.length,
  }),
);
